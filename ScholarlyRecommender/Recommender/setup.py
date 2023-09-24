from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np

setup(
    name="CythonizedNCD",
    ext_modules=cythonize(
        Extension(
            "cython_functions",
            sources=["cython_functions.pyx"],
            extra_compile_args=["-arch", "x86_64"],
        )
    ),
    include_dirs=[np.get_include()],
)
