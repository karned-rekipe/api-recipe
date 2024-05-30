pipeline {
    agent any
    environment {
        DOCKER_IMAGE = 'api-recipe'
        DOCKER_TAG = 'latest'
    }
    stages {
        stage('Build and Push Image') {
            when {
                expression {
                    return env.CHANGE_ID != null && env.GITHUB_EVENT == 'pull_request' && env.PR_ACTION == 'closed'
                }
            }
            steps {
                script {
                    // Login to Docker Hub (+ tard)
                    //sh "echo '${DOCKER_PASSWORD}' | docker login -u '${DOCKER_USER}' --password-stdin"
                    // Build the Docker image
                    sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                    // Push the image to Docker Hub
                    sh "docker push ${DOCKER_IMAGE}:${DOCKER_TAG}"
                }
            }
        }
    }
}