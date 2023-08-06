import setuptools


with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='easy-cdll',
    version='0.1.0',
    author='techsol-ntu',
    author_email='techsol.workspace.tmp@gmail.com',
    description='Boost the transaction formatting and development between python and c languages',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/techsol-ntu/easy-cdll',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.3',
)