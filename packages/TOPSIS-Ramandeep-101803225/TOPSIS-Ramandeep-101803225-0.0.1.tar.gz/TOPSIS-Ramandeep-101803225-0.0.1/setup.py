from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='TOPSIS-Ramandeep-101803225',
    version='0.0.1',
    descripiton='A very basic implementation-> TOPSIS',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Ramandeep Singh',
    author_email='rsingh1_be18@thapar.edu',
    license='MIT',
    classifiers=classifiers,
    keywords='topsis',
    packages=find_packages(),
    install_requires=['']
)