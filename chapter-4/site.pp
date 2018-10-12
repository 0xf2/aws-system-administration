require stdlib

node default {
    $userdata = parsejson($ec2_userdata)
	
    $role = $userdata['role']
	
    case $role {
        "web": {
                 require my_web_module
        }
        "db": {
                 require my_database_module
        }
        default: { fail("Unrecognised role: $role") }
    }

}