# What is this
This repo is source control for my personal website (http://ethanmotion.com) and the deployment pipeline I've built.

## Website
In the website directory is all of the content required for my website.
The website is hosted in Amazon S3 ap-southeast-2 (Sydney) region.

## Deployment
Deployment is automated using Github as source control, Github Release as the trigger, and AWS Lambda to push the files through to S3.
The Lambda function and required modules are stored in [deployment](https://github.com/ethan-motion/personal-website/tree/master/deployment).
Invoking the Lambda function is done via Amazon API Gateway, which is not currently restricted by API key (it's on my to-do list), however throttling has been enabled to minimise potential (though very unlikely) abuse. 

**Architecture diagram:** https://www.lucidchart.com/documents/view/914e6080-5b8f-4ff8-aa24-eda91f23b06a/0

### Pre-production
When the **prerelease** flag *is* selected when releasing from Github, AWS Lambda will send the Github files contained in [website](https://github.com/ethan-motion/personal-website/tree/master/website) to a S3 bucket called 
**dev.ethanmotion.com**. This deploys the pre-production website, which is restricted to my personal IP address.

### Production
When the **prerelease** flag *is not* selected when releasing from Github, AWS Lambda will send the Github files contained in [website](https://github.com/ethan-motion/personal-website/tree/master/website) to a S3 bucket called 
**ethanmotion.com**. This deploys the production website, which is open to the internet.
