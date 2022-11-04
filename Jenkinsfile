pipeline {
    agent { 
        label 'do3203'
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
                // Clean before build
                cleanWs()
                // Clone source code
                checkout scm
                sh 'chmod u+x ./services/web/entrypoint.sh'
                
            }
        }
        // stage('Test') { 
        //     steps {
        //         // 
        //     }
        // }
        stage('Deploy') { 
            steps {
                configFileProvider([configFile(fileId: '2f325b2f-2be0-4899-8829-4195a0afd001', targetLocation: '.db.prod.env'), configFile(fileId: '31b62b81-efb0-40c8-9915-c1235bd292b5', targetLocation: '.web.prod.env')]) {
                    // Run docker
                    sh 'docker compose -f docker-compose.prod.yml up -d --build'
                }
                // Open ports
                sh 'sudo ufw allow http'
                sh 'sudo ufw allow https'
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
                sh('docker compose -f docker-compose.prod.yml down -v')// Open ports
                sh 'sudo ufw delete allow http'
                sh 'sudo ufw delete allow https'
            }
        }
    }
    post {
        success {
            echo "Build completed successfully!"
        }
        failure {
            echo "Teardown initiated..."
            // Teardown docker
            sh('docker compose -f docker-compose.prod.yml down -v')
            // Open ports
            sh 'sudo ufw delete allow http'
            sh 'sudo ufw delete allow https'
            // Clean after failure
            cleanWs()
            echo "Build Failed."
        }
    }
}