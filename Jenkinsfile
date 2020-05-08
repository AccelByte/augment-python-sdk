@Library("github.com/AccelByte/jenkins-pipeline-library@dev-lib") _
// required parameters:
// :: buildTarget
// :: deployTarget
// :: BRANCH_NAME
// :: build : Parameter to indicate jobs should do build or not. Default value is false.
// :: deploy : Parameter to indicate jobs should do deployment or not. Default value is false.
// :: grade : Parameter to indicate grade of jobs, either development, staging, or production. Default value is "none"
// :: PUSH_TRIGGER : The value to indicate what kind of push triggered this jobs. The value is true when branching or tagging. The value is false when merging or commit.

//Declared variable
imageName = null
imageTag = null
config = null
version = null
targetNamespace = params.deployTarget
doBuild = params.build
doDeploy = params.deploy // packaged to PyPA repo
doTagging = false
grade = params.grade
pushTrigger = env.PUSH_TRIGGER
branchName = params.BRANCH_NAME

if (pushTrigger == "false" || doBuild) {
  nodePod(name:"augment-python-sdk-build", type:"superbuilder") {
    stage('Checkout SCM') {
      checkout scm
      bitbucketBuildStatus("INPROGRESS", "Bitbucket_Build_AccelByte", "accelbyte")
    }

    try {
      stage("Preparation") {
        config = readJSON file: "jenkins.config.json"
        version = readJSON file: "version.json"
        version = version.version
        imageName = config.build.image_name
        if (branchName == "master" || env.BRANCH_NAME == "master") {
          grade = "production"
          doBuild = true
          doDeploy = true
          doTagging = true
        } else if (pushTrigger == "false") {
          // all other branches goes through this
          doBuild = true
          doTagging = false
          doDeploy = false
        }
      }

      if (doBuild) {
        container("builder") {
          stage("Build") {
            if (config.build) {
              config.build.targets."${params.buildTarget}".env_vars.each() {
                env."${it.key}" = "${it.value}"
                if (it.value_from != null) {
                  valueFrom  = it.value_from.split("://")
                  def type = valueFrom[0]
                  def secretKey = valueFrom[1].tokenize("/")[-1]
                  def path = valueFrom[1].tokenize("/")[0] + "/" + valueFrom[1].tokenize("/")[1]
                  if (type == "vault") {
                    // get data from vault
                    def vaultUrl = "http://vault.vault:8200"
                    def vaultCredentialId = "VAULT_JENKINS"
                    def secret = getVaultSecret(path, secretKey, vaultUrl, vaultCredentialId)
                    env."${it.key}" = secret
                  }
                } else {
                  env."${it.key}" = "${it.value}"
                }
              }
              sh """
                export REVISION_ID=${version}
                export BUILD_DATE=\$(date -u -Iseconds)
                export IAM_CLIENT_ID=${env.IAM_CLIENT_ID}
                export IAM_CLIENT_SECRET=${env.IAM_CLIENT_SECRET}
                export ADMIN_USERNAME=${env.ADMIN_USERNAME}
                export ADMIN_PASSWORD=${env.ADMIN_PASSWORD}
                make clean || true
                make build
              """
            }
          }

          stage("Test") {
            if (config.build.unit_test) {
              sh "make test"
            }
          }
        }
      }
    }
    catch (err) {
      echo "Exception thrown:\n ${err}"
      currentBuild.result = "FAILURE"
    }
    finally {
      if (grade == "production" || grade == "staging") {
        slackNotifier(currentBuild.currentResult.toString(), "#jenkins-monitoring")
      }
      bitbucketBuildStatus(currentBuild.currentResult.toString(),
                          "Bitbucket_Build_AccelByte",
                          "accelbyte")
    }
  }
}