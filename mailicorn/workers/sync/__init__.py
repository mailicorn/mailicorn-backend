import gevent
from gevent.monkey import patch_all
patch_all()
import boto
from boto.sqs.message import Message
from mailicorn.models import DBSession
from mailicorn.models.users import User
from imapclient import IMAPClient
import pylibmc
import time
import hashlib
import json
import sys
from ConfigParser import ConfigParser


def GetFromQueue(queue):
    backoff_count = 1
    while True:
        rs = queue.get_messages(1)
        if len(rs) == 0:
            time.sleep(pow(3, backoff_count))
            backoff_count += 1
        else:
            return rs[0]


class SQSQueue(object):
    def __init__(self, queue):
        self.queue = queue
        self.msg = None

    def __enter__(self):
        self.msg = GetFromQueue(self.queue)
        return self.msg

    def __exit__(self):
        self.queue.delete_message(self.msg)


class SyncWorker(object):
    def __init__(self, config):
        self.config = config
        self.sqs = boto.connect_sqs()
        self.s3 = boto.connect_s3()
        self.bucket = self.s3.get_bucket(
            config.get('app:main', 'archive.bucket'))
        self.search_queue = self.sqs.get_queue(
            config.get('app:main', 'queue.search'))
        if self.search_queue is None:
            self.search_queue = self.sqs.create_queue(
                config.get('app:main', 'queue.search'))
        self.sync_queue = self.sqs.get_queue(
            config.get('app:main', 'queue.sync'))
        self.ec = pylibmc.Client(config.get('app:main', 'cache.uri'))


    def imap_sync(self, account):
        """
        Run as a greenlet to sit in the background and shit
        data into sqs/EC/S3
        :param account: The Account information we need for sync
        :type account: mailicorn.models.accounts.Account
        """
        host = account.host
        port = account.port
        ssl = account.ssl
        conn_string = "{0}:{1}".format(host, port)
        username = account.username
        password = account.password
        folders = account.folders
        owner_id = account.owner_id
        server = IMAPClient(conn_string, use_uid=True, ssl=ssl)
        server.login(username, password)
        for folder in folders:
            server.select_folder(folder.name)
            messages = server.search(['NOT DELETED'])
            response = server.fetch(messages, ['FLAGS', 'BODY'])
            for msgid, data in response.iteritems():
                MID = hashlib.sha512(str(msgid) + str(account.owner_id)).hexdigest()
                body = data['BODY']
                flags = data['FLAGS']
                mail_dict = {'mid': MID,
                             'owner_id': owner_id,
                             'body': body,
                             'flags': flags,
                             }
                mail_json = json.dumps(mail_dict)
                # send to ElasticCache First
                self.ec.set(str(MID), str(mail_json))

                # Send SQS message to CloudSearch Workers
                cs_msg = Message()
                cs_msg.set_body(mail_json)
                self.search_queue.write(cs_msg)

                # Store backup in s3 (done last since long running)
                key = self.bucket.new_key(MID)
                key.set_contents_from_str(MID, mail_json)
        server.logout()


    def run(self):
        """
        Worker run loop, consume sqs messages and sync the users they secificy
        """
        while True:
            msg = GetFromQueue(self.sync_queue)
            user_id = int(msg.body())
            user_query = DBSession.query(User).filter(User.id==user_id)
            if user_query.count() == 0:
                self.sync_queue.delete_message(msg)
                continue

            user = user_query.one()
            for account in user.accounts:
                gevent.spawn(self.imap_sync, account)
            self.sync_queue.delete(msg)

def main():
    inifile = sys.argv[1]
    config = ConfigParser()
    config.read(inifile)
    sw = SyncWorker(config)
    sw.run()
