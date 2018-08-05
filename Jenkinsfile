#!/usr/bin/env groovy
import hudson.model.*
import hudson.EnvVars
import groovy.json.JsonSlurperClassic
import groovy.json.JsonBuilder
import groovy.json.JsonOutput
import java.net.URL

node('master') {

      def LOAD_BALANCER_ARN = ''
      def TARGET_GROUP_ARN  = ''
      def VPC_LINK_ID       = ''

      stage ('Clone') {
      	checkout scm

      }

     withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'awscreds']]) {


       stage('Create Cluster'){
            sh 'aws ecs create-cluster --region us-west-2 --cluster-name fargate-cluster'
        }

        stage('Create Target Group'){
                TARGET_GROUP_ARN = sh (
                script: " aws elbv2 create-target-group \
                        --region us-west-2 \
                        --name target-group-2 \
                        --target-type ip \
                        --protocol TCP \
                        --port 443 \
                        --vpc-id vpc-0d0a766a \
                        | jq '.TargetGroups[].TargetGroupArn' ",
                returnStdout: true
                ).trim()
                echo "Target Group Arn: ${TARGET_GROUP_ARN}"
        }


        stage('Create Load Balancer'){

          LOAD_BALANCER_ARN = sh (
          script: "aws elbv2 create-load-balancer \
              --name my-load-balancer3 \
              --type network  \
              --scheme internal \
              --region us-west-2 \
              --subnets subnet-d764cb9e \
              | jq '.LoadBalancers[].LoadBalancerArn' ",
          returnStdout: true
          ).trim()
          echo "Load Balancer Arn: ${LOAD_BALANCER_ARN}"


        }

        stage('Create VPC Link'){
          VPC_LINK_ID = sh (
          script: """aws apigateway create-vpc-link \
                  --name vpc-link-1 \
                  --region us-west-2 \
                  --target-arns ${LOAD_BALANCER_ARN}  | jq '.id' """,
          returnStdout: true
          ).trim()
          echo "VPC_LINK_ID: ${VPC_LINK_ID}"
        }



        stage('Create Listener'){
          sh """aws elbv2 create-listener \
                --region us-west-2 \
                --load-balancer-arn ${LOAD_BALANCER_ARN} \
                --protocol TCP \
                --port 443 \
                --default-actions Type=forward,TargetGroupArn=${TARGET_GROUP_ARN}"""
        }

        stage('Create service'){

            sh """aws ecs create-service --cluster fargate-cluster \
                    --region us-west-2 \
                    --service-name fargate-service \
                    --task-definition first-run-task-definition:2 \
                    --desired-count 1 \
                    --launch-type "FARGATE" \
                    --load-balancers targetGroupArn=${TARGET_GROUP_ARN},containerName=jacob_personal,containerPort=443 \
                    --network-configuration awsvpcConfiguration="{subnets=[subnet-d764cb9e],securityGroups=[sg-b3efdfcb],assignPublicIp="ENABLED"}" """

        }


    }
}
