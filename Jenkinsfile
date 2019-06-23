pipeline {
  agent any
  triggers {
    pollSCM('H/15 * * * *')
  }
  stages {
    stage('Build Container') {
      agent {
        label "Pi_3"
      }
      steps {
        sh "docker build -t website ."
      }
    }
    stage('Tag Container') {
      agent {
        label "Pi_3"
      }
      steps {
        sh "docker tag website fx8350:5000/website:latest"
        sh "docker tag website fx8350:5000/website:${env.BUILD_NUMBER}"
        sh "docker tag website leonhess/website:latest"
        sh "docker tag website leonhess/website:${env.BUILD_NUMBER}"
      }
    }
    stage('Push to Registries') {
      parallel {
        stage('Push to local Registry') {
          agent {
            label "Pi_3"
          }
          steps {
            sh "docker push fx8350:5000/website:${env.BUILD_NUMBER}"
            sh "docker push fx8350:5000/website:latest"
          }
        }
        stage('Push to DockerHub') {
          agent {
            label "Pi_3"
          }
          steps {
            withDockerRegistry([credentialsId: "dockerhub", url: ""]) {
              sh "docker push leonhess/website:${env.BUILD_NUMBER}"
              sh "docker push leonhess/website:latest"
            }
          }
        }
      }
    }
    stage('Cleanup') {
      agent {
        label "Pi_3"
      }
      steps {
        sh "docker rmi fx8350:5000/website:latest"
        sh "docker rmi fx8350:5000/website:${env.BUILD_NUMBER}"
        sh "docker rmi leonhess/website:latest"
        sh "docker rmi leonhess/website:${env.BUILD_NUMBER}"
      }
    }
    stage('Deploy to swarm') {
      agent {
        label "master"
      }
      steps {
        ansiblePlaybook(
          playbook: 'deploy_to_swarm.yml',
          credentialsId: '78c069cd-77c4-4c91-89cc-7805f3c9cfe2'
          )
        }
      }
    }
  }
