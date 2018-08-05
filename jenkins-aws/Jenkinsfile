node {
  def app
  stage('Clone repository') {
    checkout scm
  }

  stage('Build images') {
    app = docker.build("gargam974/jenkins-aws:${env.BUILD_NUMBER}")
  }

  stage('Push image') {
    withCredentials([usernamePassword(credentialsId: 'dockerhub', passwordVariable: 'dockerHubPassword', usernameVariable: 'dockerHubUser')]) {
      sh "docker login -u ${env.dockerHubUser} -p ${env.dockerHubPassword}"
      app.push()
      app.push("latest")
    }
  }
}
