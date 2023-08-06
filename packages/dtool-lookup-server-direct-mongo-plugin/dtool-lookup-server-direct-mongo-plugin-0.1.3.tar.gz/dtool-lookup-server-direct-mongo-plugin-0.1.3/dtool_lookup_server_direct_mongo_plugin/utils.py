"""Utility functions."""
# TODO: expose protected members _preprocess_privileges and _dict_to_mongo_query
#       of dtool_lookup_server.utils publically for plugin API.

import logging

from flask import current_app
from dtool_lookup_server import mongo, MONGO_COLLECTION

import dtoolcore.utils
import dtool_lookup_server.utils

from .config import Config

logger = logging.getLogger(__name__)


def config_to_dict(username):
    # TODO: check on privileges
    return Config.to_dict()


def _dict_to_mongo_query(query_dict):
    """Construct mongo query as usual, but allow embedding a raw mongo query.

    Treat query_dict as in dtool_lookup_server.utils._dict_to_mongo_query, but
    additionally embed raw mongo query if key 'query' exists."""

    if "query" in query_dict and isinstance(query_dict["query"], dict):
        raw_mongo = query_dict["query"]
        del query_dict["query"]
    else:
        raw_mongo = {}

    # NOTE: This requires knowledge about the structure of what the original
    # dtool_lookup_server.utils._dict_to_mongo_query returns:
    mongo_query = dtool_lookup_server.utils._dict_to_mongo_query(query_dict)

    if len(raw_mongo) > 0 and len(mongo_query) == 0:
        mongo_query = raw_mongo
    elif len(raw_mongo) > 0 and len(mongo_query) == 1 and "$and" in mongo_query:
        mongo_query["$and"].append(raw_mongo)
    elif len(raw_mongo) > 0:
        mongo_query = {"$and": [mongo_query, raw_mongo]}

    logger.debug("Constructed mongo query: {}".format(mongo_query))
    return mongo_query


def _dict_to_mongo_aggregation(query_dict):
    """Construct mongo query as usual and prepend to aggregation pipeline."""
    if "aggregation" in query_dict and isinstance(query_dict["aggregation"], list):
        aggregation_tail = query_dict["aggregation"]
        del query_dict["aggregation"]
    else:
        aggregation_tail = []

    # unset any _id field, as type ObjectId usually not serializable
    aggregation_tail.append({'$unset': '_id'})

    match_stage = _dict_to_mongo_query(query_dict)
    if len(match_stage) > 0:
        aggregation_head = [{'$match': match_stage}]
    else:
        aggregation_head = []

    aggregation = [*aggregation_head, *aggregation_tail]
    current_app.logger.debug("Constructed mongo aggregation: {}".format(aggregation))
    return aggregation


def query_datasets_by_user(username, query):
    """Query the datasets the user has access to. Allow raw mongo 'query'.

    See dtool_lookup_server.utils.search_datasets_by_user docstring.

    :param username: username
    :param query: dictionary specifying query
    :returns: List of dicts if user is valid and has access to datasets.
              Empty list if user is valid but has not got access to any
              datasets.
    :raises: AuthenticationError if user is invalid.
    """

    query = dtool_lookup_server.utils._preprocess_privileges(username, query)
    # If there are no base URIs at this point it means that the user is not
    # allowed to search for anything.
    if len(query["base_uris"]) == 0:
        return []

    datasets = []
    mongo_query = _dict_to_mongo_query(query)
    cx = mongo.db[MONGO_COLLECTION].find(
        mongo_query,
        {
            "_id": False,
            "readme": False,
            "manifest": False,
            "annotations": False,
        }
    )
    for ds in cx:

        # Convert datetime object to float timestamp.
        for key in ("created_at", "frozen_at"):
            if key in ds:
                datetime_obj = ds[key]
                ds[key] = dtoolcore.utils.timestamp(datetime_obj)

        datasets.append(ds)
    return datasets


def aggregate_datasets_by_user(username, query):
    """Aggregate the datasets the user has access to.
    Valid keys for the query are: creator_usernames, base_uris, free_text,
    aggregation. If the query dictionary is empty, all datasets that a user has
    access to are returned.
    :param username: username
    :param query: dictionary specifying query
    :returns: List of dicts if user is valid and has access to datasets.
              Empty list if user is valid but has not got access to any
              datasets.
    :raises: AuthenticationError if user is invalid.
    """
    if not Config.ALLOW_DIRECT_AGGREGATION:
        current_app.logger.warning(
            "Received aggregate request '{}' from user '{}', but direct "
            "aggregations are disabled.".format(query, username))
        return []  # silently reject request

    # TODO: make applying privileges configurable
    query = dtool_lookup_server.utils._preprocess_privileges(username, query)

    # If there are no base URIs at this point it means that the user has not
    # got privileges to search for anything.
    # TODO: reject on blueprint level (?)
    if len(query["base_uris"]) == 0:
        return []
    datasets = []

    mongo_aggregation = _dict_to_mongo_aggregation(query)
    cx = mongo.db[MONGO_COLLECTION].aggregate(mongo_aggregation)
    # Opposed to search_datasets_by_user, here it is the aggregator's
    # responsibility to project out desired fields and remove non-serializable
    # content. The only modification always applied is removing any '_id' field.
    for ds in cx:
        # Convert datetime object to float timestamp.
        for key in ("created_at", "frozen_at"):
            if key in ds:
                datetime_obj = ds[key]
                ds[key] = dtoolcore.utils.timestamp(datetime_obj)

        datasets.append(ds)

    return datasets
