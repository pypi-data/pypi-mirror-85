#!/bin/sh
# Install tools and programs to run the CSR in the cloud
#

# Set up a directory tree for HA
if [ ! -d $HOME/cloud ]; then
    sudo mkdir $HOME/cloud
    sudo chown guestshell $HOME/cloud
fi

if [ ! -d $HOME/cloud/authMgr ]; then
    sudo mkdir $HOME/cloud/authMgr
    sudo chown guestshell $HOME/cloud/authMgr
fi

auth_dir="$HOME/cloud/authMgr/"

install_log="$auth_dir/install.log"

if [[ "$(python3 -V)" == *"Python 3"* ]]; then
    export PYTHON=$(which python3)
    export SITE=$($PYTHON -m site --user-site)
    if [[ ! -d "$SITE" ]]; then
        export PYTHON=$(which python)
        export SITE=$($PYTHON -m site --user-site)
    fi
else
    export PYTHON=$(which python)
    export SITE=$($PYTHON -m site --user-site)
fi

echo "Installing the Azure utilities package" >> $install_log

# Set up the path to python scripts
#echo 'export PYTHONPATH='$SITE'/csr_cloud:$PYTHONPATH' >> $HOME/.bashrc
echo 'export PATH='$HOME'/.local/bin:'$SITE'/csr_cloud:$PATH' >> $HOME/.bashrc
source $HOME/.bashrc

echo "Show the current PATH" >> $install_log
echo $PATH >> $install_log
#echo "Show the current PYTHONPATH" >> $install_log
#echo $PYTHONPATH >> $install_log
