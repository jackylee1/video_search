#!/usr/bin/sh

sudo yum install centos-release-scl
sudo rpm --import http://li.nux.ro/download/nux/RPM-GPG-KEY-nux.ro
sudo rpm -Uvh http://li.nux.ro/download/nux/dextop/el7/x86_64/nux-dextop-release-0-1.el7.nux.noarch.rpm
sudo yum install -y rh-python36 gcc cmake make hdf5 ffmpeg ffmpeg-devel
sudo yum group install -y "Development Tools"
scl enable rh-python36 bash
python3 -m venv py36-venv
. py36-env/bin/activate
python3 -m pip install -e .
python -m spacy download en
python -m nltk.downloader punkt averaged_perceptron_tagger wordnet
sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 5000
