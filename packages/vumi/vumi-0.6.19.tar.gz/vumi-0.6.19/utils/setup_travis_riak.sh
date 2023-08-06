#!/bin/bash -e

# We use Riak tarballs built by https://github.com/praekelt/riak-for-travis

RIAK_VERSION="${1?Please provide Riak version.}"
RIAK_FILENAME=riak-${RIAK_VERSION}.tar.bz2
RIAK_DOWNLOAD=$HOME/download/$RIAK_FILENAME
BASE_URL="https://github.com/praekelt/riak-for-travis/releases/download/riak-for-travis-0.1.0/"

echo "Setting up Riak with RIAK_VERSION='${RIAK_VERSION}'"

if [ ! -f $RIAK_DOWNLOAD ]; then
    mkdir -p $HOME/download
    wget -O $RIAK_DOWNLOAD $BASE_URL/$RIAK_FILENAME
fi

tar xjf $RIAK_DOWNLOAD -C $HOME/

# Fix jvm opts if necessary.
if [ -f $HOME/riak/etc/riak.conf ]; then
    sed -i'.bak' 's/^search.solr.jvm_options = .*$/search.solr.jvm_options = -Xms1g -Xmx1g -XX:+UseCompressedOops/' $HOME/riak/etc/riak.conf
    rm $HOME/riak/etc/riak.conf.bak
fi

$HOME/riak/bin/riak start
