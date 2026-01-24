pipeline {
    agent any

    stages {
        stage('Copy Files') {
            steps {
            sh '''
               rsync -av --delete \
               --exclude='myenv' \
               --exclude='.env' \
               --exclude='media/' \
               --exclude='.git/' \
               --exclude='.gitignore' \
               --exclude='node_modules' \
               --exclude='__pycache__' \
               --exclude='db.sqlite3' \
               --exclude='.vscode/' \
               "$WORKSPACE/furniture/" \
               /opt/Module
               rsync -av \
               "$WORKSPACE/furniture/media/" \
               /opt/Module/media/
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
        stage('Build Frontend Assets') {
            steps {
                sh '''
                   cd /opt/Module
                   npm install
                   npx tailwindcss -i ./static/src/input.css -o ./static/css/main.css --minify
                   '''
            }
        }
        stage('Migrations and Static Collection') {
            steps {
                sh '''
                   /opt/Module/myenv/bin/python3 /opt/Module/manage.py migrate --noinput
                   /opt/Module/myenv/bin/python3 /opt/Module/manage.py collectstatic --noinput
                   /opt/Module/myenv/bin/python3 /opt/Module/manage.py loaddata /opt/Module/products.json
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

