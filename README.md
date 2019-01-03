# What is this
This repo is source control for my personal website (http://ethanmotion.com) and the deployment pipeline I've built.

# Website
In the website directory is all of the content required for my website.
The website is hosted in Amazon S3 ap-southeast-2 (Sydney) region.

# Deployment
Deployment is automated using Github as the source control, Github Release as the trigger, and AWS Lambda to push the files through to S3.

### Pre-production
When the 'prerelease' flag is selected when releasing from Github, AWS Lambda will send the Github files contained in /website to a S3 bucket called 
*dev.ethanmotion.com*. This deploys the pre-production website, which is restricted to my personal IP address.

### Production
When the 'prerelease' flag is _not_ selected when releasing from Github, AWS Lambda will send the Github files contained in /website to a S3 bucket called 
*ethanmotion.com*. This deploys the production website, which is open to the internet.