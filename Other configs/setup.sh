#!/usr/bin/env bash
# 1) Declaring needed env variables
STORAGE_NAME="mydiplomastorage"
SAS="***********************************************************************************"

# 2) Updating Ubuntu OS
sudo apt-get update
sudo apt-get -y upgrade

# 3) Installing all needed packages to deploy site
sudo apt-get -y install apache2 python3-tk python3-pip python3-venv libapache2-mod-wsgi-py3

# 4) Removing old OpenSSL library and downloading the latest ver.
sudo rm -rf /usr/lib/python3/dist-packages/OpenSSL
sudo pip3 install pyopenssl
sudo pip3 install pyopenssl --upgrade

# 5) Downloading source code
cd /var/www
git clone -b azure/master --single-branch https://github.com/KinKinoV/Django_event_application.git

# 6) Creating virtual environment, then installing all needed python packages
# and then moving venv to site folder
sudo su azureuser
cd /home/azureuser/
python3 -m venv /home/azureuser/django-venv
sudo /home/azureuser/django-venv/bin/pip install -r /var/www/Django_event_application/requirments.txt
sudo mv django-venv/ /var/www/Django_event_application/django-venv

# 7) Downloading all needed files
sudo wget -O /etc/config.json "https://${STORAGE_NAME}.blob.core.windows.net/configs/config.json?${SAS}"
sudo wget -O /etc/apache2/sites-available/event-site.conf "https://${STORAGE_NAME}.blob.core.windows.net/configs/site.conf?${SAS}"
sudo wget -O /etc/apache2/sites-available/event-site-le-ssl.conf "https://${STORAGE_NAME}.blob.core.windows.net/configs/site-ssl.conf?${SAS}"
sudo wget -O /etc/ssl/options-ssl-apache.conf "https://${STORAGE_NAME}.blob.core.windows.net/configs/options-ssl-apache.conf?${SAS}"

# 8) Mounting Azure File Share for logging
sudo mkdir /mnt/logging
if [ ! -d "/etc/smbcredentials" ]; then
sudo mkdir /etc/smbcredentials
fi
if [ ! -f "/etc/smbcredentials/mydiplomastorage.cred" ]; then
    sudo bash -c 'echo "username=mydiplomastorage" >> /etc/smbcredentials/mydiplomastorage.cred'
    sudo bash -c 'echo "password=***************************************************************" >> /etc/smbcredentials/mydiplomastorage.cred'
fi
sudo chmod 600 /etc/smbcredentials/mydiplomastorage.cred
sudo bash -c 'echo "//mydiplomastorage.file.core.windows.net/logging /mnt/logging cifs nofail,credentials=/etc/smbcredentials/mydiplomastorage.cred,dir_mode=0777,file_mode=0777,serverino,nosharesock,actimeo=30" >> /etc/fstab'
sudo mount -t cifs //mydiplomastorage.file.core.windows.net/logging /mnt/logging -o credentials=/etc/smbcredentials/mydiplomastorage.cred,dir_mode=0777,file_mode=0777,serverino,nosharesock,actimeo=30

# 9) Copying SSL certificates
sudo mkdir /etc/ssl/diplomasite.northeurope.cloudapp.azure.com/
sudo cp -r /mnt/logging/secretdata /etc/ssl/diplomasite.northeurope.cloudapp.azure.com/

# 10) Enabling sites, needed modules and restarting service
sudo a2ensite event-site.conf
sudo a2ensite event-site-le-ssl.conf
sudo a2dissite 000-default.conf
sudo a2enmod ssl
sudo a2enmod rewrite
sudo service apache2 restart
