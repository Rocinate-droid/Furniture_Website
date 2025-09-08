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
                cd Furniture_Website
                python3 -m venv myenv
                source myvenv/bin/activate
                python3 -m manage.py runserver
            }
        }
    }
}