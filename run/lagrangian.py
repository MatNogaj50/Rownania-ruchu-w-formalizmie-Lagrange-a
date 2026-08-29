# run as: python3 -m lagrangian
from typing import List

import sympy as sp
from sympy.physics.mechanics import LagrangesMethod, dynamicsymbols
from sympy.printing.c import ccode

class LagrangianToC:
    vectorType: str = "float"
    def __init__(self, L: sp.Expr,
                 q: List[sp.Expr]) -> None:
        self.L = L
        self.q = q
    def generate_c_function(self, func_name="equations_of_motion", collapse_constants: bool=True) -> str:
        # 1. Initialize LagrangesMethod
        # This automatically computes d/dt(dL/dqdot) - dL/dq = Forces
        LM = LagrangesMethod(self.L, self.q)

        # 2. Form the equations
        LM.form_lagranges_equations()

        # 3. Get the Right-Hand Side (RHS) of the equations of motion.
        # LM.rhs() returns a column vector of size 2N: [q_dot; q_ddot].
        # The top half is just velocities, the bottom half is accelerations.
        # This step implicitly solves M * q_ddot = F for q_ddot.
        full_rhs = LM.rhs()

        n = len(self.q)
        # Extract only the acceleration expressions (the bottom N rows)
        accel_exprs = full_rhs[n:, 0]

        # 4. Identify Constants
        # Get all free symbols from the expressions
        # We use the derived expressions to ensure we catch everything needed
        all_free = set()
        for expr in accel_exprs:
            all_free.update(expr.free_symbols)

        # Identify dynamic symbols (q, u, t) to exclude them from the constants list
        # LM.q contains coordinates, LM.u contains speeds (velocities)
        dynamic_vars = set(LM.q) | set(LM.u) | {dynamicsymbols._t}

        constants = sorted([s for s in all_free if s not in dynamic_vars], key=lambda x: x.name)

        # 5. Create Symbol Mapping for C-Array access
        # We substitute the sympy symbols with explicit C-string formatted symbols
        # e.g. theta(t) -> q[0], u_0 -> dq[0]

        subs_map = {}

        # Map coordinates q_i -> q[i]
        for i, q_sym in enumerate(LM.q):
            # We create a dummy symbol named "q[i]" so ccode prints it exactly so
            subs_map[q_sym] = sp.Symbol(f"q[{i}]")

        # Map speeds u_i -> dq[i]
        for i, u_sym in enumerate(LM.u):
            subs_map[u_sym] = sp.Symbol(f"dq[{i}]")

        # 6. Construct the C Function
        lines = []

        # Function Signature
        if collapse_constants:
            lines.append(f"void {func_name}({self.vectorType}* q, {self.vectorType}* dq, {self.vectorType}* _dq, {self.vectorType}* _ddq, float t, size_t N) {{")
        else:
            const_args = ", ".join([f"float {c.name}" for c in constants])
            sig_constants = f", {const_args}" if const_args else ""
            lines.append(f"void {func_name}({self.vectorType}* q, {self.vectorType}* dq, {self.vectorType}* _dq, {self.vectorType}* _ddq, float t, size_t N{sig_constants}) {{")
        lines.append("    // Auto-generated Euler-Lagrange Equations using sympy.physics.mechanics")

        if collapse_constants:
            lines.append("    // Constants have been collapsed into their values.")
            default_values = {
                'g': 9.81,
                'l': 1.0,
                'l1': 1.0,
                'l2': 1.0,
                'm': 1.0,
                'm1': 1.0,
                'm2': 1.0,
                'k': 10.0
            }
            for c in constants:
                val = default_values.get(c.name, 1.0)
                lines.append(f"    float {c.name} = {val}f;")
        num_coords = len(self.q)
        lines.append(f"    for (size_t p = 0; p < N; p++) {{")
        lines.append(f"        float* q_p = q + p * {num_coords};")
        lines.append(f"        float* dq_p = dq + p * {num_coords};")
        lines.append(f"        float* _dq_p = _dq + p * {num_coords};")
        lines.append(f"        float* _ddq_p = _ddq + p * {num_coords};")

        subs_map_p = {}
        for j, q_sym in enumerate(LM.q):
            subs_map_p[q_sym] = sp.Symbol(f"q_p[{j}]")
        for j, u_sym in enumerate(LM.u):
            subs_map_p[u_sym] = sp.Symbol(f"dq_p[{j}]")
        for i, expr in enumerate(accel_exprs):
            mapped_expr = expr.subs(subs_map_p)
            c_str = ccode(mapped_expr)
            lines.append(f"        _dq_p[{i}] = dq_p[{i}];")
            lines.append(f"        _ddq_p[{i}] = {c_str};")
        lines.append("    }")
        lines.append("return;")
        lines.append("}")

        return "\n".join(lines)

if __name__ == "__main__":
    import Files_withL
    print("=== Choose given lagrangian ===")
    print("1 - Double Pendulum")
    print("2 - Spring-Mass System (2D)")
    print("3 - Spherical Pendulum")
    print("Other - Simple Pendulum (default)")
    
    nr_str = input("Number: ").strip()
    nr = int(nr_str)
    L, q = Files_withL.get_lagrangian(nr)

    gen = LagrangianToC(L, q)
    c_code = gen.generate_c_function("python_generated_eom")

    output_header_path = "../solver/generated_physics.h"
    with open(output_header_path, "w") as f:
        f.write("#ifndef GENERATED_PHYSICS_H\n")
        f.write("#define GENERATED_PHYSICS_H\n\n")
        f.write(c_code)
        f.write("\n\n#endif // GENERATED_PHYSICS_H\n")
