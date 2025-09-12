# Section 6 – Networking and Content Delivery

## 6.1 Virtual Private Cloud (VPC)

VPC provides isolated network infrastructure for your GCP resources.

### Key Features:
- Isolated Networks
- Custom Subnets
- Firewall Rules
- Private Google Access

### Java Example:
```java
import com.google.cloud.compute.v1.*;

public class VPCManager {
    private NetworksClient networksClient;
    
    public void createVPC(String projectId, String networkName) {
        Network network = Network.newBuilder()
            .setName(networkName)
            .setAutoCreateSubnetworks(false)
            .build();
        
        Operation operation = networksClient.insert(projectId, network);
        System.out.println("VPC created: " + networkName);
    }
    
    public void createSubnet(String projectId, String region, String subnetName, String cidr) {
        Subnetwork subnet = Subnetwork.newBuilder()
            .setName(subnetName)
            .setIpCidrRange(cidr)
            .setRegion(region)
            .build();
        
        System.out.println("Subnet created: " + subnetName);
    }
}
```

## 6.2 Cloud Load Balancing

Cloud Load Balancing distributes traffic across multiple instances.

### Load Balancer Types:
- HTTP(S) Load Balancing
- TCP/UDP Load Balancing
- Internal Load Balancing
- SSL Proxy Load Balancing

### Java Example:
```java
import com.google.cloud.compute.v1.*;

public class LoadBalancerManager {
    public void createHTTPLoadBalancer(String projectId, String lbName) {
        System.out.println("HTTP Load Balancer created: " + lbName);
    }
    
    public void createInternalLoadBalancer(String projectId, String lbName) {
        System.out.println("Internal Load Balancer created: " + lbName);
    }
}
```

## 6.3 Cloud CDN

Cloud CDN accelerates content delivery using Google's global edge network.

### Key Features:
- Global Edge Locations
- Automatic Caching
- SSL/TLS Termination
- Custom Cache Keys

### Java Example:
```java
public class CDNManager {
    public void enableCDN(String bucketName) {
        System.out.println("CDN enabled for bucket: " + bucketName);
    }
    
    public void configureCachePolicy(String urlPattern, int ttl) {
        System.out.println("Cache policy configured for: " + urlPattern);
    }
}
```

## 6.4 Cloud DNS

Cloud DNS provides scalable and reliable DNS services.

### Key Features:
- Managed DNS
- Global Anycast
- DNSSEC Support
- Private Zones

### Java Example:
```java
import com.google.cloud.dns.v1.*;

public class DNSManager {
    private DnsClient dnsClient;
    
    public void createZone(String projectId, String zoneName, String domain) {
        Zone zone = Zone.newBuilder()
            .setName(zoneName)
            .setDnsName(domain)
            .build();
        
        System.out.println("DNS zone created: " + zoneName);
    }
    
    public void createRecord(String zoneName, String recordName, String recordType, String recordData) {
        System.out.println("DNS record created: " + recordName);
    }
}
```

## 6.5 Cloud NAT

Cloud NAT provides outbound internet access for private instances.

### Key Features:
- Outbound Internet Access
- Static IP Addresses
- Port Allocation
- Logging and Monitoring

### Java Example:
```java
public class NATManager {
    public void createNATGateway(String projectId, String region, String gatewayName) {
        System.out.println("NAT Gateway created: " + gatewayName);
    }
    
    public void configureNATRules(String gatewayName, String subnet) {
        System.out.println("NAT rules configured for: " + subnet);
    }
}
```

## 6.6 Cloud VPN

Cloud VPN provides secure connectivity between on-premises and GCP.

### VPN Types:
- Classic VPN
- HA VPN
- Cloud VPN Interconnect
- Partner Interconnect

### Java Example:
```java
public class VPNManager {
    public void createVPNTunnel(String projectId, String region, String tunnelName) {
        System.out.println("VPN tunnel created: " + tunnelName);
    }
    
    public void configureVPNGateway(String projectId, String region, String gatewayName) {
        System.out.println("VPN gateway configured: " + gatewayName);
    }
}
```

## 6.7 Cloud Interconnect

Cloud Interconnect provides dedicated connections to Google's network.

### Interconnect Types:
- Dedicated Interconnect
- Partner Interconnect
- Cross-Cloud Interconnect
- Carrier Peering

### Java Example:
```java
public class InterconnectManager {
    public void createDedicatedInterconnect(String projectId, String interconnectName) {
        System.out.println("Dedicated Interconnect created: " + interconnectName);
    }
    
    public void createPartnerInterconnect(String projectId, String interconnectName) {
        System.out.println("Partner Interconnect created: " + interconnectName);
    }
}
```

## 6.8 Cloud Router

Cloud Router provides dynamic routing for VPC networks.

### Key Features:
- BGP Routing
- Custom Routes
- Route Advertisement
- Route Filtering

### Java Example:
```java
public class RouterManager {
    public void createRouter(String projectId, String region, String routerName) {
        System.out.println("Cloud Router created: " + routerName);
    }
    
    public void configureBGP(String routerName, String peerIP, int asn) {
        System.out.println("BGP configured for router: " + routerName);
    }
}
```

## 6.9 Firewall Rules

Firewall rules control network traffic to and from instances.

### Rule Types:
- Ingress Rules
- Egress Rules
- Priority-based Rules
- Tag-based Rules

### Java Example:
```java
import com.google.cloud.compute.v1.*;

public class FirewallManager {
    private FirewallsClient firewallsClient;
    
    public void createFirewallRule(String projectId, String ruleName, String sourceRange, int port) {
        Firewall firewall = Firewall.newBuilder()
            .setName(ruleName)
            .setSourceRanges(sourceRange)
            .addAllowed(Firewall.Allowed.newBuilder()
                .setIPProtocol("tcp")
                .addPorts(String.valueOf(port))
                .build())
            .build();
        
        System.out.println("Firewall rule created: " + ruleName);
    }
}
```

## 6.10 Network Security

Network security includes various measures to protect network infrastructure.

### Security Features:
- VPC Service Controls
- Private Google Access
- Identity-Aware Proxy
- Network Monitoring

### Java Example:
```java
public class NetworkSecurityManager {
    public void enableVPCServiceControls(String projectId, String service) {
        System.out.println("VPC Service Controls enabled for: " + service);
    }
    
    public void configurePrivateGoogleAccess(String subnetName) {
        System.out.println("Private Google Access configured for: " + subnetName);
    }
}
```