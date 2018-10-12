node default {

    require stdlib

    $userdata = loadjson('/tmp/role.json')
    $role = $userdata['role']

    case $role {
        'web': {
            include role::www::dev

        }
        'db': {
            include role::db::dev
        }
        default: { fail("Unrecognized role: ${role}") }
    }

}