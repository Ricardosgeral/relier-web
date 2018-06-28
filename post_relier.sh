#!/usr/bin/env bash

#
echo '------------------------------'
echo ' => Get repository from Gibhub'
echo ' -----------------------------'
#
if [ -d "/home/pi/relier-dash" ]; then
    sudo rm -R /home/pi/relier-dash
fi
git clone https://github.com/Ricardosgeral/relier-dash.git /home/pi/relier-dash

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
sudo pip install -r requirements.txt # install all programs neeeded




cd relier-dash
sudo git init
sudo virtualenv venv
source venv/bin/activate

sudo heroku create relier-dash
#heroku logs --tail
#heroku ps  #check how many dynos are running

heroku ps:scale web=0 #disconnects
heroku ps:scale web=1 #connects

# asks for email and password from heroku account
sudo git add .
sudo git config --global user.email ricardos.geral@gmail.com

sudo git commit -m 'Initial relier-dash commit'
sudo git push heroku master
sudo heroku ps:scale web=1
#
#sudo pip install numpy
#sudo pip install pandas
#sudo pip install configparser
#
#sudo apt-get install postgresql
#
#
#
#echo  '--------------------------------'
#echo  '=> Install python3.6  (for Dash)'
#echo  '--------------------------------'
#
##If one of the packages cannot be found, try a newer version number (e.g. libdb5.4-dev instead of libdb5.3-dev).
#sudo apt-get -y install build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev
#wget https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tar.xz
#tar xf Python-3.6.5.tar.xz
#./Python-3.6.5/configure
#make
#sudo make altinstall
#sudo rm -r Python-3.6.5
#sudo rm Python-3.6.5.tar.xz
#sudo pip3.6 install --upgrade pip
#sudo pip3.6 install numpy
#sudo pip3.6 install pandas
#sudo pip3.6 install configparser
#sudo pip3.6 install dash==0.21.1  # The core dash backend
#sudo pip3.6 install dash-renderer==0.13.0  # The dash front-end
#sudo pip3.6 install dash-html-components==0.11.0  # HTML components
#sudo pip3.6 install dash-core-components==0.23.0  # Supercharged components
#sudo pip3.6 install plotly --upgrade  # Plotly graphing library used in examples
