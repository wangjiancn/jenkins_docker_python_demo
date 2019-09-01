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
                    println env
                    // tag = sh(returnStdout: true, script: "git tag -l --points-at HEAD").trim()
                    // println tag
                    build_id = build.getBuildVariables().get('BUILD_ID')
                    println build_id 
                    date = new Date().format("YYYYMMdd")
                    println date
                    commit = build.getBuildVariables().get("GIT_COMMIT")
                    short_commit = commit ? commit[0..6] : ""
                    println commit
                    println short_commit 
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
                    test = "${env.BUILD_ID}"
                    println test
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