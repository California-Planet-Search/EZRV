from setuptools import setup

setup(
    name='EZRV',
    version='0.1.0',
    description='A Packages that keeps track of Exoplanet RV data',
    url='https://github.com/California-Planet-Search/EZRV.git',
    author='Sarah Lange & Fei Dai',
    author_email='fdai@caltech.edu',
    license='MIT License',
    packages=['EZRV'],
    install_requires=['astropy',
                      'numpy',
                      'barycorrpy',
                      'astroquery',
                      'pandas',
                      'requests',
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.5',
    ],
)
