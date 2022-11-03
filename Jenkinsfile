def agentLabel
if (BRANCH_NAME == 'dev-production-env') {
    agentLabel = 'staging'
}
else if (BRANCH_NAME == 'main') {
    agentLabel = 'do3203'
}

pipeline {
    agent { 
        node {
            label agentLabel
            // Clone source code
            checkout scm
            ws {
                withCredentials([file(credentialsId: '1f8b1838-5199-43e3-87f9-61585d127c98', variable: 'secret_file')]) {
                    // Convert to environment variables
                    sh 'export $(cat $secret_file | xargs) >/dev/null'
                }
            }
        }
    } 

    options {
        buildDiscarder logRotator( 
            daysToKeepStr: '5', 
            numToKeepStr: '5'
        )
        disableConcurrentBuilds()
    }

    stages {
        stage('Setup') { 
            steps {
                sh 'ls -la'
                // dir() {

                // }
                // Run docker
                sh('docker-compose -f docker-compose.prod.yml up -d --build')
            }
        }
        stage('Finish Testing') {
            when {
                branch 'dev-production-env'
            }
            steps {
                input message: 'Finished using the web site? (Click "Proceed" to continue)' 
                echo "Teardown initiated..."
                // Teardown docker
                sh('docker-compose -f docker-compose.prod.yml down -v')
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
        
    }
    post {
        success {
            echo "Build completed successfully!"
        }
        failure {
            echo "Teardown initiated..."
            // Teardown docker
            sh('docker-compose -f docker-compose.prod.yml down -v')
            echo "Build Failed."
        }
    }
}