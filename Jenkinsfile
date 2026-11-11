
pipeline {
    agent {
        label 'aeb-python'
    }

    options {
        skipDefaultCheckout(true)
        disableConcurrentBuilds()
        timeout(time: 20, unit: 'MINUTES')
        buildDiscarder(logRotator(
            numToKeepStr: '20',
            artifactNumToKeepStr: '20'
        ))
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Cleaning old workspace'
                deleteDir()

                echo 'Downloading latest source code'
                checkout scm
            }
        }

        stage('Setup') {
            steps {
                echo 'Creating Python test environment'
                sh '''
                    set -eu
                    python3 -m venv .venv
                    .venv/bin/python -m pip install -r requirements-dev.txt
                '''
            }
        }

        stage('Test and Coverage') {
            steps {
                echo 'Testing AEB with 95% coverage quality gate'

                sh '''
                    set -eu
                    .venv/bin/python -m pytest -v --junitxml=test-results.xml --cov=aeb --cov-branch --cov-report=term-missing --cov-report=xml:coverage.xml --cov-fail-under=95
                '''
            }

            post {
                always {
                    archiveArtifacts(
                        artifacts: 'coverage.xml',
                        allowEmptyArchive: true,
                        fingerprint: true
                    )

                    junit(
                        testResults: 'test-results.xml',
                        allowEmptyResults: false
                    )
                }
            }
        }
    }

    post {
        success {
            echo 'AEB validation completed successfully'
        }

        failure {
            echo 'AEB validation failed: review the console and test reports'
        }
    }
}

