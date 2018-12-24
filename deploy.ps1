$config = Get-Content -Path config.json -Raw | ConvertFrom-Json
$appName = $config.application_name


# Create a Key Pair
$kpName = $appName + "-key"
$keyPair = New-EC2KeyPair -KeyName $kpName
$pemFile = $kpName + ".pem"
$keyPair.KeyMaterial | Out-File -Encoding ascii $pemFile


$sgName = $appName + "-sg"
$sgDescription = "Auto Scaling Group for $appName"

# Create the security group
$sgID = New-EC2SecurityGroup `
    -GroupName $sgName `
    -GroupDescription $sgDescription

# Add Name tag to sg resource
$tag = New-Object Amazon.EC2.Model.Tag
$tag.Key = "Name"
$tag.Value = $sgName
New-EC2Tag -Resource $sgID -Tag $tag

# Add inbound SSH rule
$cidrBlocks = New-Object 'collections.generic.list[string]'
$cidrBlocks.add("0.0.0.0/0")
$ipPermissions = New-Object Amazon.EC2.Model.IpPermission
$ipPermissions.IpProtocol = "tcp"
$ipPermissions.FromPort = 22
$ipPermissions.ToPort = 22
$ipPermissions.IpRanges = $cidrBlocks
Grant-EC2SecurityGroupIngress -GroupName $sgName -IpPermissions $ipPermissions

# Add inbound HTTP rule
$cidrBlocks = New-Object 'collections.generic.list[string]'
$cidrBlocks.add("0.0.0.0/0")
$ipPermissions = New-Object Amazon.EC2.Model.IpPermission
$ipPermissions.IpProtocol = "tcp"
$ipPermissions.FromPort = 80
$ipPermissions.ToPort = 80
$ipPermissions.IpRanges = $cidrBlocks
Grant-EC2SecurityGroupIngress -GroupName $sgName -IpPermissions $ipPermissions

# Add inbound HTTPS rule
$cidrBlocks = New-Object 'collections.generic.list[string]'
$cidrBlocks.add("0.0.0.0/0")
$ipPermissions = New-Object Amazon.EC2.Model.IpPermission
$ipPermissions.IpProtocol = "tcp"
$ipPermissions.FromPort = 443
$ipPermissions.ToPort = 443
$ipPermissions.IpRanges = $cidrBlocks
Grant-EC2SecurityGroupIngress -GroupName $sgName -IpPermissions $ipPermissions

# Add inbound ICMP IPv4 rule
$cidrBlocks = New-Object 'collections.generic.list[string]'
$cidrBlocks.add("0.0.0.0/0")
$ipPermissions = New-Object Amazon.EC2.Model.IpPermission
$ipPermissions.IpProtocol = "ICMP"
$ipPermissions.FromPort = "-1"
$ipPermissions.ToPort = "-1"
$ipPermissions.IpRanges = $cidrBlocks
Grant-EC2SecurityGroupIngress -GroupName $sgName -IpPermissions $ipPermissions


# Create Launch Configuration (lc)
$lcName = $appName + "-lc"
New-ASLaunchConfiguration `
    -LaunchConfigurationName $lcName `
    -KeyName $kpName `
    -IamInstanceProfile ec2-access-s3 `
    -ImageId $config.image_ami `
    -SecurityGroup $sgID `
    -EbsOptimized 0 `
    -InstanceType $config.instance_type


# Create Auto Scaling Group (asg)
$asgName = $appName + "-asg"
New-ASAutoScalingGroup `
    -AutoScalingGroupName $asgName `
    -LaunchConfigurationName $lcName `
    -MinSize $config.asg_min_hosts `
    -MaxSize $config.asg_max_hosts `
    -DesiredCapacity $config.asg_desired_hosts `
    -AvailabilityZone @("us-east-1a") `
    -DefaultCooldown 300 `
    -HealthCheckGracePeriod 60 `
    -HealthCheckType EC2 `
    -Tag @{Key="Name"; Value=$appName}


# Create Application Load Balancer (alb)
$albName = $appName + "-alb"
$alb = New-ELB2LoadBalancer `
    -IpAddressType ipv4 `
    -Name $albName `
    -Scheme internet-facing `
    -SecurityGroup @($sgID) `
    -Type application `
    -Subnet @($config.subnet_1,$config.subnet_2,$config.subnet_3)


# Create Target Group
$tgName = $appName + "-tg"
$tg = New-ELB2TargetGroup `
    -Name $tgName `
    -Port 80 `
    -Protocol HTTP `
    -TargetType instance `
    -VpcId $config.vpc_id


# Add listener to ALB
New-ELB2Listener `
    -LoadBalancerArn $alb.LoadBalancerArn `
    -Port 80 `
    -Protocol HTTP `
    -DefaultAction @{"Type"="Forward"; "TargetGroupArn"=$tg.TargetGroupArn}


# Add Auto Scaling Policy (Target tracking)
Write-ASScalingPolicy `
    -AutoScalingGroupName $asgName `
    -PolicyType TargetTrackingScaling `
    -PolicyName cpu-usage-scale `
    -EstimatedInstanceWarmup 120 `
    -TargetTrackingConfiguration_TargetValue 60 `
    -PredefinedMetricSpecification_PredefinedMetricType ASGAverageCPUUtilization 

