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
      def LOAD_BALANCER_DNS = ''

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
                        --name target-group-7 \
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
              --name my-load-balancer-8 \
              --type network  \
              --scheme internal \
              --region us-west-2 \
              --subnets subnet-d764cb9e \
              | jq '.LoadBalancers[].LoadBalancerArn' ",
          returnStdout: true
          ).trim()
          echo "Load Balancer Arn: ${LOAD_BALANCER_ARN}"


          LOAD_BALANCER_DNS = sh(
          script: """aws elbv2 describe-load-balancers \
                  --region us-west-2 \
                  --load-balancer-arns ${LOAD_BALANCER_ARN} \
                   | jq '.LoadBalancers[].DNSName'""",
                   returnStdout: true
                   ).trim()
                   echo "Load Balancer DNS Name: ${LOAD_BALANCER_DNS}"


        }

        stage('Create Listener'){
          sh """aws elbv2 create-listener \
                --region us-west-2 \
                --load-balancer-arn ${LOAD_BALANCER_ARN} \
                --protocol TCP \
                --port 443 \
                --default-actions Type=forward,TargetGroupArn=${TARGET_GROUP_ARN}"""
        }


        stage('Wait for NLB to be active'){
          //MVP, just wait 4 min
          sleep 150
         // timeout(5) {
         //      waitUntil {
         //             def active = "active"
         //             def nlb_status = sh( script: """aws elbv2 describe-load-balancers \
         //                                  --region us-west-2 \
         //                                  --name my-load-balancer3  \
         //                                  | jq '.LoadBalancers[].State.Code' """,
         //                                  returnStdout: true ).trim()
         //
         //             echo("NLB_STATUS: " + nlb_status)
         //             echo("Active: " + active)
         //             if ( nlb_status.equalsIgnoreCase( active ) ){
         //                  return true;
         //             } else {
         //                  return false;
         //             }
         //        }
         //    }
        }



        stage('Create VPC Link'){
          VPC_LINK_ID = sh (
          script: """aws apigateway create-vpc-link \
                  --name vpc-link-2 \
                  --region us-west-2 \
                  --target-arns ${LOAD_BALANCER_ARN}  | jq '.id' """,
          returnStdout: true
          ).trim()
          echo "VPC_LINK_ID: ${VPC_LINK_ID}"

        }

        stage('Create service'){

            sh """aws ecs create-service --cluster fargate-cluster \
                    --region us-west-2 \
                    --service-name fargate-service-8 \
                    --task-definition first-run-task-definition:2 \
                    --desired-count 1 \
                    --launch-type "FARGATE" \
                    --load-balancers targetGroupArn=${TARGET_GROUP_ARN},containerName=jacob_personal,containerPort=443 \
                    --network-configuration awsvpcConfiguration="{subnets=[subnet-d764cb9e],securityGroups=[sg-b3efdfcb],assignPublicIp="ENABLED"}" """

        }


        stage('Create API-Gateway Resources'){

          API_GATEWAY_RES_1 = sh (
          script: """aws apigateway create-resource \
                    --region us-west-2 \
                    --rest-api-id h8hm94mesa \
                    --parent-id vlan6wcwxh \
                    --path-part v1 | jq '.id' """,
          returnStdout: true
          ).trim()
          echo "API_GATEWAY_RES_1: ${API_GATEWAY_RES_1}"


          API_GATEWAY_PROXY_RES = sh (
          script: """aws apigateway create-resource  \
              --region us-west-2 \
              --rest-api-id h8hm94mesa \
              --parent-id ${API_GATEWAY_RES_1} \
              --path-part {proxy+} | jq '.id' """,
          returnStdout: true
          ).trim()
          echo "API_GATEWAY_PROXY_RES: ${API_GATEWAY_PROXY_RES}"


          //CREATES THE ANY METHOD
          sh """aws apigateway put-method \
              --region us-west-2 \
              --rest-api-id h8hm94mesa \
              --resource-id ${API_GATEWAY_PROXY_RES} \
              --http-method GET \
              --authorization-type "NONE" """



      //  Create the proxy integration
        // sh """  aws apigateway put-integration \
        //         --region us-west-2 \
        //         --rest-api-id h8hm94mesa \
        //         --resource-id ${API_GATEWAY_PROXY_RES} \
        //         --uri 'http://myApi.example.com/v1' \
        //         --http-method ANY \
        //         --type HTTP_PROXY \
        //         --integration-http-method ANY \
        //         --connection-type VPC_LINK \
        //         --connection-id ${VPC_LINK_ID} """

        sh """  aws apigateway put-integration \
                --region us-west-2 \
                --rest-api-id h8hm94mesa \
                --resource-id ${API_GATEWAY_PROXY_RES} \
                --uri 'http://myApi.example.com/v1/' \
                --http-method GET \
                --type HTTP_PROXY \
                --integration-http-method GET \
                --connection-type VPC_LINK \
                --connection-id "\${stageVariables.vpcLinkId}" """


        sh   """aws apigateway update-integration \
             --region us-west-2 \
             --rest-api-id h8hm94mesa \
             --resource-id ${API_GATEWAY_PROXY_RES} \
             --http-method GET \
             --patch-operations '[{"op":"replace","path":"/connectionId","value":"${stageVariables.vpcLinkId}"}]'  """


       sh """aws apigateway create-deployment \
            --region us-west-2 \
            --rest-api-id h8hm94mesa \
            --stage-name dev \
            --variables vpcLinkId=${VPC_LINK_ID}"""


        }
    }
}
