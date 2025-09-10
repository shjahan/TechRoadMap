# Section 16 – Docker DevOps and CI/CD

## 16.1 CI/CD Pipeline Design

طراحی pipeline CI/CD برای اپلیکیشن‌های Docker.

### مراحل CI/CD Pipeline:
1. **Source Control**: کنترل نسخه
2. **Build**: ساخت ایمیج
3. **Test**: تست کردن
4. **Security Scan**: اسکن امنیتی
5. **Deploy**: استقرار
6. **Monitor**: نظارت

### مثال Pipeline:
```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Build and test
      run: |
        docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit
        docker-compose -f docker-compose.test.yml down -v
    
    - name: Run tests
      run: |
        docker-compose -f docker-compose.test.yml run --rm test npm test
        docker-compose -f docker-compose.test.yml run --rm test npm run test:integration

  build:
    needs: test
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Build Docker image
      run: |
        docker build -t my-app:${{ github.sha }} .
        docker build -t my-app:latest .
    
    - name: Push to registry
      run: |
        echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
        docker push my-app:${{ github.sha }}
        docker push my-app:latest

  deploy:
    needs: build
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to production
      run: |
        docker-compose -f docker-compose.prod.yml up -d
```

## 16.2 Jenkins with Docker

استفاده از Jenkins با Docker برای CI/CD.

### Jenkins Setup:
```yaml
version: '3.8'
services:
  jenkins:
    image: jenkins/jenkins:lts
    ports:
      - "8080:8080"
      - "50000:50000"
    volumes:
      - jenkins-data:/var/jenkins_home
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - DOCKER_HOST=unix:///var/run/docker.sock

  docker-dind:
    image: docker:dind
    privileged: true
    volumes:
      - docker-data:/var/lib/docker

volumes:
  jenkins-data:
  docker-data:
```

### Jenkinsfile:
```groovy
pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build') {
            steps {
                sh 'docker build -t my-app:${BUILD_NUMBER} .'
                sh 'docker build -t my-app:latest .'
            }
        }
        
        stage('Test') {
            steps {
                sh 'docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit'
                sh 'docker-compose -f docker-compose.test.yml down -v'
            }
        }
        
        stage('Security Scan') {
            steps {
                sh 'docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image my-app:${BUILD_NUMBER}'
            }
        }
        
        stage('Deploy') {
            steps {
                sh 'docker-compose -f docker-compose.prod.yml up -d'
            }
        }
    }
    
    post {
        always {
            sh 'docker system prune -f'
        }
    }
}
```

## 16.3 GitLab CI/CD

استفاده از GitLab CI/CD با Docker.

### GitLab CI Configuration:
```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - security
  - deploy

variables:
  DOCKER_DRIVER: overlay2
  DOCKER_TLS_CERTDIR: "/certs"

services:
  - docker:dind

test:
  stage: test
  script:
    - docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit
    - docker-compose -f docker-compose.test.yml down -v
  only:
    - merge_requests
    - main

build:
  stage: build
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker build -t $CI_REGISTRY_IMAGE:latest .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
    - docker push $CI_REGISTRY_IMAGE:latest
  only:
    - main

security:
  stage: security
  script:
    - docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  only:
    - main

deploy:
  stage: deploy
  script:
    - docker-compose -f docker-compose.prod.yml up -d
  only:
    - main
```

### GitLab Runner Configuration:
```toml
# config.toml
[[runners]]
  name = "docker-runner"
  url = "https://gitlab.com/"
  token = "your-token"
  executor = "docker"
  [runners.docker]
    tls_verify = false
    image = "docker:latest"
    privileged = true
    disable_cache = false
    volumes = ["/var/run/docker.sock:/var/run/docker.sock", "/cache"]
  [runners.cache]
    Insecure = false
```

## 16.4 GitHub Actions

استفاده از GitHub Actions با Docker.

### GitHub Actions Workflow:
```yaml
# .github/workflows/docker.yml
name: Docker CI/CD

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout
      uses: actions/checkout@v3
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Build and test
      run: |
        docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit
        docker-compose -f docker-compose.test.yml down -v

  build:
    needs: test
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    
    steps:
    - name: Checkout
      uses: actions/checkout@v3
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Log in to Container Registry
      uses: docker/login@v2
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
    
    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v4
      with:
        images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
        tags: |
          type=ref,event=branch
          type=ref,event=pr
          type=sha,prefix={{branch}}-
          type=raw,value=latest,enable={{is_default_branch}}
    
    - name: Build and push Docker image
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}

  security:
    needs: build
    runs-on: ubuntu-latest
    
    steps:
    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
        format: 'sarif'
        output: 'trivy-results.sarif'
    
    - name: Upload Trivy scan results to GitHub Security tab
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'trivy-results.sarif'

  deploy:
    needs: [build, security]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - name: Checkout
      uses: actions/checkout@v3
    
    - name: Deploy to production
      run: |
        docker-compose -f docker-compose.prod.yml up -d
```

## 16.5 Azure DevOps

استفاده از Azure DevOps با Docker.

### Azure DevOps Pipeline:
```yaml
# azure-pipelines.yml
trigger:
- main
- develop

pool:
  vmImage: 'ubuntu-latest'

variables:
  dockerRegistryServiceConnection: 'docker-registry-connection'
  imageRepository: 'my-app'
  containerRegistry: 'myregistry.azurecr.io'
  dockerfilePath: '$(Build.SourcesDirectory)/Dockerfile'
  tag: '$(Build.BuildId)'

stages:
- stage: Build
  displayName: Build and push stage
  jobs:
  - job: Build
    displayName: Build
    steps:
    - task: Docker@2
      displayName: Build and push an image to container registry
      inputs:
        command: buildAndPush
        repository: $(imageRepository)
        dockerfile: $(dockerfilePath)
        containerRegistry: $(dockerRegistryServiceConnection)
        tags: |
          $(tag)
          latest

- stage: Test
  displayName: Test stage
  dependsOn: Build
  jobs:
  - job: Test
    displayName: Test
    steps:
    - task: DockerCompose@0
      displayName: Run tests
      inputs:
        action: Run services
        dockerComposeFile: 'docker-compose.test.yml'
        detached: false
        abortOnContainerExit: true

- stage: Deploy
  displayName: Deploy stage
  dependsOn: Test
  jobs:
  - deployment: Deploy
    displayName: Deploy
    environment: 'production'
    strategy:
      runOnce:
        deploy:
          steps:
          - task: DockerCompose@0
            displayName: Deploy to production
            inputs:
              action: Run services
              dockerComposeFile: 'docker-compose.prod.yml'
              detached: true
```

## 16.6 Build Optimization

بهینه‌سازی فرآیند build برای بهبود عملکرد.

### Multi-stage Build:
```dockerfile
# Build stage
FROM node:16-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Production stage
FROM node:16-alpine
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

### Build Cache Optimization:
```yaml
# .github/workflows/docker.yml
name: Docker Build

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout
      uses: actions/checkout@v3
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Build with cache
      uses: docker/build-push-action@v4
      with:
        context: .
        push: false
        tags: my-app:latest
        cache-from: type=gha
        cache-to: type=gha,mode=max
```

### Parallel Builds:
```yaml
version: '3.8'
services:
  web:
    build:
      context: .
      dockerfile: Dockerfile.web
    ports:
      - "3000:3000"

  api:
    build:
      context: .
      dockerfile: Dockerfile.api
    ports:
      - "8000:8000"

  worker:
    build:
      context: .
      dockerfile: Dockerfile.worker
```

## 16.7 Automated Testing

تست خودکار اپلیکیشن‌های Docker.

### Test Configuration:
```yaml
# docker-compose.test.yml
version: '3.8'
services:
  test:
    build: .
    volumes:
      - ./src:/app/src
      - ./tests:/app/tests
      - /app/node_modules
    environment:
      - NODE_ENV=test
    command: npm test

  test-db:
    image: postgres:13
    environment:
      POSTGRES_DB: myapp_test
      POSTGRES_USER: test
      POSTGRES_PASSWORD: testpassword
    volumes:
      - postgres-test-data:/var/lib/postgresql/data

  test-redis:
    image: redis:alpine

volumes:
  postgres-test-data:
```

### Test Scripts:
```bash
#!/bin/bash
# test.sh

echo "Running automated tests..."

# Unit tests
echo "1. Running unit tests..."
docker-compose -f docker-compose.test.yml run --rm test npm test

# Integration tests
echo "2. Running integration tests..."
docker-compose -f docker-compose.test.yml run --rm test npm run test:integration

# E2E tests
echo "3. Running E2E tests..."
docker-compose -f docker-compose.test.yml run --rm test npm run test:e2e

# Cleanup
echo "4. Cleaning up..."
docker-compose -f docker-compose.test.yml down -v

echo "Tests completed!"
```

## 16.8 Security Scanning

اسکن امنیتی ایمیج‌های Docker.

### Trivy Security Scanner:
```yaml
# .github/workflows/security.yml
name: Security Scan

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  security:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout
      uses: actions/checkout@v3
    
    - name: Build Docker image
      run: docker build -t my-app:latest .
    
    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: 'my-app:latest'
        format: 'sarif'
        output: 'trivy-results.sarif'
    
    - name: Upload Trivy scan results to GitHub Security tab
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'trivy-results.sarif'
```

### Snyk Security Scanner:
```yaml
# .github/workflows/snyk.yml
name: Snyk Security Scan

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  security:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout
      uses: actions/checkout@v3
    
    - name: Run Snyk to check for vulnerabilities
      uses: snyk/actions/docker@master
      env:
        SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
      with:
        image: my-app:latest
        args: --severity-threshold=high
```

## 16.9 Deployment Strategies

استراتژی‌های استقرار اپلیکیشن‌های Docker.

### Blue-Green Deployment:
```yaml
# docker-compose.blue.yml
version: '3.8'
services:
  web:
    image: my-app:blue
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production

# docker-compose.green.yml
version: '3.8'
services:
  web:
    image: my-app:green
    ports:
      - "3001:3000"
    environment:
      - NODE_ENV=production
```

### Rolling Deployment:
```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  web:
    image: my-app:latest
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
        failure_action: rollback
        monitor: 60s
      rollback_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
```

### Canary Deployment:
```yaml
# docker-compose.canary.yml
version: '3.8'
services:
  web:
    image: my-app:canary
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
    deploy:
      replicas: 1
      labels:
        - "traefik.http.routers.web.rule=Host(`canary.example.com`)"

  web-stable:
    image: my-app:stable
    ports:
      - "3001:3000"
    environment:
      - NODE_ENV=production
    deploy:
      replicas: 2
      labels:
        - "traefik.http.routers.web-stable.rule=Host(`example.com`)"
```

## 16.10 Infrastructure as Code

مدیریت زیرساخت با Infrastructure as Code.

### Terraform Configuration:
```hcl
# main.tf
provider "docker" {
  host = "unix:///var/run/docker.sock"
}

resource "docker_image" "web" {
  name = "my-app:latest"
  build {
    context = "."
    tag     = ["my-app:latest"]
  }
}

resource "docker_container" "web" {
  image = docker_image.web.latest
  name  = "web"
  ports {
    internal = 3000
    external = 3000
  }
  env = [
    "NODE_ENV=production"
  ]
}
```

### Ansible Playbook:
```yaml
# playbook.yml
- hosts: docker_hosts
  become: yes
  tasks:
    - name: Install Docker
      apt:
        name: docker.io
        state: present
    
    - name: Start Docker service
      systemd:
        name: docker
        state: started
        enabled: yes
    
    - name: Pull Docker image
      docker_image:
        name: my-app:latest
        source: pull
    
    - name: Run Docker container
      docker_container:
        name: web
        image: my-app:latest
        state: started
        ports:
          - "3000:3000"
        env:
          NODE_ENV: production
        restart_policy: unless-stopped
```

### Pulumi Configuration:
```typescript
// index.ts
import * as docker from "@pulumi/docker";

const image = new docker.Image("web", {
    imageName: "my-app:latest",
    build: {
        context: ".",
    },
});

const container = new docker.Container("web", {
    image: image.imageName,
    ports: [{
        internal: 3000,
        external: 3000,
    }],
    envs: ["NODE_ENV=production"],
    restart: "unless-stopped",
});
```

این بخش شما را با تمام جنبه‌های DevOps و CI/CD با Docker آشنا می‌کند.