from setuptools import setup

with open('README.rst') as rdm:
    README = rdm.read()

setup(
    name='parspace',
    version='1.0.0',

    description='Parameter space exploration utiliy.',
    long_description=README,

    url='https://github.com/amorison/parspace',

    author='Adrien Morison',
    author_email='adrien.morison@gmail.com',

    license='Apache',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],

    python_requires='>=3.6',
    py_modules=['parspace'],
)
