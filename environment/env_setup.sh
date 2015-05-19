#! /bin/sh
sudo true

sudo iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 8000

echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
echo 'export PYENV_VIRTUALENVWRAPPER_PREFER_PYVENV="true"' >> ~/.bashrc

source ~/.bashrc

sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libxml2-dev libxslt1-dev python-dev


git clone https://github.com/yyuu/pyenv.git ~/.pyenv

pyenv install 2.7.9

pyenv rehash     # do this any time you install a new Python binary

pyenv global 2.7.9

sudo curl https://bootstrap.pypa.io/get-pip.py | python

git clone https://github.com/yyuu/pyenv-virtualenvwrapper.git ~/.pyenv/plugins/pyenv-virtualenvwrapper

pyenv virtualenvwrapper_lazy



source ~/.bashrc
