pipeline{
    agent any
    stages {
        stage ('Configure Nginx'){
            steps {
                sh 'echo "Step 11"'
                git branch: 'prod-django', url: 'https://github.com/Rocinate-droid/Furniture_Website.git'
                sh '''
                cd /var/lib/jenkins/workspace/Django-Job/furniture
                . myenv/bin/activate
                python manage.py makemigrations --merge
                python3 manage.py makemigrations --noinput
                python3 manage.py migrate --noinput
                python3 manage.py collectstatic --noinput
                sudo systemctl restart myproject
                '''
            }
        }
    }
}