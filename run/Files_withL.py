import sympy as sp
from sympy.physics.mechanics import dynamicsymbols

def get_lagrangian(choice):
    match choice:
        case 1:
            # --- Double Pendulum ---
            q1, q2 = dynamicsymbols('q1 q2')
            m1, m2, l1, l2, g = sp.symbols('m1 m2 l1 l2 g')

            x1 = l1 * sp.sin(q1)
            y1 = -l1 * sp.cos(q1)

            x2 = x1 + l2 * sp.sin(q2)
            y2 = y1 - l2 * sp.cos(q2)

            v1_sq = x1.diff(dynamicsymbols._t)**2 + y1.diff(dynamicsymbols._t)**2
            v2_sq = x2.diff(dynamicsymbols._t)**2 + y2.diff(dynamicsymbols._t)**2

            T = 0.5 * m1 * v1_sq + 0.5 * m2 * v2_sq
            V = m1 * g * y1 + m2 * g * y2
            L = T - V
            q = [q1, q2]
        case 2:
            # --- Spring-Mass System ---
            r, theta = dynamicsymbols('r theta')
            m, k, g = sp.symbols('m k g')

            T = sp.Rational(1, 2) * m * (r.diff()**2 + (r * theta.diff())**2)
            V = sp.Rational(1, 2) * k * (r - 1)**2 - m * g * r * sp.cos(theta)
            L = T - V
            q = [r, theta]
        case 3:
            # --- Spherical Pendulum ---
            theta2, phi2 = dynamicsymbols('theta phi')
            msf, lsf, g = sp.symbols('m l g')

            T = sp.Rational(1, 2) * msf * lsf**2 * (theta2.diff()**2 + sp.sin(theta2)**2 * phi2.diff()**2)
            V = msf * g * lsf * sp.cos(theta2)
            L = T - V
            q = [theta2, phi2]
        case _:
            # --- Simple Pendulum ---
            theta = dynamicsymbols('theta')
            theta_dot = theta.diff()
            m, g, l = sp.symbols('m g l')

            T = sp.Rational(1, 2) * m * (l * theta_dot)**2
            V = m * g * l * (1 - sp.cos(theta))

            L = T - V
            q = [theta]
    return L, q
