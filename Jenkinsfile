pipeline {
    agent any

    stages {
        stage('Checkout SCM') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Rocinate-droid/Furniture_Website.git'
            }
        }

        stage('Deploy and Start Django') {
            steps {
                withCredentials([
                    string(credentialsId: 'SECRET_KEY', variable: 'SECRET_KEY'),
                    string(credentialsId: 'RAZOR_KEY_ID', variable: 'RAZOR_KEY_ID'),
                    string(credentialsId: 'RAZOR_KEY_SECRET', variable: 'RAZOR_KEY_SECRET'),
                    string(credentialsId: 'DEBUG', variable: 'DEBUG'),
                    string(credentialsId: 'MAINTENANCE_MODE', variable: 'MAINTENANCE_MODE')
                ]) {
                    sh '''
                    sudo rsync -av --delete \
                      --exclude='.git' \
                      --exclude='__pycache__' \
                      --exclude='myenv/' \
                      --exclude='.env' \
                      "$WORKSPACE/furniture/" \
                      /opt/myproject/

                    sudo -u www-data /opt/myproject/myenv/bin/pip install -r /opt/myproject/requirements.txt
                    sudo chown www-data:www-data /opt/myproject/db.sqlite3
                    sudo chmod 664 /opt/myproject/db.sqlite3
                    sudo -u www-data /opt/myproject/myenv/bin/python3 /opt/myproject/manage.py migrate --noinput
                    sudo -u www-data /opt/myproject/myenv/bin/python3 /opt/myproject/manage.py collectstatic --noinput

                    sudo systemctl restart furniture
                    '''
                }
            }
        }
    }
}

