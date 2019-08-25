pipeline {
    agent none
    environment {
        CI = 'true'
    }
    stages {
        stage('Build') {
            agent any
            steps{
                script{
                    def django_project = docker.build("test-image:${env.BUILD_ID}","-f ./docker/Dockerfile.v8 .")
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