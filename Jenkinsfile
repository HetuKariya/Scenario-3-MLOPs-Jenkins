pipeline {
    agent { //agent any does not allow specifying the custom workspace
        node {
            label 'local'
            customWorkspace 'C:/Users/DELL/Desktop/MLOPS/Jenkins/Scenario-3'
        }
    }
    stages {
        stage('Checkout Code') {
            steps {
                // Scenario 3: REMOTE git repository (GitHub)
                // Replace the URL with your repo; for a private repo, add: credentialsId: 'github-creds'
                git branch: 'main',
                    url: 'https://github.com/HetuKariya/Scenario-3-MLOPs-Jenkins'
            }
        }
        stage('Show Workspace') {
            steps {
                bat 'cd'
                bat 'dir'
                withEnv(['PATH+DOCKER=C:/Users/DELL/AppData/Local/Programs/DockerDesktop/resources/bin']) {
                    bat 'where docker'
                    bat 'docker --version'
                    bat 'docker-compose version'
                }
            }
        }
        stage('Build Images') {
            steps {
                withEnv(['PATH+DOCKER=C:/Users/DELL/AppData/Local/Programs/DockerDesktop/resources/bin']) {
                    bat 'docker-compose build'
                }
            }
        }
        stage('Deploy Containers') {
            steps {
                withEnv(['PATH+DOCKER=C:/Users/DELL/AppData/Local/Programs/DockerDesktop/resources/bin']) {
                    bat 'docker-compose up -d'
                }
            }
        }
    }
}