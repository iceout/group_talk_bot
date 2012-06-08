import logging

logger = logging.getLogger(__name__)

class Command():
    
    def dispatch_command(self,command,stanza):
        command = command[1:]
        print 'the command is %s ' % (command)
        do_command = getattr(self,'do_'+command,None)
        if callable(do_command):
            do_command(stanza)
            

    def do_kickoff(self,stanza):
        jid = str(stanza.body).split(' ')[1]
        logger.info('kick off user whose JID is %s',jid)
        u=self.find_user_by_jid(jid)
        self.delete_user(u)

    def do_changenick(self,stanza):
        jid = stanza.from_jid.bare().as_string()
        print jid
        new_nickname = str(stanza.body).split(' ')[1]
        print 'new nick is %s' % (new_nickname)
        logger.info('changing nickname to %s ',new_nickname)
        self.set_nickname(jid,new_nickname)
