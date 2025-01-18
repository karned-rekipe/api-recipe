pipeline {
    agent {
        kubernetes {
            yaml """
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: docker
    image: docker:24.0.2
    command:
    - cat
    tty: true
    volumeMounts:
    - mountPath: /var/run/docker.sock
      name: docker-sock
  - name: python
    image: python:3.11-slim
    command:
    - cat
    tty: true
  volumes:
  - name: docker-sock
    hostPath:
      path: /var/run/docker.sock
"""
        }
    }

    environment {
        DOCKER_IMAGE = 'killiankopp/api-recipe'
        DOCKER_TAG = '1.0.0'
    }

    stages {
        stage('Clone Repository') {
            steps {
                script {
                    def branchName = env.BRANCH_NAME ?: 'main'
                    echo "Cloning branch: ${branchName}"

                    git branch: branchName, url: 'https://github.com/karned-rekipe/api-recipe.git'
                }
            }
        }

        stage('Detect Branch') {
            steps {
                script {
                    def scmBranch = sh(
                        script: "git rev-parse --abbrev-ref HEAD",
                        returnStdout: true
                    ).trim()

                    env.BRANCH_NAME = scmBranch
                    echo "Branch detected: ${env.BRANCH_NAME}"
                }
            }
        }

        stage('Checkout') {
            steps {
                script {
                    echo "Cloning and checking out branch: ${env.BRANCH_NAME}"

                    sh """
                        git fetch origin ${env.BRANCH_NAME}
                        git checkout ${env.BRANCH_NAME}
                    """
                }
            }
        }

        stage('Run Tests') {
            steps {
                container('python') {
                    catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                    sh '''
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
pytest --junitxml=report.xml
                    '''
                    }
                }
            }
        }

        stage('Parse Test Results') {
            steps {
                container('python') {
                    sh '''
. venv/bin/activate
python -c "
import xml.etree.ElementTree as ET

tree = ET.parse('report.xml')
root = tree.getroot()

testsuite = root.find('./testsuite')
total = int(testsuite.attrib['tests'])
failures = int(testsuite.attrib['failures'])
errors = int(testsuite.attrib['errors'])

print(f'Total tests: {total}, Failures: {failures}, Errors: {errors}')

with open('test_results.txt', 'w') as f:
    f.write(f'{total}:{failures}:{errors}')
"
                    '''
                }
            }
        }

        stage('Send Slack Message') {
            steps {
                container('python') {
                    withCredentials([string(credentialsId: 'SLACK_WEBHOOK_URL', variable: 'SLACK_WEBHOOK_URL')]) {
                        script {
                            // Lire les résultats des tests
                            def testResults = readFile('test_results.txt').trim()
                            def (total, failures, errors) = testResults.tokenize(':')

                            // Définir les variables d'environnement
                            env.TOTAL_TESTS = total
                            env.FAILURES = failures
                            env.ERRORS = errors

                            // Exécuter la commande pour envoyer un message Slack
                            sh '''
                                apt-get update && apt-get install -y curl
                                curl -X POST -H 'Content-type: application/json' --data '{
                                    "text": "API Recipe -  Tests: ''' + env.TOTAL_TESTS + ''' Failures: ''' + env.FAILURES + ''' Errors: ''' + env.ERRORS + '''",
                                    "username": "Jenkins Bot",
                                    "icon_emoji": ":rocket:"
                                }' ${SLACK_WEBHOOK_URL}
                            '''
                        }
                    }
                }
            }
        }
    }
}
