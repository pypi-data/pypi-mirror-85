from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
        name='neurosum',
        version='0.0.0.5',
        description='Runs a statistical summary for electrophysiology data.',
        long_description=long_description,
        author_email='lehenry@ucsd.edu',
        url='https://github.com/',
        include_package_data=True,
#        package_data={
#                'thebe': [ 'templates/*','static/*','core/*']
#                },
        packages=find_packages(),
        install_requires=[
            'numpy',
            'matplotlib',
            'statsmodels',
            'neurodsp',
            'scipy',
            'pyopenephys',
            'h5py'
            ],
        entry_points={
            'console_scripts': [
                'neurosum = src.summary_statistics:main',
                ]
            },
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.7',
        )
