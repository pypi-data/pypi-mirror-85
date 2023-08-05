import sys
import pathlib

from setuptools import find_packages

try:
    from skbuild import setup
except ImportError:
    print('Please update pip, you need pip 10 or greater,\n'
          ' or you need to install the PEP 518 requirements in pyproject.toml yourself', file=sys.stderr)
    raise

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')


setup(
    name="fibomat",
    version="0.1.2",
    description="fib-o-mat is a toolbox to generate patterns for focus ion beam instruments.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Victor Deinhart',
    author_email='victor.deinhart@helmholtz-berlin.de',
    url='https://gitlab.com/viggge/fib-o-mat',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: C++',
        'Topic :: Scientific/Engineering :: Physics',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
    ],
    keywords='focused ion beam, fib, pattern, patterning, beam path generation,',
    license="GPLv3",
    packages=find_packages(exclude=['test*', 'custom_backends*']),
    python_requires='>=3.8, <4',
    package_data={'fibomat': ['py.typed', 'default_backends/measure_band.ts']},
    cmake_install_dir='fibomat',
    install_requires=[
        'numpy', 'scipy', 'sympy', 'bokeh<=2.1.1', 'pint', 'ezdxf', 'pandas', 'numba'
    ],
    extras_require={
        'docs': [
            'sphinx', 'recommonmark', 'pydata_sphinx_theme', 'sphinxemoji', 'bokeh<=2.1.1'
        ],
    },
    project_urls={  # Optional
        'Bug Reports': 'https://gitlab.com/viggge/fib-o-mat/-/issues',
        'Source': 'https://gitlab.com/viggge/fib-o-mat/',
        'Documentation': "https://fib-o-mat.readthedocs.io/en/latest/",
    },
)
