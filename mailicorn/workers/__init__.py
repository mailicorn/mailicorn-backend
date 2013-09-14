import boto
import json
import time
import pylibmc


memcache_host = 'mailicache.ucd9qd.0001.use1.cache.amazonaws.com'
mc = pylibmc.Client([memcache_host])


def get_msg_body(mid):
    return mc.get(mid)


cs = boto.connect_cloudsearch()

mail_search = cs.lookup('mailicorn-1')
doc_service = mail_search.get_document_service()
search_service = mail_search.get_search_service()
sqs = boto.connect_sqs()


def index_document(mid, queue_name=None):
    if queue_name is None:
        queue_name = 'indexed-msg'
    q = sqs.get_queue(queue_name)
    doc_service.add(mid, int(time.time()), json.loads(get_msg_body(mid)))
    doc_service.commit()
    doc_service.clear_sdf()
    sqs.send_message(q, mid)
    return True


def apply_rule(mid, queue_name=None):
    if queue_name is None:
        queue_name = 'matched-action'
    q = sqs.get_queue(queue_name)
    if search_service.search(bq="(field mid '%s')" % mid):
        sqs.send_message(q, json.dumps({'mid': mid, 'ruleid': None}))
    return True


def await_mail(to_call_on, queue_name=None):
    if queue_name is None:
        queue_name = 'write-to-search'
    q = sqs.get_queue(queue_name)

    backoff = 0
    while True:
        msgs = q.get_messages(visibility_timeout=30, wait_time_seconds=20)
        if len(msgs) == 0:
            if backoff == 0:
                backoff = 2
            elif backoff > 90:
                backoff = 2
            time.sleep(backoff)
            backoff *= 2
            continue
        backoff = 0
        msg = msgs[0]
        print "Received message: ", msg.get_body_encoded()
        if to_call_on(msg.get_body_encoded()):
            msg.delete()
        print "Of type ", type(msg)
        msg.delete()
        exit()

if __name__ == '__main__':

    mails = json.loads(open(
        '/home/ryansb/code/mailicorn-backend/mail_test.json').read())
    for m in mails:
        print mc.set(str(m['mid']), str(json.dumps(m)))

    print mc.get("7eb04e1076c95ae50d75a3c88537b37b07550804")
