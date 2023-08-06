#!/usr/bin/env python
"""Core module for mongodb related operations"""

from sallron.util import settings, parser
import pymongo
import json
import os

class MongoDB():
    def __init__(self):
        """
        Single cluster, optionally database-specific pymongo object
        with utility-focused functions
        """

        self.client = MongoDB.make_client()
        self.databases = [database for database in self.client.list_database_names() if database not in settings.ADMIN_DATABASES]

    def database(self, database_name):
        if database_name not in self.databases:
            raise("Database not found")
        else:
            return getattr(self.client, database_name)

    @staticmethod
    def make_client():
        """
        Utility funciton to load MongoClient

        Args:
            -

        Returns:
            Client for a MongoDB instance
        """

        client = pymongo.MongoClient(settings.MONGO_CONN_STR)

        return client

    def insert_data(self, database, collection, data):
        """
        Utility function to insert data to a collection

        Args:
            database (str): Name of the brand in which data will be inserted
            collection (str): Name of the collection
            data (dict): Input data dict
        """

        # clean punctuation from data
        data = parser.camelify(data)
        data = parser.remove_punctuation(data)

        collection = getattr(getattr(self.client, database), collection)
        collection.insert_one(data)

    def delete_data(self, database, collection, _filter):
        """
        Utility function to delete data from collection that matches the query

        Args:
            database (str): Name of the brand in which data will be inserted
            _filter (dict): Input filter dict
            collection (str): Name of the collection
        """

        collection = getattr(getattr(self.client, database), collection)
        collection.delete_one(_filter)

    def fetch_data(self, database, collection, _filter, _one=True):
        """
        Utility function to make a filter in any collection

        Args:
            database (str): Name of the brand in which data will be inserted
            collection (str): Name of the collection
            _filter (dict): Input filter dict
            one (bool): Indicates whether to return only one object or a batch

        Returns:
            dict: Dict containing object that matches the filter
        """

        collection = getattr(getattr(self.client, database), collection)
        _object = collection.find_one(_filter) if _one else collection.find(_filter)

        return _object


class MongoDBTesting():
    def __init__(self):
        """
        Single cluster, optionally database-specific pymongo object
        with utility-focused functions
        """

        self.client = MongoDB.make_client()
        self.databases = [database for database in self.client.list_database_names() if database not in ["admin", "local"]]

    def database(self, database_name):
        if database_name not in self.databases:
            raise("Database not found")
        else:
            return getattr(self.client, database_name)

    @staticmethod
    def make_client():
        """
        Utility funciton to load MongoClient

        Args:
            -

        Returns:
            Client for a MongoDB instance
        """

        client = pymongo.MongoClient(settings.MONGO_TESTING_CONN_STR)

        return client

    def insert_data(self, database, collection, data):
        """
        Utility function to insert data to a collection

        Args:
            database (str): Name of the brand in which data will be inserted
            collection (str): Name of the collection
            data (dict): Input data dict
        """

        # clean punctuation from data
        data = parser.camelify(data)
        data = parser.remove_punctuation(data)

        collection = getattr(getattr(self.client, database), collection)
        collection.insert_one(data)

    def delete_data(self, database, collection, _filter):
        """
        Utility function to delete data from collection that matches the query

        Args:
            database (str): Name of the brand in which data will be inserted
            _filter (dict): Input filter dict
            collection (str): Name of the collection
        """

        collection = getattr(getattr(self.client, database), collection)
        collection.delete_one(_filter)

    def fetch_data(self, database, collection, _filter, _one=True):
        """
        Utility function to make a filter in any collection

        Args:
            database (str): Name of the brand in which data will be inserted
            collection (str): Name of the collection
            _filter (dict): Input filter dict
            one (bool): Indicates whether to return only one object or a batch

        Returns:
            dict: Dict containing object that matches the filter
        """

        collection = getattr(getattr(self.client, database), collection)
        _object = collection.find_one(_filter) if _one else collection.find(_filter)

        return _object

    def insert_customer(self, kwargs):
        """
        Utility function to insert a new customer

        Kwargs:
            customer-name (str): Name of the customer
            payed-until (datetime.datetime): Period in which data will be captured for the customer
            active (bool): Indicates whether customer is active or not
            api-key (str): VTEX API key
            api-token (str): VTEX API token
            environment (str): Input domain defining the environment. Normally 'vtexcommercestable'
            account-name (str): VTEX account name, e.g. fibracirurgica, electrolux, etc
            service-account (dict): Google Analytics key dict
            view-id (str): Google Analytics view ID
            timezone (str): String defining the timezone to get data. Check
                            https://gist.github.com/matheushent/40b004923b2293721d136b02b8426f67
                            for a complete list of available timezones
            pagespeed-key (str): Input key for PageSpeed API
            url (List): Comma-separated list of URLs for requesting by PageSpeed
        """

        collection = self.client[kwargs.get("customer-name")]['info']

        collection.insert_one(kwargs)

class MongoAdmin():
    def __init__(self):
        """
        Single cluster, optionally database-specific pymongo object
        with utility-focused functions
        """

        self.client = self.make_client()

        self.databases = self.client.list_database_names()[2:]

    def make_client(self):
        """
        Utility funciton to load MongoClient

        Args:
            -

        Returns:
            Client for a MongoDB instance
        """
    
        client = pymongo.MongoClient(settings.MONGO_CONN_STR)

        return client

    def capped_collection(self, coll_name, db, max_size=50000000):
        """
        Utility function to create a capped collection

        Args:
            coll_name (str): Name of the collection
            db (pymongo.database.Database): Database instance in which the collection will be created
            max_size (int): Maximum size allowed to the collection
        """

        db.create_collection(coll_name, capped=True, size=max_size)

    def insert_data(self, database, collection, data):
        """
        Utility function to insert data to a collection

        Args:
            database (str): Name of the brand in which data will be inserted
            collection (str): Name of the collection
            data (dict): Input data dict
        """

        collection = self.client[database][collection]
        collection.insert_one(data)

    def delete_data(self, database, _filter, collection='data'):
        """
        Utility function to delete data from collection that matches the query

        Args:
            database (str): Name of the brand in which data will be inserted
            _filter (dict): Input filter dict
            collection (str): Name of the collection
        """

        collection = self.client.get(database)[collection]
        collection.delete_one(_filter)

    def _filter(self, database, _filter, collection='data', one=True):
        """
        Utility function to make a filter in any collection

        Args:
            database (str): Name of the brand in which data will be inserted
            collection (str): Name of the collection
            _filter (dict): Input filter dict
            one (bool): Indicates whether to return only one object or a batch

        Returns:
            dict: Dict containing object that matches the filter
        """

        collection = self.client.get(database)[collection]

        if one:
            _object = collection.find_one(_filter)
        else:
            _object = collection.find(_filter)

        return _object

    def insert_customer(self, kwargs):
        """
        Utility function to insert a new customer

        Kwargs:
            customer-name (str): Name of the customer
            payed-until (datetime.datetime): Period in which data will be captured for the customer
            active (bool): Indicates whether customer is active or not
            api-key (str): VTEX API key
            api-token (str): VTEX API token
            environment (str): Input domain defining the environment. Normally 'vtexcommercestable'
            account-name (str): VTEX account name, e.g. fibracirurgica, electrolux, etc
            service-account (dict): Google Analytics key dict
            view-id (str): Google Analytics view ID
            timezone (str): String defining the timezone to get data. Check
                            https://gist.github.com/matheushent/40b004923b2293721d136b02b8426f67
                            for a complete list of available timezones
            pagespeed-key (str): Input key for PageSpeed API
            url (List): Comma-separated list of URLs for requesting by PageSpeed
        """

        collection = self.client[kwargs.get("customer-name")].info

        collection.insert_one(kwargs)

    def delete_customer(self, name):
        """
        Utility function to delete a customer.

        Args:
            name (str): Name of the customer
        """

        self.client.drop_database(name)

    def activate_customer(self, name):
        """
        Utility function to activate the status of a customer

        Args:
            name (str): Name of the customer
        """

        collection = self.client[name].info

        collection.update_one(
            {
                "customer-name": name
            },
            {
                "$set": {
                    "active": True
                }
            }
        )

    def deactivate_customer(self, name):
        """
        Utility function to deactivate the status of a customer

        Args:
            name (str): Name of the customer
        """

        collection = self.client[name].info

        collection.update_one(
            {
                "customer-name": name
            },
            {
                "$set": {
                    "active": False
                }
            }
        )