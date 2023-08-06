from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='topsis-yopro',
    version='0.1',
    description='A tool to calculate TOPSIS Score and Rank for given Dataset.',
    url='',
    author='Yash Shukla',
    author_email='yash981815@gmail.com',
    License='MIT',
    classifiers=classifiers,
    keywords='TOPSIS Calcula tor',
    packages=find_packages(),
    install_requires=['pandas']
)