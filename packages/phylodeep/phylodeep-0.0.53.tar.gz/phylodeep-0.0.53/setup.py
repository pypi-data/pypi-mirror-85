import os
from setuptools import setup, find_packages

setup(
    name='phylodeep',
    packages=find_packages(),
    include_package_data=True,
    package_data={'phylodeep': [os.path.join('pretrained_models', 'models', '*.json'),
                                os.path.join('pretrained_models', 'scalers', '*.pkl'),
                                os.path.join('pretrained_models', 'weights', '*.h5'),
                                os.path.join('..', 'README.md')
                                ]},
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    version='0.0.53',
    description='Phylodynamic paramater and model inference using pretrained deep neural networks',
    author='Jakub Voznica, Anna Zhukova',
    author_email='jakub.voznica@pasteur.fr',
    url='https://github.com/evolbioinfo/deepphylo',
    keywords=['deepphylo', 'deepparam', 'deepmodel', 'phylodynamics', 'deep learning', 'model selection', 'phylogeny',
              'molecular epidemiology'],
    install_requires=['ete3', 'pandas', 'numpy', 'scipy', 'sklearn', 'tensorflow', 'joblib'],
    entry_points={
            'console_scripts': [
                'paramdeep = phylodeep.paramdeep:main', 'modeldeep = phylodeep.modeldeep:main'
            ]
    },
)
