pipeline{
    agent any
    stages {
        stage ('Configure Nginx'){
            steps {
                sh 'echo "Step 1"'
                git branch: 'prod-django', url: 'https://github.com/Rocinate-droid/Furniture_Website.git'
                sh '''
                cd /var/lib/jenkins/workspace/Django-Job/furniture
                . myenv/bin/activate
                python manage.py collectstatic
                '''
            }
        }
    }
}