def basedir = env.WORKSPACE
def agentLabel
if (BRANCH_NAME == "main") {
    agentLabel = "do3203"
} else {
    agentLabel = "staging"
}

pipeline {
    agent { 
        label agentLabel
        // label 'do3203'
    } 

    options {
        buildDiscarder logRotator( 
            daysToKeepStr: '5', 
            numToKeepStr: '5'
        )
        disableConcurrentBuilds()
    }

    stages {
        stage('Cleanup Workspace') {
            steps {
                // Clean before build
                cleanWs()
                sh """
                echo "Cleaned Up Workspace For Project"
                """
            }
        }

        stage('Code Checkout') { 
            steps {
                // Clone source code
                checkout scm
                sh 'chmod u+x ./services/web/entrypoint.sh'
            }
        }

        stage(' Unit Testing') {
            steps {
                sh """
                echo "Running Unit Tests"
                """
            }
        }

        stage('Code Analysis') {
            steps {
                sh """
                echo "Running Code Analysis"
                """
            }
        }

        stage('Enable HTTP/S') {
            steps {
                sh """
                echo "Enabling HTTP/S"
                """
                // Open ports
                sh 'sudo ufw allow http'
                sh 'sudo ufw allow https'
            }
        }

        stage('Deploy') { 
            steps {
                configFileProvider([configFile(fileId: '2f325b2f-2be0-4899-8829-4195a0afd001', targetLocation: '.db.prod.env'), configFile(fileId: '31b62b81-efb0-40c8-9915-c1235bd292b5', targetLocation: '.web.prod.env')]) {}
                sh """
                echo "Deploying Code..."
                """
                // Run docker
                sh 'docker compose -f docker-compose.prod.yml up -d --build'
                sh """
                echo "Successful Deployment!"
                """
            }
        }

        stage('Finish Testing') {
            when {
                not {
                    branch 'main'
                }
            }
            steps {
                input message: 'Finished using the web site? (Click "Proceed" to continue)' 
                echo 'Teardown initiated...'
                // Teardown docker
                sh('docker compose -f docker-compose.prod.yml down -v')// Open ports
                sh 'sudo ufw delete allow http'
                sh 'sudo ufw delete allow https'
                sh 'rm ./.db.prod.env'
                sh 'rm ./.web.prod.env'
            }
        }
    }
    post {
        success {
            echo "Build completed successfully!"
        }
        failure {
            echo 'Teardown initiated...'
            // Teardown docker
            sh('docker compose -f docker-compose.prod.yml down -v')
            // Open ports
            sh 'sudo ufw delete allow http'
            sh 'sudo ufw delete allow https'
            // Clean after failure
            cleanWs()
            echo 'Build Failed.'
        }
    }
}
