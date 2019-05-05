pipeline {
  agent any
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
        sh "docker tag hs110 fx8350:5000/hs110:latest"
        sh "docker tag hs110 fx8350:5000/hs110:${env.BUILD_NUMBER}"
        sh "docker tag hs110 leonhess/hs110:latest"
        sh "docker tag hs110 leonhess/hs110:${env.BUILD_NUMBER}"
      }
    }
    stage('Push to local Registry') {
      agent {
        label "Pi_3"
      }
      steps {
        sh "docker push fx8350:5000/hs110:${env.BUILD_NUMBER}"
        sh "docker push fx8350:5000/hs110:latest"
      }
    }
    stage('Push to DockerHub') {
      agent {
        label "Pi_3"
      }
      steps {
        withDockerRegistry([credentialsId: "dockerhub", url: ""]) {
          sh "docker push leonhess/hs110:${env.BUILD_NUMBER}"
          sh "docker push leonhess/hs110:latest"
        }
      }
    }
    stage('Cleanup') {
      agent {
        label "Pi_3"
      }
      steps {
        sh "docker rmi fx8350:5000/hs110:latest"
        sh "docker rmi fx8350:5000/hs110:${env.BUILD_NUMBER}"
        sh "docker rmi leonhess/hs110:latest"
        sh "docker rmi leonhess/hs110:${env.BUILD_NUMBER}"
      }
    }
  }
}
