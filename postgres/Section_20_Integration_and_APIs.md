# Section 20 – Integration and APIs

## 20.1 REST API Development

REST API development with PostgreSQL involves creating HTTP-based APIs that expose database functionality through standard REST principles.

### Key Concepts:
- **REST Principles**: Stateless, resource-based, HTTP methods
- **API Design**: Consistent URL patterns and response formats
- **Authentication**: API key, OAuth, JWT authentication
- **Documentation**: OpenAPI/Swagger documentation

### Real-World Analogy:
REST API development is like creating a restaurant menu and service system:
- **REST Principles** = Standardized menu format and service procedures
- **API Design** = Consistent menu layout and pricing
- **Authentication** = Customer identification and access control
- **Documentation** = Menu descriptions and service instructions

### Example:
```sql
-- Create API-friendly database schema
CREATE TABLE api_users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE api_posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES api_users(id),
    title VARCHAR(200) NOT NULL,
    content TEXT,
    published BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create API functions
CREATE OR REPLACE FUNCTION get_user_by_id(user_id INTEGER)
RETURNS JSON AS $$
DECLARE
    result JSON;
BEGIN
    SELECT json_build_object(
        'id', id,
        'username', username,
        'email', email,
        'created_at', created_at,
        'updated_at', updated_at
    ) INTO result
    FROM api_users
    WHERE id = user_id;
    
    RETURN result;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_posts_by_user(user_id INTEGER, limit_count INTEGER DEFAULT 10, offset_count INTEGER DEFAULT 0)
RETURNS JSON AS $$
DECLARE
    result JSON;
BEGIN
    SELECT json_agg(
        json_build_object(
            'id', id,
            'title', title,
            'content', content,
            'published', published,
            'created_at', created_at
        )
    ) INTO result
    FROM (
        SELECT id, title, content, published, created_at
        FROM api_posts
        WHERE user_id = $1
        ORDER BY created_at DESC
        LIMIT $2 OFFSET $3
    ) posts;
    
    RETURN COALESCE(result, '[]'::json);
END;
$$ LANGUAGE plpgsql;

-- Create API endpoints using PL/pgSQL
CREATE OR REPLACE FUNCTION api_get_user(user_id INTEGER)
RETURNS TABLE(
    status_code INTEGER,
    response_body JSON
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        200 as status_code,
        get_user_by_id(user_id) as response_body;
EXCEPTION
    WHEN OTHERS THEN
        RETURN QUERY
        SELECT 
            500 as status_code,
            json_build_object('error', 'Internal server error') as response_body;
END;
$$ LANGUAGE plpgsql;
```

## 20.2 GraphQL Integration

GraphQL integration with PostgreSQL provides a flexible query language that allows clients to request exactly the data they need.

### Key Concepts:
- **Schema Definition**: Defining GraphQL schema with PostgreSQL types
- **Resolvers**: Functions that resolve GraphQL queries
- **Queries**: Read operations
- **Mutations**: Write operations
- **Subscriptions**: Real-time updates

### Real-World Analogy:
GraphQL integration is like having a customizable ordering system:
- **Schema Definition** = Menu structure and item descriptions
- **Resolvers** = Kitchen staff who prepare specific orders
- **Queries** = Placing orders for specific items
- **Mutations** = Modifying orders or adding new items
- **Subscriptions** = Real-time order updates

### Example:
```sql
-- Create GraphQL-friendly schema
CREATE TABLE graphql_users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE graphql_posts (
    id SERIAL PRIMARY KEY,
    author_id INTEGER REFERENCES graphql_users(id),
    title VARCHAR(200) NOT NULL,
    content TEXT,
    published_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE graphql_comments (
    id SERIAL PRIMARY KEY,
    post_id INTEGER REFERENCES graphql_posts(id),
    author_id INTEGER REFERENCES graphql_users(id),
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create GraphQL resolvers
CREATE OR REPLACE FUNCTION graphql_get_user(user_id INTEGER)
RETURNS JSON AS $$
DECLARE
    result JSON;
BEGIN
    SELECT json_build_object(
        'id', id,
        'name', name,
        'email', email,
        'created_at', created_at
    ) INTO result
    FROM graphql_users
    WHERE id = user_id;
    
    RETURN result;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION graphql_get_user_posts(user_id INTEGER)
RETURNS JSON AS $$
DECLARE
    result JSON;
BEGIN
    SELECT json_agg(
        json_build_object(
            'id', id,
            'title', title,
            'content', content,
            'published_at', published_at,
            'created_at', created_at
        )
    ) INTO result
    FROM graphql_posts
    WHERE author_id = user_id
    ORDER BY created_at DESC;
    
    RETURN COALESCE(result, '[]'::json);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION graphql_get_post_comments(post_id INTEGER)
RETURNS JSON AS $$
DECLARE
    result JSON;
BEGIN
    SELECT json_agg(
        json_build_object(
            'id', id,
            'content', content,
            'author', json_build_object(
                'id', u.id,
                'name', u.name
            ),
            'created_at', c.created_at
        )
    ) INTO result
    FROM graphql_comments c
    JOIN graphql_users u ON c.author_id = u.id
    WHERE c.post_id = post_id
    ORDER BY c.created_at ASC;
    
    RETURN COALESCE(result, '[]'::json);
END;
$$ LANGUAGE plpgsql;

-- Create GraphQL mutations
CREATE OR REPLACE FUNCTION graphql_create_user(name VARCHAR(100), email VARCHAR(100))
RETURNS JSON AS $$
DECLARE
    new_user_id INTEGER;
    result JSON;
BEGIN
    INSERT INTO graphql_users (name, email)
    VALUES (name, email)
    RETURNING id INTO new_user_id;
    
    SELECT json_build_object(
        'id', new_user_id,
        'name', name,
        'email', email,
        'created_at', NOW()
    ) INTO result;
    
    RETURN result;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION graphql_create_post(author_id INTEGER, title VARCHAR(200), content TEXT)
RETURNS JSON AS $$
DECLARE
    new_post_id INTEGER;
    result JSON;
BEGIN
    INSERT INTO graphql_posts (author_id, title, content, published_at)
    VALUES (author_id, title, content, NOW())
    RETURNING id INTO new_post_id;
    
    SELECT json_build_object(
        'id', new_post_id,
        'title', title,
        'content', content,
        'published_at', NOW(),
        'created_at', NOW()
    ) INTO result;
    
    RETURN result;
END;
$$ LANGUAGE plpgsql;
```

## 20.3 WebSocket Integration

WebSocket integration enables real-time communication between PostgreSQL and web clients, allowing for live data updates and notifications.

### Key Concepts:
- **WebSocket Connections**: Persistent connections for real-time communication
- **Event Triggers**: Database triggers that emit events
- **Message Broadcasting**: Sending messages to connected clients
- **Connection Management**: Managing WebSocket connections

### Real-World Analogy:
WebSocket integration is like having a direct phone line:
- **WebSocket Connections** = Direct phone lines
- **Event Triggers** = Automatic call initiation
- **Message Broadcasting** = Conference calls
- **Connection Management** = Phone system management

### Example:
```sql
-- Create WebSocket event table
CREATE TABLE websocket_events (
    id SERIAL PRIMARY KEY,
    event_type VARCHAR(50) NOT NULL,
    table_name VARCHAR(50) NOT NULL,
    record_id INTEGER,
    event_data JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create event trigger function
CREATE OR REPLACE FUNCTION websocket_notify()
RETURNS TRIGGER AS $$
DECLARE
    event_data JSONB;
BEGIN
    -- Build event data
    event_data := jsonb_build_object(
        'table', TG_TABLE_NAME,
        'operation', TG_OP,
        'old', CASE WHEN TG_OP = 'DELETE' THEN row_to_json(OLD) ELSE NULL END,
        'new', CASE WHEN TG_OP = 'INSERT' OR TG_OP = 'UPDATE' THEN row_to_json(NEW) ELSE NULL END
    );
    
    -- Insert event
    INSERT INTO websocket_events (event_type, table_name, record_id, event_data)
    VALUES (TG_OP, TG_TABLE_NAME, COALESCE(NEW.id, OLD.id), event_data);
    
    -- Notify WebSocket clients
    PERFORM pg_notify('websocket_events', event_data::text);
    
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

-- Create triggers for real-time updates
CREATE TRIGGER websocket_users_trigger
    AFTER INSERT OR UPDATE OR DELETE ON graphql_users
    FOR EACH ROW EXECUTE FUNCTION websocket_notify();

CREATE TRIGGER websocket_posts_trigger
    AFTER INSERT OR UPDATE OR DELETE ON graphql_posts
    FOR EACH ROW EXECUTE FUNCTION websocket_notify();

CREATE TRIGGER websocket_comments_trigger
    AFTER INSERT OR UPDATE OR DELETE ON graphql_comments
    FOR EACH ROW EXECUTE FUNCTION websocket_notify();

-- Create function to get recent events
CREATE OR REPLACE FUNCTION get_recent_events(limit_count INTEGER DEFAULT 50)
RETURNS JSON AS $$
DECLARE
    result JSON;
BEGIN
    SELECT json_agg(
        json_build_object(
            'id', id,
            'event_type', event_type,
            'table_name', table_name,
            'record_id', record_id,
            'event_data', event_data,
            'created_at', created_at
        )
    ) INTO result
    FROM (
        SELECT id, event_type, table_name, record_id, event_data, created_at
        FROM websocket_events
        ORDER BY created_at DESC
        LIMIT limit_count
    ) events;
    
    RETURN COALESCE(result, '[]'::json);
END;
$$ LANGUAGE plpgsql;
```

## 20.4 Message Queue Integration

Message queue integration allows PostgreSQL to work with message brokers for asynchronous processing and event-driven architectures.

### Key Concepts:
- **Message Brokers**: Systems like RabbitMQ, Apache Kafka, Redis
- **Event Publishing**: Publishing database events to message queues
- **Event Consumption**: Processing messages from queues
- **Dead Letter Queues**: Handling failed message processing

### Real-World Analogy:
Message queue integration is like a postal service system:
- **Message Brokers** = Postal service infrastructure
- **Event Publishing** = Sending mail
- **Event Consumption** = Receiving and processing mail
- **Dead Letter Queues** = Undeliverable mail handling

### Example:
```sql
-- Create message queue integration table
CREATE TABLE message_queue (
    id SERIAL PRIMARY KEY,
    queue_name VARCHAR(100) NOT NULL,
    message_type VARCHAR(50) NOT NULL,
    message_data JSONB NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    retry_count INTEGER DEFAULT 0,
    max_retries INTEGER DEFAULT 3,
    created_at TIMESTAMP DEFAULT NOW(),
    processed_at TIMESTAMP,
    error_message TEXT
);

-- Create message publishing function
CREATE OR REPLACE FUNCTION publish_message(
    queue_name VARCHAR(100),
    message_type VARCHAR(50),
    message_data JSONB
)
RETURNS INTEGER AS $$
DECLARE
    message_id INTEGER;
BEGIN
    INSERT INTO message_queue (queue_name, message_type, message_data)
    VALUES (queue_name, message_type, message_data)
    RETURNING id INTO message_id;
    
    -- Notify message queue processor
    PERFORM pg_notify('message_queue', json_build_object(
        'queue_name', queue_name,
        'message_id', message_id
    )::text);
    
    RETURN message_id;
END;
$$ LANGUAGE plpgsql;

-- Create event publishing triggers
CREATE OR REPLACE FUNCTION publish_user_events()
RETURNS TRIGGER AS $$
DECLARE
    event_data JSONB;
BEGIN
    event_data := jsonb_build_object(
        'table', 'users',
        'operation', TG_OP,
        'old', CASE WHEN TG_OP = 'DELETE' THEN row_to_json(OLD) ELSE NULL END,
        'new', CASE WHEN TG_OP = 'INSERT' OR TG_OP = 'UPDATE' THEN row_to_json(NEW) ELSE NULL END
    );
    
    PERFORM publish_message('user_events', TG_OP, event_data);
    
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER user_events_trigger
    AFTER INSERT OR UPDATE OR DELETE ON graphql_users
    FOR EACH ROW EXECUTE FUNCTION publish_user_events();

-- Create message processing function
CREATE OR REPLACE FUNCTION process_message(message_id INTEGER)
RETURNS BOOLEAN AS $$
DECLARE
    message_record RECORD;
    success BOOLEAN := TRUE;
BEGIN
    -- Get message
    SELECT * INTO message_record
    FROM message_queue
    WHERE id = message_id AND status = 'pending';
    
    IF NOT FOUND THEN
        RETURN FALSE;
    END IF;
    
    -- Process message based on type
    CASE message_record.message_type
        WHEN 'user_created' THEN
            -- Process user creation
            PERFORM handle_user_created(message_record.message_data);
        WHEN 'user_updated' THEN
            -- Process user update
            PERFORM handle_user_updated(message_record.message_data);
        WHEN 'user_deleted' THEN
            -- Process user deletion
            PERFORM handle_user_deleted(message_record.message_data);
        ELSE
            -- Unknown message type
            success := FALSE;
    END CASE;
    
    -- Update message status
    IF success THEN
        UPDATE message_queue
        SET status = 'processed', processed_at = NOW()
        WHERE id = message_id;
    ELSE
        UPDATE message_queue
        SET status = 'failed', error_message = 'Unknown message type', retry_count = retry_count + 1
        WHERE id = message_id;
    END IF;
    
    RETURN success;
END;
$$ LANGUAGE plpgsql;
```

## 20.5 Microservices Integration

Microservices integration involves connecting PostgreSQL with multiple microservices to create a distributed system architecture.

### Key Concepts:
- **Service Discovery**: Finding and connecting to microservices
- **API Gateway**: Centralized entry point for microservices
- **Data Synchronization**: Keeping data consistent across services
- **Event Sourcing**: Storing events as the source of truth

### Real-World Analogy:
Microservices integration is like managing a large organization:
- **Service Discovery** = Employee directory and contact system
- **API Gateway** = Reception desk and routing system
- **Data Synchronization** = Keeping all departments informed
- **Event Sourcing** = Maintaining detailed activity logs

### Example:
```sql
-- Create microservices registry
CREATE TABLE microservices (
    id SERIAL PRIMARY KEY,
    service_name VARCHAR(100) UNIQUE NOT NULL,
    service_url VARCHAR(200) NOT NULL,
    health_check_url VARCHAR(200),
    status VARCHAR(20) DEFAULT 'active',
    last_heartbeat TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create service discovery function
CREATE OR REPLACE FUNCTION discover_service(service_name VARCHAR(100))
RETURNS VARCHAR(200) AS $$
DECLARE
    service_url VARCHAR(200);
BEGIN
    SELECT service_url INTO service_url
    FROM microservices
    WHERE service_name = $1 AND status = 'active';
    
    RETURN service_url;
END;
$$ LANGUAGE plpgsql;

-- Create event sourcing table
CREATE TABLE event_store (
    id SERIAL PRIMARY KEY,
    aggregate_id VARCHAR(100) NOT NULL,
    aggregate_type VARCHAR(50) NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    event_data JSONB NOT NULL,
    event_version INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create event sourcing functions
CREATE OR REPLACE FUNCTION append_event(
    aggregate_id VARCHAR(100),
    aggregate_type VARCHAR(50),
    event_type VARCHAR(50),
    event_data JSONB
)
RETURNS INTEGER AS $$
DECLARE
    event_version INTEGER;
    event_id INTEGER;
BEGIN
    -- Get next version
    SELECT COALESCE(MAX(event_version), 0) + 1 INTO event_version
    FROM event_store
    WHERE aggregate_id = $1 AND aggregate_type = $2;
    
    -- Insert event
    INSERT INTO event_store (aggregate_id, aggregate_type, event_type, event_data, event_version)
    VALUES (aggregate_id, aggregate_type, event_type, event_data, event_version)
    RETURNING id INTO event_id;
    
    RETURN event_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_events(
    aggregate_id VARCHAR(100),
    aggregate_type VARCHAR(50),
    from_version INTEGER DEFAULT 0
)
RETURNS JSON AS $$
DECLARE
    result JSON;
BEGIN
    SELECT json_agg(
        json_build_object(
            'id', id,
            'event_type', event_type,
            'event_data', event_data,
            'event_version', event_version,
            'created_at', created_at
        )
    ) INTO result
    FROM event_store
    WHERE aggregate_id = $1 
        AND aggregate_type = $2 
        AND event_version > from_version
    ORDER BY event_version ASC;
    
    RETURN COALESCE(result, '[]'::json);
END;
$$ LANGUAGE plpgsql;

-- Create data synchronization function
CREATE OR REPLACE FUNCTION sync_data_to_service(
    service_name VARCHAR(100),
    table_name VARCHAR(50),
    record_id INTEGER,
    operation VARCHAR(10)
)
RETURNS BOOLEAN AS $$
DECLARE
    service_url VARCHAR(200);
    sync_data JSONB;
BEGIN
    -- Get service URL
    SELECT discover_service(service_name) INTO service_url;
    
    IF service_url IS NULL THEN
        RETURN FALSE;
    END IF;
    
    -- Build sync data
    sync_data := jsonb_build_object(
        'table', table_name,
        'record_id', record_id,
        'operation', operation,
        'timestamp', NOW()
    );
    
    -- Publish to message queue for async processing
    PERFORM publish_message(service_name || '_sync', 'data_sync', sync_data);
    
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;
```

## 20.6 API Security

API security involves implementing comprehensive security measures to protect PostgreSQL-based APIs from various threats.

### Security Measures:
- **Authentication**: Verifying user identity
- **Authorization**: Controlling access to resources
- **Rate Limiting**: Preventing abuse and DoS attacks
- **Input Validation**: Sanitizing and validating input data
- **Encryption**: Protecting data in transit and at rest

### Real-World Analogy:
API security is like securing a high-security facility:
- **Authentication** = ID verification at the entrance
- **Authorization** = Access control to specific areas
- **Rate Limiting** = Limiting the number of visitors
- **Input Validation** = Screening visitors and packages
- **Encryption** = Secure communication channels

### Example:
```sql
-- Create API security tables
CREATE TABLE api_keys (
    id SERIAL PRIMARY KEY,
    key_hash VARCHAR(64) UNIQUE NOT NULL,
    user_id INTEGER,
    permissions JSONB,
    rate_limit INTEGER DEFAULT 1000,
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    last_used_at TIMESTAMP
);

CREATE TABLE api_requests (
    id SERIAL PRIMARY KEY,
    api_key_id INTEGER REFERENCES api_keys(id),
    endpoint VARCHAR(200),
    method VARCHAR(10),
    ip_address INET,
    user_agent TEXT,
    response_status INTEGER,
    response_time INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create API key validation function
CREATE OR REPLACE FUNCTION validate_api_key(api_key VARCHAR(64))
RETURNS TABLE(
    is_valid BOOLEAN,
    user_id INTEGER,
    permissions JSONB,
    rate_limit INTEGER
) AS $$
DECLARE
    key_record RECORD;
BEGIN
    SELECT 
        ak.id,
        ak.user_id,
        ak.permissions,
        ak.rate_limit,
        ak.expires_at
    INTO key_record
    FROM api_keys ak
    WHERE ak.key_hash = encode(digest(api_key, 'sha256'), 'hex')
        AND (ak.expires_at IS NULL OR ak.expires_at > NOW());
    
    IF FOUND THEN
        -- Update last used timestamp
        UPDATE api_keys
        SET last_used_at = NOW()
        WHERE id = key_record.id;
        
        RETURN QUERY
        SELECT TRUE, key_record.user_id, key_record.permissions, key_record.rate_limit;
    ELSE
        RETURN QUERY
        SELECT FALSE, NULL::INTEGER, NULL::JSONB, NULL::INTEGER;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Create rate limiting function
CREATE OR REPLACE FUNCTION check_rate_limit(
    api_key_id INTEGER,
    rate_limit INTEGER
)
RETURNS BOOLEAN AS $$
DECLARE
    request_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO request_count
    FROM api_requests
    WHERE api_key_id = $1
        AND created_at > NOW() - INTERVAL '1 hour';
    
    RETURN request_count < rate_limit;
END;
$$ LANGUAGE plpgsql;

-- Create input validation function
CREATE OR REPLACE FUNCTION validate_input(
    input_data JSONB,
    required_fields TEXT[],
    field_types JSONB
)
RETURNS BOOLEAN AS $$
DECLARE
    field TEXT;
    field_type TEXT;
    field_value TEXT;
BEGIN
    -- Check required fields
    FOREACH field IN ARRAY required_fields
    LOOP
        IF NOT (input_data ? field) THEN
            RETURN FALSE;
        END IF;
    END LOOP;
    
    -- Check field types
    FOR field, field_type IN SELECT * FROM jsonb_each_text(field_types)
    LOOP
        field_value := input_data ->> field;
        
        CASE field_type
            WHEN 'integer' THEN
                IF field_value !~ '^\d+$' THEN
                    RETURN FALSE;
                END IF;
            WHEN 'email' THEN
                IF field_value !~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$' THEN
                    RETURN FALSE;
                END IF;
            WHEN 'uuid' THEN
                IF field_value !~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
                    RETURN FALSE;
                END IF;
        END CASE;
    END LOOP;
    
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;
```

## 20.7 API Documentation

API documentation provides comprehensive information about API endpoints, parameters, responses, and usage examples.

### Documentation Components:
- **OpenAPI/Swagger**: Standard API documentation format
- **Endpoint Documentation**: Detailed endpoint descriptions
- **Schema Definitions**: Data structure definitions
- **Example Requests**: Sample API calls
- **Authentication Guide**: Security implementation details

### Real-World Analogy:
API documentation is like a comprehensive user manual:
- **OpenAPI/Swagger** = Standardized manual format
- **Endpoint Documentation** = Detailed instructions for each feature
- **Schema Definitions** = Technical specifications
- **Example Requests** = Step-by-step examples
- **Authentication Guide** = Security procedures

### Example:
```sql
-- Create API documentation table
CREATE TABLE api_documentation (
    id SERIAL PRIMARY KEY,
    endpoint VARCHAR(200) NOT NULL,
    method VARCHAR(10) NOT NULL,
    description TEXT,
    parameters JSONB,
    responses JSONB,
    examples JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create documentation management functions
CREATE OR REPLACE FUNCTION add_endpoint_documentation(
    endpoint VARCHAR(200),
    method VARCHAR(10),
    description TEXT,
    parameters JSONB,
    responses JSONB,
    examples JSONB
)
RETURNS INTEGER AS $$
DECLARE
    doc_id INTEGER;
BEGIN
    INSERT INTO api_documentation (endpoint, method, description, parameters, responses, examples)
    VALUES (endpoint, method, description, parameters, responses, examples)
    RETURNING id INTO doc_id;
    
    RETURN doc_id;
END;
$$ LANGUAGE plpgsql;

-- Generate OpenAPI specification
CREATE OR REPLACE FUNCTION generate_openapi_spec()
RETURNS JSON AS $$
DECLARE
    spec JSON;
    paths JSON;
    path_item JSON;
    endpoint_record RECORD;
BEGIN
    -- Initialize OpenAPI spec
    spec := json_build_object(
        'openapi', '3.0.0',
        'info', json_build_object(
            'title', 'PostgreSQL API',
            'version', '1.0.0',
            'description', 'API for PostgreSQL database operations'
        ),
        'servers', json_build_array(
            json_build_object('url', 'http://localhost:3000/api')
        ),
        'paths', '{}'::json
    );
    
    -- Build paths from documentation
    paths := '{}'::json;
    
    FOR endpoint_record IN
        SELECT endpoint, method, description, parameters, responses, examples
        FROM api_documentation
        ORDER BY endpoint, method
    LOOP
        -- Add path item
        path_item := json_build_object(
            endpoint_record.method, json_build_object(
                'summary', endpoint_record.description,
                'parameters', COALESCE(endpoint_record.parameters, '[]'::json),
                'responses', COALESCE(endpoint_record.responses, '{}'::json),
                'examples', COALESCE(endpoint_record.examples, '{}'::json)
            )
        );
        
        -- Merge with existing paths
        paths := paths || path_item;
    END LOOP;
    
    -- Update spec with paths
    spec := json_set(spec, '{paths}', paths);
    
    RETURN spec;
END;
$$ LANGUAGE plpgsql;

-- Add sample documentation
INSERT INTO api_documentation (endpoint, method, description, parameters, responses, examples)
VALUES (
    '/users/{id}',
    'GET',
    'Get user by ID',
    '[
        {
            "name": "id",
            "in": "path",
            "required": true,
            "schema": {"type": "integer"},
            "description": "User ID"
        }
    ]'::jsonb,
    '{
        "200": {
            "description": "User found",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "username": {"type": "string"},
                            "email": {"type": "string"},
                            "created_at": {"type": "string", "format": "date-time"}
                        }
                    }
                }
            }
        },
        "404": {
            "description": "User not found"
        }
    }'::jsonb,
    '{
        "request": {
            "url": "/users/123",
            "method": "GET"
        },
        "response": {
            "status": 200,
            "body": {
                "id": 123,
                "username": "john_doe",
                "email": "john@example.com",
                "created_at": "2024-01-01T00:00:00Z"
            }
        }
    }'::jsonb
);
```

## 20.8 API Testing

API testing involves validating API functionality, performance, and reliability through automated and manual testing procedures.

### Testing Types:
- **Unit Testing**: Testing individual API functions
- **Integration Testing**: Testing API interactions
- **Performance Testing**: Testing API performance under load
- **Security Testing**: Testing API security measures

### Real-World Analogy:
API testing is like quality control in manufacturing:
- **Unit Testing** = Testing individual components
- **Integration Testing** = Testing component interactions
- **Performance Testing** = Stress testing under load
- **Security Testing** = Security vulnerability testing

### Example:
```sql
-- Create API testing framework
CREATE TABLE api_tests (
    id SERIAL PRIMARY KEY,
    test_name VARCHAR(100) NOT NULL,
    test_type VARCHAR(20) NOT NULL,
    endpoint VARCHAR(200),
    method VARCHAR(10),
    test_data JSONB,
    expected_result JSONB,
    actual_result JSONB,
    status VARCHAR(20) DEFAULT 'pending',
    execution_time INTEGER,
    created_at TIMESTAMP DEFAULT NOW(),
    executed_at TIMESTAMP
);

-- Create test execution function
CREATE OR REPLACE FUNCTION execute_api_test(test_id INTEGER)
RETURNS BOOLEAN AS $$
DECLARE
    test_record RECORD;
    start_time TIMESTAMP;
    end_time TIMESTAMP;
    result BOOLEAN := FALSE;
BEGIN
    -- Get test details
    SELECT * INTO test_record
    FROM api_tests
    WHERE id = test_id;
    
    IF NOT FOUND THEN
        RETURN FALSE;
    END IF;
    
    -- Mark test as running
    UPDATE api_tests
    SET status = 'running', executed_at = NOW()
    WHERE id = test_id;
    
    start_time := NOW();
    
    -- Execute test based on type
    CASE test_record.test_type
        WHEN 'unit' THEN
            result := execute_unit_test(test_record);
        WHEN 'integration' THEN
            result := execute_integration_test(test_record);
        WHEN 'performance' THEN
            result := execute_performance_test(test_record);
        WHEN 'security' THEN
            result := execute_security_test(test_record);
        ELSE
            result := FALSE;
    END CASE;
    
    end_time := NOW();
    
    -- Update test results
    UPDATE api_tests
    SET 
        status = CASE WHEN result THEN 'passed' ELSE 'failed' END,
        execution_time = EXTRACT(EPOCH FROM (end_time - start_time))::INTEGER
    WHERE id = test_id;
    
    RETURN result;
END;
$$ LANGUAGE plpgsql;

-- Create unit test function
CREATE OR REPLACE FUNCTION execute_unit_test(test_record RECORD)
RETURNS BOOLEAN AS $$
DECLARE
    actual_result JSONB;
    expected_result JSONB;
BEGIN
    -- Execute the function being tested
    CASE test_record.endpoint
        WHEN '/users/{id}' THEN
            SELECT get_user_by_id((test_record.test_data->>'id')::INTEGER) INTO actual_result;
        WHEN '/posts' THEN
            SELECT get_posts_by_user((test_record.test_data->>'user_id')::INTEGER) INTO actual_result;
        ELSE
            RETURN FALSE;
    END CASE;
    
    expected_result := test_record.expected_result;
    
    -- Compare results
    RETURN actual_result = expected_result;
END;
$$ LANGUAGE plpgsql;

-- Create performance test function
CREATE OR REPLACE FUNCTION execute_performance_test(test_record RECORD)
RETURNS BOOLEAN AS $$
DECLARE
    start_time TIMESTAMP;
    end_time TIMESTAMP;
    execution_time INTEGER;
    max_execution_time INTEGER := 1000; -- 1 second
BEGIN
    start_time := NOW();
    
    -- Execute the test multiple times
    FOR i IN 1..100 LOOP
        CASE test_record.endpoint
            WHEN '/users/{id}' THEN
                PERFORM get_user_by_id((test_record.test_data->>'id')::INTEGER);
            WHEN '/posts' THEN
                PERFORM get_posts_by_user((test_record.test_data->>'user_id')::INTEGER);
        END CASE;
    END LOOP;
    
    end_time := NOW();
    execution_time := EXTRACT(EPOCH FROM (end_time - start_time))::INTEGER;
    
    -- Check if execution time is within limits
    RETURN execution_time < max_execution_time;
END;
$$ LANGUAGE plpgsql;
```

## 20.9 API Monitoring

API monitoring involves tracking API performance, usage, and health to ensure optimal operation and identify issues.

### Monitoring Metrics:
- **Response Time**: API response latency
- **Throughput**: Requests per second
- **Error Rate**: Percentage of failed requests
- **Availability**: API uptime percentage
- **Resource Usage**: CPU, memory, and database usage

### Real-World Analogy:
API monitoring is like having a comprehensive dashboard in a control room:
- **Response Time** = Speed indicators
- **Throughput** = Volume indicators
- **Error Rate** = Error indicators
- **Availability** = Status indicators
- **Resource Usage** = Resource meters

### Example:
```sql
-- Create API monitoring tables
CREATE TABLE api_metrics (
    id SERIAL PRIMARY KEY,
    endpoint VARCHAR(200) NOT NULL,
    method VARCHAR(10) NOT NULL,
    response_time INTEGER NOT NULL,
    status_code INTEGER NOT NULL,
    timestamp TIMESTAMP DEFAULT NOW()
);

CREATE TABLE api_alerts (
    id SERIAL PRIMARY KEY,
    alert_type VARCHAR(50) NOT NULL,
    threshold_value DECIMAL(10,2) NOT NULL,
    current_value DECIMAL(10,2) NOT NULL,
    message TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create monitoring functions
CREATE OR REPLACE FUNCTION record_api_metric(
    endpoint VARCHAR(200),
    method VARCHAR(10),
    response_time INTEGER,
    status_code INTEGER
)
RETURNS VOID AS $$
BEGIN
    INSERT INTO api_metrics (endpoint, method, response_time, status_code)
    VALUES (endpoint, method, response_time, status_code);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_api_stats(
    endpoint VARCHAR(200),
    time_period INTERVAL DEFAULT '1 hour'
)
RETURNS TABLE(
    avg_response_time DECIMAL(10,2),
    max_response_time INTEGER,
    min_response_time INTEGER,
    total_requests BIGINT,
    success_rate DECIMAL(5,2),
    error_rate DECIMAL(5,2)
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        ROUND(AVG(response_time), 2) as avg_response_time,
        MAX(response_time) as max_response_time,
        MIN(response_time) as min_response_time,
        COUNT(*) as total_requests,
        ROUND(COUNT(*) FILTER (WHERE status_code < 400)::DECIMAL / COUNT(*) * 100, 2) as success_rate,
        ROUND(COUNT(*) FILTER (WHERE status_code >= 400)::DECIMAL / COUNT(*) * 100, 2) as error_rate
    FROM api_metrics
    WHERE endpoint = $1
        AND timestamp >= NOW() - time_period;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION check_api_alerts()
RETURNS VOID AS $$
DECLARE
    alert_record RECORD;
    current_value DECIMAL(10,2);
BEGIN
    -- Check response time alerts
    FOR alert_record IN
        SELECT DISTINCT endpoint, 'response_time' as alert_type, 1000 as threshold
        FROM api_metrics
        WHERE timestamp >= NOW() - INTERVAL '5 minutes'
    LOOP
        SELECT AVG(response_time) INTO current_value
        FROM api_metrics
        WHERE endpoint = alert_record.endpoint
            AND timestamp >= NOW() - INTERVAL '5 minutes';
        
        IF current_value > alert_record.threshold THEN
            INSERT INTO api_alerts (alert_type, threshold_value, current_value, message)
            VALUES (
                'high_response_time',
                alert_record.threshold,
                current_value,
                'High response time detected for ' || alert_record.endpoint
            );
        END IF;
    END LOOP;
    
    -- Check error rate alerts
    FOR alert_record IN
        SELECT DISTINCT endpoint, 'error_rate' as alert_type, 5.0 as threshold
        FROM api_metrics
        WHERE timestamp >= NOW() - INTERVAL '5 minutes'
    LOOP
        SELECT 
            COUNT(*) FILTER (WHERE status_code >= 400)::DECIMAL / COUNT(*) * 100
        INTO current_value
        FROM api_metrics
        WHERE endpoint = alert_record.endpoint
            AND timestamp >= NOW() - INTERVAL '5 minutes';
        
        IF current_value > alert_record.threshold THEN
            INSERT INTO api_alerts (alert_type, threshold_value, current_value, message)
            VALUES (
                'high_error_rate',
                alert_record.threshold,
                current_value,
                'High error rate detected for ' || alert_record.endpoint
            );
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;
```

## 20.10 Best Practices

Best practices for API integration ensure reliable, secure, and maintainable API implementations.

### Key Practices:
- **RESTful Design**: Following REST principles consistently
- **Error Handling**: Implementing comprehensive error handling
- **Versioning**: Managing API versions effectively
- **Documentation**: Maintaining up-to-date documentation
- **Testing**: Implementing comprehensive testing strategies

### Real-World Analogy:
Best practices are like following professional standards:
- **RESTful Design** = Following industry standards
- **Error Handling** = Having proper contingency plans
- **Versioning** = Managing different versions of products
- **Documentation** = Maintaining professional records
- **Testing** = Quality assurance procedures

### Example:
```sql
-- Create API best practices monitoring function
CREATE OR REPLACE FUNCTION check_api_best_practices()
RETURNS TABLE(
    practice_name TEXT,
    status TEXT,
    recommendation TEXT
) AS $$
BEGIN
    -- Check for proper error handling
    RETURN QUERY
    SELECT 
        'Error Handling'::TEXT,
        CASE 
            WHEN EXISTS (
                SELECT 1 FROM api_documentation 
                WHERE responses::text LIKE '%error%'
            ) THEN 'GOOD'
            ELSE 'NEEDS_IMPROVEMENT'
        END,
        CASE 
            WHEN EXISTS (
                SELECT 1 FROM api_documentation 
                WHERE responses::text LIKE '%error%'
            ) THEN 'Error handling is documented'
            ELSE 'Document error responses for all endpoints'
        END;
    
    -- Check for API versioning
    RETURN QUERY
    SELECT 
        'API Versioning'::TEXT,
        CASE 
            WHEN EXISTS (
                SELECT 1 FROM api_documentation 
                WHERE endpoint LIKE '%/v%'
            ) THEN 'GOOD'
            ELSE 'NEEDS_IMPROVEMENT'
        END,
        CASE 
            WHEN EXISTS (
                SELECT 1 FROM api_documentation 
                WHERE endpoint LIKE '%/v%'
            ) THEN 'API versioning is implemented'
            ELSE 'Implement API versioning strategy'
        END;
    
    -- Check for rate limiting
    RETURN QUERY
    SELECT 
        'Rate Limiting'::TEXT,
        CASE 
            WHEN EXISTS (
                SELECT 1 FROM api_keys 
                WHERE rate_limit > 0
            ) THEN 'GOOD'
            ELSE 'NEEDS_IMPROVEMENT'
        END,
        CASE 
            WHEN EXISTS (
                SELECT 1 FROM api_keys 
                WHERE rate_limit > 0
            ) THEN 'Rate limiting is configured'
            ELSE 'Implement rate limiting for API protection'
        END;
    
    -- Check for authentication
    RETURN QUERY
    SELECT 
        'Authentication'::TEXT,
        CASE 
            WHEN EXISTS (
                SELECT 1 FROM api_keys 
                WHERE status = 'active'
            ) THEN 'GOOD'
            ELSE 'NEEDS_IMPROVEMENT'
        END,
        CASE 
            WHEN EXISTS (
                SELECT 1 FROM api_keys 
                WHERE status = 'active'
            ) THEN 'Authentication is implemented'
            ELSE 'Implement API authentication'
        END;
END;
$$ LANGUAGE plpgsql;

-- Use the best practices checker
SELECT * FROM check_api_best_practices();
```