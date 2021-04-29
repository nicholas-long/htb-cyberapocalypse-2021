#!/bin/bash
hash=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1 | md5sum | cut -d ' ' -f 1)
sed -i "s/hash/$hash/g" /tomcat/webapps/ROOT/WEB-INF/web.xml
./catalina.sh run
