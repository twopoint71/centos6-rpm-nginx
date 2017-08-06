summary: nginx high performance web server
name: nginx
version: 1.12.1
release: 1.el6
# MIT License
# http://opensource.org/licenses/MIT
license: MIT
source:  http://nginx.org/download/nginx-1.12.1.tar.gz
source1: ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-8.41.tar.gz
source2: http://zlib.net/zlib-1.2.11.tar.gz
source3: https://www.openssl.org/source/openssl-1.0.2l.tar.gz

%description
The nginx-filesystem package contains the basic directory layout
for the Nginx server including the correct permissions for the
directories.

%global usr_bin_dir %_usr/bin
%global usr_sbin_dir %_usr/sbin
%global sbin_dir /sbin
%global nginx_prefix %_usr/local/nginx

%prep
%setup
%setup -D -T -b 1
%setup -D -T -b 2
%setup -D -T -b 3

%pre
# shamelessly nabbed and modified from 
# http://stackoverflow.com/questions/14810684/check-whether-a-user-exists
# installs user for "rpm -i"
ret=0
%usr_bin_dir/getent passwd %name >> /dev/null 2>&1 && ret=1
if [ ${ret} -lt 1 ]
  then 
    %usr_sbin_dir/useradd -c "Nginx" -s /bin/false -r -d %nginx_prefix/sbin %name 2>/dev/null
  fi

%post
%sbin_dir/chkconfig nginx on 2>/dev/null
%sbin_dir/service nginx stop
%sbin_dir/service nginx start

%preun
%sbin_dir/chkconfig nginx off 2>/dev/null
%sbin_dir/service nginx stop

# preserve configs
%__cp -f %nginx_prefix/conf/nginx.conf %nginx_prefix/conf/nginx.conf.rpmsave
%__cp -f %nginx_prefix/sites-available/vhost.example.conf %nginx_prefix/sites-available/vhost.example.conf.rpmsave

%postun
for i in cache logs sbin ssl
  do
    %__rm -rf %nginx_prefix/${i}
  done
%__rm -f %_sysconfdir/init.d/nginx
%__rm -f %_sysconfdir/logrotate.d/nginx
%__rm -f %_usr/local/sbin/nginx

%build
./configure \
--prefix=%nginx_prefix \
--with-http_gzip_static_module \
--with-http_v2_module \
--with-http_stub_status_module \
--with-ipv6 \
--with-file-aio \
--with-zlib=%_builddir/zlib-1.2.11 \
--with-pcre=%_builddir/pcre-8.41 \
--http-client-body-temp-path=%nginx_prefix/cache/client_temp \
--http-proxy-temp-path=%nginx_prefix/cache/proxy_temp \
--http-fastcgi-temp-path=%nginx_prefix/cache/fastcgi_temp \
--http-uwsgi-temp-path=%nginx_prefix/cache/uwsgi_temp \
--http-scgi-temp-path=%nginx_prefix/cache/scgi_temp \
--error-log-path=%nginx_prefix/logs/error.log \
--http-log-path=%nginx_prefix/logs/access.log \
--pid-path=%nginx_prefix/nginx.pid \
--user=%name \
--group=%name \
--with-http_ssl_module \
--with-openssl-opt=enable-tlsext \
--with-openssl=%_builddir/openssl-1.0.2l

%install
# shamelessly nabbed and modified from 
# http://stackoverflow.com/questions/14810684/check-whether-a-user-exists
# installs user for "rpmbuild"
ret=0
%usr_bin_dir/getent passwd %name >> /dev/null 2>&1 && ret=1
if [ ${ret} -lt 1 ]
  then 
    %usr_sbin_dir/useradd -c "Nginx" -s /bin/false -r -d %nginx_prefix/sbin %name 2>/dev/null
  fi

%make_install

%__install -p -m 0755 -d %buildroot/%nginx_prefix/logs
%__install -p -m 0755 -d %buildroot/%nginx_prefix/ssl
%__install -p -m 0755 -d %buildroot/%nginx_prefix/cache
%__install -p -m 0755 -d %buildroot/%nginx_prefix/sites-available
%__install -p -m 0755 -d %buildroot/%nginx_prefix/sites-enabled

# nabbed and modified from the el7 nginx rpm in the epel repo
# thanks Jamie Nguyen
%__install -p -m 0644 -D %_sourcedir/nginxtras/nginx.logrotate %buildroot/%_sysconfdir/logrotate.d/nginx

# add init.d script
%__install -p -m 0755 -o root -g root -D %_sourcedir/nginxtras/nginx %buildroot/%_sysconfdir/init.d/nginx

# add custom nginx config
%__install -p -m 0644 -o nginx -g nginx -D %_sourcedir/nginxtras/nginx.conf %buildroot/%nginx_prefix/conf/nginx.conf
%__install -p -m 0644 -o nginx -g nginx -D %_sourcedir/nginxtras/vhost.example.conf %buildroot/%nginx_prefix/sites-available/vhost.example.conf
%__ln_s %nginx_prefix/sites-available/vhost.example.conf %buildroot/%nginx_prefix/sites-enabled/vhost.example.conf

# add binary symlink to /usr/local/sbin (a default path)
%__install -p -m 0755 -o root -g root -d %buildroot/%_prefix/local/sbin
%__ln_s %nginx_prefix/sbin/nginx %buildroot/%_prefix/local/sbin/nginx

# add custom html / php files
%__install -p -m 0644 -o nginx -g nginx -D %_sourcedir/nginxtras/index.html %buildroot/%nginx_prefix/html/index.html
%__install -p -m 0644 -o nginx -g nginx -D %_sourcedir/nginxtras/php-test.php %buildroot/%nginx_prefix/html/php-test.php

# adjust permissions
%usr_bin_dir/find %buildroot/%nginx_prefix -type f -exec %__chmod 0644 {} \; -exec %__chown %name:%name {} \;
%usr_bin_dir/find %buildroot/%nginx_prefix -type d -exec %__chmod 0755 {} \; -exec %__chown %name:%name {} \;
%__chmod 0755 %buildroot/%nginx_prefix/sbin/nginx

%files
# disk cache
%dir %nginx_prefix/cache

# conf
%config(noreplace) %nginx_prefix/conf/fastcgi.conf
%config(noreplace) %nginx_prefix/conf/fastcgi.conf.default
%config(noreplace) %nginx_prefix/conf/fastcgi_params
%config(noreplace) %nginx_prefix/conf/fastcgi_params.default
%config(noreplace) %nginx_prefix/conf/koi-utf
%config(noreplace) %nginx_prefix/conf/koi-win
%config(noreplace) %nginx_prefix/conf/mime.types
%config(noreplace) %nginx_prefix/conf/mime.types.default
%config(noreplace) %nginx_prefix/conf/nginx.conf
%config(noreplace) %nginx_prefix/conf/nginx.conf.default
%config(noreplace) %nginx_prefix/conf/scgi_params
%config(noreplace) %nginx_prefix/conf/scgi_params.default
%config(noreplace) %nginx_prefix/conf/uwsgi_params
%config(noreplace) %nginx_prefix/conf/uwsgi_params.default
%config(noreplace) %nginx_prefix/conf/win-utf

# html
%config(noreplace) %nginx_prefix/html/50x.html
%config(noreplace) %nginx_prefix/html/index.html
%config(noreplace) %nginx_prefix/html/php-test.php

# init.d script
%_sysconfdir/init.d/nginx

# logs
%dir %nginx_prefix/logs
%config(noreplace) %_sysconfdir/logrotate.d/nginx

# sbin
%nginx_prefix/sbin/nginx

# ssl (until they call it opentls)
%dir %nginx_prefix/ssl

# sites-(available|enabled) taking a page from Apache
%dir %nginx_prefix/sites-available
%dir %nginx_prefix/sites-enabled
%config(noreplace) %nginx_prefix/sites-available/vhost.example.conf
%config(noreplace) %nginx_prefix/sites-enabled/vhost.example.conf

# symlink
%config(noreplace) %_prefix/local/sbin/nginx

# append --define 'noclean 1' to rpmbuild if desired to keep the buildroot directory
# shamelessly nabbed from
# http://stackoverflow.com/questions/13830262/rpmbuild-clean-phase-without-removing-files
%clean
%if "%noclean" == ""
   rm -rf $RPM_BUILD_ROOT
%endif
