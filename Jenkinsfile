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
                python3 manage.py collectstatic -y
                '''
            }
        }
    }
}