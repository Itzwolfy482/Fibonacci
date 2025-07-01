from setuptools import setup, Extension
import platform

# Compiler flags based on platform
extra_compile_args = []
extra_link_args = []

if platform.system() == "Windows":
    extra_compile_args = ['/O2', '/favor:INTEL64']  # Optimize for speed and Intel 64-bit
elif platform.system() in ["Linux", "Darwin"]:  # Linux or macOS
    extra_compile_args = ['-O3', '-march=native', '-ffast-math']
    extra_link_args = ['-O3']

mmfv4_extension = Extension(
    'mmfv4_bigint',
    sources=['mmfv4_bigint_module.c'],
    extra_compile_args=extra_compile_args,
    extra_link_args=extra_link_args,
)

setup(
    name='mmfv4_bigint',
    version='1.0',
    description='Optimized matrix multiplication with assembly for Fibonacci calculations',
    ext_modules=[mmfv4_extension],
    zip_safe=False,
)