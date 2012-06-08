

from db import *

class Messages():
    
    def get_message_reveivers(self):
        return self.get_online_users()

    def dispatch_message(self,msg,current_jid,timestamp=None):
        receivers = self.get_message_reveivers()
        for receiver in receivers:
            if receiver.bare()==current_jid:
                continue
            sender = self.find_user_by_jid(current_jid.as_string())
            if sender:
                nick = sender['nickname']
                msg='['+str(nick)+'] : '+msg
                self.send_message(receiver,msg)
            else:
                logger.info("%s does not exist in the database",current_jid.as_string())
