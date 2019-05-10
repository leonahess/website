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
    stage('Deploy to leon-raspi-cluster-3') {
      agent {
        label "master"
      }
      steps {
        sshagent(credentials: ['d4eb3f5d-d0f5-4964-8bad-038f0d774551']) {
          sh "ssh -o StrictHostKeyChecking=no pi@leon-raspi-cluster-3 docker kill website"
          sh "ssh -o StrictHostKeyChecking=no pi@leon-raspi-cluster-3 docker rm website"
          sh "ssh -o StrictHostKeyChecking=no pi@leon-raspi-cluster-3 docker run --restart always -d --name=website -p 5000:5000 fx8350:5000/website:latest"
        }
      }
    }
  }
}
