## Nginx rpm spec for CentOS 6
Installs all nginx items in the default nginx location /usr/local/nginx.  
Customizations are under SOURCES/nginxtras (e.g. nginx.conf, etc).  
Should work seamlessly on RHEL, Scientific Linux, Oracle Linux, Amazon Linux, and any Linux evolved from RHEL 6.  
Big thanks to some old posts at stackoverflow and the EPEL nginx package maintainer Jamie Nguyen.  

This revision incorporates the following

software | version
-------- | -------
nginx | 1.12.1
pcre | 8.41
zlib | 1.2.11
openssl | 1.0.2l

## Build Guide
Since some files require root ownership, it is best to build as root
1. Assumes start from fresh server install, so some packages are needed
   ```bash
   # yum install -y gcc gcc-c++ make rpm-build wget
   ```
2. Run rpmbuild one time to get the initial file structure setup (yes, it will fail)
   ```bash
   # cd rpmbuild -ba nginx.spec
   ```
3. Clone repo, files should populate in the correct directories
   ```bash
   # git clone https://github.com/twopoint71/centos6-rpm-nginx ./rpmbuild
   ```
4. Retrieve sources
   ```bash
   # cd rpmbuild/SOURCES
   # wget http://nginx.org/download/nginx-1.12.1.tar.gz
   # wget ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-8.41.tar.gz
   # wget http://zlib.net/zlib-1.2.11.tar.gz
   # wget https://www.openssl.org/source/openssl-1.0.2l.tar.gz
   ```
5. Build the rpm
   ```bash
   # cd ../SPECS
   #rpmbuild -ba nginx.spec
   ```
   
## Licensing
The MIT License. See LICENSE.txt for details.
