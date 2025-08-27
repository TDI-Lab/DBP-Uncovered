# DBP Uncovered Tool

Welcome to the **DBP Uncovered Tool**.  
Please follow the instructions below to set up the platform on Ubuntu. A similar setup works on Mac adn Windows.

---

## Prerequisites
- Python 3.10 (or newer, Python 3.x compatible)
- MySQL installed locally or accessible remotely (Instructions are given for mysql installtion)

---

## 1. Install MySQL
MySQL is required to store user responses in the database.

```bash
# Install MySQL server
sudo apt install mysql-server

# Install MySQL client libraries
sudo apt install libmysqlclient-dev

# Install build tools and Python headers
sudo apt install -y build-essential pkg-config python3-dev default-libmysqlclient-dev
```
## 2. Install Python venv
```bash
# Install venv if not already installed
sudo apt install python3-venv

# Create a virtual environment
python3 -m venv <your-env-name>

# Activate the environment
source <your-env-name>/bin/activate

# Install project dependencies
pip install -r requirements.txt
```

## 3. Create mysql database and tables

### Enter MySQL shell using sudo mysql or any other user as per your preference

```bash
# Inside MySQL shell, run:
CREATE DATABASE <db_name>;
CREATE USER '<username>'@'localhost' IDENTIFIED BY '<password>';
GRANT ALL PRIVILEGES ON <db_name>.* TO '<username>'@'localhost';
FLUSH PRIVILEGES;
```

### Exit the MySQL shell
### Create the tables in the database

```bash
# From the project root, run:
mysql -u <username> -p <db_name> < create_db.sql
```

## 4. Create a .env file for storing variables

```bash
nano .env
```

### Past the following content in the .env file.
### Remember to replace the values with your credentials

```bash
DB_HOST=localhost
DB_PORT=3306
DB_USER=<username>
DB_PASSWORD=<password>
DB_NAME=<db_name>
SECRET_KEY="<your-secure-secret-key>"
```
## 5. Run the application

```bash
#From project root, run the following.
python3 app.py
```

