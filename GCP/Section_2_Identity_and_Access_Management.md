# Section 2 – Identity and Access Management

## 2.1 Google Cloud Identity

Google Cloud Identity is a cloud-based identity and access management service that provides a foundation for secure access to Google Cloud services and third-party applications.

### Key Concepts:
- **Identity Provider (IdP)**: Centralized system for managing user identities
- **Single Sign-On (SSO)**: Users authenticate once to access multiple services
- **Multi-Factor Authentication (MFA)**: Additional security layer beyond passwords
- **Directory Services**: Centralized user and group management

### Real-World Analogy:
Think of Google Cloud Identity like a master key system for a large office building:
- **Master Key** (Identity): Proves who you are
- **Key Cards** (Authentication): Different access levels for different areas
- **Security Guards** (Authorization): Check if you can enter specific rooms

### Java Example - Identity Verification:
```java
import com.google.auth.oauth2.GoogleCredentials;
import com.google.auth.oauth2.ServiceAccountCredentials;

public class IdentityVerification {
    private GoogleCredentials credentials;
    
    public IdentityVerification() {
        this.credentials = ServiceAccountCredentials.fromStream(
            getClass().getResourceAsStream("/service-account-key.json")
        );
    }
    
    public boolean verifyIdentity(String userId) {
        try {
            return credentials.getAccessToken() != null;
        } catch (Exception e) {
            System.err.println("Identity verification failed: " + e.getMessage());
            return false;
        }
    }
}
```

## 2.2 Identity and Access Management (IAM)

IAM is the core service for managing access to GCP resources. It controls who (identity) has what access (permission) to which resources.

### IAM Components:
- **Principals**: Users, groups, service accounts, or domains
- **Roles**: Collections of permissions
- **Resources**: GCP resources like projects, buckets, or instances
- **Policies**: Bindings between principals, roles, and resources

### Java Example - IAM Policy Management:
```java
import com.google.cloud.iam.v1.Policy;
import com.google.cloud.iam.v1.Binding;

public class IAMPolicyManager {
    public void grantRole(String resource, String principal, String role) {
        try {
            Binding binding = Binding.newBuilder()
                .setRole(role)
                .addMembers("user:" + principal)
                .build();
            
            System.out.println("Role " + role + " granted to " + principal);
        } catch (Exception e) {
            System.err.println("Failed to grant role: " + e.getMessage());
        }
    }
}
```

## 2.3 Service Accounts

Service accounts are special Google accounts that represent non-human users, such as applications or virtual machines, that need to access GCP resources.

### Service Account Types:
- **Google-Managed**: Automatically created by GCP services
- **User-Managed**: Created and managed by users
- **Default Service Account**: Automatically assigned to resources
- **Custom Service Account**: Created for specific applications

### Java Example - Service Account Usage:
```java
import com.google.auth.oauth2.ServiceAccountCredentials;
import com.google.cloud.storage.Storage;
import com.google.cloud.storage.StorageOptions;

public class ServiceAccountExample {
    private ServiceAccountCredentials credentials;
    private Storage storage;
    
    public ServiceAccountExample(String keyFilePath) {
        try {
            this.credentials = ServiceAccountCredentials.fromStream(
                new FileInputStream(keyFilePath)
            );
            
            this.storage = StorageOptions.newBuilder()
                .setCredentials(credentials)
                .build()
                .getService();
        } catch (Exception e) {
            throw new RuntimeException("Failed to initialize service account", e);
        }
    }
    
    public void listBuckets() {
        storage.list().iterateAll().forEach(bucket -> {
            System.out.println("Bucket: " + bucket.getName());
        });
    }
}
```

## 2.4 Resource Hierarchy

GCP organizes resources in a hierarchical structure that affects how IAM policies are inherited and applied.

### Hierarchy Levels:
- **Organization**: Top-level container (optional)
- **Folder**: Logical grouping of projects
- **Project**: Base-level container for resources
- **Resource**: Individual GCP resources

### Java Example - Resource Hierarchy Navigation:
```java
import com.google.cloud.resourcemanager.v3.Project;
import com.google.cloud.resourcemanager.v3.ProjectsClient;

public class ResourceHierarchyManager {
    private ProjectsClient projectsClient;
    
    public void listProjectsInOrganization(String organizationId) {
        try {
            String parent = "organizations/" + organizationId;
            
            projectsClient.listProjects(parent).iterateAll().forEach(project -> {
                System.out.println("Project: " + project.getName());
                System.out.println("Project ID: " + project.getProjectId());
            });
        } catch (Exception e) {
            System.err.println("Failed to list projects: " + e.getMessage());
        }
    }
}
```

## 2.5 Organization Policies

Organization policies are constraints that control how GCP resources can be used across your organization, providing governance and compliance controls.

### Policy Types:
- **List Policies**: Control which values are allowed or denied
- **Boolean Policies**: Simple allow/deny constraints
- **Restriction Policies**: Limit specific resource configurations
- **Custom Policies**: User-defined constraints

### Java Example - Organization Policy Management:
```java
import com.google.cloud.orgpolicy.v2.OrgPolicyClient;
import com.google.cloud.orgpolicy.v2.Policy;

public class OrganizationPolicyManager {
    private OrgPolicyClient orgPolicyClient;
    
    public void createDomainRestrictionPolicy(String organizationId) {
        try {
            Policy policy = Policy.newBuilder()
                .setSpec(Policy.Spec.newBuilder()
                    .setRules(Policy.Rule.newBuilder()
                        .setValues(Policy.StringValues.newBuilder()
                            .addAllowedValues("example.com")
                            .build())
                        .build())
                    .build())
                .build();
            
            String parent = "organizations/" + organizationId;
            orgPolicyClient.createPolicy(parent, policy);
            System.out.println("Domain restriction policy created successfully");
        } catch (Exception e) {
            System.err.println("Failed to create policy: " + e.getMessage());
        }
    }
}
```

## 2.6 Access Context Manager

Access Context Manager provides context-aware access control based on attributes like device security, location, and time.

### Key Features:
- **Access Levels**: Define conditions for access
- **Access Policies**: Bind access levels to resources
- **Device Trust**: Verify device security status
- **Location-Based Access**: Control access based on geographic location

### Java Example - Access Context Management:
```java
import com.google.identity.accesscontextmanager.v1.AccessContextManagerClient;
import com.google.identity.accesscontextmanager.v1.AccessLevel;

public class AccessContextManager {
    private AccessContextManagerClient client;
    
    public void createAccessLevel(String organizationId, String accessLevelName) {
        try {
            AccessLevel accessLevel = AccessLevel.newBuilder()
                .setTitle("Secure Access Level")
                .setBasic(AccessLevel.Basic.newBuilder()
                    .addConditions(AccessLevel.Condition.newBuilder()
                        .setDevicePolicy(AccessLevel.DevicePolicy.newBuilder()
                            .setRequireScreenLock(true)
                            .build())
                        .build())
                    .build())
                .build();
            
            String parent = "organizations/" + organizationId;
            client.createAccessLevel(parent, accessLevel);
            System.out.println("Access level created: " + accessLevelName);
        } catch (Exception e) {
            System.err.println("Failed to create access level: " + e.getMessage());
        }
    }
}
```

## 2.7 Identity-Aware Proxy (IAP)

IAP provides identity-based access control for applications and VMs, enabling secure access without VPNs.

### Key Features:
- **Zero-Trust Access**: Verify identity for every request
- **Application-Level Security**: Protect individual applications
- **No VPN Required**: Access applications directly through IAP
- **Audit Logging**: Track all access attempts

### Java Example - IAP Integration:
```java
import com.google.auth.oauth2.IdTokenCredentials;
import com.google.auth.oauth2.IdTokenProvider;

public class IAPIntegration {
    private IdTokenProvider idTokenProvider;
    
    public void accessIAPProtectedResource(String targetAudience) {
        try {
            IdTokenCredentials credentials = IdTokenCredentials.newBuilder()
                .setIdTokenProvider(idTokenProvider)
                .setTargetAudience(targetAudience)
                .build();
            
            String accessToken = credentials.getAccessToken().getTokenValue();
            makeAuthenticatedRequest(accessToken);
        } catch (Exception e) {
            System.err.println("Failed to access IAP protected resource: " + e.getMessage());
        }
    }
}
```

## 2.8 Cloud Identity for Customers and Partners

Cloud Identity for Customers and Partners (CICP) provides identity management for external users and partners.

### Key Features:
- **External User Management**: Manage customers and partners
- **B2B Integration**: Seamless partner access
- **Custom Branding**: White-label identity experience
- **API Access**: Programmatic user management

### Java Example - External User Management:
```java
import com.google.cloud.identity.v1.User;
import com.google.cloud.identity.v1.UsersClient;

public class ExternalUserManager {
    private UsersClient usersClient;
    
    public void createExternalUser(String email, String displayName) {
        try {
            User user = User.newBuilder()
                .setPrimaryEmail(email)
                .setName(User.Name.newBuilder()
                    .setGivenName(displayName)
                    .setFamilyName("User")
                    .build())
                .setPassword("temporary-password")
                .setChangePasswordAtNextLogin(true)
                .build();
            
            User createdUser = usersClient.createUser(user);
            System.out.println("External user created: " + createdUser.getName());
        } catch (Exception e) {
            System.err.println("Failed to create external user: " + e.getMessage());
        }
    }
}
```

## 2.9 Multi-Factor Authentication

MFA adds an additional layer of security by requiring users to provide two or more verification factors.

### Authentication Factors:
- **Something You Know**: Password or PIN
- **Something You Have**: Phone, hardware token, or app
- **Something You Are**: Biometric authentication
- **Somewhere You Are**: Location-based verification

### Java Example - MFA Implementation:
```java
public class MFAImplementation {
    public boolean authenticateWithMFA(String username, String password, String mfaCode) {
        try {
            if (!verifyCredentials(username, password)) {
                return false;
            }
            
            if (!verifyMFACode(username, mfaCode)) {
                return false;
            }
            
            String sessionToken = generateSessionToken(username);
            System.out.println("MFA authentication successful for user: " + username);
            return true;
        } catch (Exception e) {
            System.err.println("MFA authentication failed: " + e.getMessage());
            return false;
        }
    }
    
    private boolean verifyCredentials(String username, String password) {
        return true; // Placeholder
    }
    
    private boolean verifyMFACode(String username, String code) {
        return true; // Placeholder
    }
    
    private String generateSessionToken(String username) {
        return "session-token-" + username;
    }
}
```

## 2.10 Security Keys

Security keys are physical devices that provide strong authentication using public key cryptography.

### Key Types:
- **FIDO2/WebAuthn**: Modern standard for web authentication
- **U2F**: Universal 2nd Factor authentication
- **Titan Security Keys**: Google's hardware security keys
- **Third-Party Keys**: Compatible security keys

### Java Example - Security Key Integration:
```java
import com.google.auth.oauth2.ExternalAccountCredentials;

public class SecurityKeyIntegration {
    public boolean authenticateWithSecurityKey(String username) {
        try {
            ExternalAccountCredentials externalCredentials = 
                ExternalAccountCredentials.newBuilder()
                    .setAudience("//iam.googleapis.com/projects/PROJECT_ID/locations/global/workloadIdentityPools/POOL_ID/providers/PROVIDER_ID")
                    .setSubjectTokenType("urn:ietf:params:oauth:token-type:jwt")
                    .setTokenUrl("https://sts.googleapis.com/v1/token")
                    .setCredentialSource(ExternalAccountCredentials.CredentialSource.newBuilder()
                        .setFile("/path/to/security-key-credentials.json")
                        .build())
                    .build();
            
            String accessToken = externalCredentials.getAccessToken().getTokenValue();
            System.out.println("Security key authentication successful for user: " + username);
            return true;
        } catch (Exception e) {
            System.err.println("Security key authentication failed: " + e.getMessage());
            return false;
        }
    }
}
```