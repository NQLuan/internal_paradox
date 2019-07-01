# company-api

### Requirements
Mysql 3.5

Python 3.6 or 2.7

### Installation

1. Install packages

    ```
        sudo apt-get -y install python-virtualenv mysql-server mysql-client python3 python3-dev python3-pip python-mysqldb libmysqlclient-dev
    ```

2. Create virtualenv
    ```
        virtualenv --python=/usr/bin/python3 env
        source /home/ubuntu/env/bin/activate
        deactivate
    ```

2. Install all dependencies:
    ```
        cd src
        pip3 install -r requirements.txt
    ```

3. Init config & database
    ```
        cp src/core/sample.config.env config.env
        cd src
        python3 manage.py migrate
    ```

4. Start API Server
    ```
        cd src
        python3 manage.py runserver 127.0.0.1:8001
        http://127.0.0.1:8001/
    ```
