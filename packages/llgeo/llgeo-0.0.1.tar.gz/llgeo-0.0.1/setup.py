import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()
    
setuptools.setup(
    name = 'llgeo',
    version = '0.0.1',
    author = 'Laura Luna',
    author_email = 'lauralunacabrera@gmail.com',
    description = 'Python library for Geotechnical Engineering',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = '', # Need to add this in once Git repo is created
    packages = setuptools.find_packages(),
    classifiers = [ 'Programming Language :: Python :: 3',
                    'License :: OSI Approved :: MIT License',
                    'Operating System :: OS Independent',
                      ],
    python_requires = '>=3.7'
)    