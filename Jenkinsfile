def agentLabel
if (BRANCH_NAME == 'dev-production-env') {
    agentLabel = 'staging'
}
else if (BRANCH_NAME == 'main') {
    agentLabel = 'do3203'
}

pipeline {
    agent { label agentLabel } 
    stages {
        stage('Build') { 
            steps {
                withCredentials([file(credentialsId: '1f8b1838-5199-43e3-87f9-61585d127c98', variable: 'secret_file')]) {
                    // Convert to environment variables
                    sh('export $(cat $secret_file | xargs)')
                }
                // Run docker
                sh('docker-compose -f docker-compose.prod.yml up -d --build')
                
            }
        }
        // stage('Test') { 
        //     steps {
        //         // 
        //     }
        // }
        // stage('Deploy') { 
        //     steps {
        //         // 
        //     }
        // }
        post {
            success {
                echo "Run completed successfully!"
            }
            failure {
                echo "Teardown initiated..."
                // Teardown docker
                sh('docker-compose -f docker-compose.prod.yml down -v')
                echo "Build Failed."
            }
        }
    }
}