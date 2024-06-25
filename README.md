## Blog Post

### Deployment Pipeline Steps
- TRIGGER
  - On push to main
- TEST
  - Setup Python virtual environment and install dependencies
  - Execute django tests against an sqlite3 database
  - Generate coverage report
- BUILD
  - Login to dockerhub
  - Prepare, build, and push image to dockerhub
- DEPLOY
  - SSH into a remote EC2 instance
  - Pull GitHub repo and checkout main branch
  - Execute docker-compose file, restarting if required
---
### Setup
- A host machine with docker, docker-compose, and git installed
- Requirements for docker container in Dockerfile and docker-compose.yaml
- Requirements for the Django app in requirements.txt
