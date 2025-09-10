# Section 20 – Docker Alternatives and Ecosystem

## 20.1 Podman

Podman یک جایگزین open-source برای Docker است که بدون daemon کار می‌کند.

### ویژگی‌های Podman:
- **Rootless**: اجرا بدون root
- **Daemonless**: بدون daemon
- **Docker Compatible**: سازگار با Docker
- **Kubernetes Native**: پشتیبانی از Kubernetes
- **Security**: امنیت بالا

### نصب Podman:
```bash
# Ubuntu/Debian
sudo apt-get install podman

# CentOS/RHEL
sudo yum install podman

# macOS
brew install podman

# Windows
winget install RedHat.Podman
```

### دستورات Podman:
```bash
# اجرای کانتینر
podman run -d nginx

# ساخت ایمیج
podman build -t my-app .

# مشاهده کانتینرها
podman ps

# مشاهده ایمیج‌ها
podman images

# اجرای Pod
podman play kube pod.yaml
```

### مثال Podman Compose:
```yaml
# podman-compose.yml
version: '3.8'
services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./html:/usr/share/nginx/html

  db:
    image: postgres:13
    environment:
      POSTGRES_PASSWORD: password
    volumes:
      - postgres-data:/var/lib/postgresql/data

volumes:
  postgres-data:
```

### Podman vs Docker:
```bash
# Docker
docker run -d nginx
docker build -t my-app .
docker-compose up

# Podman
podman run -d nginx
podman build -t my-app .
podman-compose up
```

## 20.2 Containerd

Containerd یک runtime کانتینر سطح پایین است که توسط Docker استفاده می‌شود.

### ویژگی‌های Containerd:
- **Low-level**: سطح پایین
- **OCI Compatible**: سازگار با OCI
- **Plugin Architecture**: معماری پلاگین
- **Production Ready**: آماده production
- **CNCF Project**: پروژه CNCF

### نصب Containerd:
```bash
# Ubuntu/Debian
sudo apt-get install containerd

# CentOS/RHEL
sudo yum install containerd

# از GitHub
wget https://github.com/containerd/containerd/releases/download/v1.6.0/containerd-1.6.0-linux-amd64.tar.gz
tar xvf containerd-1.6.0-linux-amd64.tar.gz
sudo cp bin/* /usr/local/bin/
```

### پیکربندی Containerd:
```toml
# /etc/containerd/config.toml
version = 2
root = "/var/lib/containerd"
state = "/run/containerd"

[grpc]
  address = "/run/containerd/containerd.sock"
  uid = 0
  gid = 0

[plugins."io.containerd.grpc.v1.cri"]
  sandbox_image = "k8s.gcr.io/pause:3.6"
  [plugins."io.containerd.grpc.v1.cri".containerd]
    snapshotter = "overlayfs"
    [plugins."io.containerd.grpc.v1.cri".containerd.runtimes]
      [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc]
        runtime_type = "io.containerd.runc.v2"
```

### استفاده از Containerd:
```bash
# اجرای کانتینر
ctr run -d docker.io/library/nginx:alpine nginx

# مشاهده کانتینرها
ctr containers list

# مشاهده tasks
ctr tasks list

# توقف کانتینر
ctr tasks kill nginx
```

## 20.3 CRI-O

CRI-O یک runtime کانتینر مخصوص Kubernetes است.

### ویژگی‌های CRI-O:
- **Kubernetes Native**: مخصوص Kubernetes
- **OCI Compatible**: سازگار با OCI
- **Security Focused**: تمرکز بر امنیت
- **Lightweight**: سبک
- **Production Ready**: آماده production

### نصب CRI-O:
```bash
# Ubuntu/Debian
sudo apt-get install cri-o

# CentOS/RHEL
sudo yum install cri-o

# از GitHub
wget https://github.com/cri-o/cri-o/releases/download/v1.24.0/cri-o-1.24.0-linux-amd64.tar.gz
tar xvf cri-o-1.24.0-linux-amd64.tar.gz
sudo cp bin/* /usr/local/bin/
```

### پیکربندی CRI-O:
```toml
# /etc/crio/crio.conf
[crio]
  root = "/var/lib/containers/storage"
  runroot = "/var/run/containers/storage"
  storage_driver = "overlay"
  storage_option = ["overlay.mount_program=/usr/bin/fuse-overlayfs"]

[crio.runtime]
  runtime = "runc"
  runtime_untrusted_workload = ""
  default_workload_trust = "trusted"

[crio.image]
  default_transport = "docker://"
  pause_image = "k8s.gcr.io/pause:3.6"
```

### استفاده از CRI-O:
```bash
# اجرای Pod
crictl run pod.yaml container.yaml

# مشاهده Pods
crictl pods

# مشاهده Containers
crictl ps

# مشاهده Images
crictl images
```

## 20.4 LXC/LXD

LXC/LXD یک سیستم کانتینری‌سازی سطح سیستم عامل است.

### ویژگی‌های LXC/LXD:
- **System Containers**: کانتینرهای سیستم
- **Full OS**: سیستم عامل کامل
- **Lightweight VMs**: ماشین‌های مجازی سبک
- **Snapshots**: پشتیبان‌گیری
- **Clustering**: خوشه‌بندی

### نصب LXD:
```bash
# Ubuntu/Debian
sudo apt-get install lxd

# CentOS/RHEL
sudo yum install lxd

# از Snap
sudo snap install lxd
```

### استفاده از LXD:
```bash
# ایجاد container
lxc launch ubuntu:20.04 mycontainer

# مشاهده containers
lxc list

# ورود به container
lxc exec mycontainer -- /bin/bash

# توقف container
lxc stop mycontainer

# حذف container
lxc delete mycontainer
```

### مثال LXD Configuration:
```yaml
# lxd-config.yaml
config:
  core.https_address: '[::]:8443'
  core.trust_password: password
networks:
- name: lxdbr0
  type: bridge
  config:
    ipv4.address: 10.0.0.1/24
    ipv4.nat: "true"
profiles:
- name: default
  devices:
    root:
      path: /
      pool: default
      type: disk
```

## 20.5 rkt

rkt یک runtime کانتینر جایگزین Docker است.

### ویژگی‌های rkt:
- **Security First**: امنیت اول
- **Pod Native**: مخصوص Pod
- **ACIs**: Application Container Images
- **No Daemon**: بدون daemon
- **CNCF Project**: پروژه CNCF

### نصب rkt:
```bash
# Ubuntu/Debian
sudo apt-get install rkt

# CentOS/RHEL
sudo yum install rkt

# از GitHub
wget https://github.com/rkt/rkt/releases/download/v1.30.0/rkt-v1.30.0.tar.gz
tar xvf rkt-v1.30.0.tar.gz
sudo cp rkt-v1.30.0/rkt /usr/local/bin/
```

### استفاده از rkt:
```bash
# اجرای کانتینر
rkt run docker://nginx:alpine

# مشاهده pods
rkt list

# توقف pod
rkt stop <pod-id>

# حذف pod
rkt rm <pod-id>
```

### مثال rkt Pod:
```yaml
# pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
spec:
  containers:
  - name: nginx
    image: nginx:alpine
    ports:
    - containerPort: 80
```

## 20.6 Singularity

Singularity یک runtime کانتینر مخصوص HPC و scientific computing است.

### ویژگی‌های Singularity:
- **HPC Focused**: مخصوص HPC
- **Security**: امنیت بالا
- **Performance**: عملکرد بالا
- **Scientific Computing**: محاسبات علمی
- **No Root**: بدون root

### نصب Singularity:
```bash
# Ubuntu/Debian
sudo apt-get install singularity

# CentOS/RHEL
sudo yum install singularity

# از GitHub
wget https://github.com/sylabs/singularity/releases/download/v3.9.0/singularity-3.9.0.tar.gz
tar xvf singularity-3.9.0.tar.gz
cd singularity-3.9.0
./mconfig
make -C builddir
sudo make -C builddir install
```

### استفاده از Singularity:
```bash
# اجرای container
singularity run docker://nginx:alpine

# ساخت image
singularity build myapp.sif docker://myapp:latest

# اجرای image
singularity run myapp.sif

# مشاهده images
singularity cache list
```

### مثال Singularity Definition:
```singularity
# myapp.def
Bootstrap: docker
From: nginx:alpine

%post
    apk add --no-cache curl

%runscript
    exec nginx -g "daemon off;"
```

## 20.7 Docker vs Alternatives

مقایسه Docker با جایگزین‌هایش.

### مقایسه کلی:

| Feature | Docker | Podman | Containerd | CRI-O | LXC/LXD | rkt | Singularity |
|---------|--------|--------|------------|-------|---------|-----|-------------|
| Daemon | Yes | No | Yes | No | Yes | No | No |
| Root Required | Yes | No | Yes | Yes | Yes | No | No |
| Docker Compatible | Yes | Yes | Yes | Yes | No | No | Yes |
| Kubernetes | Yes | Yes | Yes | Yes | No | Yes | No |
| Security | Good | Excellent | Good | Excellent | Good | Excellent | Excellent |
| Performance | Good | Good | Excellent | Good | Good | Good | Excellent |
| HPC Support | No | No | No | No | No | No | Yes |

### انتخاب مناسب:

#### **برای Development:**
- **Docker**: آسان و محبوب
- **Podman**: امن‌تر و بدون daemon

#### **برای Production:**
- **Containerd**: سطح پایین و کارآمد
- **CRI-O**: مخصوص Kubernetes

#### **برای HPC:**
- **Singularity**: مخصوص محاسبات علمی

#### **برای System Containers:**
- **LXC/LXD**: کانتینرهای سیستم کامل

## 20.8 Container Runtime Comparison

مقایسه runtimeهای کانتینر.

### مقایسه Runtimeها:

#### **Docker:**
```bash
# مزایا
- آسان برای استفاده
- اکوسیستم بزرگ
- ابزارهای زیاد
- مستندات کامل

# معایب
- نیاز به daemon
- امنیت متوسط
- مصرف منابع بالا
```

#### **Podman:**
```bash
# مزایا
- بدون daemon
- امنیت بالا
- سازگار با Docker
- rootless

# معایب
- اکوسیستم کوچک‌تر
- ابزارهای کمتر
- مستندات محدود
```

#### **Containerd:**
```bash
# مزایا
- سطح پایین
- عملکرد بالا
- پلاگین‌های زیاد
- production ready

# معایب
- پیچیده
- نیاز به ابزارهای اضافی
- مستندات فنی
```

## 20.9 Migration Strategies

استراتژی‌های مهاجرت بین runtimeهای کانتینر.

### مهاجرت از Docker به Podman:

#### **1. نصب Podman:**
```bash
# Ubuntu/Debian
sudo apt-get install podman

# CentOS/RHEL
sudo yum install podman
```

#### **2. تنظیم alias:**
```bash
# در ~/.bashrc
alias docker=podman
alias docker-compose=podman-compose
```

#### **3. تست compatibility:**
```bash
# تست دستورات
podman run nginx
podman build -t my-app .
podman-compose up
```

### مهاجرت از Docker به Containerd:

#### **1. نصب Containerd:**
```bash
# Ubuntu/Debian
sudo apt-get install containerd

# CentOS/RHEL
sudo yum install containerd
```

#### **2. تنظیم CRI:**
```toml
# /etc/containerd/config.toml
[plugins."io.containerd.grpc.v1.cri"]
  sandbox_image = "k8s.gcr.io/pause:3.6"
```

#### **3. استفاده از crictl:**
```bash
# اجرای کانتینر
crictl run container.yaml pod.yaml

# مشاهده کانتینرها
crictl ps
```

## 20.10 Future of Containerization

آینده کانتینری‌سازی و تکنولوژی‌های نوظهور.

### روندهای آینده:

#### **1. WebAssembly (WASM):**
```dockerfile
# Dockerfile برای WASM
FROM wasm32-unknown-unknown
COPY target/wasm32-unknown-unknown/release/app.wasm /app.wasm
CMD ["/app.wasm"]
```

#### **2. Unikernels:**
```dockerfile
# Dockerfile برای Unikernel
FROM unikernel/nginx
COPY nginx.conf /etc/nginx/nginx.conf
CMD ["nginx", "-g", "daemon off;"]
```

#### **3. Serverless Containers:**
```yaml
# serverless.yml
functions:
  web:
    image: my-app:latest
    events:
      - http:
          path: /
          method: get
```

#### **4. Edge Computing:**
```yaml
# edge-deployment.yml
apiVersion: v1
kind: Pod
metadata:
  name: edge-app
spec:
  nodeSelector:
    kubernetes.io/hostname: edge-node
  containers:
  - name: app
    image: my-app:latest
```

### تکنولوژی‌های نوظهور:

#### **1. gVisor:**
```yaml
# gvisor-runtime.yml
apiVersion: v1
kind: Pod
spec:
  runtimeClassName: gvisor
  containers:
  - name: app
    image: my-app:latest
```

#### **2. Kata Containers:**
```yaml
# kata-runtime.yml
apiVersion: v1
kind: Pod
spec:
  runtimeClassName: kata
  containers:
  - name: app
    image: my-app:latest
```

#### **3. Firecracker:**
```yaml
# firecracker-runtime.yml
apiVersion: v1
kind: Pod
spec:
  runtimeClassName: firecracker
  containers:
  - name: app
    image: my-app:latest
```

### پیش‌بینی‌های آینده:

#### **1. Container Security:**
- امنیت بیشتر
- Zero-trust architecture
- Hardware-based security

#### **2. Performance:**
- عملکرد بهتر
- مصرف منابع کمتر
- سرعت بالاتر

#### **3. Developer Experience:**
- ابزارهای بهتر
- مستندات کامل‌تر
- پشتیبانی بهتر

#### **4. Cloud Integration:**
- ادغام بهتر با cloud
- serverless containers
- edge computing

این بخش شما را با تمام جایگزین‌های Docker و آینده کانتینری‌سازی آشنا می‌کند.