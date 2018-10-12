require stdlib

node default {

    $userdata = parsejson($ec2_userdata)

    # Set variables from userdata
    $role = $userdata['role']
    $db_endpoint = $userdata['db_endpoint']
    $db_user = $userdata['db_user']
    $db_password = $userdata['db_password']

    case $role {
        "web": { $role_class = "myblog::web" }
        "celery": { $role_class = "myblog::celery" }
        default: { fail("Unrecognized role: $role") }
    }

    # Main myblog class, takes all params
    class { "myblog":
        db_endpoint => $db_endpoint,
        db_user => $db_user,
        db_password => $db_password
    }
    # Role-specific class, e.g. myblog::web
    class { $role_class: }

}