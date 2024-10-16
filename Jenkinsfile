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
                    sh "docker build -t ${DOCKER_IMAGE} ."
                }
            }
        }

        stage('Gamma') {
            steps {
                script {
                    sh "docker-compose -f docker-compose.gamma.yaml up -d --force-recreate"
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
                    sh "docker-compose -f docker-compose.prod.yaml up -d --force-recreate"
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
                    // Remove unused Docker images
                    sh "docker image prune -af"
                    
                    // Optionally, you can also remove unused volumes
                    sh "docker volume prune -f"
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