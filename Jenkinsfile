pipeline {
    agent any

    environment {
        PYTHON = '/Library/Frameworks/Python.framework/Versions/3.12/bin/python3'
        VENV_DIR = 'myenv'
        REQUIREMENTS_FILE = 'requirements.txt'
    }

    stages {
        stage('Setup') {
            steps {
                script {
                    // Check if the virtual environment exists, if not, create it
                    if (!file(VENV_DIR).exists()) {
                        sh "${PYTHON} -m venv ${VENV_DIR}"
                    }
                }
            }
        }

        stage('Install dependencies') {
            steps {
                script {
                    // Activate the virtual environment
                    sh "source ${VENV_DIR}/bin/activate"

                    // Install dependencies only if not already installed
                    sh "pip install --upgrade --quiet --requirement ${REQUIREMENTS_FILE} > /dev/null"
                }
            }
        }

        stage('Run Behave tests') {
            steps {
                script {
                    // Run Behave tests
                    sh "behave"
                }
            }
        }
    }

    post {
        always {
            // Deactivate the virtual environment
            sh "deactivate"
        }
    }
}
