# Serverless app

## Description
This terraform configuration will create a lambda link to an aws api gateway

## Input data
| Name | Description |
|:---:| --- |
|**sqs_id**| The id of a sqs queue |
|**sqs_arn**| The arn of a sqs queue |

## Output data
| Name | Description |
|:---:| --- |
|**automate_lambda_base_url**| API base url |