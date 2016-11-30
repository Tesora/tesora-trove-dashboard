#!/bin/sh

# This script is borrowed from Sahara who borrowed from neutron-* repos.

# Many of horizon's repos suffer from the problem of depending on horizon,
# but it not existing on pypi.

# This wrapper for tox's package installer will use the existing package
# if it exists, else use zuul-cloner if that program exists, else grab it
# from horizon master via a hard-coded URL. That last case should only
# happen with devs running unit tests locally.

# From the tox.ini config page:
# install_command=ARGV
# default:
# pip install {opts} {packages}

ZUUL_CLONER=/usr/zuul-env/bin/zuul-cloner
BRANCH_NAME=${BRANCH_NAME:-master}
BRANCH_NAME=${ZUUL_BRANCH:-$BRANCH_NAME}
horizon_installed=$(echo "import horizon" | python 2>/dev/null ; echo $?)

set -e

install_cmd="pip install $1"
shift

if [ $horizon_installed -eq 0 ]; then
    echo "ALREADY INSTALLED" > /tmp/tox_install.txt
    echo "Horizon already installed; using existing package"
elif [ -x "$ZUUL_CLONER" ]; then
    export ZUUL_BRANCH=${ZUUL_BRANCH-$BRANCH}
    echo "ZUUL CLONER" > /tmp/tox_install.txt
    cwd=$(/bin/pwd)
    cd /tmp
    $ZUUL_CLONER --cache-dir \
        /opt/git \
        --branch $BRANCH_NAME \
        git://git.openstack.org \
        openstack/horizon
    cd openstack/horizon
    $install_cmd -e .
    cd "$cwd"
else
    echo "PIP HARDCODE" > /tmp/tox_install.txt
    if [ -z "$HORIZON_PIP_LOCATION" ]; then
        HORIZON_PIP_LOCATION="git+https://git.openstack.org/openstack/horizon@$BRANCH_NAME#egg=horizon"
    fi
    $install_cmd -U -e ${HORIZON_PIP_LOCATION}
fi

$install_cmd -U $*

install_cmd="pip install"
uninstall_cmd="pip uninstall -y"

# remove the horizon installed from source (can't get rid of it in test-requirements.txt due to global requirements conflict
$uninstall_cmd horizon

# TODO: replace the hardcoded branch with env variable
HORIZON_PIP_LOCATION="git+https://git.openstack.org/openstack/horizon@master#egg=horizon"
$install_cmd -U -e ${HORIZON_PIP_LOCATION}

# install python-troveclient from source
PYTHON_TROVECLIENT_PIP_LOCATION="git://github.com/Tesora/tesora-python-troveclient.git@$BRANCH_NAME#egg=python-troveclient"
$install_cmd -U -e ${PYTHON_TROVECLIENT_PIP_LOCATION}

PYTHON_MISTRALCLIENT_PIP_LOCATION="git://github.com/Tesora/tesora-python-mistralclient.git@$BRANCH_NAME#egg=python-mistralclient"
$install_cmd -U -e ${PYTHON_MISTRALCLIENT_PIP_LOCATION}

exit $?
