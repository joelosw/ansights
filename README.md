[Description of the Dataset on the Coding daVinci Website](https://codingdavinci.de/daten/deutscher-reichsanzeiger-und-preussischer-staatsanzeiger)

# Setup The Repo
1. Clone this repo
2. 
    ```
    git submodule update --init --recursive
    ```
3. 
    Change your Name/Passwd in [config/sql_credentials.txt](config/sql_credentials.txt) and execute
    ``` bash
    git update-index --assume-unchanged config/sql_credentials.txt
    ```
    so that they are not tracked and uploaded to GitHub 


4. Create a venv/ conda env and enter it
5. 
    ```
    python3 -m pip install -r requirements.txt
    ```

## Using NER with Spacy:
```
python -m spacy download de_core_news_md
```

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
