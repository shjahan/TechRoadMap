# Section 20 - Nginx Troubleshooting

## 20.1 Troubleshooting Concepts

Troubleshooting Nginx involves systematically identifying, diagnosing, and resolving issues that prevent Nginx from functioning correctly or performing optimally.

### Key Concepts:
- **Systematic Approach**: Following a structured methodology to identify problems
- **Log Analysis**: Using logs to understand what's happening
- **Performance Monitoring**: Identifying bottlenecks and performance issues
- **Configuration Validation**: Ensuring configurations are correct and optimal
- **Network Diagnostics**: Checking connectivity and network-related issues
- **Resource Monitoring**: Monitoring CPU, memory, and disk usage
- **Error Classification**: Categorizing and prioritizing different types of errors

### Real-world Analogy:
Think of Nginx troubleshooting like being a detective:
- **Evidence Collection** is like gathering logs and metrics
- **Hypothesis Formation** is like developing theories about what went wrong
- **Testing** is like running experiments to verify theories
- **Solution Implementation** is like making the arrest and fixing the problem

### Troubleshooting Framework:
```
Problem Identification → Data Collection → Analysis → Hypothesis → Testing → Solution
         ↓                    ↓           ↓         ↓         ↓        ↓
    Error Messages        Logs, Metrics  Patterns  Theories  Validation  Fix
```

## 20.2 Common Issues

### 1. Configuration Issues:
```bash
# Common configuration problems
nginx -t
# nginx: [emerg] unexpected "}" in /etc/nginx/nginx.conf:45

# Solution: Check syntax
nginx -t -c /etc/nginx/nginx.conf

# Check specific configuration
nginx -T | grep -i error
```

### 2. Permission Issues:
```bash
# Permission problems
# nginx: [emerg] open() "/var/log/nginx/access.log" failed (13: Permission denied)

# Solution: Fix permissions
sudo chown -R nginx:nginx /var/log/nginx
sudo chmod 755 /var/log/nginx
sudo chmod 644 /var/log/nginx/*.log
```

### 3. Port Conflicts:
```bash
# Port already in use
# nginx: [emerg] bind() to 0.0.0.0:80 failed (98: Address already in use)

# Solution: Check what's using the port
sudo netstat -tlnp | grep :80
sudo lsof -i :80

# Kill the process or change Nginx port
sudo kill -9 <PID>
```

### 4. File Not Found:
```bash
# Missing files
# nginx: [emerg] open() "/etc/nginx/nginx.conf" failed (2: No such file or directory)

# Solution: Check file existence
ls -la /etc/nginx/nginx.conf
sudo find / -name "nginx.conf" 2>/dev/null
```

## 20.3 Configuration Issues

### 1. Syntax Errors:
```bash
# Test configuration syntax
nginx -t

# Common syntax errors:
# - Missing semicolons
# - Unmatched braces
# - Invalid directives
# - Wrong context usage

# Example of fixing syntax errors
# Before (incorrect):
server {
    listen 80
    server_name example.com
    root /var/www/html
}

# After (correct):
server {
    listen 80;
    server_name example.com;
    root /var/www/html;
}
```

### 2. Context Errors:
```bash
# Check configuration context
nginx -T | grep -A 5 -B 5 "error"

# Common context errors:
# - Directives in wrong context
# - Missing required contexts
# - Invalid context nesting

# Example of context error:
# This is wrong (directive in wrong context):
events {
    worker_processes auto;  # This should be in main context
}

# This is correct:
worker_processes auto;
events {
    worker_connections 1024;
}
```

### 3. Include Errors:
```bash
# Check included files
nginx -T | grep include

# Common include errors:
# - Missing files
# - Invalid file paths
# - Circular includes

# Example of fixing include errors
# Check if included files exist
ls -la /etc/nginx/conf.d/
ls -la /etc/nginx/sites-enabled/

# Fix missing files
sudo touch /etc/nginx/conf.d/default.conf
sudo chmod 644 /etc/nginx/conf.d/default.conf
```

## 20.4 Performance Issues

### 1. High CPU Usage:
```bash
# Check CPU usage
top -p $(pgrep nginx)
htop -p $(pgrep nginx)

# Check for CPU-intensive operations
grep -i "cpu" /var/log/nginx/error.log

# Solutions:
# - Optimize worker processes
# - Check for inefficient configurations
# - Monitor upstream servers
```

### 2. High Memory Usage:
```bash
# Check memory usage
free -h
ps aux --sort=-%mem | head -10

# Check Nginx memory usage
pmap $(pgrep nginx)

# Solutions:
# - Optimize buffer sizes
# - Check for memory leaks
# - Monitor upstream connections
```

### 3. Slow Response Times:
```bash
# Check response times
curl -w "@curl-format.txt" -o /dev/null -s http://example.com/

# Check upstream response times
grep "upstream_response_time" /var/log/nginx/access.log | tail -10

# Solutions:
# - Optimize upstream servers
# - Check network connectivity
# - Review caching configuration
```

### 4. Connection Issues:
```bash
# Check connection limits
ss -tuln | grep :80
netstat -an | grep :80 | wc -l

# Check worker connections
nginx -T | grep worker_connections

# Solutions:
# - Increase worker connections
# - Optimize keep-alive settings
# - Check upstream server health
```

## 20.5 Debugging Techniques

### 1. Enable Debug Logging:
```nginx
# Enable debug logging
error_log /var/log/nginx/debug.log debug;

# Or for specific server
server {
    listen 80;
    server_name example.com;
    
    error_log /var/log/nginx/example.com.debug.log debug;
    
    location / {
        root /var/www/html;
    }
}
```

### 2. Use Debug Headers:
```nginx
# Add debug headers
server {
    listen 80;
    server_name example.com;
    
    # Debug headers
    add_header X-Response-Time $request_time;
    add_header X-Upstream-Response-Time $upstream_response_time;
    add_header X-Connection-Count $connection_active;
    add_header X-Request-ID $request_id;
    
    location / {
        root /var/www/html;
    }
}
```

### 3. Monitor Real-time:
```bash
# Monitor logs in real-time
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log

# Monitor specific patterns
tail -f /var/log/nginx/access.log | grep "404"
tail -f /var/log/nginx/error.log | grep "error"
```

### 4. Test Configuration:
```bash
# Test configuration changes
nginx -t

# Test with specific configuration
nginx -t -c /etc/nginx/nginx.conf

# Test with different user
nginx -t -u nginx
```

## 20.6 Troubleshooting Tools

### 1. Built-in Tools:
```bash
# Nginx built-in tools
nginx -t                    # Test configuration
nginx -T                    # Show full configuration
nginx -s reload             # Reload configuration
nginx -s quit               # Graceful shutdown
nginx -s reopen             # Reopen log files
nginx -s stop               # Stop Nginx
```

### 2. System Tools:
```bash
# System monitoring tools
top                         # Process monitoring
htop                        # Enhanced process monitoring
ps                          # Process status
netstat                     # Network connections
ss                          # Socket statistics
lsof                        # List open files
strace                      # System call tracing
```

### 3. Network Tools:
```bash
# Network debugging tools
curl                        # HTTP client
wget                        # HTTP client
telnet                      # Network connectivity
ping                        # Network connectivity
traceroute                  # Network path tracing
nmap                        # Network scanning
```

### 4. Log Analysis Tools:
```bash
# Log analysis tools
grep                        # Text search
awk                         # Text processing
sed                         # Text editing
tail                        # Log tailing
head                        # Log head
sort                        # Text sorting
uniq                        # Unique lines
```

## 20.7 Troubleshooting Best Practices

### 1. Systematic Approach:
```bash
#!/bin/bash
# Systematic troubleshooting script

echo "Nginx Troubleshooting Checklist"
echo "=============================="

# 1. Check if Nginx is running
echo "1. Checking if Nginx is running..."
if systemctl is-active --quiet nginx; then
    echo "   ✓ Nginx is running"
else
    echo "   ✗ Nginx is not running"
    echo "   Solution: sudo systemctl start nginx"
    exit 1
fi

# 2. Check configuration
echo "2. Checking configuration..."
if nginx -t > /dev/null 2>&1; then
    echo "   ✓ Configuration is valid"
else
    echo "   ✗ Configuration has errors"
    echo "   Solution: nginx -t (check output for errors)"
    exit 1
fi

# 3. Check ports
echo "3. Checking ports..."
if netstat -tlnp | grep -q ":80 "; then
    echo "   ✓ Port 80 is listening"
else
    echo "   ✗ Port 80 is not listening"
    echo "   Solution: Check Nginx configuration and restart"
fi

# 4. Check logs
echo "4. Checking logs..."
if [ -f /var/log/nginx/error.log ]; then
    echo "   Recent error logs:"
    tail -5 /var/log/nginx/error.log
else
    echo "   ✗ Error log file not found"
fi

# 5. Check performance
echo "5. Checking performance..."
RESPONSE_TIME=$(curl -w "%{time_total}" -o /dev/null -s http://localhost/ 2>/dev/null)
if [ $? -eq 0 ]; then
    echo "   ✓ Response time: ${RESPONSE_TIME}s"
else
    echo "   ✗ Cannot connect to Nginx"
fi
```

### 2. Log Analysis:
```bash
#!/bin/bash
# Log analysis script

echo "Nginx Log Analysis"
echo "================="

# Analyze access logs
echo "1. Access Log Analysis:"
echo "   Total requests: $(wc -l < /var/log/nginx/access.log)"
echo "   Unique IPs: $(awk '{print $1}' /var/log/nginx/access.log | sort | uniq | wc -l)"
echo "   Top IPs:"
awk '{print $1}' /var/log/nginx/access.log | sort | uniq -c | sort -nr | head -5

# Analyze error logs
echo ""
echo "2. Error Log Analysis:"
if [ -f /var/log/nginx/error.log ]; then
    echo "   Total errors: $(wc -l < /var/log/nginx/error.log)"
    echo "   Recent errors:"
    tail -5 /var/log/nginx/error.log
else
    echo "   No error log found"
fi

# Analyze response codes
echo ""
echo "3. Response Code Analysis:"
awk '{print $9}' /var/log/nginx/access.log | sort | uniq -c | sort -nr

# Analyze response times
echo ""
echo "4. Response Time Analysis:"
awk '{print $NF}' /var/log/nginx/access.log | awk '{sum+=$1; count++} END {print "Average response time: " sum/count " seconds"}'
```

### 3. Performance Monitoring:
```bash
#!/bin/bash
# Performance monitoring script

echo "Nginx Performance Monitoring"
echo "==========================="

# System metrics
echo "1. System Metrics:"
echo "   CPU Usage: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)%"
echo "   Memory Usage: $(free | grep Mem | awk '{printf "%.1f%%", $3/$2 * 100.0}')"
echo "   Load Average: $(uptime | awk '{print $10,$11,$12}')"

# Nginx metrics
echo ""
echo "2. Nginx Metrics:"
if curl -s http://localhost/nginx_status > /dev/null 2>&1; then
    echo "   Nginx Status:"
    curl -s http://localhost/nginx_status
else
    echo "   Nginx status endpoint not available"
fi

# Connection metrics
echo ""
echo "3. Connection Metrics:"
echo "   Active connections: $(ss -tuln | grep :80 | wc -l)"
echo "   Listening ports:"
netstat -tlnp | grep nginx

# Process metrics
echo ""
echo "4. Process Metrics:"
echo "   Nginx processes: $(ps aux | grep nginx | grep -v grep | wc -l)"
echo "   Memory usage:"
ps aux --sort=-%mem | grep nginx | head -3
```

## 20.8 Troubleshooting Documentation

### 1. Issue Tracking:
```bash
#!/bin/bash
# Issue tracking script

echo "Nginx Issue Tracking"
echo "==================="

# Create issue log
ISSUE_LOG="/var/log/nginx/issues.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$TIMESTAMP] Starting issue investigation" >> $ISSUE_LOG

# Check common issues
echo "Checking common issues..."

# Check if Nginx is running
if ! systemctl is-active --quiet nginx; then
    echo "[$TIMESTAMP] ISSUE: Nginx is not running" >> $ISSUE_LOG
    echo "Solution: sudo systemctl start nginx" >> $ISSUE_LOG
fi

# Check configuration
if ! nginx -t > /dev/null 2>&1; then
    echo "[$TIMESTAMP] ISSUE: Configuration has errors" >> $ISSUE_LOG
    echo "Solution: nginx -t (check output for errors)" >> $ISSUE_LOG
fi

# Check ports
if ! netstat -tlnp | grep -q ":80 "; then
    echo "[$TIMESTAMP] ISSUE: Port 80 is not listening" >> $ISSUE_LOG
    echo "Solution: Check Nginx configuration and restart" >> $ISSUE_LOG
fi

# Check logs for errors
if [ -f /var/log/nginx/error.log ]; then
    ERROR_COUNT=$(grep -c "error" /var/log/nginx/error.log)
    if [ $ERROR_COUNT -gt 0 ]; then
        echo "[$TIMESTAMP] ISSUE: $ERROR_COUNT errors found in error log" >> $ISSUE_LOG
        echo "Solution: Check error log for details" >> $ISSUE_LOG
    fi
fi

echo "Issue investigation completed. Check $ISSUE_LOG for details."
```

### 2. Solution Database:
```bash
#!/bin/bash
# Solution database script

echo "Nginx Solution Database"
echo "======================"

# Common solutions
echo "Common Nginx Issues and Solutions:"
echo ""

echo "1. Configuration Errors:"
echo "   Problem: nginx: [emerg] unexpected '}' in /etc/nginx/nginx.conf:45"
echo "   Solution: Check syntax with 'nginx -t' and fix missing semicolons or braces"
echo ""

echo "2. Permission Denied:"
echo "   Problem: nginx: [emerg] open() '/var/log/nginx/access.log' failed (13: Permission denied)"
echo "   Solution: sudo chown -R nginx:nginx /var/log/nginx"
echo ""

echo "3. Port Already in Use:"
echo "   Problem: nginx: [emerg] bind() to 0.0.0.0:80 failed (98: Address already in use)"
echo "   Solution: sudo netstat -tlnp | grep :80 and kill the process or change Nginx port"
echo ""

echo "4. High CPU Usage:"
echo "   Problem: Nginx using too much CPU"
echo "   Solution: Check worker processes, optimize configuration, check upstream servers"
echo ""

echo "5. High Memory Usage:"
echo "   Problem: Nginx using too much memory"
echo "   Solution: Optimize buffer sizes, check for memory leaks, monitor upstream connections"
echo ""

echo "6. Slow Response Times:"
echo "   Problem: Slow response times"
echo "   Solution: Check upstream servers, optimize caching, review network connectivity"
echo ""

echo "7. 502 Bad Gateway:"
echo "   Problem: 502 Bad Gateway errors"
echo "   Solution: Check upstream servers, verify proxy configuration, check timeouts"
echo ""

echo "8. 404 Not Found:"
echo "   Problem: 404 Not Found errors"
echo "   Solution: Check root directory, verify file paths, check location blocks"
echo ""
```

## 20.9 Troubleshooting Automation

### 1. Automated Monitoring:
```bash
#!/bin/bash
# Automated monitoring script

echo "Nginx Automated Monitoring"
echo "========================="

# Configuration
ALERT_EMAIL="admin@example.com"
LOG_FILE="/var/log/nginx/monitoring.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Log function
log_message() {
    echo "[$TIMESTAMP] $1" >> $LOG_FILE
}

# Check Nginx status
if ! systemctl is-active --quiet nginx; then
    log_message "ALERT: Nginx is not running"
    echo "ALERT: Nginx is not running" | mail -s "Nginx Down Alert" $ALERT_EMAIL
fi

# Check configuration
if ! nginx -t > /dev/null 2>&1; then
    log_message "ALERT: Configuration has errors"
    echo "ALERT: Configuration has errors" | mail -s "Nginx Config Alert" $ALERT_EMAIL
fi

# Check response time
RESPONSE_TIME=$(curl -w "%{time_total}" -o /dev/null -s http://localhost/ 2>/dev/null)
if [ $? -eq 0 ]; then
    if (( $(echo "$RESPONSE_TIME > 2.0" | bc -l) )); then
        log_message "ALERT: High response time: ${RESPONSE_TIME}s"
        echo "ALERT: High response time: ${RESPONSE_TIME}s" | mail -s "Nginx Performance Alert" $ALERT_EMAIL
    fi
else
    log_message "ALERT: Cannot connect to Nginx"
    echo "ALERT: Cannot connect to Nginx" | mail -s "Nginx Connection Alert" $ALERT_EMAIL
fi

# Check error rate
if [ -f /var/log/nginx/access.log ]; then
    ERROR_COUNT=$(tail -100 /var/log/nginx/access.log | grep -c " 5[0-9][0-9] ")
    if [ $ERROR_COUNT -gt 10 ]; then
        log_message "ALERT: High error rate: $ERROR_COUNT errors in last 100 requests"
        echo "ALERT: High error rate: $ERROR_COUNT errors in last 100 requests" | mail -s "Nginx Error Alert" $ALERT_EMAIL
    fi
fi

log_message "Monitoring check completed"
```

### 2. Automated Recovery:
```bash
#!/bin/bash
# Automated recovery script

echo "Nginx Automated Recovery"
echo "======================="

# Configuration
LOG_FILE="/var/log/nginx/recovery.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Log function
log_message() {
    echo "[$TIMESTAMP] $1" >> $LOG_FILE
}

# Check if Nginx is running
if ! systemctl is-active --quiet nginx; then
    log_message "Nginx is not running, attempting to start..."
    
    # Start Nginx
    if systemctl start nginx; then
        log_message "Nginx started successfully"
    else
        log_message "Failed to start Nginx"
        exit 1
    fi
fi

# Check configuration
if ! nginx -t > /dev/null 2>&1; then
    log_message "Configuration has errors, attempting to fix..."
    
    # Try to fix common issues
    sudo chown -R nginx:nginx /var/log/nginx
    sudo chmod 755 /var/log/nginx
    sudo chmod 644 /var/log/nginx/*.log
    
    # Test configuration again
    if nginx -t > /dev/null 2>&1; then
        log_message "Configuration fixed, reloading Nginx..."
        nginx -s reload
    else
        log_message "Failed to fix configuration"
        exit 1
    fi
fi

# Check if port is listening
if ! netstat -tlnp | grep -q ":80 "; then
    log_message "Port 80 is not listening, restarting Nginx..."
    systemctl restart nginx
fi

log_message "Recovery attempt completed"
```

## 20.10 Troubleshooting Prevention

### 1. Proactive Monitoring:
```bash
#!/bin/bash
# Proactive monitoring script

echo "Nginx Proactive Monitoring"
echo "========================="

# Configuration
LOG_FILE="/var/log/nginx/proactive.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Log function
log_message() {
    echo "[$TIMESTAMP] $1" >> $LOG_FILE
}

# Monitor system resources
CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
MEMORY_USAGE=$(free | grep Mem | awk '{printf "%.1f", $3/$2 * 100.0}')

if (( $(echo "$CPU_USAGE > 80" | bc -l) )); then
    log_message "WARNING: High CPU usage: $CPU_USAGE%"
fi

if (( $(echo "$MEMORY_USAGE > 80" | bc -l) )); then
    log_message "WARNING: High memory usage: $MEMORY_USAGE%"
fi

# Monitor disk space
DISK_USAGE=$(df /var/log/nginx | awk 'NR==2{print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 80 ]; then
    log_message "WARNING: High disk usage: $DISK_USAGE%"
fi

# Monitor Nginx performance
if curl -s http://localhost/nginx_status > /dev/null 2>&1; then
    ACTIVE_CONNECTIONS=$(curl -s http://localhost/nginx_status | awk 'NR==1{print $3}')
    if [ $ACTIVE_CONNECTIONS -gt 1000 ]; then
        log_message "WARNING: High active connections: $ACTIVE_CONNECTIONS"
    fi
fi

# Monitor error rate
if [ -f /var/log/nginx/access.log ]; then
    ERROR_RATE=$(tail -1000 /var/log/nginx/access.log | grep -c " 5[0-9][0-9] ")
    if [ $ERROR_RATE -gt 50 ]; then
        log_message "WARNING: High error rate: $ERROR_RATE errors in last 1000 requests"
    fi
fi

log_message "Proactive monitoring completed"
```

### 2. Preventive Maintenance:
```bash
#!/bin/bash
# Preventive maintenance script

echo "Nginx Preventive Maintenance"
echo "==========================="

# Configuration
LOG_FILE="/var/log/nginx/maintenance.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Log function
log_message() {
    echo "[$TIMESTAMP] $1" >> $LOG_FILE
}

# 1. Check configuration
log_message "Checking configuration..."
if nginx -t > /dev/null 2>&1; then
    log_message "Configuration is valid"
else
    log_message "Configuration has errors, fixing..."
    # Fix common issues
    sudo chown -R nginx:nginx /var/log/nginx
    sudo chmod 755 /var/log/nginx
    sudo chmod 644 /var/log/nginx/*.log
fi

# 2. Rotate logs
log_message "Rotating logs..."
if [ -f /etc/logrotate.d/nginx ]; then
    logrotate -f /etc/logrotate.d/nginx
    log_message "Logs rotated successfully"
else
    log_message "Log rotation configuration not found"
fi

# 3. Check disk space
log_message "Checking disk space..."
DISK_USAGE=$(df /var/log/nginx | awk 'NR==2{print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 90 ]; then
    log_message "WARNING: Disk usage is high: $DISK_USAGE%"
    # Clean old logs
    find /var/log/nginx -name "*.log.*" -mtime +30 -delete
    log_message "Cleaned old log files"
fi

# 4. Check for updates
log_message "Checking for updates..."
if command -v apt > /dev/null 2>&1; then
    apt list --upgradable | grep nginx
elif command -v yum > /dev/null 2>&1; then
    yum check-update nginx
fi

# 5. Restart Nginx if needed
log_message "Checking if restart is needed..."
if [ -f /var/run/nginx.pid ]; then
    PID=$(cat /var/run/nginx.pid)
    if ! kill -0 $PID 2>/dev/null; then
        log_message "Nginx process not running, starting..."
        systemctl start nginx
    fi
fi

log_message "Preventive maintenance completed"
```