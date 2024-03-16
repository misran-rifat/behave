pipeline {
    agent any
    
    stages {
        stage('Setup') {
            steps {
                sh 'PYTHON="/Library/Frameworks/Python.framework/Versions/3.12/bin/python3"'
                sh '$PYTHON -m venv myenv'
                sh 'source myenv/bin/activate'
            }
        }
        
        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        
        stage('Run Tests') {
            steps {
                sh 'behave'
            }
        }
    }
}
