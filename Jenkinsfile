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
                    docker.withRegistry("https://${env.DOCKER_REG_ALI}", "docker") {
                        django_project = docker.build("${env.DOCKER_REG_ALI}/test-docker-image:${env.BUILD_ID}","-f ./docker/Dockerfile.v8 .")
                    }
                }
            }
        }
        stage('Deploy') {
            agent any
            when { tag "*" }
            steps {
                sh 'find -maxdepth 2'
                script{
                    def tag = sh(returnStdout: true, script: "git tag -l --points-at HEAD").trim()
                    println tag
                    if(tag){
                        docker.withRegistry("https://${env.DOCKER_REG_ALI}", "docker") {
                            django_project.push(tag)
                        }
                    }
                }
                sh "echo Deploy completed"
            }
        }
    }
}