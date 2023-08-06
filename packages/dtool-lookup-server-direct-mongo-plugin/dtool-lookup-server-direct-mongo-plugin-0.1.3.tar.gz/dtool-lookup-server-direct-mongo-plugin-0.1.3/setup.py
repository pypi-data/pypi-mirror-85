from setuptools import setup
from setuptools_scm import get_version
version = get_version(root='.', relative_to=__file__)


def local_scheme(version):
    """Skip the local version (eg. +xyz of 0.6.1.dev4+gdf99fe2)
    to be able to upload to Test PyPI"""
    return ""


url = "https://github.com/IMTEK-Simulation/dtool-lookup-server-direct-mongo-plugin"
readme = open('README.rst').read()

setup(
    name="dtool-lookup-server-direct-mongo-plugin",
    packages=["dtool_lookup_server_direct_mongo_plugin"],
    description="""This plugin allows to submit mongo queries and aggregation
                   pipelines directly to the lookup server's underlying MongoDB.""",
    long_description=readme,
    author="Johannes Hörmann",
    author_email="johannes.hoermann@imtek.uni-freiburg.de",
    use_scm_version={"local_scheme": local_scheme},
    url=url,
    entry_points={
        'dtool_lookup_server.blueprints': [
            'dtool_lookup_server_direct_mongo_plugin=dtool_lookup_server_direct_mongo_plugin:mongo_bp',
        ],
    },
    setup_requires=['setuptools_scm'],
    install_requires=[
        "dtool-lookup-server>=0.15.0",
        "dtoolcore>=3.17.0",
    ],
    download_url="{}/tarball/{}".format(url, version),
    license="MIT"
)
