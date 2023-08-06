from setuptools import setup

description = 'Generic model field for storing big integer field.'

try:
    with open('README.rst') as f:
        long_description = f.read()
except IOError:
    long_description = description

setup(
    name='django-big-positive-int-field',
    version='1.0.0',
    description=description,
    author='Rahul',
    author_email='skrsinghrahul@gmail.com',
    url='https://github.com/meetrks/django-big-positive-int-field',
    long_description=long_description,
    packages=['big_positive_int_field'],
    install_requires=['django >= 2.2'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
