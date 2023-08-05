from setuptools import setup
setup(
    name='kafka-connect-python-helper',
    version='0.0.6',
    description='Toolset for Kafka Connect REST API',
    long_description='This package can be used to simplify HTTP commands for the Kafka Connect REST API. The package is created spefically for deploying connectors automatically, but can also be used to simplify one-time commands.',
    url='https://github.com/MrMarshall/kafka-connect-python-helper',
    author='Marcel Renders',
    license='MIT',
    packages=['connect_helper'],
    install_requires=[
        'requests (>=2.24.0)',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',
    ],
)
