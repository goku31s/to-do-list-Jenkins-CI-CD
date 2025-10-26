// Define environment variables
def DOCKER_IMAGE_NAME = "goku431/3-tier-todo-app" // <-- REPLACE
def K8S_MANIFEST_DIR = "kubernetes-manifests"

pipeline {
    // Run on the Jenkins VM itself (not a k8s pod agent)
    agent any 

    environment {
        // Use the short commit hash as the image tag
        IMAGE_TAG = env.GIT_COMMIT.take(7)
    }

    stages {
        stage('Checkout Code') {
            steps {
                // Checkout the repo this Jenkinsfile is in
                checkout scm
            }
        }

        stage('Build & Push Docker Image') {
            steps {
                // Use the DOCKERHUB_CREDS ID we created in Jenkins
                withCredentials([usernamePassword(credentialsId: 'DOCKERHUB_CREDS', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh "docker login -u $DOCKER_USER -p $DOCKER_PASS"
                    sh "docker build -t $DOCKER_IMAGE_NAME:$IMAGE_TAG -t $DOCKER_IMAGE_NAME:latest ."
                    sh "docker push --all-tags $DOCKER_IMAGE_NAME"
                }
            }
        }

        stage('Prepare Manifests') {
            steps {
                // Use yq to find and replace the image placeholder
                sh "yq -i '(.spec.template.spec.containers[] | select(.name==\"webapp\") | .image) = \"$DOCKER_IMAGE_NAME:$IMAGE_TAG\"' $K8S_MANIFEST_DIR/webapp.yaml"
            }
        }

        stage('Deploy to GKE') {
            steps {
                // Apply all manifests in the kubernetes directory
                // kubectl is already authenticated via the GCE VM setup
                sh "kubectl apply -f $K8S_MANIFEST_DIR/"

                // Wait for the new version to roll out
                sh "kubectl rollout status deployment/webapp-deployment --timeout=300s"
            }
        }
    }
}
