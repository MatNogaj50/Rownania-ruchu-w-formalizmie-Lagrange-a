#ifndef GENERATED_PHYSICS_H
#define GENERATED_PHYSICS_H

void python_generated_eom(float* q, float* dq, float* _dq, float* _ddq, float t, size_t N) {
    // Auto-generated Euler-Lagrange Equations using sympy.physics.mechanics
    // Constants have been collapsed into their values.
    float g = 9.81f;
    float l = 1.0f;
    for (size_t p = 0; p < N; p++) {
        float* q_p = q + p * 1;
        float* dq_p = dq + p * 1;
        float* _dq_p = _dq + p * 1;
        float* _ddq_p = _ddq + p * 1;
        _dq_p[0] = dq_p[0];
        _ddq_p[0] = -g*sin(q_p[0])/l;
    }
return;
}

#endif // GENERATED_PHYSICS_H
