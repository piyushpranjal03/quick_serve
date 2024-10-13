pipeline {
    agent any

    triggers {
        githubPush()
    }


    environment {
        DOCKER_IMAGE = 'quick_serve'
        GAMMA_PORT = '8081'
        PROD_PORT = '8082'
        GAMMA_CONTAINER_NAME = 'quick_serve-gamma'
        PROD_CONTAINER_NAME = 'quick_serve-prod'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                script {
                    sh "docker-compose build"
                }
            }
        }

        stage('Gamma') {
            steps {
                script {
                    sh "docker-compose -f docker-compose.yaml -f docker-compose.gamma.yaml up -d --build --force-recreate --name ${GAMMA_CONTAINER_NAME}"
                    sh "sleep 10"
                    def response = sh(script: "curl -s -o /dev/null -w '%{http_code}' http://localhost:${GAMMA_PORT}/health", returnStdout: true).trim()
                    if (response != "200") {
                        error "Gamma health check failed with status ${response}"
                    }
                }
            }
        }

        stage('Prod') {
            steps {
                input "Deploy to Production?"
                script {
                    sh "docker-compose -f docker-compose.yaml -f docker-compose.prod.yaml down"
                    sh "docker-compose -f docker-compose.yaml -f docker-compose.prod.yaml up -d --build --force-recreate --name ${PROD_CONTAINER_NAME}"
                    sh "sleep 10"
                    def response = sh(script: "curl -s -o /dev/null -w '%{http_code}' http://localhost:${PROD_PORT}/health", returnStdout: true).trim()
                    if (response != "200") {
                        error "Production health check failed with status ${response}"
                    }
                }
            }
        }
        stage('Cleanup') {
            steps {
                script {
                    sh "docker-compose down --remove-orphans"
                }
            }
        }
    }

    post {
        failure {
            echo 'The Pipeline failed :('
        }
    }
}
