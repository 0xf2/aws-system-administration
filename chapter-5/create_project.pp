class myblog::create_project {

    # Create the Mezzanine project
    exec { "init-mezzanine-project":
        command => "/usr/local/bin/mezzanine-project $myblog::app_path",
        user => "mezzanine",
        creates => "$myblog::app_path/__init__.py"
    }

    # Create the local_settings.py file
    file { "$myblog::app_path/myblog/local_settings.py":
        ensure => present,
        content => template("myblog/local_settings.py.erb"),
        owner => "mezzanine",
        group => "mezzanine",
        require => Exec["init-mezzanine-project"],
        notify  => Exec["init-mezzanine-db"]
    }

    # Create the database
    exec { "init-mezzanine-db":
        command => "/usr/bin/python manage.py createdb --noinput",
        user => "mezzanine",
        cwd => "$myblog::app_path",
        refreshonly => true
    }