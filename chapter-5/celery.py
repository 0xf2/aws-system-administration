class myblog::celery {
    Class["myblog::celery"] -> Class["myblog"]

    supervisor::service { "myblog_celery":
        ensure  => present,
        enable  => true,
        command => "/usr/bin/python ${myblog::app_path}/manage.py celery -A myblog worker",
        user    => "mezzanine",
        group   => "mezzanine"
    }

}