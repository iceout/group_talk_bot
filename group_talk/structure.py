from mongokit import Document,Connection
import datetime
import logging

import config
logger = logging.getLogger(__name__)
global connection
class User(Document):
    __collection__ = config.connection_prefix+'User'
    __database__ = config.database
    use_schemaless = True
    structure={
        'jid':str,
        'nickname':str,
        'join_time':datetime.datetime,
        'last_login_time':datetime.datetime,
        'flag':int
        }
    required_fields = ['jid']
    default_values = {
                'join_time':datetime.datetime.utcnow(),
                'flag':1,
            }

def init():
    global connection
    logger.info('connecting to database')
    #conn_args = getattr(config,'conn_args',{})
    connection = Connection()
    logger.info('database connected ')
    connection.register([User])
