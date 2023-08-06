 sudo apt-get install python-pip python-dev build-essential python3-dev
sudo pip install --upgrade pip
sudo pip install --upgrade virtualenv

cd $PROJECT_DIRECTORY

virtualenv --system-site-packages -p /usr/bin/python2.7 env

source env/bin/actuvate

pip install -r requirements.txt
pip install -e ../arquants-base (el path puede cambiar aro)
para guardar una nueva dep: pip freez > requetiments.txt


hola

