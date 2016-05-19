<h2>nginx rpm spec file & some nginxtras</h2>

<h3>nginx custom rpm build for CentOS 6</h3>
<p>Pretty straight forward. Installs all nginx items in /etc/nginx<br>
<p>Uses latest pcre, zlib, and openssl<br>
<p>Should work seamlessly on RHEL, Scientific Linux, Oracle, and Amazon 6.<br>
<p>Big thanks to some old posts at stackoverflow and the EPEL nginx package maintainer Jamie Nguyen.</p>

<h3>about</h3>
<p>This install puts all things nginx in the /etc/nginx directory.  Including logs, confs, the binary, all of it.</p>
<p>This comes from an old habit.  I know this should rightfully be in /usr, but . . . old habits.</p>

<p>Quick RPM Build Cheat</p>
```
rpmbuild -ba nginx.spec
```

<h3>Licensing</h3>
<p>The MIT License.  See LICENSE.txt for details</p>

