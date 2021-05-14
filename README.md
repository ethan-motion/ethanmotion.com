# What's this?
This repo is source control for my personal website (http://ethanmotion.com), open to the internet.

## Architecture
![architecture](architecture_diagram.png)

## Deployment
Deployment is done locally at the moment, to both my dev environment, and production. Source can be either local, or what's in GitHub master branch.

### Development
**dev.ethanmotion.com**. This is my pre-prod website. Access is restricted using a CloudFront distribution with an attached Lambda@Edge Lambda, requiring authentication to pass through.

### Production
**ethanmotion.com** and **www.ethanmotion.com** both route to my ethanmotion.com bucket.
