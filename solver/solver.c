#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "generated_physics.h"

typedef struct {
	float x;
	float y;
} Vector2D;

void wrapper_generated_eom(Vector2D* q, Vector2D* dq, Vector2D* _dq, Vector2D* _ddq, float t, size_t N) {
    python_generated_eom((float*)q, (float*)dq, (float*)_dq, (float*)_ddq, t, N);
}

void RK4_2D(Vector2D* r, Vector2D* v, Vector2D* dr, Vector2D* dv, float t, float dt,
	    	void(*dfdt)(Vector2D*,Vector2D*,Vector2D*,Vector2D*,float,size_t), size_t N){
	/* RK4 Implementation in 2D
	 * r = position array
	 * v = velocity array
	 * dr = derivative of position array
	 * dv = derivative of velocity array
	 * t = current time
	 * dt = time step
	 * dfdt = function that computes derivatives
	 * N = number of elements
	 */

	// Temporary arrays
	const float one_sixth = 0x1.555556p-3f;
	size_t size = N * sizeof(Vector2D);
	Vector2D* tmp_x = malloc(size);
	Vector2D* tmp_v = malloc(size);

	// k1, k2, k3, k4 arrays for position and velocity
	Vector2D* k1_dr = malloc(size); Vector2D* k1_dv = malloc(size);
	Vector2D* k2_dr = malloc(size); Vector2D* k2_dv = malloc(size);
	Vector2D* k3_dr = malloc(size); Vector2D* k3_dv = malloc(size);
	Vector2D* k4_dr = malloc(size); Vector2D* k4_dv = malloc(size);

	// Calculate k1
	dfdt(r, v, k1_dr, k1_dv, t, N);

	// Calculate k2
	for(size_t i=0U; i<N; ++i){
		tmp_x[i].x = r[i].x + 0.5f * dt * k1_dr[i].x;
		tmp_x[i].y = r[i].y + 0.5f * dt * k1_dr[i].y;
		tmp_v[i].x = v[i].x + 0.5f * dt * k1_dv[i].x;
		tmp_v[i].y = v[i].y + 0.5f * dt * k1_dv[i].y;
	}
	dfdt(tmp_x, tmp_v, k2_dr, k2_dv, t+0.5f*dt, N);

	// Calculate k3
	for(size_t i=0U; i<N; ++i){
		tmp_x[i].x = r[i].x + 0.5f * dt * k2_dr[i].x;
		tmp_x[i].y = r[i].y + 0.5f * dt * k2_dr[i].y;
		tmp_v[i].x = v[i].x + 0.5f * dt * k2_dv[i].x;
		tmp_v[i].y = v[i].y + 0.5f * dt * k2_dv[i].y;
	}
	dfdt(tmp_x, tmp_v, k3_dr, k3_dv, t+0.5f*dt, N);

	// Calculate k4
	for(size_t i=0U; i<N; ++i){
		tmp_x[i].x = r[i].x + dt * k3_dr[i].x;
		tmp_x[i].y = r[i].y + dt * k3_dr[i].y;
		tmp_v[i].x = v[i].x + dt * k3_dv[i].x;
		tmp_v[i].y = v[i].y + dt * k3_dv[i].y;
	}
	dfdt(tmp_x, tmp_v, k4_dr, k4_dv, t+dt, N);

	// Combine to get final dr and dv
	for(size_t i=0U; i<N; ++i){
		dr[i].x = dt * one_sixth * (k1_dr[i].x + 2.0f * k2_dr[i].x + 2.0f * k3_dr[i].x + k4_dr[i].x);
		dr[i].y = dt * one_sixth * (k1_dr[i].y + 2.0f * k2_dr[i].y + 2.0f * k3_dr[i].y + k4_dr[i].y);
		dv[i].x = dt * one_sixth * (k1_dv[i].x + 2.0f * k2_dv[i].x + 2.0f * k3_dv[i].x + k4_dv[i].x);
		dv[i].y = dt * one_sixth * (k1_dv[i].y + 2.0f * k2_dv[i].y + 2.0f * k3_dv[i].y + k4_dv[i].y);
	}

	// Cleanup
	free(tmp_x); free(tmp_v);
	free(k1_dr); free(k1_dv);
	free(k2_dr); free(k2_dv);
	free(k3_dr); free(k3_dv);
	free(k4_dr); free(k4_dv);
	return;
}

void next_2D(Vector2D* coord, Vector2D* vel, Vector2D* new_coord, Vector2D* new_vel, float dt, size_t N) {
	size_t size = N * sizeof(Vector2D);
    Vector2D* dq = malloc(size);
    Vector2D* dqdot = malloc(size);

    RK4_2D(coord, vel, dq, dqdot, 0.0f, dt, &wrapper_generated_eom, N);

    for(size_t i = 0; i < N; i++) {
        new_coord[i].x = coord[i].x + dq[i].x;
        new_coord[i].y = coord[i].y + dq[i].y;
        new_vel[i].x = vel[i].x + dqdot[i].x;
        new_vel[i].y = vel[i].y + dqdot[i].y;
    }

    free(dq);
    free(dqdot);

	return;
}
