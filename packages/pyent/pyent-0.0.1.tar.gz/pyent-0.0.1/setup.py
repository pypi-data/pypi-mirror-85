from setuptools import setup
from Cython.Build import cythonize

with open('README.md') as fp:
    long_description = fp.read()

setup(
    name='pyent',
    version='0.0.1',
    author='Inndy Lin',
    author_email='inndy.tw@gmail.com',
    description='Unix utility `ent` reimplement with cython. Calculating data entropy',
    ext_modules=cythonize('ent.pyx', language_level=3),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/inndy/pyent',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        ],
    python_requires='>=3.6', # at least I had tested
    zip_safe=False, # what do this even mean? LOL
)
