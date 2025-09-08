pipeline{
    agent any
    stages {
        stage ('Configure Nginx'){
            steps {
                sh 'echo "Step 1"'
                git branch: 'prod-django', url: 'https://github.com/Rocinate-droid/Furniture_Website.git'
            }
        }
        stage ('Run Django') {
            steps {
                sh'''
                cd furniture
                python3 -m venv myenv
                pwd
                source myenv/bin/activate
                python3 -m manage.py runserver
                '''
            }
        }
    }
}