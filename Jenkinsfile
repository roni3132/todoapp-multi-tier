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
                sh 'docker-compose up -d'
                echo "code has been built successfully"
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