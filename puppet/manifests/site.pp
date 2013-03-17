#ft: ruby
stage { [pre, post]: }
Stage[pre] -> Stage[main] -> Stage[post]

class { apt-hupdate: stage => pre }

Exec { path => [ "/usr/local/bin", "/usr/bin", "/bin", "/usr/local/games", "/usr/games" ] }

File { owner => 0, group => 0, mode => 0644 }

file { '/var/www':
  ensure => "directory",
}

file { '/var/www/drunkspotting.com':
   ensure => 'link',
   target => '/home/vagrant/drunkspotting.com',
}

include puppet

include nginxphp

class { 'nginxphp::php': php_packages => [ "php5-curl", "php5-imagick", "php5-xcache", "php5-xdebug" ], withppa => true }

include nginxphp::nginx

nginxphp::fpmconfig { 'drunkspotting': php_devmode => true, fpm_listen => '127.0.0.1:9000', fpm_allowed_clients => '127.0.0.1', fpm_user => 'www-data', fpm_group => 'www-data' }

nginxphp::nginx_addphpconfig { 'local.drunkspotting.com': website_root => "/var/www/drunkspotting.com/ui/web", php_pool_addr => "127.0.0.1:9000", default_controller => "index_dev.php", require => Nginxphp::Fpmconfig['drunkspotting'] }
