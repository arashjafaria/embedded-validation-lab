
pipeline {
    agent {
        label 'aeb-python'
    }

    options {
        skipDefaultCheckout(true)
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Downloading source code from GitHub'
                checkout scm
            }
        }

        stage('Test') {
            steps {
                echo 'Running automated AEB tests'
                sh 'python -m pytest -v --junitxml=test-results.xml'
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: 'test-results.xml'
        }
    }
}

