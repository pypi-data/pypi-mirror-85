import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='seaoligo-common',
    version='2.0.7',
    author='SEA Biopharma',
    author_email='sea.biopharma@gmail.com',
    description='SEA Web Services common python packages',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/sea-biopharma/seaoligo-common',
    packages=setuptools.find_packages(),
    install_requires=[
        'flask>=1.1.2',
        'flask-sqlalchemy>=2.4.4',
        'pyjwt>=1.7.1',
        'strawberry-graphql>=0.41.0',
    ],
    python_requires='>=3.8',
)
