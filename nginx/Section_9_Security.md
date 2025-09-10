# Section 9 - Security

## 9.1 Security Concepts

Security in Nginx involves protecting the web server, applications, and data from various threats and attacks. This includes implementing proper access controls, encryption, monitoring, and following security best practices.

### Key Security Concepts:
- **Confidentiality**: Protecting data from unauthorized access
- **Integrity**: Ensuring data hasn't been tampered with
- **Availability**: Ensuring services remain accessible
- **Authentication**: Verifying user identity
- **Authorization**: Controlling access to resources
- **Non-repudiation**: Preventing denial of actions

### Real-world Analogy:
Web server security is like a bank's security system that:
- Requires proper identification (authentication)
- Controls access to different areas (authorization)
- Monitors all activities (logging and monitoring)
- Has multiple layers of protection (defense in depth)
- Responds to threats quickly (incident response)

### Common Security Threats:
1. **DDoS Attacks**: Overwhelming the server with traffic
2. **SQL Injection**: Malicious code injection through input
3. **Cross-Site Scripting (XSS)**: Injecting malicious scripts
4. **Cross-Site Request Forgery (CSRF)**: Unauthorized actions
5. **Brute Force Attacks**: Attempting to guess passwords
6. **Man-in-the-Middle**: Intercepting communications
7. **Directory Traversal**: Accessing restricted directories

### Security Layers:
```
Application Layer (Nginx)
├── Access Control
├── Rate Limiting
├── Input Validation
├── Security Headers
└── SSL/TLS
```

### Example Basic Security Configuration:
```nginx
server {
    listen 80;
    server_name example.com;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # Hide server information
    server_tokens off;
    
    location / {
        root /var/www/html;
    }
}
```

## 9.2 Access Control

Access control determines who can access what resources and under what conditions.

### IP-based Access Control:
```nginx
# Allow specific IPs
server {
    listen 80;
    server_name example.com;
    
    location /admin {
        allow 192.168.1.0/24;
        allow 10.0.0.0/8;
        deny all;
        
        root /var/www/admin;
    }
}

# Deny specific IPs
server {
    listen 80;
    server_name example.com;
    
    location / {
        deny 192.168.1.100;
        deny 10.0.0.50;
        allow all;
        
        root /var/www/html;
    }
}
```

### User Authentication:
```nginx
# Basic authentication
server {
    listen 80;
    server_name example.com;
    
    location /secure {
        auth_basic "Restricted Area";
        auth_basic_user_file /etc/nginx/.htpasswd;
        
        root /var/www/secure;
    }
}

# Create password file
# htpasswd -c /etc/nginx/.htpasswd username
```

### Advanced Access Control:
```nginx
# Time-based access control
map $time_iso8601 $is_work_hours {
    default 0;
    ~^(\d{4})-(\d{2})-(\d{2})T(0[9-9]|1[0-7]): 1;
}

server {
    listen 80;
    server_name example.com;
    
    location /admin {
        if ($is_work_hours = 0) {
            return 403 "Access denied outside work hours";
        }
        
        allow 192.168.1.0/24;
        deny all;
        
        root /var/www/admin;
    }
}
```

### Geographic Access Control:
```nginx
# Using GeoIP module
geo $allowed_country {
    default no;
    US yes;
    CA yes;
    GB yes;
}

server {
    listen 80;
    server_name example.com;
    
    location / {
        if ($allowed_country = no) {
            return 403 "Access denied from your country";
        }
        
        root /var/www/html;
    }
}
```

### Role-based Access Control:
```nginx
# Role-based access using headers
map $http_x_user_role $is_admin {
    default 0;
    "admin" 1;
    "superuser" 1;
}

server {
    listen 80;
    server_name example.com;
    
    location /admin {
        if ($is_admin = 0) {
            return 403 "Admin access required";
        }
        
        root /var/www/admin;
    }
}
```

## 9.3 Rate Limiting

Rate limiting controls the number of requests a client can make within a specific time period to prevent abuse and DDoS attacks.

### Basic Rate Limiting:
```nginx
# Define rate limiting zones
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;

server {
    listen 80;
    server_name example.com;
    
    # API rate limiting
    location /api/ {
        limit_req zone=api burst=20 nodelay;
        proxy_pass http://backend;
    }
    
    # Login rate limiting
    location /login {
        limit_req zone=login burst=5 nodelay;
        # Login handling
    }
}
```

### Advanced Rate Limiting:
```nginx
# Multiple rate limiting zones
limit_req_zone $binary_remote_addr zone=general:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=api:10m rate=50r/s;
limit_req_zone $binary_remote_addr zone=upload:10m rate=1r/s;

# Rate limiting by user
limit_req_zone $http_x_user_id zone=user:10m rate=100r/s;

server {
    listen 80;
    server_name example.com;
    
    # General rate limiting
    limit_req zone=general burst=20 nodelay;
    
    # API rate limiting
    location /api/ {
        limit_req zone=api burst=100 nodelay;
        proxy_pass http://backend;
    }
    
    # Upload rate limiting
    location /upload {
        limit_req zone=upload burst=2 nodelay;
        client_max_body_size 10M;
        # Upload handling
    }
    
    # User-specific rate limiting
    location /user/ {
        limit_req zone=user burst=200 nodelay;
        proxy_pass http://backend;
    }
}
```

### Rate Limiting with Whitelist:
```nginx
# Whitelist for trusted IPs
geo $trusted_ip {
    default 0;
    192.168.1.0/24 1;
    10.0.0.0/8 1;
}

# Rate limiting zones
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

map $trusted_ip $rate_limit {
    default "api";
    "1" "off";
}

server {
    listen 80;
    server_name example.com;
    
    location /api/ {
        limit_req zone=$rate_limit burst=20 nodelay;
        proxy_pass http://backend;
    }
}
```

### Rate Limiting Headers:
```nginx
# Rate limiting with custom headers
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

server {
    listen 80;
    server_name example.com;
    
    location /api/ {
        limit_req zone=api burst=20 nodelay;
        
        # Rate limiting headers
        add_header X-RateLimit-Limit "10" always;
        add_header X-RateLimit-Remaining "9" always;
        add_header X-RateLimit-Reset "3600" always;
        
        proxy_pass http://backend;
    }
}
```

## 9.4 DDoS Protection

DDoS (Distributed Denial of Service) protection involves implementing measures to prevent and mitigate DDoS attacks.

### Basic DDoS Protection:
```nginx
# DDoS protection zones
limit_req_zone $binary_remote_addr zone=ddos:10m rate=1r/s;
limit_conn_zone $binary_remote_addr zone=conn_limit_per_ip:10m;

server {
    listen 80;
    server_name example.com;
    
    # DDoS protection
    limit_req zone=ddos burst=5 nodelay;
    limit_conn conn_limit_per_ip 10;
    
    # Timeout settings
    client_body_timeout 10s;
    client_header_timeout 10s;
    keepalive_timeout 5s;
    
    location / {
        root /var/www/html;
    }
}
```

### Advanced DDoS Protection:
```nginx
# Multiple DDoS protection layers
limit_req_zone $binary_remote_addr zone=ddos:10m rate=1r/s;
limit_req_zone $binary_remote_addr zone=api_ddos:10m rate=5r/s;
limit_conn_zone $binary_remote_addr zone=conn_limit:10m;

# Rate limiting by request size
limit_req_zone $binary_remote_addr zone=large_requests:10m rate=1r/s;

server {
    listen 80;
    server_name example.com;
    
    # Global DDoS protection
    limit_req zone=ddos burst=5 nodelay;
    limit_conn conn_limit 10;
    
    # Large request protection
    client_max_body_size 1M;
    limit_req zone=large_requests burst=2 nodelay;
    
    # API-specific protection
    location /api/ {
        limit_req zone=api_ddos burst=20 nodelay;
        proxy_pass http://backend;
    }
    
    # Static content protection
    location ~* \.(css|js|png|jpg|jpeg|gif|ico|svg)$ {
        limit_req zone=ddos burst=10 nodelay;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### DDoS Protection with Fail2ban:
```nginx
# Nginx configuration for Fail2ban
server {
    listen 80;
    server_name example.com;
    
    # Logging for Fail2ban
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;
    
    location / {
        root /var/www/html;
    }
}
```

```bash
# Fail2ban configuration
# /etc/fail2ban/jail.local
[nginx-http-auth]
enabled = true
port = http,https
logpath = /var/log/nginx/error.log

[nginx-limit-req]
enabled = true
port = http,https
logpath = /var/log/nginx/error.log
maxretry = 10
```

### DDoS Protection with Cloudflare:
```nginx
# Cloudflare IP ranges
geo $cloudflare_ip {
    default 0;
    173.245.48.0/20 1;
    103.21.244.0/22 1;
    103.22.200.0/22 1;
    # Add more Cloudflare IP ranges
}

# Rate limiting for non-Cloudflare IPs
map $cloudflare_ip $rate_limit {
    default "ddos";
    "1" "off";
}

server {
    listen 80;
    server_name example.com;
    
    # DDoS protection for non-Cloudflare IPs
    limit_req zone=$rate_limit burst=5 nodelay;
    
    location / {
        root /var/www/html;
    }
}
```

## 9.5 Security Headers

Security headers provide additional protection against various web vulnerabilities.

### Basic Security Headers:
```nginx
server {
    listen 80;
    server_name example.com;
    
    # Basic security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    location / {
        root /var/www/html;
    }
}
```

### Comprehensive Security Headers:
```nginx
server {
    listen 80;
    server_name example.com;
    
    # Comprehensive security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self'; frame-ancestors 'self';" always;
    add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;
    add_header Cross-Origin-Embedder-Policy "require-corp" always;
    add_header Cross-Origin-Opener-Policy "same-origin" always;
    add_header Cross-Origin-Resource-Policy "same-origin" always;
    
    location / {
        root /var/www/html;
    }
}
```

### HTTPS Security Headers:
```nginx
server {
    listen 443 ssl http2;
    server_name example.com;
    
    ssl_certificate /path/to/cert.crt;
    ssl_certificate_key /path/to/key.key;
    
    # HTTPS security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    location / {
        root /var/www/html;
    }
}
```

### Dynamic Security Headers:
```nginx
# Dynamic security headers based on content type
map $sent_http_content_type $csp_header {
    default "default-src 'self'";
    "text/html" "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'";
    "application/json" "default-src 'self'";
}

server {
    listen 80;
    server_name example.com;
    
    location / {
        root /var/www/html;
        
        # Dynamic CSP header
        add_header Content-Security-Policy $csp_header always;
        
        # Other security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
    }
}
```

## 9.6 Security Best Practices

### 1. Server Hardening:
```nginx
# Server hardening configuration
server {
    listen 80;
    server_name example.com;
    
    # Hide server information
    server_tokens off;
    more_clear_headers 'Server';
    more_clear_headers 'X-Powered-By';
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=general:10m rate=10r/s;
    limit_req zone=general burst=20 nodelay;
    
    location / {
        root /var/www/html;
    }
}
```

### 2. Input Validation:
```nginx
# Input validation and sanitization
server {
    listen 80;
    server_name example.com;
    
    # Block suspicious requests
    if ($request_uri ~* "(<|>|'|\"|;|\(|\)|%0A|%0D|%22|%27|%3C|%3E|%00)") {
        return 403;
    }
    
    # Block common attack patterns
    if ($request_uri ~* "(union|select|insert|delete|update|drop|create|alter|exec|script)") {
        return 403;
    }
    
    # Block suspicious user agents
    if ($http_user_agent ~* "(bot|crawler|spider|scraper)") {
        return 403;
    }
    
    location / {
        root /var/www/html;
    }
}
```

### 3. File Upload Security:
```nginx
# Secure file upload configuration
server {
    listen 80;
    server_name example.com;
    
    # File upload security
    client_max_body_size 10M;
    client_body_timeout 60s;
    client_header_timeout 60s;
    
    location /upload {
        # Restrict file types
        if ($request_filename ~* \.(php|jsp|asp|sh|cgi)$) {
            return 403;
        }
        
        # Restrict file size
        client_max_body_size 5M;
        
        # Upload handling
        proxy_pass http://upload_backend;
    }
}
```

### 4. API Security:
```nginx
# API security configuration
server {
    listen 80;
    server_name api.example.com;
    
    # API rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=100r/s;
    limit_req zone=api burst=200 nodelay;
    
    # API authentication
    location /api/ {
        # Require API key
        if ($http_x_api_key = "") {
            return 401 "API key required";
        }
        
        # Validate API key format
        if ($http_x_api_key !~* "^[a-zA-Z0-9]{32}$") {
            return 401 "Invalid API key format";
        }
        
        proxy_pass http://api_backend;
    }
}
```

## 9.7 Security Testing

### 1. Security Headers Testing:
```bash
# Test security headers
curl -I https://example.com/ | grep -i "x-"

# Test specific headers
curl -I https://example.com/ | grep -i "content-security-policy"
curl -I https://example.com/ | grep -i "strict-transport-security"
```

### 2. Rate Limiting Testing:
```bash
# Test rate limiting
for i in {1..20}; do
    curl -I http://example.com/api/
done

# Test with different IPs
curl -H "X-Forwarded-For: 192.168.1.100" http://example.com/api/
curl -H "X-Forwarded-For: 192.168.1.101" http://example.com/api/
```

### 3. DDoS Protection Testing:
```bash
# Test DDoS protection
ab -n 1000 -c 100 http://example.com/

# Test with large requests
curl -X POST -d "$(head -c 1000000 /dev/zero)" http://example.com/upload
```

### 4. Security Scanning:
```bash
# Use security scanning tools
nmap -sV -sC example.com
nikto -h example.com
dirb http://example.com/
```

## 9.8 Security Monitoring

### 1. Security Logging:
```nginx
# Security-focused logging
log_format security '$remote_addr - $remote_user [$time_local] '
                   '"$request" $status $body_bytes_sent '
                   '"$http_referer" "$http_user_agent" '
                   'rt=$request_time uct="$upstream_connect_time" '
                   'uht="$upstream_header_time" urt="$upstream_response_time" '
                   'upstream_addr="$upstream_addr" '
                   'upstream_status="$upstream_status"';

server {
    listen 80;
    server_name example.com;
    
    # Security logging
    access_log /var/log/nginx/security.log security;
    
    location / {
        root /var/www/html;
    }
}
```

### 2. Security Monitoring Scripts:
```bash
#!/bin/bash
# Security monitoring script

LOG_FILE="/var/log/nginx/security.log"
ALERT_EMAIL="admin@example.com"

# Monitor for suspicious activity
SUSPICIOUS_REQUESTS=$(grep -E "(union|select|insert|delete|update|drop|create|alter|exec|script)" $LOG_FILE | wc -l)

if [ $SUSPICIOUS_REQUESTS -gt 10 ]; then
    echo "ALERT: $SUSPICIOUS_REQUESTS suspicious requests detected" | mail -s "Security Alert" $ALERT_EMAIL
fi

# Monitor for high error rates
ERROR_RATE=$(grep " 4[0-9][0-9] " $LOG_FILE | wc -l)
TOTAL_REQUESTS=$(grep -c "GET\|POST\|PUT\|DELETE" $LOG_FILE)

if [ $TOTAL_REQUESTS -gt 0 ]; then
    ERROR_PERCENTAGE=$((ERROR_RATE * 100 / TOTAL_REQUESTS))
    if [ $ERROR_PERCENTAGE -gt 20 ]; then
        echo "ALERT: High error rate detected: $ERROR_PERCENTAGE%" | mail -s "High Error Rate Alert" $ALERT_EMAIL
    fi
fi
```

### 3. Real-time Security Monitoring:
```bash
# Real-time security monitoring
tail -f /var/log/nginx/security.log | grep -E "(4[0-9][0-9]|5[0-9][0-9])" | while read line; do
    echo "Security Alert: $line"
    # Send alert notification
done
```

## 9.9 Security Troubleshooting

### 1. Common Security Issues:

#### 403 Forbidden Errors:
```bash
# Check access control configuration
nginx -T | grep -A 5 "allow\|deny"

# Check file permissions
ls -la /var/www/html/

# Check error logs
tail -f /var/log/nginx/error.log
```

#### Rate Limiting Issues:
```bash
# Check rate limiting configuration
nginx -T | grep -A 5 "limit_req"

# Test rate limiting
curl -I http://example.com/api/

# Check rate limiting logs
grep "limiting requests" /var/log/nginx/error.log
```

#### SSL/TLS Issues:
```bash
# Check SSL configuration
openssl s_client -connect example.com:443

# Check certificate validity
openssl x509 -in /path/to/cert.crt -text -noout

# Test SSL security
curl -I https://example.com/
```

### 2. Security Debugging:
```nginx
# Enable security debugging
error_log /var/log/nginx/security_debug.log debug;

server {
    listen 80;
    server_name example.com;
    
    # Debug headers
    add_header X-Debug-Remote-Addr $remote_addr;
    add_header X-Debug-User-Agent $http_user_agent;
    add_header X-Debug-Request-Uri $request_uri;
    
    location / {
        root /var/www/html;
    }
}
```

### 3. Security Incident Response:
```bash
#!/bin/bash
# Security incident response script

INCIDENT_LOG="/var/log/nginx/security_incident.log"
BLOCKED_IPS="/etc/nginx/blocked_ips.conf"

# Function to block IP
block_ip() {
    local ip=$1
    echo "Blocking IP: $ip"
    echo "deny $ip;" >> $BLOCKED_IPS
    nginx -s reload
    echo "$(date): Blocked IP $ip" >> $INCIDENT_LOG
}

# Function to unblock IP
unblock_ip() {
    local ip=$1
    echo "Unblocking IP: $ip"
    sed -i "/deny $ip;/d" $BLOCKED_IPS
    nginx -s reload
    echo "$(date): Unblocked IP $ip" >> $INCIDENT_LOG
}

# Monitor for attacks
tail -f /var/log/nginx/access.log | grep -E "(4[0-9][0-9]|5[0-9][0-9])" | while read line; do
    ip=$(echo $line | awk '{print $1}')
    echo "Suspicious activity from IP: $ip"
    # Implement automatic blocking logic here
done
```

## 9.10 Security Compliance

### 1. PCI DSS Compliance:
```nginx
# PCI DSS compliant configuration
server {
    listen 443 ssl http2;
    server_name payment.example.com;
    
    ssl_certificate /path/to/cert.crt;
    ssl_certificate_key /path/to/key.key;
    
    # Strong SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # Access control
    allow 192.168.1.0/24;
    deny all;
    
    location / {
        root /var/www/payment;
    }
}
```

### 2. GDPR Compliance:
```nginx
# GDPR compliant configuration
server {
    listen 80;
    server_name example.com;
    
    # Privacy headers
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    # Cookie consent
    location /cookie-consent {
        root /var/www/html;
        add_header Set-Cookie "consent=accepted; Path=/; Max-Age=31536000; Secure; HttpOnly";
    }
    
    location / {
        root /var/www/html;
    }
}
```

### 3. Security Audit Configuration:
```nginx
# Security audit configuration
server {
    listen 80;
    server_name example.com;
    
    # Comprehensive logging
    log_format audit '$remote_addr - $remote_user [$time_local] '
                    '"$request" $status $body_bytes_sent '
                    '"$http_referer" "$http_user_agent" '
                    'rt=$request_time uct="$upstream_connect_time" '
                    'uht="$upstream_header_time" urt="$upstream_response_time" '
                    'upstream_addr="$upstream_addr" '
                    'upstream_status="$upstream_status" '
                    'request_id="$request_id"';
    
    access_log /var/log/nginx/audit.log audit;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    location / {
        root /var/www/html;
    }
}
```

### 4. Compliance Monitoring:
```bash
#!/bin/bash
# Security compliance monitoring script

# Check SSL configuration
check_ssl() {
    local domain=$1
    local ssl_test=$(echo | openssl s_client -servername $domain -connect $domain:443 2>/dev/null | openssl x509 -noout -text | grep -E "Not After|Not Before")
    echo "SSL Certificate Status for $domain:"
    echo "$ssl_test"
}

# Check security headers
check_headers() {
    local domain=$1
    echo "Security Headers for $domain:"
    curl -I https://$domain/ | grep -i "x-"
}

# Check rate limiting
check_rate_limiting() {
    echo "Testing rate limiting..."
    for i in {1..20}; do
        curl -I http://example.com/api/ 2>/dev/null | grep -i "x-ratelimit"
    done
}

# Run compliance checks
check_ssl "example.com"
check_headers "example.com"
check_rate_limiting
```