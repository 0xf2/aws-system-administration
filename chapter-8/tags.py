from boto.utils import get_instance_metadata
from boto.ec2 import connect_to_region

metadata = get_instance_metadata()
my_instance_id = metadata['instance-id']

conn = connect_to_region('us-east-1')
for reservations in conn.get_all_instances(filters={'instance-id': my_instance_id}):
# There will be only one instance in the results 
 for instance in reservations.instances:
   for tag in instance.tags:
     # Iterate through the tags, printing the keys and values
     print "Key \'%s\' has value \'%s\'" % (tag, instance.tags[tag])