#!/usr/bin/env python

from boto.ec2 import connect_to_region

ec2_conn = connect_to_region('us-east-1')

print 'Deleting retired AMI images.\n'

for image in ec2_conn.get_all_images(owners = 'self', filters = {'tag:environment': 'retired'}):
  print ' Deleting image %s and associated snapshot' % (image.id)
  image.deregister(delete_snapshot = True)