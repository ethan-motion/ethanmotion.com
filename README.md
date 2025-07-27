# What's this?
This repo is source control for my personal website (http://ethanmotion.com), open to the internet.

## Architecture
![architecture](architecture_diagram.png)

## Deployment
Deployment is done locally at the moment, to both my dev environment, and production. Source can be either local, or what's in GitHub master branch.

### How to Deploy
1. Set AWS credentials in your environment.
2. Run `python deploy.py --env prod` to deploy to production.
3. Run `python deploy.py --env dev` to deploy to development.

### Local Development
1. Open `website/index.html` in your browser.
2. Edit files in `website/` and refresh to see changes.

### Development
**dev.ethanmotion.com**. This is my pre-prod website. Access is restricted using a CloudFront distribution with an attached Lambda@Edge Lambda, requiring authentication to pass through.

### Production
**ethanmotion.com** and **www.ethanmotion.com** both route to my ethanmotion.com bucket.
