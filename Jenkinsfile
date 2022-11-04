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

    environment {
        FLASK_APP           = 'cmsapp/__init__.py'
        FLASK_DEBUG         = '0'
        CMS_DEBUG           = '0'
        SECRET_KEY          = credentials('42595a53-fa69-4969-9f3b-4c451c4029e9')
        ASSETS_ROOT         = credentials('da799f08-884d-4b4c-9de5-591ec54b13db')
        DB_ENGINE           = credentials('f6839d67-125b-4fe5-9d50-bba1962b12da')
        DB_USERNAME         = credentials('dd4b6deb-a438-49a6-b74a-890b9088229d')
        DB_PASS             = credentials('145d582c-92de-469f-a6eb-50cc3c41018d')
        DB_HOST             = 'db'
        DB_PORT             = credentials('7d66c581-74c4-4b4d-8af7-9bb543120d49')
        DB_NAME             = credentials('8a82ed55-83ba-4b3a-8c54-821286187d71')
        TOKEN_SECRET_KEY    = credentials('b1b1f16e-adfd-4250-a56a-777336fe11bd')
        GENERATE_TOKEN_SALT = credentials('30992ac8-9e8a-4523-b7f3-98fa4fa5de46')
        APP_MAIL_USERNAME   = credentials('3db30906-2f58-4c6c-b08b-ae45b97a643a')
        APP_MAIL_PASSWORD   = credentials('1fcca20a-cafd-4679-ac4a-2859be287545')
        MAIL_SERVER         = 'smtp.googlemail.com'
        MAIL_PORT           = '465'
        MAIL_USE_TLS        = 'False'
        MAIL_USE_SSL        = 'True'
    }

    stages {
        stage('Setup') { 
            steps {
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
                // Run docker
                sh('docker compose -f docker-compose.prod.yml up -d --build')
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
                sh('docker compose -f docker-compose.prod.yml down -v')
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
            echo "Build Failed."
        }
    }
}