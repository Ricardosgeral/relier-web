#!/usr/bin/env bash

#
echo '------------------------------'
echo ' => Get repository from Gibhub'
echo ' -----------------------------'
#
if [ -d "/home/pi/relier-web" ]; then
    sudo rm -R /home/pi/relier-web
fi
git clone https://github.com/Ricardosgeral/relier-web.git /home/pi/relier-web

#
sudo apt-get install -y curl software-properties-common
curl -sL https://deb.nodesource.com/setup_10.x | sudo bash -
sudo apt-get install -y nodejs
sudo apt-get install -y postgresql
#sudo npm install -g heroku
curl https://cli-assets.heroku.com/install.sh | sh

sudo pip3 install virtualenv
#sudo pip install libpq-dev==9.4.3

sudo virtual env -p /usr/bin/python3 relier-dash-env
sudo source relier-dash-env/bin/activate
sudo pip install -r requirements.txt # dependencies that heroku will install in is server



cd relier-web
sudo git init
sudo virtualenv venv
source venv/bin/activate

sudo heroku create relier-web
#heroku logs --tail
#heroku ps  #check how many dynos are running

heroku ps:scale web=0 #disconnects
heroku ps:scale web=1 #connects

# asks for email and password from heroku account
sudo git add .
sudo git config --global user.email ricardos.geral@gmail.com

sudo git commit -m 'Initial relier-web commit'
sudo git push heroku master
sudo heroku ps:scale web=1
#
#sudo pip install numpy
#sudo pip install pandas
#sudo pip install configparser
#
#sudo apt-get install postgresql
