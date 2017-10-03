node {
    stage('Prepare') {
        echo 'Preparing environment..'
        if (isUnix()) {
            sh 'sudo add-apt-repository ppa:jonathonf/python-3.6'
            sh 'sudo apt-get update'
            sh 'sudo apt-get install python3.6'
            sh 'sudo apt-get install pip'
            sh 'pip install virtualenv'
            sh 'virtualenv -p python3.6 venv'
            sh 'source venv/bin/activate'
            sh 'pip install pybuilder'
            sh 'pyb install_dependencies'
        }
    }
    stage('Build') {
        echo 'Building..'
    }
    stage('Test') {
        echo 'Testing..'
    }
    stage('Deploy') {
        echo 'Deploying....'
    }

}