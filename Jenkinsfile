pipeline{
    agent any
    stages{
        stage("GET CODE"){
            steps{
                git url: "https://github.com/roni3132/todoapp-multi-tier.git",branch: "main"
                echo "code has been pulled successfully"
            }
        }
        stage("BUILD CODE"){
            steps{
                sh 'docker-compose down'
                sh 'docker-compose build --no-cache'
                echo "code has been built successfully"
            }
        }
        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockeridpass', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PAT')]) {
                    sh 'echo $DOCKER_PAT | docker login -u $DOCKER_USER --password-stdin'
                    sh 'docker tag todoapp-backend:latest roni313233/todoapp-backend:latest'
                    sh 'docker push roni313233/todoapp-backend:latest'
                    echo "Docker login and image push successful"
                }
            }
        }
         stage("Deploy CODE"){
            steps{
                sh 'docker-compose up -d'
                echo "code has been deployed successfully"
            }
        }
        stage("TEST CODE"){
            steps{
                sh 'docker ps -a'
                echo "code has been tested successfully"
            }
        }

    }
}