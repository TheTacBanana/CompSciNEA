from setuptools import setup
from Cython.Build import cythonize

setup(
    name="mathlib",
    ext_modules = cythonize("Scripts\\mathlib.pyx", annotate=True)
)