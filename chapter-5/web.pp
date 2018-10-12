class myblog::web {
    Class["myblog::web"] -> Class["myblog"]

    require myblog::mynginx

    supervisor::service { "myblog_app":
        ensure  => present,
        enable  => true,
        command => "/usr/bin/python ${myblog::app_path}/manage.py runserver",
        stopasgroup => true,
        killasgroup => true,
        user    => "mezzanine",
        group   => "mezzanine"
    }

}