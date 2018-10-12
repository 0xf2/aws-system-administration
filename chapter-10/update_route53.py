#!/usr/bin/python

import argparse
import boto.route53
from boto.utils import get_instance_metadata

def do_startup():
	""" This function is executed when the instance launches. The instance's
		IP address will be added to the master or slave DNS record. If the
		record does not exist it will be created.
	"""
	# Check if the master resource record exists
	if zone.get_cname(master_hostname) is None:
		print 'Creating master record: %s' % master_hostname
		status = zone.add_cname(master_hostname, instance_ip, ttl)
		return
	print "Master record exists. Assuming slave role"
 # Check if the slave resource record exists - if more than one result is
 # found by get_cname, an exception is raised. This means that more than 
 # one record exists so we can ignore it.
	try:
		slave_rr_exists = (zone.get_cname(slave_hostname) != None)
	except boto.exception.TooManyRecordsException:
		slave_rr_exists = True

	if slave_rr_exists:
		print 'Slave record exists. Adding instance to pool: %s' \ 
		       % slave_hostname
	else:
		print 'Creating slave record: %s' % slave_hostname
	# Create or update the slave Weighted Resource Record Set
	status = zone.add_cname(slave_hostname, instance_ip, ttl, slave_identifier)


def do_promote():
	master_rr = zone.get_cname(master_hostname)
	print 'Updating master record: %s %s' % (master_hostname, instance_ip)
	zone.update_cname(master_hostname, instance_ip)
	# Remove this instance from the slave CNAME pool by deleting its WRRS
	print 'Removing slave CNAME: %s %s' % (slave_hostname, slave_identifier)
	zone.delete_cname(slave_hostname, slave_identifier)


parser = argparse.ArgumentParser(description='Update Route 53 master/slave DNS records')
parser.add_argument('action', choices=['startup', 'promote'])
#parser.add_argument('--hosted-zone-id', required=True)
parser.add_argument('--domain', required=True)
parser.add_argument('--cluster-name', required=True)
parser.add_argument('--test')


args = parser.parse_args()

metadata = get_instance_metadata()

instance_ip = metadata['local-ipv4']
instance_id = metadata['instance-id']

ttl = 60 # seconds

master_hostname = 'master-%s.%s' % (args.cluster_name, args.domain)
slave_hostname = 'slave-%s.%s' % (args.cluster_name, args.domain)
# Identifier used for slave Weighted Resource Record Set
slave_identifier = ('slave-%s' % instance_id, 10)


conn = boto.route53.connect_to_region('us-east-1')
zone = conn.get_zone(args.domain)

if args.action == 'startup':
	do_startup()
elif args.action == 'promote':
	do_promote()