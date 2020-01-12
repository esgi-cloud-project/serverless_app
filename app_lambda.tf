resource "aws_iam_role" "iam_automate_lambda" {
  name = "esgi_cloud_iam_lambda"

  assume_role_policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": "sts:AssumeRole",
        "Principal": {
            "Service": "lambda.amazonaws.com"
        },
        "Effect": "Allow",
        "Sid": ""
      }
    ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "iam_policies_automate_lambda" {
  role= "${aws_iam_role.iam_automate_lambda.name}"
  policy_arn= "arn:aws:iam::aws:policy/AmazonSQSFullAccess"
}


data "archive_file" "lambda" {
  type        = "zip"
  source_dir = "${path.module}/automate_lambda"
  output_path = "${path.module}/lambda.zip"
}

resource "aws_lambda_function" "automate_lambda" {
    filename = "${path.module}/lambda.zip"
    function_name = "esgi_cloud_cps_lambda_trigger"
    handler = "index.handler"
    runtime = "python3.8"
    role = "${aws_iam_role.iam_automate_lambda.arn}"
    source_code_hash = "${data.archive_file.lambda.output_base64sha256}"
    environment {
        variables = {
           EVENT_SERVICE_URL = var.sqs_id, 
           EVENT_SERVICE_ARN = var.sqs_arn, 
        }
    }
}

resource "aws_lambda_permission" "automate_lambda" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.automate_lambda.arn}"
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_api_gateway_deployment.automate_lambda.execution_arn}/*/*"
}