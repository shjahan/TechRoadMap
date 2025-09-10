# Section 17 – Advanced Docker Features

## 17.1 Docker BuildKit

Docker BuildKit موتور build پیشرفته‌ای است که عملکرد و قابلیت‌های بیشتری ارائه می‌دهد.

### ویژگی‌های BuildKit:
- **Parallel Builds**: ساخت موازی
- **Cache Optimization**: بهینه‌سازی کش
- **Multi-platform Support**: پشتیبانی از چندین پلتفرم
- **Advanced Caching**: کش پیشرفته
- **Secret Management**: مدیریت secrets

### فعال‌سازی BuildKit:
```bash
# فعال‌سازی BuildKit
export DOCKER_BUILDKIT=1

# یا در docker-compose
export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1
```

### BuildKit Dockerfile:
```dockerfile
# syntax=docker/dockerfile:1
FROM node:16-alpine

# Build stage
FROM node:16-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci --only=production

# Production stage
FROM node:16-alpine
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

### BuildKit با Docker Compose:
```yaml
version: '3.8'
services:
  web:
    build:
      context: .
      dockerfile: Dockerfile
      cache_from:
        - my-app:latest
      cache_to:
        - my-app:latest
    ports:
      - "3000:3000"
```

## 17.2 Multi-platform Builds

ساخت ایمیج‌ها برای چندین پلتفرم.

### Multi-platform Build:
```bash
# ساخت برای چندین پلتفرم
docker buildx build --platform linux/amd64,linux/arm64 -t my-app:latest .

# ساخت و push برای چندین پلتفرم
docker buildx build --platform linux/amd64,linux/arm64 -t my-app:latest --push .
```

### Buildx Builder:
```bash
# ایجاد builder جدید
docker buildx create --name multiarch --driver docker-container --use

# بررسی builder
docker buildx ls

# ساخت با builder جدید
docker buildx build --platform linux/amd64,linux/arm64 -t my-app:latest .
```

### Multi-platform Dockerfile:
```dockerfile
# syntax=docker/dockerfile:1
FROM --platform=$BUILDPLATFORM node:16-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM --platform=$TARGETPLATFORM node:16-alpine
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

## 17.3 Build Cache Optimization

بهینه‌سازی کش build برای بهبود عملکرد.

### Cache Mounts:
```dockerfile
# syntax=docker/dockerfile:1
FROM node:16-alpine

WORKDIR /app

# Cache mount برای npm
COPY package*.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci --only=production

# Cache mount برای apt
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && apt-get install -y curl

COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

### Registry Cache:
```yaml
# docker-compose.yml
version: '3.8'
services:
  web:
    build:
      context: .
      cache_from:
        - my-app:latest
        - my-app:build
      cache_to:
        - my-app:build
    ports:
      - "3000:3000"
```

### BuildKit Cache:
```bash
# ساخت با cache
docker buildx build --cache-from type=local,src=/tmp/.buildx-cache \
  --cache-to type=local,dest=/tmp/.buildx-cache-new \
  -t my-app:latest .

# استفاده از registry cache
docker buildx build --cache-from type=registry,ref=my-app:build \
  --cache-to type=registry,ref=my-app:build,mode=max \
  -t my-app:latest .
```

## 17.4 Docker Content Trust

Docker Content Trust برای امنیت ایمیج‌ها.

### فعال‌سازی Content Trust:
```bash
# فعال‌سازی Content Trust
export DOCKER_CONTENT_TRUST=1

# یا برای یک دستور خاص
DOCKER_CONTENT_TRUST=1 docker push my-app:latest
```

### Signing Images:
```bash
# Sign کردن ایمیج
docker trust key generate my-key
docker trust signer add --key my-key.pub my-key my-app:latest
docker trust sign my-app:latest
```

### Content Trust Configuration:
```json
{
  "trust": {
    "default": {
      "enabled": true,
      "signing": {
        "enabled": true,
        "key": "my-key"
      }
    }
  }
}
```

## 17.5 Docker Secrets

مدیریت secrets در Docker.

### Docker Secrets:
```yaml
# docker-compose.yml
version: '3.8'
services:
  web:
    image: my-app:latest
    secrets:
      - db_password
      - api_key
    environment:
      - DB_PASSWORD_FILE=/run/secrets/db_password
      - API_KEY_FILE=/run/secrets/api_key

secrets:
  db_password:
    file: ./secrets/db_password.txt
  api_key:
    file: ./secrets/api_key.txt
```

### Docker Swarm Secrets:
```bash
# ایجاد secret
echo "mysecretpassword" | docker secret create db_password -

# استفاده از secret
docker service create \
  --name web \
  --secret db_password \
  my-app:latest
```

### Secrets در Dockerfile:
```dockerfile
# syntax=docker/dockerfile:1
FROM node:16-alpine

# Mount secret
RUN --mount=type=secret,id=db_password \
    echo "DB_PASSWORD=$(cat /run/secrets/db_password)" >> .env

COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

## 17.6 Docker Configs

مدیریت configuration files در Docker.

### Docker Configs:
```yaml
# docker-compose.yml
version: '3.8'
services:
  web:
    image: nginx:alpine
    configs:
      - nginx_config
      - ssl_cert
    ports:
      - "80:80"
      - "443:443"

configs:
  nginx_config:
    file: ./nginx.conf
  ssl_cert:
    file: ./ssl/cert.pem
```

### Docker Swarm Configs:
```bash
# ایجاد config
docker config create nginx_config nginx.conf

# استفاده از config
docker service create \
  --name web \
  --config nginx_config \
  nginx:alpine
```

### Configs در Dockerfile:
```dockerfile
# syntax=docker/dockerfile:1
FROM nginx:alpine

# Copy config
COPY --from=nginx_config /etc/nginx/nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## 17.7 Docker Plugins

پلاگین‌های Docker برای گسترش قابلیت‌ها.

### Plugin Management:
```bash
# لیست پلاگین‌ها
docker plugin ls

# نصب پلاگین
docker plugin install store/weaveworks/net-plugin:latest

# فعال‌سازی پلاگین
docker plugin enable weaveworks/net-plugin:latest

# غیرفعال‌سازی پلاگین
docker plugin disable weaveworks/net-plugin:latest
```

### Custom Plugin:
```go
// main.go
package main

import (
    "github.com/docker/go-plugins-helpers/volume"
)

type MyVolumeDriver struct{}

func (d *MyVolumeDriver) Create(req *volume.CreateRequest) error {
    // Create volume logic
    return nil
}

func (d *MyVolumeDriver) Mount(req *volume.MountRequest) (*volume.MountResponse, error) {
    // Mount volume logic
    return &volume.MountResponse{Mountpoint: "/mnt/volume"}, nil
}

func main() {
    driver := &MyVolumeDriver{}
    handler := volume.NewHandler(driver)
    handler.ServeUnix("my-volume-driver", 0)
}
```

## 17.8 Custom Buildx Drivers

ایجاد driverهای سفارشی برای BuildKit.

### Custom Driver:
```go
// driver.go
package main

import (
    "context"
    "github.com/moby/buildkit/client/llb"
)

type CustomDriver struct{}

func (d *CustomDriver) Build(ctx context.Context, req *llb.Definition) (*llb.Result, error) {
    // Custom build logic
    return &llb.Result{}, nil
}

func main() {
    driver := &CustomDriver{}
    // Register driver
}
```

### Buildx Driver Configuration:
```yaml
# buildx-config.yml
version: "1.0"
drivers:
  - name: custom-driver
    type: custom
    config:
      endpoint: "unix:///var/run/custom-driver.sock"
```

## 17.9 Advanced Networking

شبکه‌بندی پیشرفته در Docker.

### Custom Network Drivers:
```yaml
# docker-compose.yml
version: '3.8'
services:
  web:
    image: nginx:alpine
    networks:
      - custom-network
    ports:
      - "80:80"

networks:
  custom-network:
    driver: custom
    driver_opts:
      type: bridge
      bridge: custom-bridge
      subnet: 172.20.0.0/16
      gateway: 172.20.0.1
```

### Network Policies:
```yaml
# network-policy.yml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: web-network-policy
spec:
  podSelector:
    matchLabels:
      app: web
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 80
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: database
    ports:
    - protocol: TCP
      port: 5432
```

## 17.10 Container Runtime Interface

رابط runtime کانتینرها.

### CRI Configuration:
```yaml
# cri-config.yml
version: "1.0"
runtime:
  name: containerd
  endpoint: "unix:///var/run/containerd/containerd.sock"
  timeout: 30s
  debug: false
```

### Custom Runtime:
```go
// runtime.go
package main

import (
    "context"
    "github.com/containerd/containerd"
)

type CustomRuntime struct {
    client *containerd.Client
}

func (r *CustomRuntime) CreateContainer(ctx context.Context, req *CreateContainerRequest) (*CreateContainerResponse, error) {
    // Custom container creation logic
    return &CreateContainerResponse{}, nil
}

func (r *CustomRuntime) StartContainer(ctx context.Context, req *StartContainerRequest) (*StartContainerResponse, error) {
    // Custom container start logic
    return &StartContainerResponse{}, nil
}

func main() {
    runtime := &CustomRuntime{}
    // Register runtime
}
```

### Runtime Configuration:
```json
{
  "runtimes": {
    "custom": {
      "path": "/usr/local/bin/custom-runtime",
      "runtimeArgs": ["--debug"]
    }
  }
}
```

این بخش شما را با تمام ویژگی‌های پیشرفته Docker آشنا می‌کند.