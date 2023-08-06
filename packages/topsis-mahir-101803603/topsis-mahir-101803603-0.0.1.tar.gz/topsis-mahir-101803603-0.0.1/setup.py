from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='topsis-mahir-101803603',
    version='0.0.1',
    description='A very basic calculator',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Joshua Lowe',
    author_email='mahir007mahir@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='topsis101803603',
    packages=find_packages(),
    install_requires=['']
)