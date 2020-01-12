resource "aws_api_gateway_rest_api" "automate_lambda" {
  name        = "esgi_cloud_api_gateway_lambda"
  description = "Call the lambda for the project"
}

resource "aws_api_gateway_resource" "automate_lambda_proxy" {
   rest_api_id = aws_api_gateway_rest_api.automate_lambda.id
   parent_id   = aws_api_gateway_rest_api.automate_lambda.root_resource_id
   path_part   = "update"
}

resource "aws_api_gateway_method" "automate_lambda_proxy" {
   rest_api_id   = aws_api_gateway_rest_api.automate_lambda.id
   resource_id   = aws_api_gateway_resource.automate_lambda_proxy.id
   http_method   = "ANY"
   authorization = "NONE"
}

resource "aws_api_gateway_integration" "automate_lambda" {
   rest_api_id = aws_api_gateway_rest_api.automate_lambda.id
   resource_id = aws_api_gateway_resource.automate_lambda_proxy.id
   http_method = aws_api_gateway_method.automate_lambda_proxy.http_method

   integration_http_method = "POST"
   type                    = "AWS_PROXY"
   uri                     = aws_lambda_function.automate_lambda.invoke_arn
}

resource "aws_api_gateway_deployment" "automate_lambda" {
  depends_on = [
    "aws_api_gateway_integration.automate_lambda"
  ]

  rest_api_id = "${aws_api_gateway_rest_api.automate_lambda.id}"
  stage_name  = "test"
}

output "automate_lambda_base_url" {
  value = aws_api_gateway_deployment.automate_lambda.invoke_url
}