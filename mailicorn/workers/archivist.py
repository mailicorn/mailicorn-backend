import boto

from mailicorn.workers.cache_grabber import get_msg_body

bucket = boto.connect_s3().get_bucket('archive.mailicorn.com')


def archive_mail(mid):
    body = get_msg_body(mid)
    key = bucket.new_key(mid)
    key.set_contents_from_string(body)
    return True
