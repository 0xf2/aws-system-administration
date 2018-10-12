require 'facter'
require 'json'

if Facter.value("ec2_instance_id") != nil
 instance_id = Facter.value("ec2_instance_id")
 region = Facter.value("ec2_placement_availability_zone")[0..-2]

 cmd = <<eos
  aws ec2 describe-tags
   --filters \"name=resource-id,values=#{instance_id}\"
   --region #{region}
   | jq '[.Tags[] | {key: .Key, value: .Value}]'
 eos
 tags = Facter::Util::Resolution.exec(cmd)

 parsed_tags = JSON.parse(tags)
 parsed_tags.each do |tag|
  fact = "ec2_tag_#{tag["key"]}"
  Facter.add(fact) { setcode { tag["value"] } }
 end
end