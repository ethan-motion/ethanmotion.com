resource "aws_cloudfront_distribution" "EM30Y9BEWP31R" {
  aliases = ["ethanmotion.com", "www.ethanmotion.com"]
  comment = "Test"
  default_cache_behavior {
    allowed_methods = ["GET", "HEAD"]
    cached_methods  = ["GET", "HEAD"]
    compress        = false
    default_ttl     = 0
    forwarded_values {
      cookies {
        forward           = "none"
        whitelisted_names = []
      }
      headers                 = []
      query_string            = false
      query_string_cache_keys = []
    }
    max_ttl                = 0
    min_ttl                = 0
    smooth_streaming       = false
    target_origin_id       = "S3-ethanmotion.com"
    viewer_protocol_policy = "redirect-to-https"
  }
  default_root_object = "index.html"
  enabled             = true
  http_version        = "http2"
  is_ipv6_enabled     = true
  origin {
    connection_attempts = 3
    connection_timeout  = 10
    domain_name         = "ethanmotion.com.s3.amazonaws.com"
    origin_id           = "S3-ethanmotion.com"
    origin_path         = ""
    s3_origin_config {
      origin_access_identity = "origin-access-identity/cloudfront/E1NGKUUCFMUVP3"
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
}
