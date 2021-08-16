#!/usr/bin/env python3

import os
import boto3
import json
import botocore
import argparse

endpoint_url = 'http://rook-ceph-rgw-s3a.openshift-storage'
aws_access_key_id = os.environ['ACCESS_KEY_ID']
aws_secret_access_key = os.environ['SECRET_ACCESS_KEY']

s3 = boto3.client('s3',
                endpoint_url = endpoint_url,
                aws_access_key_id = aws_access_key_id,
                aws_secret_access_key = aws_secret_access_key,
                region_name = 'default',
                config=botocore.client.Config(signature_version = 's3'))

sns = boto3.client('sns', 
                endpoint_url = endpoint_url, 
                aws_access_key_id = aws_access_key_id,
                aws_secret_access_key= aws_secret_access_key,
                region_name='default', 
                config=botocore.client.Config(signature_version = 's3'))

attributes = {}
attributes['push-endpoint'] = 'kafka://my-cluster-kafka-bootstrap.ach:9092'
attributes['kafka-ack-level'] = 'broker'

def create_topic(topic):
    topic_arn = sns.create_topic(Name=topic, Attributes=attributes)['TopicArn']
    return topic_arn

create_topic('rdfi')
create_topic('odfi')
create_topic('merchant-upload')

sns.list_topics()

def create_bucket(bucket_name):
    result = s3.create_bucket(Bucket=bucket_name)
    return result

create_bucket('ach-merchant-upload')
for i in range(1,8):
    create_bucket('ach-odfi-0620000'+str(i))
    create_bucket('ach-rdfi-0620000'+str(i))

s3.list_buckets()['Buckets']

bucket_notifications_configuration = {
            "TopicConfigurations": [
                {
                    "Id": 'merchant-upload',
                    "TopicArn": 'arn:aws:sns:s3a::merchant-upload',
                    "Events": ["s3:ObjectCreated:*", "s3:ObjectRemoved:*"]
                }
            ]
        }

s3.put_bucket_notification_configuration(Bucket = 'ach-merchant-upload',
        NotificationConfiguration=bucket_notifications_configuration)

s3.get_bucket_notification_configuration(Bucket = 'ach-merchant-upload')

for i in range(1,8):
    bucket_notifications_configuration = {
                "TopicConfigurations": [
                    {
                        "Id": 'ach-odfi-0620000'+str(i),
                        "TopicArn": 'arn:aws:sns:s3a::odfi',
                        "Events": ["s3:ObjectCreated:*", "s3:ObjectRemoved:*"]
                    }
                ]
            }
    s3.put_bucket_notification_configuration(Bucket = 'ach-odfi-0620000'+str(i),
        NotificationConfiguration=bucket_notifications_configuration)

for i in range(1,8):
    print('ach-odfi-0620000'+str(i))
    print(s3.get_bucket_notification_configuration(Bucket = 'ach-odfi-0620000'+str(i))['TopicConfigurations'])

for i in range(1,8):
    bucket_notifications_configuration = {
                "TopicConfigurations": [
                    {
                        "Id": 'ach-rdfi-0620000'+str(i),
                        "TopicArn": 'arn:aws:sns:s3a::rdfi',
                        "Events": ["s3:ObjectCreated:*", "s3:ObjectRemoved:*"]
                    }
                ]
            }
    s3.put_bucket_notification_configuration(Bucket = 'ach-rdfi-0620000'+str(i),
        NotificationConfiguration=bucket_notifications_configuration)

for i in range(1,8):
    print(s3.get_bucket_notification_configuration(Bucket = 'ach-rdfi-0620000'+str(i))['TopicConfigurations'])
