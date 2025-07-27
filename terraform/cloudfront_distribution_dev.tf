resource "aws_cloudfront_distribution" "E2N0SDO3M868R" {
  aliases = ["dev.ethanmotion.com"]
  comment = "dev.ethanmotion.com"
  default_cache_behavior {
    allowed_methods           = ["GET", "HEAD"]
    cache_policy_id           = ""
    cached_methods            = ["GET", "HEAD"]
    compress                  = true
    default_ttl               = 0
    field_level_encryption_id = ""
    forwarded_values {
      cookies {
        forward           = "none"
        whitelisted_names = []
      }
      headers                 = []
      query_string            = false
      query_string_cache_keys = []
    }
    lambda_function_association {
      event_type   = "viewer-request"
      include_body = true
      lambda_arn   = "arn:aws:lambda:us-east-1:330756613296:function:dev-ethanmotion-com-password-protect:9"
    }
    max_ttl                  = 0
    min_ttl                  = 0
    origin_request_policy_id = ""
    realtime_log_config_arn  = ""
    smooth_streaming         = false
    target_origin_id         = "S3-dev.ethanmotion.com"
    trusted_key_groups       = []
    trusted_signers          = []
    viewer_protocol_policy   = "redirect-to-https"
  }
  default_root_object = "index.html"
  enabled             = true
  http_version        = "http2"
  is_ipv6_enabled     = true
  origin {
    connection_attempts = 3
    connection_timeout  = 10
    domain_name         = "dev.ethanmotion.com.s3.amazonaws.com"
    origin_id           = "S3-dev.ethanmotion.com"
    origin_path         = ""
    s3_origin_config {
      origin_access_identity = "origin-access-identity/cloudfront/E6OS7EAN0IBZP"
    }
  }
  price_class = "PriceClass_All"
  restrictions {
    geo_restriction {
      restriction_type = "none"
      locations        = []
    }
  }
  retain_on_delete = false
  viewer_certificate {
    acm_certificate_arn            = "arn:aws:acm:us-east-1:330756613296:certificate/be7dbb59-db36-4033-9bfa-ebcbd8f177b5"
    cloudfront_default_certificate = false
    iam_certificate_id             = ""
    minimum_protocol_version       = "TLSv1.2_2018"
    ssl_support_method             = "sni-only"
  }
  wait_for_deployment = true
  web_acl_id          = ""
  custom_error_response {
    error_code         = 404
    response_code      = 404
    response_page_path = "/error.html"
  }
  custom_error_response {
    error_code         = 403
    response_code      = 404
    response_page_path = "/error.html"
  }
}
