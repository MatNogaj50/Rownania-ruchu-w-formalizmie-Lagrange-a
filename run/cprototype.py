"""
A prototype Python script that demonstrates how to interface with a C library
"""

# === IMPORTS ===
import numpy as np
from ctypes import c_float, c_int, Structure, POINTER, byref, cdll

# === CTYPES STRUCTURE DEFINITION ===
class Vector2D(Structure):
    """
    A ctypes Structure to represent a 2D vector, allowing it
    to be passed to and from the C library.
    """
    _fields_ = [("x", c_float),
                ("y", c_float)]

    def __repr__(self):
        """String representation for debugging."""
        return f"({self.x:.4f}, {self.y:.4f})"

    def __call__(self, data, i):
        """
        A helper method to update a numpy array (for plotting)
        with this vector's data at a specific index 'i'.
        """
        data[i, :] = np.array((self.x, self.y))

class EOMSolver:
    def __init__(self, path, NUMBER_OF_PARTICLES=1, DIMENSIONS=2):
        """
        Load a C shared library from the specified path.
        """
        self.lib = cdll.LoadLibrary(path)
        self.NUMBER_OF_PARTICLES = NUMBER_OF_PARTICLES
        self.DIMENSIONS = 2
        self.c_vec_ptr = POINTER(Vector2D) # Alias for pointer to Vector2D
        self._prototype_2D()
        self.next_step.restype = None

    def _prototype_2D(self):
        """
        Prototype the 2D next step function from the C library.
        Assuming function
        `void next_2D(Vector2D* coord, Vector2D* vel, Vector2D* new_coord, Vector2D* new_vel, float dt, size_t N);`
        exists in the C library.
        """
        self.next_step = self.lib.next_2D
        self.c_arr = Vector2D*self.NUMBER_OF_PARTICLES # Alias for pointer to an array of Vector2D
        self.next_step.argtypes = [self.c_vec_ptr, self.c_vec_ptr,
                                   self.c_vec_ptr, self.c_vec_ptr, c_float, c_int]

    def vector(self, x=0.0, y=0.0, z=0.0):
        return Vector2D(x=x, y=y)
