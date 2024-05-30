pipeline {
    agent any
    environment {
        DOCKER_IMAGE = 'api-recipe'
    }
    stages {
        stage('Build') {
            when {
                expression {
                    return env.GIT_BRANCH == 'main'
                }
            }
            steps {
                script {
                    checkout scm
                    sh 'docker build -t $DOCKER_IMAGE .'
                    sh 'docker push $DOCKER_IMAGE'
                }
            }
        }
    }
}