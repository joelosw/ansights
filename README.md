[Description of the Dataset on the Coding daVinci Website](https://codingdavinci.de/daten/deutscher-reichsanzeiger-und-preussischer-staatsanzeiger)

# Visual Anzeights
Welcome to our Coding daVinci repository. Please don't judge us on the current state of the Code.
We  know it is very messy and not well documented, but we are working on that.
This Repository is the Backend of our project, providing a flask application that is called by out [ReactApp](AppVisualAnzeights)

## Setup The Repo
1. Clone this repo
2. 
    ```
    git submodule update --init --recursive
    ```
3. Create a venv/ conda env and enter it
4. 
    ```
    python3 -m pip install -r requirements.txt
    ```
5.
    ```
    python -m spacy download de_core_news_md
    ```
## Runt the flask app
1. 
    ```
    cd src/flask_backend
    ```
2. 
    ```
    python3 -m flask run
    ```

# Deprercatwed Below
## Get the SQL Database:
1. Install MariaDB \[[Windows](https://www.mariadbtutorial.com/getting-started/install-mariadb/) | [Arch](https://wiki.archlinux.org/title/MariaDB)\]

### Using Linux:
``` bash
mariadb-install-db --user=mysql --basedir=/usr --datadir=/var/lib/mysql
sudo systemctl start mariadb.service
sudo mysql -u root -p
```
Using the MariaDB CLI
```
CREATE DATABASE reichsanzeiger;
``` 
Then exit, go back to terminal and import data:
``` bash
sudo mysql -u root -p reichsanzeiger < Reichsanzeiger-Repo/reichsanzeiger.sql
```
2. Setting up a new user with password
``` bash
CREATE USER 'NAME'@'localhost' IDENTIFIED BY 'PASSWORD';
GRANT ALL PRIVILEGES ON reichsanzeiger.* TO 'NAME'@'localhost';
FLUSH PRIVILEGES;
quit;
```
