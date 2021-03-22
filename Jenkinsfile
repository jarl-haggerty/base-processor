#!groovy

node('executor') {
  ws("base-processors") {
    checkout scm

    def authorName  = sh(returnStdout: true, script: 'git --no-pager show --format="%an" --no-patch')
    def isMain    = env.BRANCH_NAME == "main"
    def serviceName = env.JOB_NAME.tokenize("/")[1]

    def commitHash  = sh(returnStdout: true, script: 'git rev-parse HEAD | cut -c-7').trim()
    def imageTag    = "${env.BUILD_NUMBER}-${commitHash}"

    try {
      //stage("Test") {
      //  sh """make test"""
      //}

      if(isMain) {
        stage("Build Image") {
          parallel (
            "build_base_processor" : {
              sh "IMAGE_TAG=${imageTag} docker-compose build base_processor"
              sh "IMAGE_TAG=latest docker-compose build base_processor"
            },
            "build_base_processor_test" : {
              sh "IMAGE_TAG=${imageTag} docker-compose build base_processor_test"
              sh "IMAGE_TAG=latest docker-compose build base_processor_test"
            },
            // "build_base_processor_freesurfer" : {
            //   sh "IMAGE_TAG=${imageTag} docker-compose -f docker-compose-freesurfer.yml build base_processor_freesurfer"
            //   sh "IMAGE_TAG=latest docker-compose -f docker-compose-freesurfer.yml build base_processor_freesurfer"
            // },
            // "build_base_processor_freesurfer_test" : {
            //   sh "IMAGE_TAG=${imageTag} docker-compose -f docker-compose-freesurfer.yml build base_processor_freesurfer_test"
            //   sh "IMAGE_TAG=latest docker-compose -f docker-compose-freesurfer.yml build base_processor_freesurfer_test"
            // },
            "build_base_processor_pandas" : {
              sh "IMAGE_TAG=${imageTag} docker-compose -f docker-compose-pandas.yml build base_processor_pandas"
              sh "IMAGE_TAG=latest docker-compose -f docker-compose-pandas.yml build base_processor_pandas"
            },
            "build_base_processor_pandas_test" : {
              sh "IMAGE_TAG=${imageTag} docker-compose -f docker-compose-pandas.yml build base_processor_pandas_test"
              sh "IMAGE_TAG=latest docker-compose -f docker-compose-pandas.yml build base_processor_pandas_test"
            },
            "build_base_processor_java_python" : {
              sh "IMAGE_TAG=${imageTag} docker-compose -f docker-compose-java.yml build base_processor_java_python"
              sh "IMAGE_TAG=latest docker-compose -f docker-compose-java.yml build base_processor_java_python"
            },
            "build_base_processor_ubuntu" : {
              sh "IMAGE_TAG=${imageTag} docker-compose -f docker-compose-ubuntu.yml build base_processor_ubuntu"
              sh "IMAGE_TAG=latest docker-compose -f docker-compose-ubuntu.yml build base_processor_ubuntu"
            },
            "build_base_processor_ubuntu_test" : {
              sh "IMAGE_TAG=${imageTag} docker-compose -f docker-compose-ubuntu.yml build base_processor_ubuntu_test"
              sh "IMAGE_TAG=latest docker-compose -f docker-compose-ubuntu.yml build base_processor_ubuntu_test"
            }
          )
        }

        stage("Push Image") {
          parallel (
            "push_base_processor": {
              sh "IMAGE_TAG=${imageTag} docker-compose push base_processor"
              sh "IMAGE_TAG=latest docker-compose push base_processor"
            },
            "push_base_processor_test": {
              sh "IMAGE_TAG=${imageTag} docker-compose push base_processor_test"
              sh "IMAGE_TAG=latest docker-compose push base_processor_test"
            },
            // "push_base_processor_freesurfer": {
            //   sh "IMAGE_TAG=${imageTag} docker-compose -f docker-compose-freesurfer.yml push base_processor_freesurfer"
            //   sh "IMAGE_TAG=latest docker-compose -f docker-compose-freesurfer.yml push base_processor_freesurfer"
            // },
            // "push_base_processor_freesurfer_test": {
            //   sh "IMAGE_TAG=${imageTag} docker-compose -f docker-compose-freesurfer.yml push base_processor_freesurfer_test"
            //   sh "IMAGE_TAG=latest docker-compose -f docker-compose-freesurfer.yml push base_processor_freesurfer_test"
            // },
            "push_base_processor_pandas": {
              sh "IMAGE_TAG=${imageTag} docker-compose -f docker-compose-pandas.yml push base_processor_pandas"
              sh "IMAGE_TAG=latest docker-compose -f docker-compose-pandas.yml push base_processor_pandas"
            },
            "push_base_processor_pandas_test": {
              sh "IMAGE_TAG=${imageTag} docker-compose -f docker-compose-pandas.yml push base_processor_pandas_test"
              sh "IMAGE_TAG=latest docker-compose -f docker-compose-pandas.yml push base_processor_pandas_test"
            },
            "push_base_processor_ubuntu": {
              sh "IMAGE_TAG=${imageTag} docker-compose -f docker-compose-ubuntu.yml push base_processor_ubuntu"
              sh "IMAGE_TAG=latest docker-compose -f docker-compose-ubuntu.yml push base_processor_ubuntu"
            },
            "push_base_processor_ubuntu_test": {
              sh "IMAGE_TAG=${imageTag} docker-compose -f docker-compose-ubuntu.yml push base_processor_ubuntu_test"
              sh "IMAGE_TAG=latest docker-compose -f docker-compose-ubuntu.yml push base_processor_ubuntu_test"
            },
            "push_base_processor_java_python": {
              sh "IMAGE_TAG=${imageTag} docker-compose -f docker-compose-java.yml push base_processor_java_python"
              sh "IMAGE_TAG=latest docker-compose -f docker-compose-java.yml push base_processor_java_python"
            }
          )
        }

        // stage("Deploy") {
        //   build job: "service-deploy/blackfynn-non-prod/us-east-1/dev-vpc-use1/dev/freesurfer-processor",
        //   parameters: [
        //     string(name: 'IMAGE_TAG', value: imageTag),
        //     string(name: 'TERRAFORM_ACTION', value: 'apply')
        //   ]
        // }
      }
    } catch (e) {
      // slackSend(color: '#b20000', message: "FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL}) by ${authorName}")
      throw e
    }

    // slackSend(color: '#006600', message: "SUCCESSFUL: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL}) by ${authorName}")
  }
}
