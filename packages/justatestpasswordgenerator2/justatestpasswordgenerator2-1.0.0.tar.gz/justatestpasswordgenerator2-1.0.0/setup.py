from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='justatestpasswordgenerator2',
    version='1.0.0',
    description='A random password generator',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Joseph Keyes',
    author_email='josephkeyes404@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='password, generator, random',
    packages=find_packages(),
    install_requires=['']
)