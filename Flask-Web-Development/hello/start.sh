#!/bin/bash

#先执行`chmod u+x ./start.sh`使脚本有执行权限
#然后`./start.sh`即可执行脚本
echo "Start Run Server Flask"
./manage.py runserver --host 0.0.0.0
