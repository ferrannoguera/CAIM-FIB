mkdir /tmp/data
mkdir /tmp/logs
cp -r ESconf /tmp/
unzip novels.zip -d /tmp
tar -xzf 20_newsgroups.tar.gz --directory /tmp
/opt/elasticsearch-5.4.1/bin/elasticsearch -Epath.conf=/tmp/ESconf

