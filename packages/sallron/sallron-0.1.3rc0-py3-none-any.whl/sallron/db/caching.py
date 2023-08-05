#!/usr/bin/env python
from sallron.util import settings
from sallron.db import mongo
from walrus import Database
from redis import Redis
from time import sleep
import datetime
import schedule
import logging
import os
import sys

_REDIS_HOST = '127.0.0.1' # standard

class RedisCache():
    def __init__(self):

        self.cache_logger = logging.getLogger('cache')
        self.cache = Database().cache()

        self.connection_retries = 0
        self.max_connection_retries = 3

        # redis-server check and handling
        if not(self._check_connection()):
            self.cache_logger.warning("Redis-server not running!")
            try:
                self.cache_logger.info("Starting redis-server on background.")
                self._start_redis()
            except:
                # self.cache_logger.warning("Redis-server not installed!")
                # self._install_redis()
                self.cache_logger.warning("Redis-server could not be started!")
                sys.exit()

    def schedule_new_customers_checking(self, mongo_client, interface, interface_name, fn):
        """
        Utility function to schedule checking of customers

        Args:
            mongo_client (MongoDB class instance): MongoDB class instance defined in ```e_raptor/db/mongo.py```
            interface (str): Interface that is running at the moment.
            fn (function object): Function to be scheduled in case a new customer was added.
        """
        self.cache.set(f"{interface_name}_customers", mongo_client.databases)

        # schedule checking new customers
        schedule.every().day.at("15:00").do(
            self._check_customers,
            interface=interface,
            interface_name=interface_name,
            fn=fn
        )

    def _check_customers(self, interface, interface_name, fn):
        """
        Utility function to check whether a new customer was added to MongoDB.
        In case it was, schedule all functions to the new customer

        Args:
            interface (str): Interface that is running at the moment.
            fn (function object): Function to be scheduled in case a new customer was added.
        """

        current_customers = self.cache.get(f"{interface_name}_customers")

        real_customers = mongo.MongoDB().databases

        intersection = list(
            set(current_customers).intersection(real_customers)
        )

        if intersection == real_customers:

            self.cache_logger.info("No new customer added between {} and {}".format(
                self.cache.get("lastRun"),
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))
        
        else:

            self.cache.set(f"{interface_name}_customers", real_customers)

            for customer in set(real_customers) - set(current_customers):

                fn(customer, interface, interface_name)
                self.cache_logger.info("New customer added between {} and {}: {}".format(
                    self.cache.get("lastRun"),
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    customer
                ))

            schedule.run_all()

        # set date of last time this function has run
        self.cache.set("lastRun", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def _check_connection(self):
        r = Redis(_REDIS_HOST, socket_connect_timeout=1) # short timeout for the test
        try:
            r.ping() 
            self.cache_logger.info('Connected to Redis @"{}"'.format(_REDIS_HOST))
            return True
        except:
            self.cache_logger.info('Failed to ping Redis, check your connection.')
            return False

    def _start_redis(self):
        if settings.OS == 'UBUNTU':
            os.popen("service redis-server start --daemonize yes")
        else:
            os.popen("redis-server --daemonize yes")
        sleep(2)
        if (self._check_connection()):
            self.cache_logger.info("Redis-server started.")
            self.connection_retries = 0
        else:
            self.connection_retries += self.connection_retries
            if self.connection_retries < self.max_connection_retries:
                self.cache_logger.info(f"Failed to start redis-server, retrying for the {self.connection_retries} time.")
                self._start_redis()
            else:
                self.cache_logger.warning("Max retries reached, check your redis-server installation/config.")

    def _install_redis(self):
        """
        Try to stay away from using this function. Not tested.
        """
        os.popen("sudo -s")
        if settings.OS == 'UBUNTU':
            os.popen("apt install redis-server")
        else:
            os.popen("brew install redis")
        sleep(10)
        self.cache_logger.info("Redis-server installed.")
