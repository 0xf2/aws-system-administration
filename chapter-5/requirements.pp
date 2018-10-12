class myblog::requirements {

    $packages = ["python-dev", "python-pip", "libtiff5-dev", "libjpeg8-dev", "zlib1g-dev", "libfreetype6-dev","python-mysqldb", "mysql-client-5.6",
 "libmysqlclient-dev"]

    package { $packages:
        ensure  => installed
    }

    $pip_packages = ["Mezzanine"]

    package { $pip_packages:
        ensure  => installed,
        provider => pip,
        require => Package[$packages]
    }

    user { "mezzanine":
        ensure  => present
    }

    file { "$myblog::app_path":
        ensure  => "directory",
        owner   => "mezzanine",
        group   => "mezzanine"
    }

}