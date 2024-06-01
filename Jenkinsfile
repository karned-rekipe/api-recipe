pipeline {
    agent {
        docker {
            image 'ubuntu:22.04'
            args '-u root:root' // Run as root to install any necessary dependencies
        }
    }
    
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials-id') // Replace with your Jenkins credentials ID
        DOCKERHUB_REPO = 'your-dockerhub-repo/your-image-name'
    }

    stages {
        stage('Install Dependencies') {
            steps {
                script {
                    sh '''
                        apt-get update
                        apt-get install -y docker.io
                    '''
                }
            }
        }

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                script {
                    sh 'docker build -t ${DOCKERHUB_REPO}:${env.BUILD_ID} .'
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    // Add your test commands here
                    sh 'echo "Running tests..."'
                }
            }
        }

        stage('Push to DockerHub') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', DOCKERHUB_CREDENTIALS) {
                        sh 'docker push ${DOCKERHUB_REPO}:${env.BUILD_ID}'
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'Build and push succeeded!'
        }
        failure {
            echo 'Build failed.'
        }
    }
}