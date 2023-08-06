from setuptools import setup

version = {}
with open('suncal/version.py', 'r') as f:
    exec(f.read(), version)

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='suncal',
    version=version['__version__'],
    description='Sandia PSL Uncertainty Calculator',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Collin J. Delker',
    author_email='uncertainty@sandia.gov',
    url='https://sandiapsl.github.io',
    project_urls={'Source': 'https://github.com/SandiaPSL/UncertaintyCalc'},
    python_requires='>=3.5',
    install_requires=[
        'pyqt5',
        'numpy>=1.15',
        'matplotlib>=3.1',
        'scipy>=1.1',
        'sympy>=1.3',
        'pint>=0.9',
        'markdown>=3.1',
        'pyyaml>=5.1',
        ],
    packages=['suncal', 'suncal.gui', 'suncal.intervals', 'psluncert'],
    package_dir={'suncal': 'suncal', 'suncal.gui': 'suncal/gui', 'suncal.intervals': 'suncal/intervals', 'psluncert': 'suncal'},
    entry_points={
        'console_scripts': ['suncal = suncal.__main__:main_unc',
                            'suncalf = suncal.__main__:main_setup',
                            'suncalrev = suncal.__main__:main_reverse',
                            'suncalrisk = suncal.__main__:main_risk',
                            'suncalfit = suncal.__main__:main_curvefit',
                            ],
        'gui_scripts': ['suncalui = suncal.gui.gui_main:main'],
        },
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        ]
    )
