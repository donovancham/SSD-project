// Defined to better control app execution based on workspace
def basedir = env.WORKSPACE

// Defined to control execution on live testing or live deploy environment
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
            daysToKeepStr: '10', 
            numToKeepStr: '40'
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
                // // Warnings next gen
                // recordIssues enabledForFailure: true, tools: owaspDependencyCheck()
            }
        }

        stage ('OWASP Dependency-Check Vulnerabilities') {
            steps {
                // Create folder for reports
                sh 'mkdir owasp-reports'
                // Invoke dependency check
                dependencyCheck additionalArguments: ''' 
                    -o "owasp-reports" 
                    -s "./services/web" 
                    -f "ALL" 
                    --prettyPrint 
                    --enableExperimental 
                    --disablePyDist "false" 
                    --disablePyPkg "false" 
                    --disableMSBuild "true" 
                    --disableNodeJS "true" 
                    --disablePnpmAudit "true" 
                    --disableNodeAudit "true" 
                    ''', odcInstallation: 'CMS'    // Installations are defined in the Jenkins Global Tool Configuration.

                // Publish report
                dependencyCheckPublisher failedNewCritical: 1, failedNewHigh: 2, failedNewLow: 10, failedNewMedium: 5, failedTotalCritical: 1, failedTotalHigh: 2, failedTotalLow: 10, failedTotalMedium: 5, pattern: 'owasp-reports/dependency-check-report.xml'
            }
            post {
                success {
                    // Warnings next gen
                    recordIssues(
                        enabledForFailure: true, 
                        tool: owaspDependencyCheck()
                    )
                }
            }
        }

        // https://igorski.co/sonarqube-scans-using-jenkins-declarative-pipelines/
        stage('SonarQube analysis') {
            environment {
                // Defined for Sonarqube
                scannerHome = tool 'SonarScanner4.7'
            }
            
            steps {
                withSonarQubeEnv('Sonarqube') { 
                    sh '${scannerHome}/bin/sonar-scanner'
                }
            }
            post {
                always {
                    // Warnings next gen
                    recordIssues(
                        enabledForFailure: true, 
                        tool: sonarQube()
                    )
                }
            }
        }

        stage('Deploy: Open Ports') {
            steps {
                sh """
                echo "Enabling HTTP/S"
                """
                // Open ports
                sh 'sudo ufw allow http'
                sh 'sudo ufw allow https'
            }
        }

        stage('Deploy: Starting Services') { 
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

        stage('Deploy: HTTPS Config') {
             steps {
                 sh '''
                 docker exec cmsapp-proxy sh -c "mv /etc/nginx/conf.d/nginx.new /etc/nginx/conf.d/nginx.conf;"
                 '''
             }
        }
        
        stage('Cleanup Files') {
            when {
                branch 'main'
            }
            steps {
                sh """
                echo "Cleaning up files in live environment..."
                """
                sh 'rm ./.db.prod.env'
                sh 'rm ./.web.prod.env'
            }
        }

        stage('Finish Testing') {
            when {
                not {
                    branch 'main'
                }
            }
            steps {
                timeout(time: 3, unit: 'HOURS') {
                    input message: 'Finished using the web site? (Click "Proceed" to continue)' 
                }
                echo 'Teardown initiated...'
                // Teardown docker
                sh 'docker compose -f docker-compose.prod.yml down -v'
                // Close ports
                sh 'sudo ufw delete allow http'
                sh 'sudo ufw delete allow https'
                // Ensure sensitive files are removed
                sh 'rm ./.db.prod.env'
                sh 'rm ./.web.prod.env'
                // Clean workspace to be safe
                cleanWs()
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
            sh 'docker compose -f docker-compose.prod.yml down -v'
            // Close ports
            sh 'sudo ufw delete allow http'
            sh 'sudo ufw delete allow https'
            // Clean after failure
            cleanWs()
            echo 'Build Failed.'
        }
    }
}
