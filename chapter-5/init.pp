class myblog ( $db_endpoint, $db_user, $db_password ) {

    $app_path = "/srv/mezzanine"
    
    class {"supervisor": }

    require myblog::requirements
}