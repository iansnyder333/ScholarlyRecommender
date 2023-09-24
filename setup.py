from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np

setup(
    name="CythonizedNCD",
    ext_modules=cythonize(
        Extension(
            "ScholarlyRecommender.Recommender.cython_functions",
            sources=["ScholarlyRecommender/Recommender/cython/cython_functions.pyx"],
            extra_compile_args=["-arch", "x86_64"],
        )
    ),
    include_dirs=[np.get_include()],
)
