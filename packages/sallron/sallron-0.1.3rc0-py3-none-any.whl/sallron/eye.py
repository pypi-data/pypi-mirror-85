from sallron.util import settings, logger, executor
from sallron.enforcer import write_pid
from sallron.db import caching, mongo
import datetime
import schedule
import logging
import inspect
import pytz
import os

class TheEyeofSauron:
    def __init__(self, customer, info, interface_class, interface_name):
        write_pid(str(os.getpid()))
        # Logging
        self.sauron_logger = logging.getLogger('sauron')
        self.sauron_logger.info('Intializing.')

        # Internal class variables
        self._customer = customer
        self._info = info
        self._interface = interface_class(**info.get(interface_name))
        self._interface_name = interface_name

    def setup_schedulers(self, dictator, mongo_client):

        # filter methods and get only the blocks
        methods = filter(
            lambda method: not isinstance(
                inspect.getattr_static(self._interface, method.__name__),
                staticmethod
            ),
            filter(
                lambda method: not method.__name__.startswith('_'),
                filter(
                    inspect.ismethod,
                    map(
                        lambda name: getattr(self._interface, name),
                        dir(self._interface)
                    )
                )
            )
        )

        for method in methods:
            if method.__name__ != "load_time_block":
                schedule.every(dictator.get(self._interface_name).get(method.__name__)).minutes.do(
                    self.fetch_and_store,
                    method=method,
                    period=dictator.get(self._interface_name).get(method.__name__),
                    mongo_client=mongo_client
                )
            else:
                schedule.every().day.at(
                    datetime.time(
                        hour=23, 
                        minute=00, 
                        tzinfo=pytz.timezone(settings.TIMEZONE)).strftime("%H:%M")
                        ).do(
                            self.fetch_and_store,
                            method=method,
                            period=dictator.get(self._interface_name).get(method.__name__),
                            mongo_client=mongo_client)

    def fetch_and_store(self, method, period, mongo_client):
        self.sauron_logger.info(
            'Fetching and storing: {0}'.format(
                method.__name__
            ))

        fetched_data = method(period=period)

        self.sauron_logger.debug('Data received: {0}'.format(fetched_data))

        mongo_client.insert_data(self._customer, method.__name__, fetched_data)

def ring_ruler(interface, interface_name, log_dir, key_path, test=False):
    mongo_client = mongo.MongoDB()

    def fn(_customer, _interface, _interface_name):

        mongo_client = mongo.MongoDB()

        info = mongo_client.fetch_data(_customer, settings.ADMIN_COLLECTION, {})

        saruman = TheEyeofSauron(_customer, info, _interface, _interface_name)

        saruman.setup_schedulers(info.get("schedulers"), mongo_client)

    for customer in mongo_client.databases:
        fn(customer, interface, interface_name)

    cache_server = caching.RedisCache()
    cache_server.schedule_new_customers_checking(mongo_client, interface, interface_name, fn)

    executor.schedule_log_sending_and_kill_process(log_dir, 'America/Sao_Paulo')

    schedule.run_all() # run all jobs straight away so we're not left without data for long
    if not(test):
        while True:
            schedule.run_pending()

def configureye(**kwargs):
    for key, value in kwargs.items():
        setattr(settings, key, value)