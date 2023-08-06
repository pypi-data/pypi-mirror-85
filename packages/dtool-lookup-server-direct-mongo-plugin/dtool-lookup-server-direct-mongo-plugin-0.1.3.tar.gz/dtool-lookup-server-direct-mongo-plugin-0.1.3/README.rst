Dtool Lookup Server Direct Mongo Plugin
=======================================

- GitHub: https://github.com/IMTEK-Simulation/dtool-lookup-server-direct-mongo-plugin
- PyPI: https://pypi.org/project/dtool-lookup-server-direct-mongo-plugin/
- Free software: MIT License


Features
--------

- Query datasets via mongo language
- Funnel datadata through aggregation pipelines 


Introduction
------------

`dtool <https://dtool.readthedocs.io>`_ is a command line tool for packaging
data and metadata into a dataset. A dtool dataset manages data and metadata
without the need for a central database.

However, if one has to manage more than a hundred datasets it can be helpful
to have the datasets' metadata stored in a central server to enable one to
quickly find datasets of interest.

The `dtool-lookup-server <https://github.com/jic-dtool/dtool-lookup-server>`_ 
provides a web API for registering datasets' metadata
and provides functionality to lookup, list and search for datasets.

This plugin allows to submit plain mongo queries and aggregation pipelines
directly to the lookup server's underlying database.