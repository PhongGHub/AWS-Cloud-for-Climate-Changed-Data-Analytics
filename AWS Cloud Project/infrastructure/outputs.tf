output "s3_bucket_name" {
  value = aws_s3_bucket.data_lake.bucket
}

output "kinesis_stream_name" {
  value = aws_kinesis_stream.climate_stream.name
}

output "lambda_function_name" {
  value = aws_lambda_function.processor.function_name
}
