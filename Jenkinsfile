
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

        stage('Setup') {
            steps {
                echo 'Preparing Python testing environment'
                sh '''
                    python3 -m venv --clear .venv
                    .venv/bin/python -m pip install -r requirements-dev.txt
                '''
            }
        }

        stage('Test and Coverage') {
            steps {
                echo 'Running AEB tests with a 95% coverage gate'
                sh '''
                    .venv/bin/python -m pytest -v \
                        --junitxml=test-results.xml \
                        --cov=aeb \
                        --cov-branch \
                        --cov-report=term-missing \
                        --cov-report=xml:coverage.xml \
                        --cov-fail-under=95
                '''
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true,
                  testResults: 'test-results.xml'
        }
    }
}

