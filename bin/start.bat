@echo off
set "basedir=%~dp0"
set "PATH=%PATH%;%basedir%/../ext/phantomjs-2.1.1-windows/bin"

python ../main/tmall.py