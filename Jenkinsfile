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
        sh "docker build -t hs110 ."
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
  }
}
