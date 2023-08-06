import os
import json
import boto
from boto.s3.key import Key


def bucket():
    name = os.environ['POSTAL_AWS_BUCKET']
    region = os.environ['POSTAL_AWS_REGION']
    return boto.connect_s3(host=f's3-{region}.amazonaws.com').get_bucket(name)

def get(key):
    try:
        k = Key(bucket())
        k.key = key
        return json.loads(k.get_contents_as_string())
    except boto.exception.S3ResponseError as exc:
        if exc.status == 404: return {}
        raise exc

def set(key, value):
    k = Key(bucket())
    k.key = key
    k.set_contents_from_string(json.dumps(value))
