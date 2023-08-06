from setuptools import setup


setup(
    name='dcx_utils',
    version="0.1-alpha1",
    author='Mathias Santos de Brito',
    author_email='msbrito@uesc.br',
    description='Support library to be used with Backend frameworks to add support '
                'for DCX-UI',
    license="MIT",
    keywords="dcx",
    url="http://github.com/profmathias/cet-100",
    packages=['dcx_utils'],
    long_description='This library should be used when you want to integrate some '
                     'backend frameworks with DCX-UI.',
    install_requires=['django', 'djangorestframework'],
    python_requires='>=3.6, <4',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],
)
