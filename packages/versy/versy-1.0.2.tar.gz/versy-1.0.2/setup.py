_classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Topic :: Software Development :: Libraries',
    'Topic :: Utilities',
]


def _version():
    with open('versy/versy.py') as fp:
        line = next(i for i in fp if i.startswith('__version__'))
        return line.strip().split()[-1].strip("'")


with open('requirements.txt') as f:
    REQUIRED = f.read().splitlines()

if __name__ == '__main__':
    from setuptools import setup

    setup(
        name='versy',
        version=_version(),
        author='Tom Ritchford',
        author_email='tom@swirly.com',
        url='https://github.com/rec/versy',
        tests_require=['pytest'],
        py_modules=['versy'],
        description='Update the Python version number',
        long_description=open('README.rst').read(),
        license='MIT',
        classifiers=_classifiers,
        keywords=['documentation'],
        scripts=['scripts/versy'],
        packages=['versy'],
        install_requires=REQUIRED,
    )
