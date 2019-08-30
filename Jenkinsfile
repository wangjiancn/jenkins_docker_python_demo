pipeline {
    agent none
    environment {
        CI = 'true'
    }
    stages {
        stage('Build') {
            agent any
                steps{
                    sh "printenv"
                    sh "echo printenv complete"
                    script{
                        docker.withRegistry("${env.DOCKER_REG_ALI}", "docker") {
                            def django_project = docker.build("test-docker-image:${env.BUILD_ID}","-f ./docker/Dockerfile.v8 .")
                            django_project.push()
                    }
                }
            }
        }
        stage('Deploy') {
            agent any
            steps {
                sh 'find -maxdepth 2'
                sh "echo Deploy completed"
            }
        }
    }
}