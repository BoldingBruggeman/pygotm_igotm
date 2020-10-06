import os.path
from setuptools import setup

try:
    import wheel.bdist_wheel
    class bdist_wheel(wheel.bdist_wheel.bdist_wheel):
        def finalize_options(self):
            wheel.bdist_wheel.bdist_wheel.finalize_options(self)
            self.root_is_pure = False
        def get_tag(self):
            python, abi, plat = wheel.bdist_wheel.bdist_wheel.get_tag(self)
            python, abi = 'py2.py3', 'none'
            return python, abi, plat
except ImportError:
    bdist_wheel = None

setup(
    name='pygotm',
    version='0.1',
    description='Python wrapper for GOTM',
    author='Jorn Bruggeman',
    author_email='jorn@bolding-bruggeman.com',
    license='GPL',
    packages=['pygotm'],
    package_data={'pygotm': ['*.so', '*.dll', '*.dylib', 'schemas/*']},
    cmdclass={'bdist_wheel': bdist_wheel},
    zip_safe=False
)


