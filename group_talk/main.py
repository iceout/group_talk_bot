import logging

from pyxmpp2.jid import JID
from pyxmpp2.message import Message
from pyxmpp2.presence import Presence
from pyxmpp2.client import Client

from pyxmpp2.settings import XMPPSettings

from pyxmpp2.interfaces import EventHandler, event_handler, QUIT
from pyxmpp2.interfaces import XMPPFeatureHandler
from pyxmpp2.interfaces import presence_stanza_handler, message_stanza_handler
from pyxmpp2.streamevents import AuthorizedEvent, DisconnectedEvent

from message import *
from db_op import *
from command import *

class Talkbot(DB_oper,EventHandler,XMPPFeatureHandler,Messages,Command):

    def __init__(self,jid,settings):
        self.client = Client(JID(jid),[self],settings)
        
    def run_bot(self):
        self.client.connect()
        self.client.run()

    def stop_bot(self):
        self.client.disconnect()

    @event_handler(DisconnectedEvent)
    def handle_disconnect(self,event):
        return QUIT

    @event_handler()
    def handle_all(self,event):
        logging.info(u"--{0}".format(event))

    @message_stanza_handler()
    def handle_message(self,stanza):
        if stanza.stanza_type!='chat':
            return True
        current_jid = stanza.from_jid
        body = stanza.body
        if body[0]=='-':
            logging.info(u"handle command which is {0}".format(body))
            command = body.split(' ')[0]
            print 'in main command is %s' % (command)
            self.dispatch_command(command,stanza)
            logging.info(u"handle command which is {0} done".format(body))
        else:
            logging.info(u"handle common message which is {0}".format(body))
            self.dispatch_message(stanza.body,current_jid.bare())
            logging.info(u"handle common message whcih is {0} done".format(body))
        return True

    @presence_stanza_handler("subscribe")
    def handle_subscribe(self,stanza):
        logging.info(u"{0} request presence subscripiton ".format(stanza.from_jid))
        
        sender = stanza.from_jid
        bare_jid = sender.bare().as_string()
        self.add_user(bare_jid)

        presence = Presence(to_jid=stanza.from_jid.bare(),stanza_type="subscribe")
        return [stanza.make_accept_response(),presence]

    def get_online_users(self):
        users = [x.jid for x in self.client.roster if x.subscription=='both']
        print self.client.roster
        return users

    def send_message(self,receiver,msg):
        if isinstance(receiver,str):
            receiver=JID(receiver)
        message = Message(
                        stanza_type='chat',
                        from_jid = self.client.jid,
                        to_jid = receiver,
                        body = msg,)
        self.send(message)

    def send(self,stanza):
        self.client.stream.send(stanza)

    def do_unsubscribe(self,jid,type = 'unsubscribe'):
        jid = JID(jid)
        presence = Presence(to_jid=jid,stanza_type=type)
        self.send(presence)

    def delete_from_roster(self,jid):
        self.client.roster.delItem(jid)

your_jid = r'ghy@iceout.info'
logging.basicConfig(level=logging.INFO)

settings = XMPPSettings({
                            "software_name": "Talkbot",
                            u"starttls": True,
                            u"password": r'1',
                            u"tls_verify_peer": False,
                           })
bot = Talkbot(your_jid,settings) 
try :
    DB_oper.db_init()
    bot.run_bot()
except KeyboardInterrupt:
    bot.stop_bot()


        
