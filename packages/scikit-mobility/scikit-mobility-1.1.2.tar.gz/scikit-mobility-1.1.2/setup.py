from setuptools import setup

long_description = open('README.md').read()

DEPENDENCIES = ['numpy', 'scipy', 'pandas', 'geopandas', 'powerlaw', 'tqdm', 'requests',
                'scikit-learn', 'statsmodels', 'folium', 'matplotlib', 'geojson', 'shapely', 'rtree']

TEST_DEPENDENCIES = ['pytest']

setup(
    name='scikit-mobility',
    url="https://github.com/scikit-mobility",
    version='1.1.2',
    packages=['skmob', 'skmob.core', 'skmob.utils', 'skmob.io', 'skmob.measures', 'skmob.models',
              'skmob.preprocessing', 'skmob.privacy', 'skmob.tessellation'],
    license='MIT',
    python_requires='>=3.6',
    description='A toolbox for analyzing and processing mobility data.',
    long_description=long_description,
    maintainer='skmob Developers',
    maintainer_email='gianni.barlacchi@gmail.com',
    classifiers=['Intended Audience :: Science/Research',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved',
                 'Programming Language :: Python',
                 'Topic :: Software Development',
                 'Topic :: Scientific/Engineering',
                 'Operating System :: Microsoft :: Windows',
                 'Operating System :: Unix',
                 'Operating System :: MacOS',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7',
                 'Programming Language :: Python :: 3.8',
                 ],
    install_requires=DEPENDENCIES,
    tests_require=TEST_DEPENDENCIES
    )
