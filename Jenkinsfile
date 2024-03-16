pipeline {
    agent any
    
    stages {
        stage('Setup') {
            steps {
                script {
                    sh '''
                    PYTHON="/Library/Frameworks/Python.framework/Versions/3.12/bin/python3"
                    $PYTHON -m venv myenv
                    source myenv/bin/activate
                    '''
                }
            }
        }
        
        stage('Install Dependencies') {
            steps {
                script {
                    sh 'source myenv/bin/activate && pip install -r requirements.txt'
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                script {
                    sh 'source myenv/bin/activate && behave'
                }
            }
        }
    }
}
