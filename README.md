# Fairy Bang

## Installation
```bash
sudo apt update

# --- Build Dependencies ---
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev \
libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl \
git postgresql postgresql-client psycopg2 libpq-dev tor

sudo systemctl enable tor

# --- Installing Python --- 

# Installing pyenv
curl https://pyenv.run | bash

# Load pyenv automatically by adding
# the following to ~/.bashrc:
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

. ~/.bashrc

# Installing python specific version
pyenv install --list | grep " 3\.[678]"
pyenv install -v 3.7.7
pyenv versions
pyenv global 3.7.7

# Check current python version
pyenv versions


# --- Configuring PostrgreSQL ---
systemctl enable postgresql
passwd postgres
su - postgres
psql -c "ALTER USER postgres WITH PASSWORD 'cyberpunk';"

# Settings auth by md5 password
vim /etc/postgresql/11/main/pg_hba.conf

# Change peer to md5 in the following string
# "local" is for Unix domain socket connections only
local   all all md5

systemctl restart postgresql

# Creating new DB and ROLE for it
psql
CREATE DATABASE fairybang;
CREATE DATABASE girls;
CREATE USER cyberpunk PASSWORD 'cyberpunk';
ctrl+d

# Testing connection to DB
psql -d fairybang -U cyberpunk
psql -d girls -U cyberpunk

# --- Transfer Database ---
# Here will be transfering girls db 
from localhost to remote server.
pg_dump -h 127.0.0.1 -U cyberpunk -F c -f girls.tar.gz girls
scp girls.tar.gz root@<remote_host>:~
pg_restore -h 127.0.0.1 -U cyberpunk -F c -d girls girls.tar.gz

# --- Configuring supervisor ---
sudo apt install supervisor
sudo vi /etc/supervisor/conf.d/fairybang.conf

# Example config file.
command=/bin/bash -c "/root/.local/bin/fairybang /root/FairyBang/src/config.yaml"
autostart=true
autorestart=true
stopsignal=KILL
numprocs=1

# Save, reread and start app
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start fairybang

# --- Installing app ---

# Previously copy app dir on your server
# then follow next steps
cd FairyBang
python setup.py install --user
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
. ~/.bashrc

# Then modify your config.yaml file
# with DEBUG=True for testing
# and exec following step
fairybang <path_to_your_config.yaml>

# Quick'n'dirty SSL certificate generation
cd ~
mkdir certs

openssl genrsa -out webhook_pkey.pem 2048
openssl req -new -x509 -days 3650 -key webhook_pkey.pem -out webhook_cert.pem

# When asked for "Common Name (e.g. server FQDN or YOUR name)" you should reply
# with the same value in you put in WEBHOOK_HOST

# Fill in webhook fields in config.yaml
# set DEBUG=False and run bot again


```
