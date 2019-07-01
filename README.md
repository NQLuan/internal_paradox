# company-api

### Requirements
Mysql 3.5

Python 3.6 or 2.7

### Installation

1. Create virtualenv
    ```
        virtualenv --python=/usr/bin/python3 env
        source /home/ubuntu/env/bin/activate
        deactivate
    ```

2. Install all dependencies:
    ```
        cd ../src
        pip3 install -r requirements.txt
    ```

3. Init config & database
    ```
        mkdir /etc/core
        cp ../src/core/sample.config.env /etc/core/config.env
        cd ../src
        python3 manage.py migrate
    ```

4. Start API Server
    ```
        cd ../src
        python3 manage.py runserver 127.0.0.1:8001
        http://127.0.0.1:8001/
    ```
