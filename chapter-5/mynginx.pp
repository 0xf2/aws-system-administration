class myblog::mynginx {

    class { "nginx": }

    nginx::resource::upstream { "myblog_app":
        ensure  => present,
        members => [
            'localhost:8000',
        ]
    }

    nginx::resource::vhost { "blog.example.com":
        ensure  => enable,
        listen_options => "default",
        proxy   => "http://myblog_app"
    }

}