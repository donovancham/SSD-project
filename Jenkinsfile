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
            environment {
                FLASK_APP='cmsapp/__init__.py'
                FLASK_DEBUG='1'
                CMS_DEBUG='1'
                SECRET_KEY = credentials('42595a53-fa69-4969-9f3b-4c451c4029e9')
                DB_USERNAME = credentials('dd4b6deb-a438-49a6-b74a-890b9088229d')
                DB_PASS = credentials('145d582c-92de-469f-a6eb-50cc3c41018d')
                DB_NAME = credentials('8a82ed55-83ba-4b3a-8c54-821286187d71')
                DB_PORT = credentials('7d66c581-74c4-4b4d-8af7-9bb543120d49')
                ASSETS_ROOT = credentials('da799f08-884d-4b4c-9de5-591ec54b13db')
                DB_ENGINE = credentials('f6839d67-125b-4fe5-9d50-bba1962b12da')
                DB_HOST = 'db'
                TOKEN_SECRET_KEY = credentials('b1b1f16e-adfd-4250-a56a-777336fe11bd')
                GENERATE_TOKEN_SALT = credentials('30992ac8-9e8a-4523-b7f3-98fa4fa5de46')
                APP_MAIL_USERNAME = credentials('3db30906-2f58-4c6c-b08b-ae45b97a643a')
                APP_MAIL_PASSWORD = credentials('1fcca20a-cafd-4679-ac4a-2859be287545')
                MAIL_SERVER = 'smtp.googlemail.com'
                MAIL_PORT = '465'
                MAIL_USE_TLS = 'False'
                MAIL_USE_SSL = 'True'
            }

            steps {
                sh """
                echo "Running Unit Tests"
                """
                // Executing tests
                dir('services/web') {
                    withPythonEnv('/usr/bin/python3.10') {
                        sh 'pip install --upgrade pip'
                        sh 'pip3 install -r requirements.txt'
                        sh 'python3 -m pytest -v --junit-xml=reports/pytest.xml'
                        // Publish report
                        junit 'reports/pytest.xml'
                    }
                }
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
                configFileProvider([configFile(fileId: '2f325b2f-2be0-4899-8829-4195a0afd001', targetLocation: '.db.prod.env'), configFile(fileId: '31b62b81-efb0-40c8-9915-c1235bd292b5', targetLocation: '.web.prod.env'), configFile(fileId: 'a29bf18a-9f36-4631-ac61-9841ce2ab486', targetLocation: 'services/nginx/certs/selfsigned.crt'), configFile(fileId: '18acff6d-749d-4014-9aca-0acc2407c90a', targetLocation: 'services/nginx/ssl/private/selfsigned.key')]) {}
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
