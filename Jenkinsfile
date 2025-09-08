pipeline{
    agent any
    stages {
        stage ('Configure Nginx'){
            steps {
                sh 'echo "Step 1"'
                git branch: 'prod-django', url: 'https://github.com/Rocinate-droid/Furniture_Website.git'
            }
        }
    }
}