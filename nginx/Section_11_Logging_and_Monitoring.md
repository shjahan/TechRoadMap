# Section 11 - Logging and Monitoring

## 11.1 Logging Concepts

Logging in Nginx involves recording information about requests, responses, errors, and system events to help with debugging, monitoring, and analysis.

### Key Logging Concepts:
- **Access Logs**: Record information about client requests
- **Error Logs**: Record errors and warnings
- **Custom Logs**: User-defined log formats for specific needs
- **Log Rotation**: Managing log file size and retention
- **Log Analysis**: Extracting insights from log data
- **Real-time Monitoring**: Watching logs as they happen

### Real-world Analogy:
Logging is like a security camera system that:
- Records all activities (access logs)
- Alerts when problems occur (error logs)
- Provides different views of the same events (custom logs)
- Automatically manages storage space (log rotation)
- Helps identify patterns and issues (log analysis)
- Allows real-time monitoring of activities (real-time monitoring)

### Types of Logs in Nginx:
1. **Access Logs**: HTTP requests and responses
2. **Error Logs**: System errors and warnings
3. **Debug Logs**: Detailed debugging information
4. **Custom Logs**: Application-specific logging

### Example Basic Logging:
```nginx
# Basic logging configuration
http {
    # Access log format
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';
    
    # Error log
    error_log /var/log/nginx/error.log;
    
    # Access log
    access_log /var/log/nginx/access.log main;
    
    server {
        listen 80;
        server_name example.com;
        
        location / {
            root /var/www/html;
        }
    }
}
```

## 11.2 Access Logs

Access logs record information about client requests, including IP addresses, request methods, response codes, and more.

### Basic Access Log Configuration:
```nginx
# Basic access log
http {
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';
    
    access_log /var/log/nginx/access.log main;
    
    server {
        listen 80;
        server_name example.com;
        
        location / {
            root /var/www/html;
        }
    }
}
```

### Advanced Access Log Configuration:
```nginx
# Advanced access log with detailed information
http {
    # Detailed log format
    log_format detailed '$remote_addr - $remote_user [$time_local] '
                       '"$request" $status $body_bytes_sent '
                       '"$http_referer" "$http_user_agent" '
                       'rt=$request_time uct="$upstream_connect_time" '
                       'uht="$upstream_header_time" urt="$upstream_response_time" '
                       'upstream_addr="$upstream_addr" '
                       'upstream_status="$upstream_status"';
    
    # JSON log format
    log_format json_combined escape=json
        '{'
            '"time_local":"$time_local",'
            '"remote_addr":"$remote_addr",'
            '"remote_user":"$remote_user",'
            '"request":"$request",'
            '"status": "$status",'
            '"body_bytes_sent":"$body_bytes_sent",'
            '"request_time":"$request_time",'
            '"http_referrer":"$http_referer",'
            '"http_user_agent":"$http_user_agent"'
        '}';
    
    # Performance log format
    log_format performance '$remote_addr - $remote_user [$time_local] '
                          '"$request" $status $body_bytes_sent '
                          'rt=$request_time uct="$upstream_connect_time" '
                          'uht="$upstream_header_time" urt="$upstream_response_time"';
    
    server {
        listen 80;
        server_name example.com;
        
        # Detailed logging
        access_log /var/log/nginx/access.log detailed;
        
        # JSON logging
        access_log /var/log/nginx/access.json json_combined;
        
        # Performance logging
        access_log /var/log/nginx/performance.log performance;
        
        location / {
            root /var/www/html;
        }
    }
}
```

### Conditional Access Logging:
```nginx
# Conditional access logging
map $status $loggable {
    ~^[23] 0;
    default 1;
}

server {
    listen 80;
    server_name example.com;
    
    # Log only errors and redirects
    access_log /var/log/nginx/access.log main if=$loggable;
    
    # Log all requests to a separate file
    access_log /var/log/nginx/all_requests.log main;
    
    location / {
        root /var/www/html;
    }
}
```

### Access Log Variables:
```nginx
# Common access log variables
log_format custom '$remote_addr - $remote_user [$time_local] '
                  '"$request" $status $body_bytes_sent '
                  '"$http_referer" "$http_user_agent" '
                  'rt=$request_time uct="$upstream_connect_time" '
                  'uht="$upstream_header_time" urt="$upstream_response_time" '
                  'upstream_addr="$upstream_addr" '
                  'upstream_status="$upstream_status" '
                  'request_id="$request_id" '
                  'connection="$connection" '
                  'connection_requests="$connection_requests"';
```

## 11.3 Error Logs

Error logs record system errors, warnings, and debugging information.

### Basic Error Log Configuration:
```nginx
# Basic error log
error_log /var/log/nginx/error.log;

# Error log with level
error_log /var/log/nginx/error.log warn;

# Error log levels: debug, info, notice, warn, error, crit, alert, emerg
```

### Advanced Error Log Configuration:
```nginx
# Advanced error log configuration
http {
    # Global error log
    error_log /var/log/nginx/error.log warn;
    
    server {
        listen 80;
        server_name example.com;
        
        # Server-specific error log
        error_log /var/log/nginx/example.com.error.log;
        
        location / {
            root /var/www/html;
        }
    }
    
    server {
        listen 80;
        server_name api.example.com;
        
        # API-specific error log
        error_log /var/log/nginx/api.error.log;
        
        location / {
            proxy_pass http://backend;
        }
    }
}
```

### Debug Error Logging:
```nginx
# Debug error logging
error_log /var/log/nginx/debug.log debug;

# Debug logging for specific server
server {
    listen 80;
    server_name example.com;
    
    # Debug logging
    error_log /var/log/nginx/example.com.debug.log debug;
    
    location / {
        root /var/www/html;
    }
}
```

### Error Log Analysis:
```bash
# Analyze error logs
grep "error" /var/log/nginx/error.log | tail -10
grep "warn" /var/log/nginx/error.log | tail -10
grep "crit" /var/log/nginx/error.log | tail -10

# Count error types
grep "error" /var/log/nginx/error.log | awk '{print $4}' | sort | uniq -c
```

## 11.4 Log Configuration

Log configuration involves setting up log formats, destinations, and rotation policies.

### Log Format Configuration:
```nginx
# Multiple log formats
http {
    # Basic format
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';
    
    # Detailed format
    log_format detailed '$remote_addr - $remote_user [$time_local] '
                       '"$request" $status $body_bytes_sent '
                       '"$http_referer" "$http_user_agent" '
                       'rt=$request_time uct="$upstream_connect_time" '
                       'uht="$upstream_header_time" urt="$upstream_response_time"';
    
    # JSON format
    log_format json_combined escape=json
        '{'
            '"time_local":"$time_local",'
            '"remote_addr":"$remote_addr",'
            '"request":"$request",'
            '"status": "$status",'
            '"body_bytes_sent":"$body_bytes_sent"'
        '}';
    
    # Performance format
    log_format performance '$remote_addr [$time_local] '
                          '"$request" $status $body_bytes_sent '
                          'rt=$request_time uct="$upstream_connect_time" '
                          'urt="$upstream_response_time"';
}
```

### Log Destination Configuration:
```nginx
# Multiple log destinations
server {
    listen 80;
    server_name example.com;
    
    # Multiple access logs
    access_log /var/log/nginx/access.log main;
    access_log /var/log/nginx/performance.log performance;
    access_log /var/log/nginx/security.log security;
    
    # Error logs
    error_log /var/log/nginx/error.log warn;
    error_log /var/log/nginx/debug.log debug;
    
    location / {
        root /var/www/html;
    }
}
```

### Log Rotation Configuration:
```bash
# Logrotate configuration for Nginx
# /etc/logrotate.d/nginx
/var/log/nginx/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 640 nginx adm
    sharedscripts
    postrotate
        if [ -f /var/run/nginx.pid ]; then
            kill -USR1 $(cat /var/run/nginx.pid)
        fi
    endscript
}
```

## 11.5 Log Analysis

Log analysis involves extracting insights and patterns from log data.

### Basic Log Analysis:
```bash
# Basic log analysis commands
# Count requests by status code
awk '{print $9}' /var/log/nginx/access.log | sort | uniq -c | sort -nr

# Count requests by IP
awk '{print $1}' /var/log/nginx/access.log | sort | uniq -c | sort -nr | head -10

# Count requests by user agent
awk -F'"' '{print $6}' /var/log/nginx/access.log | sort | uniq -c | sort -nr | head -10

# Count requests by hour
awk '{print $4}' /var/log/nginx/access.log | cut -d: -f2 | sort | uniq -c
```

### Advanced Log Analysis:
```bash
# Advanced log analysis script
#!/bin/bash

LOG_FILE="/var/log/nginx/access.log"
DATE=$(date +%Y-%m-%d)

echo "=== Nginx Log Analysis for $DATE ==="
echo ""

# Total requests
TOTAL_REQUESTS=$(wc -l < $LOG_FILE)
echo "Total requests: $TOTAL_REQUESTS"

# Requests by status code
echo ""
echo "Requests by status code:"
awk '{print $9}' $LOG_FILE | sort | uniq -c | sort -nr

# Top IPs
echo ""
echo "Top 10 IPs:"
awk '{print $1}' $LOG_FILE | sort | uniq -c | sort -nr | head -10

# Top user agents
echo ""
echo "Top 10 User Agents:"
awk -F'"' '{print $6}' $LOG_FILE | sort | uniq -c | sort -nr | head -10

# Requests by hour
echo ""
echo "Requests by hour:"
awk '{print $4}' $LOG_FILE | cut -d: -f2 | sort | uniq -c | sort -n

# Average response time
echo ""
echo "Average response time:"
awk '{print $NF}' $LOG_FILE | awk '{sum+=$1; count++} END {print sum/count " seconds"}'
```

### Log Analysis with AWK:
```bash
# AWK-based log analysis
#!/bin/awk -f
# log_analysis.awk

BEGIN {
    total_requests = 0
    total_bytes = 0
    status_codes[200] = 0
    status_codes[404] = 0
    status_codes[500] = 0
}

{
    total_requests++
    total_bytes += $10
    status_codes[$9]++
}

END {
    print "Total requests: " total_requests
    print "Total bytes: " total_bytes
    print "Average bytes per request: " total_bytes/total_requests
    print "Status 200: " status_codes[200]
    print "Status 404: " status_codes[404]
    print "Status 500: " status_codes[500]
}
```

### Log Analysis with Python:
```python
#!/usr/bin/env python3
# log_analysis.py

import re
from collections import Counter
from datetime import datetime

def parse_log_line(line):
    """Parse a single log line"""
    pattern = r'(\d+\.\d+\.\d+\.\d+) - - \[(.*?)\] "(.*?)" (\d+) (\d+) "(.*?)" "(.*?)"'
    match = re.match(pattern, line)
    if match:
        return {
            'ip': match.group(1),
            'timestamp': match.group(2),
            'request': match.group(3),
            'status': int(match.group(4)),
            'bytes': int(match.group(5)),
            'referer': match.group(6),
            'user_agent': match.group(7)
        }
    return None

def analyze_logs(log_file):
    """Analyze Nginx access logs"""
    requests = []
    
    with open(log_file, 'r') as f:
        for line in f:
            parsed = parse_log_line(line)
            if parsed:
                requests.append(parsed)
    
    # Basic statistics
    total_requests = len(requests)
    total_bytes = sum(r['bytes'] for r in requests)
    
    # Status codes
    status_codes = Counter(r['status'] for r in requests)
    
    # Top IPs
    top_ips = Counter(r['ip'] for r in requests)
    
    # Top user agents
    top_user_agents = Counter(r['user_agent'] for r in requests)
    
    print(f"Total requests: {total_requests}")
    print(f"Total bytes: {total_bytes}")
    print(f"Average bytes per request: {total_bytes/total_requests:.2f}")
    print(f"Status codes: {dict(status_codes.most_common())}")
    print(f"Top 10 IPs: {dict(top_ips.most_common(10))}")
    print(f"Top 10 User Agents: {dict(top_user_agents.most_common(10))}")

if __name__ == "__main__":
    analyze_logs('/var/log/nginx/access.log')
```

## 11.6 Logging Best Practices

### 1. Log Format Standardization:
```nginx
# Standardized log formats
http {
    # Standard access log format
    log_format standard '$remote_addr - $remote_user [$time_local] '
                       '"$request" $status $body_bytes_sent '
                       '"$http_referer" "$http_user_agent" '
                       '"$http_x_forwarded_for"';
    
    # Performance log format
    log_format performance '$remote_addr [$time_local] '
                          '"$request" $status $body_bytes_sent '
                          'rt=$request_time uct="$upstream_connect_time" '
                          'urt="$upstream_response_time"';
    
    # Security log format
    log_format security '$remote_addr - $remote_user [$time_local] '
                       '"$request" $status $body_bytes_sent '
                       '"$http_referer" "$http_user_agent" '
                       'rt=$request_time';
}
```

### 2. Log Rotation Strategy:
```bash
# Comprehensive log rotation
# /etc/logrotate.d/nginx
/var/log/nginx/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 640 nginx adm
    sharedscripts
    prerotate
        if [ -d /etc/logrotate.d/httpd-prerotate ]; then
            run-parts /etc/logrotate.d/httpd-prerotate
        fi
    endscript
    postrotate
        if [ -f /var/run/nginx.pid ]; then
            kill -USR1 $(cat /var/run/nginx.pid)
        fi
    endscript
}
```

### 3. Log Security:
```nginx
# Secure logging configuration
server {
    listen 80;
    server_name example.com;
    
    # Log sensitive information
    access_log /var/log/nginx/access.log standard;
    
    # Don't log sensitive endpoints
    location /admin {
        access_log off;
        # Admin handling
    }
    
    # Log security events
    location /login {
        access_log /var/log/nginx/security.log security;
        # Login handling
    }
}
```

### 4. Log Monitoring:
```bash
# Log monitoring script
#!/bin/bash

LOG_FILE="/var/log/nginx/access.log"
ERROR_LOG="/var/log/nginx/error.log"
ALERT_EMAIL="admin@example.com"

# Monitor for high error rates
ERROR_COUNT=$(grep " 5[0-9][0-9] " $LOG_FILE | wc -l)
TOTAL_REQUESTS=$(wc -l < $LOG_FILE)

if [ $TOTAL_REQUESTS -gt 0 ]; then
    ERROR_RATE=$((ERROR_COUNT * 100 / TOTAL_REQUESTS))
    if [ $ERROR_RATE -gt 10 ]; then
        echo "High error rate detected: $ERROR_RATE%" | mail -s "Nginx Error Alert" $ALERT_EMAIL
    fi
fi

# Monitor for suspicious activity
SUSPICIOUS_IPS=$(awk '{print $1}' $LOG_FILE | sort | uniq -c | sort -nr | head -5)
echo "Top IPs: $SUSPICIOUS_IPS"
```

## 11.7 Logging Testing

### 1. Log Format Testing:
```bash
# Test log format
curl http://example.com/
tail -1 /var/log/nginx/access.log

# Test different log formats
curl -H "User-Agent: TestBot" http://example.com/
curl -H "X-Forwarded-For: 192.168.1.100" http://example.com/
```

### 2. Log Rotation Testing:
```bash
# Test log rotation
sudo logrotate -d /etc/logrotate.d/nginx

# Force log rotation
sudo logrotate -f /etc/logrotate.d/nginx
```

### 3. Log Analysis Testing:
```bash
# Test log analysis scripts
./log_analysis.sh
python3 log_analysis.py
```

## 11.8 Logging Performance

### 1. Log Performance Optimization:
```nginx
# Optimized logging configuration
http {
    # Use syslog for better performance
    access_log syslog:server=127.0.0.1:514,facility=local7,tag=nginx,severity=info main;
    
    # Buffer logs for better performance
    access_log /var/log/nginx/access.log main buffer=64k flush=5s;
    
    # Disable logging for static files
    location ~* \.(css|js|png|jpg|jpeg|gif|ico|svg)$ {
        access_log off;
        expires 1y;
    }
}
```

### 2. Log Performance Monitoring:
```bash
# Monitor log performance
iostat -x 1
iotop -p $(pgrep nginx)
```

## 11.9 Logging Troubleshooting

### 1. Common Logging Issues:

#### Logs Not Being Written:
```bash
# Check log file permissions
ls -la /var/log/nginx/
sudo chown nginx:nginx /var/log/nginx/*.log
sudo chmod 644 /var/log/nginx/*.log
```

#### Log Rotation Issues:
```bash
# Check logrotate configuration
sudo logrotate -d /etc/logrotate.d/nginx

# Check logrotate status
sudo logrotate -s /var/lib/logrotate/status
```

#### Log Analysis Issues:
```bash
# Check log format
nginx -T | grep log_format

# Test log parsing
head -1 /var/log/nginx/access.log | awk '{print $1}'
```

### 2. Log Debugging:
```bash
# Debug logging issues
tail -f /var/log/nginx/error.log
grep "log" /var/log/nginx/error.log
```

## 11.10 Logging Security

### 1. Log Access Control:
```bash
# Secure log files
sudo chown nginx:nginx /var/log/nginx/
sudo chmod 750 /var/log/nginx/
sudo chmod 640 /var/log/nginx/*.log
```

### 2. Log Encryption:
```bash
# Encrypt log files
sudo gpg --symmetric --cipher-algo AES256 /var/log/nginx/access.log
```

### 3. Log Integrity:
```bash
# Verify log integrity
md5sum /var/log/nginx/access.log
sha256sum /var/log/nginx/access.log
```

### 4. Log Retention Policy:
```bash
# Log retention script
#!/bin/bash

LOG_DIR="/var/log/nginx"
RETENTION_DAYS=30

# Remove old log files
find $LOG_DIR -name "*.log.*" -mtime +$RETENTION_DAYS -delete

# Compress old logs
find $LOG_DIR -name "*.log.*" -mtime +7 -exec gzip {} \;
```