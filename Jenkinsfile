pipeline {
    agent any

    stages {
        stage('Checkout SCM') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Rocinate-droid/Furniture_Website.git'
            }
        }
        stage('Copy Files') {
            steps {
            sh '''
               rsync -av --delete \
               --exclude='myenv' \
               --exclude='.env' \
               "$WORKSPACE/furniture/" \
               /opt/Module
               '''
            }
        }
        stage('Install requirements') {
            steps {
                sh '''
                   /opt/Module/myenv/bin/pip install -r /opt/Module/requirements.txt
                   '''
            }
        }
        stage('Migrations and Static Collection') {
            steps {
                sh '''
                   /opt/Module/myenv/bin/python3 /opt/Module/manage.py migrate --noinput
                   /opt/Module/myenv/bin/python3 /opt/Module/manage.py collectstatic --noinput
                   '''
            }
        }
        stage('Restart Furniture Service') {
            steps {
                sh 'sudo /bin/systemctl restart furniture.service'
            }
        }
    
    }
}

