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
                sh 'docker-compose build --no-cache'
                echo "code has been built successfully"
            }
        }
        stage('SONARQUBE SCAN') {
            steps {
                withSonarQubeEnv('Sonar') {
                    sh "${tool 'Sonar'}/bin/sonar-scanner"
                }
            }
        }
        stage('SonarQube Quality Gate') {
            steps {
                timeout(time: 2, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
        stage("Trivy Scan"){
            steps{
                sh 'trivy image todoapp-backend:latest'
            }
        }
        stage("OWASP Scan"){
            steps{
                dependencyCheck additionalArguments: '--scan ./ ', odcInstallation: 'OWASP'
                dependencyCheckPublisher pattern: '**/dependency-check-report.xml'
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockeridpass', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PAT')]) {
                    sh 'echo $DOCKER_PAT | docker login -u $DOCKER_USER --password-stdin'
                    sh 'docker tag todoapp-backend:latest $DOCKER_USER/todoapp-backend:latest'
                    sh 'docker push $DOCKER_USER/todoapp-backend:latest'
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