import setuptools

setuptools.setup(
    name='TOPSIS-Sabhya-101803456',
    version='0.0.1',
    description='A package for TOPSIS Analysis of the data given',
    url='https://github.com/SabhyaGrover/DataScienceFundamentals',
    author='Sabhya Grover',
    author_email='sabgrohyaver@gmail.com',
    license='BSD 2-clause',
    packages=setuptools.find_packages(),
    install_requires=['pandas',
                      'numpy',
                      ],
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Education',
        'Natural Language :: English',
        'License :: Free For Educational Use',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering :: Information Analysis'
    ],
)