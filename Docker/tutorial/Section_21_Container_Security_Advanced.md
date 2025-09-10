# Section 21 – Container Security Advanced

## 21.1 Container Runtime Security

امنیت runtime کانتینرها برای محافظت از سیستم‌های production.

### اصول Runtime Security:

#### **1. User Namespaces:**
```yaml
# docker-compose.yml
version: '3.8'
services:
  web:
    image: nginx:alpine
    user: "1000:1000"
    userns_mode: "host"
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
```

#### **2. Seccomp Profiles:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    security_opt:
      - seccomp=./seccomp-profile.json
```

### فایل seccomp-profile.json:
```json
{
  "defaultAction": "SCMP_ACT_ERRNO",
  "architectures": [
    "SCMP_ARCH_X86_64",
    "SCMP_ARCH_X86",
    "SCMP_ARCH_X32"
  ],
  "syscalls": [
    {
      "names": [
        "accept",
        "accept4",
        "access",
        "alarm",
        "bind",
        "brk",
        "clock_getres",
        "clock_gettime",
        "close",
        "connect",
        "dup",
        "dup2",
        "dup3",
        "epoll_create",
        "epoll_create1",
        "epoll_ctl",
        "epoll_pwait",
        "epoll_wait",
        "eventfd",
        "eventfd2",
        "exit",
        "exit_group",
        "fchdir",
        "fchmod",
        "fchown",
        "fchown32",
        "fcntl",
        "fcntl64",
        "fdatasync",
        "fgetxattr",
        "flistxattr",
        "flock",
        "fork",
        "fstat",
        "fstat64",
        "fstatat64",
        "fstatfs",
        "fstatfs64",
        "fsync",
        "ftruncate",
        "ftruncate64",
        "futex",
        "getcwd",
        "getdents",
        "getdents64",
        "getegid",
        "getegid32",
        "geteuid",
        "geteuid32",
        "getgid",
        "getgid32",
        "getgroups",
        "getgroups32",
        "getpeername",
        "getpgid",
        "getpgrp",
        "getpid",
        "getppid",
        "getpriority",
        "getrandom",
        "getresgid",
        "getresgid32",
        "getresuid",
        "getresuid32",
        "getrlimit",
        "get_robust_list",
        "getrusage",
        "getsid",
        "getsockname",
        "getsockopt",
        "get_thread_area",
        "gettid",
        "gettimeofday",
        "getuid",
        "getuid32",
        "getxattr",
        "inotify_add_watch",
        "inotify_init",
        "inotify_init1",
        "inotify_rm_watch",
        "io_cancel",
        "ioctl",
        "io_destroy",
        "io_getevents",
        "ioprio_get",
        "ioprio_set",
        "io_setup",
        "io_submit",
        "ipc",
        "kill",
        "lchown",
        "lchown32",
        "lgetxattr",
        "link",
        "linkat",
        "listen",
        "listxattr",
        "llistxattr",
        "lremovexattr",
        "lseek",
        "lsetxattr",
        "lstat",
        "lstat64",
        "madvise",
        "mincore",
        "mkdir",
        "mkdirat",
        "mknod",
        "mknodat",
        "mlock",
        "mlockall",
        "mmap",
        "mmap2",
        "mprotect",
        "mq_getsetattr",
        "mq_notify",
        "mq_open",
        "mq_timedreceive",
        "mq_timedsend",
        "mq_unlink",
        "mremap",
        "msgctl",
        "msgget",
        "msgrcv",
        "msgsnd",
        "msync",
        "munlock",
        "munlockall",
        "munmap",
        "nanosleep",
        "newfstatat",
        "_newselect",
        "open",
        "openat",
        "pause",
        "pipe",
        "pipe2",
        "poll",
        "ppoll",
        "prctl",
        "pread64",
        "preadv",
        "prlimit64",
        "pselect6",
        "ptrace",
        "pwrite64",
        "pwritev",
        "read",
        "readahead",
        "readlink",
        "readlinkat",
        "readv",
        "recv",
        "recvfrom",
        "recvmmsg",
        "recvmsg",
        "remap_file_pages",
        "removexattr",
        "rename",
        "renameat",
        "renameat2",
        "restart_syscall",
        "rmdir",
        "rt_sigaction",
        "rt_sigpending",
        "rt_sigprocmask",
        "rt_sigqueueinfo",
        "rt_sigreturn",
        "rt_sigsuspend",
        "rt_sigtimedwait",
        "rt_tgsigqueueinfo",
        "sched_get_priority_max",
        "sched_get_priority_min",
        "sched_getaffinity",
        "sched_getparam",
        "sched_getscheduler",
        "sched_rr_get_interval",
        "sched_setaffinity",
        "sched_setparam",
        "sched_setscheduler",
        "sched_yield",
        "seccomp",
        "select",
        "send",
        "sendfile",
        "sendfile64",
        "sendmmsg",
        "sendmsg",
        "sendto",
        "setfsgid",
        "setfsgid32",
        "setfsuid",
        "setfsuid32",
        "setgid",
        "setgid32",
        "setgroups",
        "setgroups32",
        "setitimer",
        "setpgid",
        "setpriority",
        "setregid",
        "setregid32",
        "setresgid",
        "setresgid32",
        "setresuid",
        "setresuid32",
        "setreuid",
        "setreuid32",
        "setrlimit",
        "set_robust_list",
        "setsid",
        "setsockopt",
        "set_thread_area",
        "set_tid_address",
        "setuid",
        "setuid32",
        "setxattr",
        "shmat",
        "shmctl",
        "shmdt",
        "shmget",
        "shutdown",
        "sigaltstack",
        "signalfd",
        "signalfd4",
        "sigreturn",
        "socket",
        "socketcall",
        "socketpair",
        "splice",
        "stat",
        "stat64",
        "statfs",
        "statfs64",
        "symlink",
        "symlinkat",
        "sync",
        "sync_file_range",
        "syncfs",
        "sysinfo",
        "syslog",
        "tee",
        "tgkill",
        "time",
        "timer_create",
        "timer_delete",
        "timer_getoverrun",
        "timer_gettime",
        "timer_settime",
        "timerfd_create",
        "timerfd_gettime",
        "timerfd_settime",
        "times",
        "tkill",
        "truncate",
        "truncate64",
        "ugetrlimit",
        "umask",
        "uname",
        "unlink",
        "unlinkat",
        "utime",
        "utimensat",
        "utimes",
        "vfork",
        "vmsplice",
        "wait4",
        "waitid",
        "waitpid",
        "write",
        "writev"
      ],
      "action": "SCMP_ACT_ALLOW"
    }
  ]
}
```

#### **3. AppArmor Profiles:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    security_opt:
      - apparmor:docker-nginx
```

### فایل AppArmor Profile:
```bash
# /etc/apparmor.d/docker-nginx
#include <tunables/global>

profile docker-nginx flags=(attach_disconnected,mediate_deleted) {
  #include <abstractions/base>

  # Allow read access to nginx files
  /usr/share/nginx/html/** r,
  /etc/nginx/** r,
  /var/log/nginx/** rw,

  # Deny write access to system files
  deny /etc/** w,
  deny /usr/** w,
  deny /var/** w,

  # Allow network access
  network,
}
```

## 21.2 Image Vulnerability Management

مدیریت آسیب‌پذیری‌های ایمیج‌ها.

### اسکن امنیتی:

#### **1. Trivy Scanner:**
```bash
# اسکن ایمیج
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image nginx:alpine

# اسکن با خروجی JSON
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image --format json nginx:alpine

# اسکن با خروجی SARIF
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image --format sarif nginx:alpine
```

#### **2. Clair Scanner:**
```yaml
# clair-scanner.yml
version: '3.8'
services:
  clair:
    image: quay.io/coreos/clair:latest
    ports:
      - "6060:6060"
    volumes:
      - ./clair-config.yaml:/etc/clair/config.yaml:ro

  clair-scanner:
    image: arminc/clair-scanner:latest
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
    command: clair-scanner --clair=http://clair:6060 nginx:alpine
    depends_on:
      - clair
```

#### **3. Snyk Scanner:**
```bash
# اسکن با Snyk
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  snyk/snyk:docker nginx:alpine

# اسکن با API key
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  -e SNYK_TOKEN=your-token \
  snyk/snyk:docker nginx:alpine
```

### Automated Security Scanning:
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

## 21.3 Runtime Security Monitoring

نظارت بر امنیت runtime کانتینرها.

### ابزارهای Monitoring:

#### **1. Falco:**
```yaml
# falco.yml
version: '3.8'
services:
  falco:
    image: falcosecurity/falco:latest
    privileged: true
    volumes:
      - /var/run/docker.sock:/host/var/run/docker.sock:ro
      - /dev:/host/dev:ro
      - /proc:/host/proc:ro
      - /boot:/host/boot:ro
      - /lib/modules:/host/lib/modules:ro
      - /usr:/host/usr:ro
      - /etc:/host/etc:ro
    environment:
      - FALCO_GRPC_ENABLED=true
      - FALCO_GRPC_BIND_ADDRESS=0.0.0.0:5060
    ports:
      - "5060:5060"
```

#### **2. Sysdig:**
```yaml
# sysdig.yml
version: '3.8'
services:
  sysdig:
    image: sysdig/agent:latest
    privileged: true
    volumes:
      - /var/run/docker.sock:/host/var/run/docker.sock:ro
      - /dev:/host/dev:ro
      - /proc:/host/proc:ro
      - /boot:/host/boot:ro
      - /lib/modules:/host/lib/modules:ro
      - /usr:/host/usr:ro
      - /etc:/host/etc:ro
    environment:
      - SYSDIG_ACCESS_KEY=your-access-key
      - SYSDIG_COLLECTOR=collector.sysdigcloud.com
```

#### **3. Twistlock:**
```yaml
# twistlock.yml
version: '3.8'
services:
  twistlock:
    image: twistlock/defender:latest
    privileged: true
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - /var/lib/docker:/var/lib/docker:ro
    environment:
      - TWISTLOCK_CONSOLE_ADDRESS=your-console-address
      - TWISTLOCK_DEFENDER_TOKEN=your-token
```

### Security Rules:
```yaml
# falco-rules.yml
- rule: Write to sensitive file
  desc: Detect writes to sensitive files
  condition: >
    open_write and
    (fd.name contains "/etc/passwd" or
     fd.name contains "/etc/shadow" or
     fd.name contains "/etc/sudoers")
  output: >
    Sensitive file written to (user=%user.name
    command=%proc.cmdline file=%fd.name)
  priority: WARNING

- rule: Container escape
  desc: Detect container escape attempts
  condition: >
    spawned_process and
    container and
    (proc.name in (shell_binaries) or
     proc.name in (system_binaries))
  output: >
    Container escape attempt (user=%user.name
    command=%proc.cmdline container=%container.name)
  priority: CRITICAL
```

## 21.4 Network Segmentation

جداسازی شبکه برای امنیت کانتینرها.

### Network Policies:

#### **1. Kubernetes Network Policy:**
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

#### **2. Docker Network Segmentation:**
```yaml
# docker-compose.yml
version: '3.8'
services:
  frontend:
    image: nginx:alpine
    networks:
      - frontend
    ports:
      - "80:80"

  backend:
    image: my-app:latest
    networks:
      - frontend
      - backend

  database:
    image: postgres:13
    networks:
      - backend
    environment:
      POSTGRES_PASSWORD: password

networks:
  frontend:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
  backend:
    driver: bridge
    internal: true
    ipam:
      config:
        - subnet: 172.21.0.0/16
```

#### **3. Istio Service Mesh:**
```yaml
# istio-policy.yml
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: web-policy
spec:
  selector:
    matchLabels:
      app: web
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/default/sa/frontend"]
    to:
    - operation:
        methods: ["GET", "POST"]
        paths: ["/api/*"]
```

## 21.5 Secrets Management

مدیریت secrets در کانتینرها.

### ابزارهای Secrets Management:

#### **1. Docker Secrets:**
```yaml
# docker-compose.yml
version: '3.8'
services:
  web:
    image: nginx:alpine
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

#### **2. HashiCorp Vault:**
```yaml
# vault.yml
version: '3.8'
services:
  vault:
    image: vault:latest
    ports:
      - "8200:8200"
    environment:
      - VAULT_DEV_ROOT_TOKEN_ID=root
      - VAULT_DEV_LISTEN_ADDRESS=0.0.0.0:8200
    cap_add:
      - IPC_LOCK

  web:
    image: nginx:alpine
    environment:
      - VAULT_ADDR=http://vault:8200
      - VAULT_TOKEN=root
    depends_on:
      - vault
```

#### **3. Kubernetes Secrets:**
```yaml
# k8s-secrets.yml
apiVersion: v1
kind: Secret
metadata:
  name: web-secrets
type: Opaque
data:
  db-password: cGFzc3dvcmQ=
  api-key: YWJjZGVmZ2g=

---
apiVersion: v1
kind: Pod
metadata:
  name: web
spec:
  containers:
  - name: web
    image: nginx:alpine
    env:
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: web-secrets
          key: db-password
    - name: API_KEY
      valueFrom:
        secretKeyRef:
          name: web-secrets
          key: api-key
```

## 21.6 Compliance and Governance

رعایت مقررات و حاکمیت امنیتی.

### ابزارهای Compliance:

#### **1. OpenSCAP:**
```yaml
# openscap.yml
version: '3.8'
services:
  openscap:
    image: openscap/openscap:latest
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./oscap-reports:/reports
    command: |
      oscap-docker image nginx:alpine \
        --report /reports/nginx-alpine-report.html \
        --profile xccdf_org.ssgproject.content_profile_docker
```

#### **2. InSpec:**
```ruby
# inspec-profile.rb
title "Docker Security Profile"

control "docker-001" do
  impact 1.0
  title "Docker daemon should not run as root"
  desc "Docker daemon should not run as root user"
  
  describe docker do
    its("daemon.user") { should_not eq "root" }
  end
end

control "docker-002" do
  impact 1.0
  title "Docker containers should not run as root"
  desc "Docker containers should not run as root user"
  
  docker.containers.running?.each do |container|
    describe container do
      its("user") { should_not eq "root" }
    end
  end
end
```

#### **3. CIS Docker Benchmark:**
```bash
# اجرای CIS Docker Benchmark
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  -v /etc:/host/etc:ro \
  -v /usr:/host/usr:ro \
  -v /var/lib/docker:/var/lib/docker:ro \
  aquasec/docker-bench-security
```

## 21.7 Security Scanning Tools

ابزارهای اسکن امنیتی کانتینرها.

### ابزارهای اسکن:

#### **1. Trivy:**
```bash
# اسکن ایمیج
trivy image nginx:alpine

# اسکن با خروجی JSON
trivy image --format json nginx:alpine

# اسکن با خروجی SARIF
trivy image --format sarif nginx:alpine

# اسکن با خروجی HTML
trivy image --format html nginx:alpine
```

#### **2. Clair:**
```yaml
# clair.yml
version: '3.8'
services:
  clair:
    image: quay.io/coreos/clair:latest
    ports:
      - "6060:6060"
    volumes:
      - ./clair-config.yaml:/etc/clair/config.yaml:ro

  clair-scanner:
    image: arminc/clair-scanner:latest
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
    command: clair-scanner --clair=http://clair:6060 nginx:alpine
    depends_on:
      - clair
```

#### **3. Anchore:**
```yaml
# anchore.yml
version: '3.8'
services:
  anchore-engine:
    image: anchore/anchore-engine:latest
    ports:
      - "8228:8228"
    environment:
      - ANCHORE_DB_PASSWORD=password
    volumes:
      - anchore-db:/var/lib/postgresql/data

  anchore-cli:
    image: anchore/anchore-cli:latest
    command: anchore-cli image add nginx:alpine
    depends_on:
      - anchore-engine

volumes:
  anchore-db:
```

## 21.8 Threat Detection

تشخیص تهدیدات امنیتی در کانتینرها.

### ابزارهای Threat Detection:

#### **1. Falco:**
```yaml
# falco.yml
version: '3.8'
services:
  falco:
    image: falcosecurity/falco:latest
    privileged: true
    volumes:
      - /var/run/docker.sock:/host/var/run/docker.sock:ro
      - /dev:/host/dev:ro
      - /proc:/host/proc:ro
      - /boot:/host/boot:ro
      - /lib/modules:/host/lib/modules:ro
      - /usr:/host/usr:ro
      - /etc:/host/etc:ro
    environment:
      - FALCO_GRPC_ENABLED=true
      - FALCO_GRPC_BIND_ADDRESS=0.0.0.0:5060
    ports:
      - "5060:5060"
```

#### **2. Sysdig:**
```yaml
# sysdig.yml
version: '3.8'
services:
  sysdig:
    image: sysdig/agent:latest
    privileged: true
    volumes:
      - /var/run/docker.sock:/host/var/run/docker.sock:ro
      - /dev:/host/dev:ro
      - /proc:/host/proc:ro
      - /boot:/host/boot:ro
      - /lib/modules:/host/lib/modules:ro
      - /usr:/host/usr:ro
      - /etc:/host/etc:ro
    environment:
      - SYSDIG_ACCESS_KEY=your-access-key
      - SYSDIG_COLLECTOR=collector.sysdigcloud.com
```

#### **3. Twistlock:**
```yaml
# twistlock.yml
version: '3.8'
services:
  twistlock:
    image: twistlock/defender:latest
    privileged: true
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - /var/lib/docker:/var/lib/docker:ro
    environment:
      - TWISTLOCK_CONSOLE_ADDRESS=your-console-address
      - TWISTLOCK_DEFENDER_TOKEN=your-token
```

## 21.9 Incident Response

پاسخ به حوادث امنیتی در کانتینرها.

### فرآیند Incident Response:

#### **1. تشخیص حادثه:**
```bash
# بررسی لاگ‌های کانتینر
docker logs container_name | grep -i error
docker logs container_name | grep -i warning

# بررسی processes
docker top container_name

# بررسی network connections
docker exec container_name netstat -tuln
```

#### **2. جداسازی کانتینر:**
```bash
# توقف کانتینر
docker stop container_name

# حذف کانتینر
docker rm container_name

# حذف ایمیج
docker rmi image_name
```

#### **3. تحلیل حادثه:**
```bash
# بررسی system logs
journalctl -u docker.service

# بررسی container logs
docker logs container_name

# بررسی network traffic
tcpdump -i any port 80
```

### Incident Response Script:
```bash
#!/bin/bash
# incident-response.sh

CONTAINER_NAME=$1

if [ -z "$CONTAINER_NAME" ]; then
    echo "Usage: $0 <container_name>"
    exit 1
fi

echo "=== Incident Response for Container: $CONTAINER_NAME ==="

echo "1. Container Status:"
docker ps -a | grep $CONTAINER_NAME

echo "2. Container Logs:"
docker logs $CONTAINER_NAME

echo "3. Container Processes:"
docker top $CONTAINER_NAME

echo "4. Container Network:"
docker inspect $CONTAINER_NAME | grep -A 10 "NetworkSettings"

echo "5. Container Volumes:"
docker inspect $CONTAINER_NAME | grep -A 10 "Mounts"

echo "6. System Logs:"
journalctl -u docker.service --since "1 hour ago" | tail -20

echo "7. Stopping Container:"
docker stop $CONTAINER_NAME

echo "8. Removing Container:"
docker rm $CONTAINER_NAME

echo "Incident Response completed!"
```

## 21.10 Security Automation

خودکارسازی امنیت کانتینرها.

### ابزارهای Security Automation:

#### **1. OPA Gatekeeper:**
```yaml
# gatekeeper.yml
apiVersion: templates.gatekeeper.sh/v1beta1
kind: ConstraintTemplate
metadata:
  name: k8srequiredlabels
spec:
  crd:
    spec:
      names:
        kind: K8sRequiredLabels
      validation:
        properties:
          labels:
            type: array
            items:
              type: string
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8srequiredlabels
        violation[{"msg": msg}] {
          required := input.parameters.labels
          provided := input.review.object.metadata.labels
          missing := required[_]
          not provided[missing]
          msg := sprintf("Missing required label: %v", [missing])
        }
```

#### **2. Kyverno:**
```yaml
# kyverno-policy.yml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-labels
spec:
  validationFailureAction: enforce
  background: true
  rules:
  - name: check-labels
    match:
      any:
      - resources:
          kinds:
          - Pod
    validate:
      message: "Label 'app' is required"
      pattern:
        metadata:
          labels:
            app: "?*"
```

#### **3. Security Automation Script:**
```bash
#!/bin/bash
# security-automation.sh

echo "=== Security Automation ==="

echo "1. Scanning images for vulnerabilities..."
docker images | grep -v REPOSITORY | awk '{print $1":"$2}' | while read image; do
    echo "Scanning $image..."
    trivy image --severity HIGH,CRITICAL $image
done

echo "2. Checking container security..."
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}" | while read line; do
    if [[ $line == *"root"* ]]; then
        echo "WARNING: Container running as root: $line"
    fi
done

echo "3. Checking network security..."
docker network ls | grep bridge | while read line; do
    network_id=$(echo $line | awk '{print $1}')
    echo "Checking network $network_id..."
    docker network inspect $network_id | grep -i "internal.*true"
done

echo "4. Checking volume security..."
docker volume ls | while read line; do
    if [[ $line == *"REPOSITORY"* ]]; then
        continue
    fi
    volume_name=$(echo $line | awk '{print $2}')
    echo "Checking volume $volume_name..."
    docker volume inspect $volume_name | grep -i "driver.*local"
done

echo "Security automation completed!"
```

این بخش شما را با تمام جنبه‌های امنیت پیشرفته کانتینرها آشنا می‌کند.