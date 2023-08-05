from os import path, getcwd

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

try:
    with open(path.join(getcwd(), 'VERSION')) as version_file:
        version = version_file.read().strip()
except IOError:
    raise

setup(
    name='helix.events.sdk',
    version=version,
    packages=find_packages(),
    url='https://github.com/icanbwell/helix.events.sdk',
    license='Apache 2.0',
    author='Michael Vidal',
    author_email='michael.vidal@icanbwell.com',
    description='Event SDK for creating Events in the helix architecture',
    install_requires=["cloudevents==1.2.0", "fhir.resources==5.1.1", "kafka-python==2.0.2"],
    package_data={"helix_events_sdk": ["py.typed"]},
    long_description=long_description,
    long_description_content_type="text/markdown",
)
