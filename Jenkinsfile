pipeline {
    agent {
        docker { image 'node:20.11.1-alpine3.19' } // on y croit !
    }
    stages {
        stage('Test') {
            steps {
                sh 'node --version'
            }
        }
    }
}