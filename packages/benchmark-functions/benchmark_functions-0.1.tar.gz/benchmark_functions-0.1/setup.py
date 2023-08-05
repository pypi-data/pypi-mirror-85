from setuptools import setup, find_packages

VERSION = '0.1'

with open('README_pip.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='benchmark_functions',
    version=VERSION,
    description='A benchmark functions collection wrote in Python 3, suited for assessing the performances of optimisation problems on deterministic functions.',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='GNUv3',
    packages=['benchmark_functions'],
    author='Luca Baronti',
    author_email='lbaronti@gmail.com',
    keywords=['Optimisation', 'Optimization', 'Benchmark', 'Functions'],
    url='https://gitlab.com/luca.baronti/python_benchmark_functions',
    download_url='https://pypi.org/project/benchmark_functions/',
		classifiers=[
			# How mature is this project? Common values are
			'Development Status :: 3 - Alpha',
			# Indicate who your project is intended for
			'Intended Audience :: Education',
			'Intended Audience :: Science/Research',
			'Topic :: Scientific/Engineering :: Mathematics',
			# Pick your license as you wish (should match "license" above)
			'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
			# Specify all Python versions you support here.
			'Programming Language :: Python :: 3',
		]
)

install_requires = [
    'numpy'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires, include_package_data=True)