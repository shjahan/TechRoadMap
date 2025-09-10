# Section 14 - Nginx with Python

## 14.1 Python Integration Concepts

Python integration with Nginx involves using Nginx as a reverse proxy to serve Python web applications, typically using WSGI (Web Server Gateway Interface) or ASGI (Asynchronous Server Gateway Interface) protocols.

### Key Concepts:
- **WSGI**: Web Server Gateway Interface for synchronous Python applications
- **ASGI**: Asynchronous Server Gateway Interface for async Python applications
- **uWSGI**: High-performance WSGI server
- **Gunicorn**: Python WSGI HTTP Server
- **Process Management**: Managing Python application processes

### Real-world Analogy:
Think of Nginx with Python like a restaurant with specialized cooking stations:
- **Nginx** is the head waiter who takes orders and serves customers
- **WSGI/ASGI** is the communication system between waiter and kitchen
- **Python Application** is the specialized chef who prepares custom dishes
- **uWSGI/Gunicorn** is the kitchen manager who coordinates the cooking process

### Architecture Overview:
```
Client Request → Nginx → WSGI/ASGI → Python Application → Response
                     ↓
                Static Files (CSS, JS, Images)
```

### Example Basic Configuration:
```nginx
upstream python_backend {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}

server {
    listen 80;
    server_name example.com;
    root /var/www/html;

    # Serve static files directly
    location /static/ {
        alias /var/www/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Proxy to Python application
    location / {
        proxy_pass http://python_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 14.2 WSGI Configuration

WSGI (Web Server Gateway Interface) is a specification that describes how a web server communicates with web applications written in Python.

### Basic WSGI Configuration:
```nginx
server {
    listen 80;
    server_name example.com;
    root /var/www/html;

    # WSGI application
    location / {
        include uwsgi_params;
        uwsgi_pass 127.0.0.1:8000;
    }
}
```

### Advanced WSGI Configuration:
```nginx
upstream wsgi_backend {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
    server 127.0.0.1:8003;
}

server {
    listen 80;
    server_name example.com;
    root /var/www/html;

    # Static files
    location /static/ {
        alias /var/www/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    # Media files
    location /media/ {
        alias /var/www/media/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # WSGI application
    location / {
        include uwsgi_params;
        uwsgi_pass wsgi_backend;
        
        # Timeouts
        uwsgi_connect_timeout 30s;
        uwsgi_send_timeout 30s;
        uwsgi_read_timeout 30s;
        
        # Buffering
        uwsgi_buffering on;
        uwsgi_buffer_size 4k;
        uwsgi_buffers 8 4k;
        uwsgi_busy_buffers_size 8k;
        
        # Error handling
        uwsgi_intercept_errors on;
    }
}
```

### WSGI Parameters:
```nginx
# Common uWSGI parameters
uwsgi_param QUERY_STRING $query_string;
uwsgi_param REQUEST_METHOD $request_method;
uwsgi_param CONTENT_TYPE $content_type;
uwsgi_param CONTENT_LENGTH $content_length;
uwsgi_param REQUEST_URI $request_uri;
uwsgi_param PATH_INFO $document_uri;
uwsgi_param DOCUMENT_ROOT $document_root;
uwsgi_param SERVER_PROTOCOL $server_protocol;
uwsgi_param REQUEST_SCHEME $scheme;
uwsgi_param HTTPS $https if_not_empty;
uwsgi_param REMOTE_ADDR $remote_addr;
uwsgi_param REMOTE_PORT $remote_port;
uwsgi_param SERVER_PORT $server_port;
uwsgi_param SERVER_NAME $server_name;
```

## 14.3 uWSGI Integration

uWSGI is a full-stack solution for building hosting services, particularly for Python web applications.

### uWSGI Configuration:
```ini
# uwsgi.ini
[uwsgi]
# Application settings
module = wsgi:application
master = true
processes = 4
threads = 2

# Socket settings
socket = 127.0.0.1:8000
chmod-socket = 666
vacuum = true
die-on-term = true

# Logging
logto = /var/log/uwsgi/uwsgi.log
log-maxsize = 50000000
log-backupcount = 5

# Performance
max-requests = 1000
harakiri = 30
harakiri-verbose = true

# Memory
limit-as = 512
reload-mercy = 10

# Stats
stats = 127.0.0.1:9191
stats-http = true
```

### Nginx Configuration for uWSGI:
```nginx
upstream uwsgi_backend {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
    server 127.0.0.1:8003;
}

server {
    listen 80;
    server_name example.com;
    root /var/www/html;

    # Static files
    location /static/ {
        alias /var/www/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # uWSGI application
    location / {
        include uwsgi_params;
        uwsgi_pass uwsgi_backend;
        
        # Timeouts
        uwsgi_connect_timeout 30s;
        uwsgi_send_timeout 30s;
        uwsgi_read_timeout 30s;
        
        # Buffering
        uwsgi_buffering on;
        uwsgi_buffer_size 4k;
        uwsgi_buffers 8 4k;
    }

    # uWSGI stats
    location /uwsgi-stats {
        include uwsgi_params;
        uwsgi_pass 127.0.0.1:9191;
        allow 127.0.0.1;
        deny all;
    }
}
```

### uWSGI with Multiple Applications:
```ini
# Multiple applications configuration
[uwsgi:app1]
module = app1.wsgi:application
socket = 127.0.0.1:8000
processes = 2

[uwsgi:app2]
module = app2.wsgi:application
socket = 127.0.0.1:8001
processes = 2

[uwsgi:api]
module = api.wsgi:application
socket = 127.0.0.1:8002
processes = 4
```

```nginx
# Nginx configuration for multiple applications
server {
    listen 80;
    server_name app1.example.com;
    
    location / {
        include uwsgi_params;
        uwsgi_pass 127.0.0.1:8000;
    }
}

server {
    listen 80;
    server_name app2.example.com;
    
    location / {
        include uwsgi_params;
        uwsgi_pass 127.0.0.1:8001;
    }
}

server {
    listen 80;
    server_name api.example.com;
    
    location / {
        include uwsgi_params;
        uwsgi_pass 127.0.0.1:8002;
    }
}
```

## 14.4 Gunicorn Integration

Gunicorn is a Python WSGI HTTP Server for UNIX, designed to be simple and efficient.

### Gunicorn Configuration:
```python
# gunicorn.conf.py
import multiprocessing

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
preload_app = True

# Logging
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "myapp"

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190
```

### Nginx Configuration for Gunicorn:
```nginx
upstream gunicorn_backend {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
    server 127.0.0.1:8003;
}

server {
    listen 80;
    server_name example.com;
    root /var/www/html;

    # Static files
    location /static/ {
        alias /var/www/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Gunicorn application
    location / {
        proxy_pass http://gunicorn_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
        
        # Buffering
        proxy_buffering on;
        proxy_buffer_size 4k;
        proxy_buffers 8 4k;
        proxy_busy_buffers_size 8k;
        
        # Connection optimization
        proxy_http_version 1.1;
        proxy_set_header Connection "";
    }
}
```

### Gunicorn with Systemd:
```ini
# /etc/systemd/system/myapp.service
[Unit]
Description=MyApp Gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/myapp
Environment="PATH=/var/www/myapp/venv/bin"
ExecStart=/var/www/myapp/venv/bin/gunicorn --config gunicorn.conf.py wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

## 14.5 Python Best Practices

### 1. Application Structure:
```python
# wsgi.py
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
application = get_wsgi_application()
```

### 2. Environment Configuration:
```python
# settings.py
import os

DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'myapp'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = '/var/www/media/'
```

### 3. Security Configuration:
```python
# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# HTTPS settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### 4. Nginx Security Configuration:
```nginx
# Security configuration for Python applications
server {
    listen 80;
    server_name example.com;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;
    
    # Static files
    location /static/ {
        alias /var/www/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # API endpoints
    location /api/ {
        limit_req zone=api burst=20 nodelay;
        
        proxy_pass http://gunicorn_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    # Login endpoint
    location /login/ {
        limit_req zone=login burst=5 nodelay;
        
        proxy_pass http://gunicorn_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    # Block sensitive files
    location ~* \.(env|pyc|pyo|pyd|log)$ {
        deny all;
    }
}
```

## 14.6 Python Testing

### 1. Unit Testing:
```python
# tests/test_views.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_api_endpoint(self):
        response = self.client.get('/api/health/')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'OK'})

    def test_authenticated_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)
```

### 2. Integration Testing:
```python
# tests/test_integration.py
from django.test import TestCase, Client
from django.contrib.auth.models import User

class IntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_user_registration_flow(self):
        # Register user
        response = self.client.post('/register/', {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        })
        self.assertEqual(response.status_code, 302)
        
        # Login user
        response = self.client.post('/login/', {
            'username': 'newuser',
            'password': 'complexpass123'
        })
        self.assertEqual(response.status_code, 302)
        
        # Access protected page
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)
```

### 3. Load Testing:
```bash
# Load testing with Apache Bench
ab -n 1000 -c 10 http://example.com/api/health/

# Load testing with wrk
wrk -t12 -c400 -d30s http://example.com/api/health/

# Load testing with Locust
locust -f locustfile.py --host=http://example.com
```

### 4. Nginx Testing:
```bash
# Test Nginx configuration
nginx -t

# Test with curl
curl -H "Host: example.com" http://localhost/api/health/

# Test load balancing
for i in {1..10}; do
    curl -H "Host: example.com" http://localhost/api/health/
    echo
done
```

## 14.7 Python Performance

### 1. Gunicorn Performance Tuning:
```python
# gunicorn.conf.py - Performance optimized
import multiprocessing

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gevent"
worker_connections = 1000
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
preload_app = True

# Memory optimization
worker_tmp_dir = "/dev/shm"
worker_class = "gevent"
worker_connections = 1000

# CPU optimization
worker_class = "sync"
threads = 2
```

### 2. uWSGI Performance Tuning:
```ini
# uwsgi.ini - Performance optimized
[uwsgi]
module = wsgi:application
master = true
processes = 8
threads = 2
socket = 127.0.0.1:8000

# Performance settings
max-requests = 1000
harakiri = 30
reload-mercy = 10
worker-reload-mercy = 10

# Memory optimization
limit-as = 512
reload-on-as = 400
reload-on-rss = 400

# CPU optimization
cpu-affinity = 1
```

### 3. Nginx Performance Configuration:
```nginx
# High-performance Nginx configuration for Python
worker_processes auto;
worker_cpu_affinity auto;
worker_rlimit_nofile 65535;

events {
    worker_connections 1024;
    use epoll;
    multi_accept on;
}

http {
    # Basic optimizations
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    keepalive_requests 100;
    
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css application/json application/javascript;
    
    # Upstream configuration
    upstream python_backend {
        least_conn;
        server 127.0.0.1:8000;
        server 127.0.0.1:8001;
        server 127.0.0.1:8002;
        server 127.0.0.1:8003;
        
        keepalive 32;
    }
    
    server {
        listen 80;
        server_name example.com;
        
        # Static files
        location /static/ {
            alias /var/www/static/;
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
        
        # Python application
        location / {
            proxy_pass http://python_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            
            # Connection optimization
            proxy_http_version 1.1;
            proxy_set_header Connection "";
            
            # Buffering
            proxy_buffering on;
            proxy_buffer_size 4k;
            proxy_buffers 8 4k;
        }
    }
}
```

### 4. Caching Strategy:
```python
# Django caching configuration
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Cache settings
CACHE_TTL = 60 * 15  # 15 minutes
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
```

```nginx
# Nginx caching for Python applications
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=python_cache:10m max_size=1g inactive=60m;

server {
    listen 80;
    server_name example.com;
    
    # Cache API responses
    location /api/ {
        proxy_cache python_cache;
        proxy_cache_valid 200 302 10m;
        proxy_cache_valid 404 1m;
        proxy_cache_key "$scheme$request_method$host$request_uri";
        
        proxy_pass http://python_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    # No cache for dynamic content
    location /api/auth/ {
        proxy_pass http://python_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 14.8 Python Troubleshooting

### 1. Common Issues:

#### Import Errors:
```bash
# Check Python path
python -c "import sys; print(sys.path)"

# Check virtual environment
which python
pip list

# Check application logs
tail -f /var/log/gunicorn/error.log
```

#### Memory Issues:
```bash
# Check Python memory usage
ps aux | grep python
pmap $(pgrep python)

# Monitor memory in real-time
watch -n 1 'ps aux --sort=-%mem | head -10'
```

#### Connection Issues:
```bash
# Check if Python app is listening
netstat -tlnp | grep :8000
lsof -i :8000

# Test connection
curl http://localhost:8000/api/health/
```

### 2. Debugging Tools:
```python
# Django debug configuration
DEBUG = True
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

### 3. Performance Monitoring:
```python
# Performance monitoring middleware
import time
import logging

logger = logging.getLogger(__name__)

class PerformanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        
        response = self.get_response(request)
        
        duration = time.time() - start_time
        logger.info(f"{request.method} {request.path} - {response.status_code} - {duration:.3f}s")
        
        return response
```

## 14.9 Python Security

### 1. Input Validation:
```python
# Django form validation
from django import forms
from django.core.validators import validate_email

class UserForm(forms.Form):
    username = forms.CharField(max_length=150, min_length=3)
    email = forms.EmailField(validators=[validate_email])
    password = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput,
        help_text="Password must be at least 8 characters long"
    )
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not any(c.isupper() for c in password):
            raise forms.ValidationError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in password):
            raise forms.ValidationError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in password):
            raise forms.ValidationError("Password must contain at least one digit")
        return password
```

### 2. Authentication and Authorization:
```python
# Django authentication
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

@login_required
def protected_view(request):
    return render(request, 'protected.html')

@permission_required('app.can_view_sensitive_data')
def sensitive_view(request):
    return render(request, 'sensitive.html')

class ProtectedView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'app.can_view_sensitive_data'
    
    def get(self, request):
        return render(request, 'sensitive.html')
```

### 3. Nginx Security Configuration:
```nginx
# Security configuration for Python applications
server {
    listen 80;
    server_name example.com;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;
    
    # API endpoints
    location /api/ {
        limit_req zone=api burst=20 nodelay;
        
        proxy_pass http://python_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    # Admin interface
    location /admin/ {
        limit_req zone=login burst=5 nodelay;
        
        # IP whitelist
        allow 192.168.1.0/24;
        deny all;
        
        proxy_pass http://python_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    # Block sensitive files
    location ~* \.(env|pyc|pyo|pyd|log|sqlite3)$ {
        deny all;
    }
}
```

### 4. HTTPS Configuration:
```nginx
# HTTPS configuration for Python applications
server {
    listen 443 ssl http2;
    server_name example.com;
    
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # Python application
    location / {
        proxy_pass http://python_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# HTTP to HTTPS redirect
server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}
```

## 14.10 Python Documentation

### 1. API Documentation:
```python
# Django REST Framework documentation
from rest_framework import serializers, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined']
        read_only_fields = ['id', 'date_joined']

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@api_view(['GET'])
def health_check(request):
    """
    Health check endpoint
    
    Returns the current status of the application
    """
    return Response({'status': 'OK', 'timestamp': timezone.now()})
```

### 2. Configuration Documentation:
```nginx
# =============================================================================
# Python Integration Configuration
# =============================================================================
# 
# This configuration provides:
# - WSGI/ASGI communication with Python applications
# - Load balancing across Python processes
# - Static file serving optimization
# - Security headers and rate limiting
# 
# Dependencies:
# - Python 3.8+ with virtual environment
# - Django/Flask/FastAPI application
# - Gunicorn or uWSGI server
# - Redis for caching (optional)
# 
# =============================================================================

upstream python_backend {
    least_conn;
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
    server 127.0.0.1:8003;
    
    keepalive 32;
}

server {
    listen 80;
    server_name example.com;
    
    # Static and media files
    location /static/ {
        alias /var/www/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    location /media/ {
        alias /var/www/media/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Python application
    location / {
        proxy_pass http://python_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Connection optimization
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        
        # Timeouts
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }
}
```

### 3. Deployment Documentation:
```bash
#!/bin/bash
# Python application deployment script

echo "Starting Python application deployment..."

# Activate virtual environment
source /var/www/myapp/venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart Gunicorn
systemctl restart myapp

# Reload Nginx
nginx -s reload

echo "Deployment completed successfully!"
```

### 4. Monitoring Documentation:
```bash
#!/bin/bash
# Python application monitoring script

echo "=== Python Application Status ==="
echo "Date: $(date)"
echo ""

# Check Gunicorn processes
echo "Gunicorn Processes:"
ps aux | grep gunicorn | grep -v grep

# Check memory usage
echo ""
echo "Memory Usage:"
ps aux --sort=-%mem | grep python | head -5

# Check response time
echo ""
echo "Response Time Test:"
time curl -s http://localhost:8000/api/health/ > /dev/null

# Check error rate
echo ""
echo "Error Rate (last 100 requests):"
tail -100 /var/log/nginx/access.log | grep -c " 5[0-9][0-9] "

# Check application logs
echo ""
echo "Recent Errors:"
tail -10 /var/log/gunicorn/error.log
```