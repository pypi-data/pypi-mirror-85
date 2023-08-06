from setuptools import setup


setup(
    name='aidkitmlevaluate',
    version='0.1.0',
    description='A test Python package for an interface to evaluate ML models',
    #url='https://github.com/shuds13/pyexample',
    author='Sachin Manjunath',
    author_email='sachin.mhegde@gmail.com',
    #license='BSD 2-clause',
    packages=['aidkitmlevaluate'],
    install_requires=['tensorflow>=2.0',
                      'numpy',
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        #'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)