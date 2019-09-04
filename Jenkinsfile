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
                script{
                    def date = new Date().format("YYYYMMdd")
                    def commit = env.GIT_COMMIT
                    def short_commit = commit ? commit[0..6] : ""
                    local_tag = date + "-" + short_commit
                    IMAGE_NAME = "${env.DOCKER_REG_ALI}/test-docker-image"
                    docker.withRegistry("https://${env.DOCKER_REG_ALI}", "docker") {
                        image = docker.build("${IMAGE_NAME}:${local_tag}","-f ./docker/Dockerfile.v8 .")
                    }
                }
                sh "docker rmi ${${IMAGE_NAME}:${local_tag}"
            }
        }
        stage('Deploy') {
            agent any
            when { tag "*" }
            steps {
                script{
                    // 出现两个Tag取最后一个
                    def tag1 = sh(returnStdout: true, script: "git tag -l --points-at HEAD").trim()
                    println tag1
                    def tag = sh(returnStdout: true, script: "git tag -l --points-at HEAD").trim().split("\n")[-1]
                    println tag
                    docker.withRegistry("https://${env.DOCKER_REG_ALI}", "docker") {
                        image = docker.build(
                            "${IMAGE_NAME}:${tag}",
                            "--build-arg version=${tag} --build-arg date=${local_tag}  -f ./docker/Dockerfile.v8 ."
                            )
                        image.push()
                    }
                    println image
                    println image.name
                    println image.tag
                }
                sh "echo Deploy completed"
            }
        }
    }
}