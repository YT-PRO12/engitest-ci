// Linux agent with Python 3.11+; JUnit and Pipeline plugins required.
pipeline {
    agent any
    options { timestamps(); disableConcurrentBuilds() }
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Environment') {
            steps {
                sh 'python3 -m venv .venv'
                sh '.venv/bin/python -m pip install -r requirements-dev.txt'
            }
        }
        stage('Lint and test') {
            steps {
                sh '.venv/bin/python -m ruff check .'
                sh '.venv/bin/python -m pytest --cov=engitest --cov-branch --cov-fail-under=90 --cov-report=xml --junitxml=test-results/junit.xml'
            }
        }
        stage('Build and verify wheel') {
            steps {
                sh '.venv/bin/python -m build'
                sh '.venv/bin/python scripts/smoke_wheel.py'
            }
        }
    }
    post {
        always {
            junit allowEmptyResults: true, testResults: 'test-results/junit.xml'
            archiveArtifacts allowEmptyArchive: true, artifacts: 'test-results/**,coverage.xml'
        }
        success { archiveArtifacts artifacts: 'dist/*', fingerprint: true }
    }
}
