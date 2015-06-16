from setuptools import setup, find_packages


setup(
    name='Django React',
    version='0.0.1',
    description="This package replaces Django\'s original templating engine with Facebook's ReactJS library.",
    long_description="This package requires Node.js installed on your machine to render React on server side.",
    url='https://github.com/pypa/sampleproject',
    author='Vojtěch Tranta',
    author_email='vojta.tranta@gmail.com',
    license='MIT',
    package_dir={'django_react': 'django_react'},
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],

    keywords='react nodejs javascript isomorphism template',

    packages=find_packages(exclude=['js']),

    install_requires=['requests', 'Naked'],
)
