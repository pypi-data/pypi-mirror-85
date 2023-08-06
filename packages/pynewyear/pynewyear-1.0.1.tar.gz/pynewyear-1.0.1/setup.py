import setuptools

from pynewyear import __version__

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='pynewyear',
    version=__version__,
    author='Baboshin Sergey',
    author_email='ijustbsd@gmail.com',
    description='Happy New Year! 🎄',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ijustbsd/pynewyear',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7'
)
