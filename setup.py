from setuptools import setup

setup(
    name='uppasd_sweeper',
    version='1.0',
    py_modules=['t_sweeper'],
    install_requires=['numpy'],
    entry_points={
        'console_scripts': [
            't_sweeper=t_sweeper:main',
        ],
    },
    author='Anders Bergman',
    description='Temperature sweep wrapperfor UppASD simulations',
    url='https://github.com/anbergman/uppasd_sweeper',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
