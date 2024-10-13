pipeline {
    agent any

    triggers {
        githubPush()
    }


    environment {
        DOCKER_IMAGE = 'quick_serve'
        GAMMA_PORT = '8081'
        PROD_PORT = '8082'
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
                    sh "docker-compose build --no-cache"
                }
            }
        }

        stage('Gamma') {
            steps {
                script {
                    sh "docker-compose -f docker-compose.yaml -f docker-compose.gamma.yaml up -d"
                    sh "sleep 10" // Wait for the application to start
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
                    sh "docker-compose -f docker-compose.yaml -f docker-compose.prod.yaml up -d"
                    sh "sleep 10" // Wait for the application to start
                    def response = sh(script: "curl -s -o /dev/null -w '%{http_code}' http://localhost:${PROD_PORT}/health", returnStdout: true).trim()
                    if (response != "200") {
                        error "Production health check failed with status ${response}"
                    }
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