# Section 7 - SSL/TLS Configuration

## 7.1 SSL/TLS Concepts

SSL (Secure Sockets Layer) and TLS (Transport Layer Security) are cryptographic protocols that provide secure communication over a computer network. TLS is the successor to SSL and is widely used for securing web traffic.

### Key Concepts:
- **Encryption**: Data is encrypted during transmission
- **Authentication**: Server identity is verified using certificates
- **Integrity**: Data cannot be modified during transmission
- **Handshake**: Process of establishing secure connection
- **Certificates**: Digital documents that prove server identity

### Real-world Analogy:
SSL/TLS is like a secure postal service that:
- Uses special locked boxes (encryption) to protect your mail
- Verifies the identity of the sender and recipient (authentication)
- Ensures the mail hasn't been tampered with (integrity)
- Has a special handshake process to establish trust before sending mail

### SSL vs TLS:
- **SSL 1.0/2.0/3.0**: Deprecated due to security vulnerabilities
- **TLS 1.0**: Legacy support, not recommended
- **TLS 1.1**: Legacy support, not recommended
- **TLS 1.2**: Widely supported, secure
- **TLS 1.3**: Latest version, most secure and efficient

### Basic SSL/TLS Flow:
```
1. Client Hello: Client sends supported cipher suites
2. Server Hello: Server chooses cipher suite and sends certificate
3. Key Exchange: Client and server exchange keys
4. Finished: Secure connection established
```

### Example Basic Configuration:
```nginx
server {
    listen 443 ssl http2;
    server_name example.com;
    
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;
    
    location / {
        root /var/www/html;
    }
}
```

## 7.2 Certificate Management

Certificate management involves obtaining, installing, and maintaining SSL/TLS certificates for secure communication.

### Types of Certificates:

#### 1. Self-Signed Certificates:
```bash
# Generate self-signed certificate
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

# Generate with specific subject
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes \
    -subj "/C=US/ST=State/L=City/O=Organization/CN=example.com"
```

#### 2. Let's Encrypt Certificates:
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d example.com -d www.example.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

#### 3. Commercial Certificates:
```bash
# Generate Certificate Signing Request (CSR)
openssl req -new -newkey rsa:2048 -nodes -keyout example.com.key -out example.com.csr

# Submit CSR to Certificate Authority
# Install received certificate
```

### Certificate Installation:
```nginx
# Basic certificate configuration
server {
    listen 443 ssl http2;
    server_name example.com;
    
    # Certificate files
    ssl_certificate /etc/ssl/certs/example.com.crt;
    ssl_certificate_key /etc/ssl/private/example.com.key;
    
    # Certificate chain (if needed)
    ssl_trusted_certificate /etc/ssl/certs/ca-bundle.crt;
    
    location / {
        root /var/www/html;
    }
}
```

### Certificate Chain:
```nginx
# Full certificate chain
server {
    listen 443 ssl http2;
    server_name example.com;
    
    # Certificate with chain
    ssl_certificate /etc/ssl/certs/example.com-fullchain.crt;
    ssl_certificate_key /etc/ssl/private/example.com.key;
    
    # Intermediate certificates
    ssl_trusted_certificate /etc/ssl/certs/intermediate.crt;
}
```

### Certificate Validation:
```bash
# Check certificate validity
openssl x509 -in certificate.crt -text -noout

# Check certificate expiration
openssl x509 -in certificate.crt -noout -dates

# Verify certificate chain
openssl verify -CAfile ca-bundle.crt certificate.crt
```

## 7.3 SSL Configuration

SSL configuration in Nginx involves setting up secure connections with proper encryption and security settings.

### Basic SSL Configuration:
```nginx
server {
    listen 443 ssl http2;
    server_name example.com;
    
    # Certificate files
    ssl_certificate /etc/ssl/certs/example.com.crt;
    ssl_certificate_key /etc/ssl/private/example.com.key;
    
    # SSL protocols
    ssl_protocols TLSv1.2 TLSv1.3;
    
    # SSL ciphers
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;
    
    location / {
        root /var/www/html;
    }
}
```

### Advanced SSL Configuration:
```nginx
server {
    listen 443 ssl http2;
    server_name example.com;
    
    # Certificate files
    ssl_certificate /etc/ssl/certs/example.com.crt;
    ssl_certificate_key /etc/ssl/private/example.com.key;
    
    # SSL protocols (secure)
    ssl_protocols TLSv1.2 TLSv1.3;
    
    # Modern cipher suites
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    
    # SSL session management
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    ssl_session_tickets off;
    
    # OCSP stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    ssl_trusted_certificate /etc/ssl/certs/ca-bundle.crt;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    
    location / {
        root /var/www/html;
    }
}
```

### SSL Performance Optimization:
```nginx
# SSL performance settings
server {
    listen 443 ssl http2;
    server_name example.com;
    
    ssl_certificate /etc/ssl/certs/example.com.crt;
    ssl_certificate_key /etc/ssl/private/example.com.key;
    
    # Performance optimizations
    ssl_session_cache shared:SSL:50m;
    ssl_session_timeout 1d;
    ssl_session_tickets off;
    
    # Buffer sizes
    ssl_buffer_size 8k;
    
    # Early data (TLS 1.3)
    ssl_early_data on;
    
    location / {
        root /var/www/html;
    }
}
```

## 7.4 TLS Configuration

TLS configuration focuses on modern security standards and performance optimizations.

### Modern TLS Configuration:
```nginx
server {
    listen 443 ssl http2;
    server_name example.com;
    
    ssl_certificate /etc/ssl/certs/example.com.crt;
    ssl_certificate_key /etc/ssl/private/example.com.key;
    
    # TLS 1.2 and 1.3 only
    ssl_protocols TLSv1.2 TLSv1.3;
    
    # Modern cipher suites
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305;
    ssl_prefer_server_ciphers off;
    
    # TLS 1.3 specific settings
    ssl_conf_command Ciphersuites TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256;
    ssl_conf_command Options PrioritizeChaCha;
    
    location / {
        root /var/www/html;
    }
}
```

### TLS 1.3 Configuration:
```nginx
# TLS 1.3 optimized configuration
server {
    listen 443 ssl http2;
    server_name example.com;
    
    ssl_certificate /etc/ssl/certs/example.com.crt;
    ssl_certificate_key /etc/ssl/private/example.com.key;
    
    # TLS 1.3 only
    ssl_protocols TLSv1.3;
    
    # TLS 1.3 cipher suites
    ssl_conf_command Ciphersuites TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256;
    
    # Early data support
    ssl_early_data on;
    
    # Session resumption
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 1d;
    ssl_session_tickets off;
    
    location / {
        root /var/www/html;
    }
}
```

### TLS Security Hardening:
```nginx
# Hardened TLS configuration
server {
    listen 443 ssl http2;
    server_name example.com;
    
    ssl_certificate /etc/ssl/certs/example.com.crt;
    ssl_certificate_key /etc/ssl/private/example.com.key;
    
    # Only secure protocols
    ssl_protocols TLSv1.2 TLSv1.3;
    
    # Strong cipher suites only
    ssl_ciphers ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305;
    ssl_prefer_server_ciphers off;
    
    # Perfect Forward Secrecy
    ssl_ecdh_curve secp384r1;
    
    # OCSP stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    ssl_trusted_certificate /etc/ssl/certs/ca-bundle.crt;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    location / {
        root /var/www/html;
    }
}
```

## 7.5 SSL Best Practices

### 1. Certificate Management:
```nginx
# Use full certificate chain
server {
    listen 443 ssl http2;
    server_name example.com;
    
    ssl_certificate /etc/ssl/certs/example.com-fullchain.crt;
    ssl_certificate_key /etc/ssl/private/example.com.key;
    
    # Verify certificate chain
    ssl_trusted_certificate /etc/ssl/certs/ca-bundle.crt;
}
```

### 2. Security Headers:
```nginx
# Comprehensive security headers
server {
    listen 443 ssl http2;
    server_name example.com;
    
    ssl_certificate /etc/ssl/certs/example.com.crt;
    ssl_certificate_key /etc/ssl/private/example.com.key;
    
    # HSTS with preload
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    
    # Content Security Policy
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'" always;
    
    # Other security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    location / {
        root /var/www/html;
    }
}
```

### 3. HTTP to HTTPS Redirect:
```nginx
# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name example.com www.example.com;
    return 301 https://$server_name$request_uri;
}

# HTTPS server
server {
    listen 443 ssl http2;
    server_name example.com www.example.com;
    
    ssl_certificate /etc/ssl/certs/example.com.crt;
    ssl_certificate_key /etc/ssl/private/example.com.key;
    
    location / {
        root /var/www/html;
    }
}
```

### 4. Certificate Auto-Renewal:
```bash
# Certbot auto-renewal
sudo crontab -e

# Add this line for daily renewal check
0 12 * * * /usr/bin/certbot renew --quiet --nginx

# Test renewal
sudo certbot renew --dry-run
```

### 5. SSL Monitoring:
```nginx
# SSL status endpoint
server {
    listen 443 ssl http2;
    server_name example.com;
    
    ssl_certificate /etc/ssl/certs/example.com.crt;
    ssl_certificate_key /etc/ssl/private/example.com.key;
    
    # SSL status endpoint
    location /ssl-status {
        access_log off;
        return 200 "SSL: $ssl_protocol\nCipher: $ssl_cipher\n";
        add_header Content-Type text/plain;
    }
    
    location / {
        root /var/www/html;
    }
}
```

## 7.6 SSL Testing

### 1. Basic SSL Test:
```bash
# Test SSL connection
openssl s_client -connect example.com:443 -servername example.com

# Test specific TLS version
openssl s_client -connect example.com:443 -tls1_2

# Test certificate validity
openssl s_client -connect example.com:443 -showcerts
```

### 2. SSL Labs Testing:
```bash
# Online SSL testing
curl -s "https://api.ssllabs.com/api/v3/analyze?host=example.com"

# Test specific endpoint
curl -s "https://api.ssllabs.com/api/v3/analyze?host=example.com&publish=on&startNew=on"
```

### 3. Certificate Testing:
```bash
# Check certificate expiration
echo | openssl s_client -servername example.com -connect example.com:443 2>/dev/null | openssl x509 -noout -dates

# Check certificate chain
echo | openssl s_client -servername example.com -connect example.com:443 2>/dev/null | openssl x509 -noout -text

# Test certificate installation
curl -I https://example.com/
```

### 4. Performance Testing:
```bash
# Test SSL handshake performance
time openssl s_client -connect example.com:443 -servername example.com < /dev/null

# Test with different cipher suites
openssl s_client -connect example.com:443 -cipher ECDHE-RSA-AES256-GCM-SHA384
```

## 7.7 SSL Performance

### 1. SSL Session Caching:
```nginx
# Optimize SSL session caching
server {
    listen 443 ssl http2;
    server_name example.com;
    
    ssl_certificate /etc/ssl/certs/example.com.crt;
    ssl_certificate_key /etc/ssl/private/example.com.key;
    
    # Session caching
    ssl_session_cache shared:SSL:50m;
    ssl_session_timeout 1d;
    ssl_session_tickets off;
    
    location / {
        root /var/www/html;
    }
}
```

### 2. SSL Buffer Optimization:
```nginx
# Optimize SSL buffers
server {
    listen 443 ssl http2;
    server_name example.com;
    
    ssl_certificate /etc/ssl/certs/example.com.crt;
    ssl_certificate_key /etc/ssl/private/example.com.key;
    
    # Buffer optimization
    ssl_buffer_size 8k;
    
    # Early data (TLS 1.3)
    ssl_early_data on;
    
    location / {
        root /var/www/html;
    }
}
```

### 3. OCSP Stapling:
```nginx
# Enable OCSP stapling for performance
server {
    listen 443 ssl http2;
    server_name example.com;
    
    ssl_certificate /etc/ssl/certs/example.com.crt;
    ssl_certificate_key /etc/ssl/private/example.com.key;
    
    # OCSP stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    ssl_trusted_certificate /etc/ssl/certs/ca-bundle.crt;
    ssl_stapling_file /var/cache/nginx/ocsp.der;
    
    location / {
        root /var/www/html;
    }
}
```

### 4. HTTP/2 with SSL:
```nginx
# Enable HTTP/2 for better performance
server {
    listen 443 ssl http2;
    server_name example.com;
    
    ssl_certificate /etc/ssl/certs/example.com.crt;
    ssl_certificate_key /etc/ssl/private/example.com.key;
    
    # HTTP/2 settings
    http2_max_field_size 4k;
    http2_max_header_size 16k;
    http2_max_requests 1000;
    
    location / {
        root /var/www/html;
    }
}
```

## 7.8 SSL Troubleshooting

### 1. Common SSL Issues:

#### Certificate Errors:
```bash
# Check certificate validity
openssl x509 -in certificate.crt -text -noout

# Verify certificate chain
openssl verify -CAfile ca-bundle.crt certificate.crt

# Check certificate expiration
openssl x509 -in certificate.crt -noout -dates
```

#### Protocol Errors:
```bash
# Test SSL protocols
openssl s_client -connect example.com:443 -tls1_2
openssl s_client -connect example.com:443 -tls1_3

# Check supported protocols
nmap --script ssl-enum-ciphers -p 443 example.com
```

#### Cipher Suite Issues:
```bash
# Test specific cipher suites
openssl s_client -connect example.com:443 -cipher ECDHE-RSA-AES256-GCM-SHA384

# List supported cipher suites
openssl ciphers -v
```

### 2. Debug SSL Configuration:
```nginx
# Enable SSL debug logging
error_log /var/log/nginx/ssl_debug.log debug;

server {
    listen 443 ssl http2;
    server_name example.com;
    
    ssl_certificate /etc/ssl/certs/example.com.crt;
    ssl_certificate_key /etc/ssl/private/example.com.key;
    
    # Debug headers
    add_header X-SSL-Protocol $ssl_protocol;
    add_header X-SSL-Cipher $ssl_cipher;
    
    location / {
        root /var/www/html;
    }
}
```

### 3. SSL Monitoring:
```bash
# Monitor SSL connections
ss -tuln | grep :443

# Check SSL certificate status
curl -I https://example.com/

# Monitor SSL errors
tail -f /var/log/nginx/error.log | grep ssl
```

## 7.9 SSL Security

### 1. Security Hardening:
```nginx
# Hardened SSL configuration
server {
    listen 443 ssl http2;
    server_name example.com;
    
    ssl_certificate /etc/ssl/certs/example.com.crt;
    ssl_certificate_key /etc/ssl/private/example.com.key;
    
    # Only secure protocols
    ssl_protocols TLSv1.2 TLSv1.3;
    
    # Strong cipher suites
    ssl_ciphers ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305;
    ssl_prefer_server_ciphers off;
    
    # Perfect Forward Secrecy
    ssl_ecdh_curve secp384r1;
    
    # OCSP stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    ssl_trusted_certificate /etc/ssl/certs/ca-bundle.crt;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    location / {
        root /var/www/html;
    }
}
```

### 2. Certificate Pinning:
```nginx
# Certificate pinning
server {
    listen 443 ssl http2;
    server_name example.com;
    
    ssl_certificate /etc/ssl/certs/example.com.crt;
    ssl_certificate_key /etc/ssl/private/example.com.key;
    
    # Certificate pinning
    add_header Public-Key-Pins 'pin-sha256="base64+primary=="; pin-sha256="base64+backup=="; max-age=2592000; includeSubDomains' always;
    
    location / {
        root /var/www/html;
    }
}
```

### 3. DDoS Protection:
```nginx
# SSL DDoS protection
limit_req_zone $binary_remote_addr zone=ssl:10m rate=1r/s;

server {
    listen 443 ssl http2;
    server_name example.com;
    
    ssl_certificate /etc/ssl/certs/example.com.crt;
    ssl_certificate_key /etc/ssl/private/example.com.key;
    
    # Rate limiting
    limit_req zone=ssl burst=5 nodelay;
    
    location / {
        root /var/www/html;
    }
}
```

## 7.10 SSL Documentation

### 1. Configuration Documentation:
```nginx
# =============================================================================
# SSL/TLS Configuration Documentation
# =============================================================================
# 
# File: /etc/nginx/sites-available/example.com
# Purpose: SSL/TLS configuration for example.com
# Last Modified: 2024-01-15
# 
# =============================================================================
# SSL Configuration Overview
# =============================================================================
# 
# This configuration provides:
# - TLS 1.2 and 1.3 support
# - Modern cipher suites
# - OCSP stapling
# - HSTS with preload
# - Security headers
# 
# =============================================================================
# Certificate Information
# =============================================================================
# 
# Certificate: /etc/ssl/certs/example.com.crt
# Private Key: /etc/ssl/private/example.com.key
# CA Bundle: /etc/ssl/certs/ca-bundle.crt
# 
# =============================================================================

server {
    listen 443 ssl http2;
    server_name example.com;
    
    # Certificate files
    ssl_certificate /etc/ssl/certs/example.com.crt;
    ssl_certificate_key /etc/ssl/private/example.com.key;
    
    # SSL protocols
    ssl_protocols TLSv1.2 TLSv1.3;
    
    # Cipher suites
    ssl_ciphers ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    
    # Session management
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 1d;
    ssl_session_tickets off;
    
    # OCSP stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    ssl_trusted_certificate /etc/ssl/certs/ca-bundle.crt;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    
    location / {
        root /var/www/html;
    }
}
```

### 2. Maintenance Procedures:
```bash
# Certificate renewal procedure
#!/bin/bash
# SSL Certificate Renewal Script

echo "Starting SSL certificate renewal..."

# Check certificate expiration
CERT_EXPIRY=$(openssl x509 -enddate -noout -in /etc/ssl/certs/example.com.crt | cut -d= -f2)
CERT_EXPIRY_EPOCH=$(date -d "$CERT_EXPIRY" +%s)
CURRENT_EPOCH=$(date +%s)
DAYS_UNTIL_EXPIRY=$(( (CERT_EXPIRY_EPOCH - CURRENT_EPOCH) / 86400 ))

echo "Certificate expires in $DAYS_UNTIL_EXPIRY days"

if [ $DAYS_UNTIL_EXPIRY -lt 30 ]; then
    echo "Certificate expires soon, renewing..."
    certbot renew --nginx --quiet
    nginx -s reload
    echo "Certificate renewed and Nginx reloaded"
else
    echo "Certificate is still valid"
fi
```

### 3. Monitoring and Alerting:
```bash
# SSL monitoring script
#!/bin/bash
# SSL Certificate Monitoring

DOMAIN="example.com"
CERT_PATH="/etc/ssl/certs/example.com.crt"
ALERT_DAYS=30

# Check certificate expiration
CERT_EXPIRY=$(openssl x509 -enddate -noout -in $CERT_PATH | cut -d= -f2)
CERT_EXPIRY_EPOCH=$(date -d "$CERT_EXPIRY" +%s)
CURRENT_EPOCH=$(date +%s)
DAYS_UNTIL_EXPIRY=$(( (CERT_EXPIRY_EPOCH - CURRENT_EPOCH) / 86400 ))

if [ $DAYS_UNTIL_EXPIRY -lt $ALERT_DAYS ]; then
    echo "ALERT: SSL certificate for $DOMAIN expires in $DAYS_UNTIL_EXPIRY days"
    # Send alert notification
    # mail -s "SSL Certificate Expiry Alert" admin@example.com
fi

# Check SSL configuration
echo "Testing SSL configuration..."
curl -I https://$DOMAIN/ > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "SSL configuration is working correctly"
else
    echo "ERROR: SSL configuration test failed"
fi
```