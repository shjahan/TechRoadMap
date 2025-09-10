# Section 9 - Database Patterns

## 9.1 Data Access Object (DAO)

The DAO pattern encapsulates data access logic, providing a clean interface between business logic and data persistence.

### When to Use:
- When you need to separate data access from business logic
- When you want to abstract database operations
- When you need to support multiple data sources

### Real-World Analogy:
Think of a library catalog system. Instead of directly searching through bookshelves, you use a catalog (DAO) that knows how to find books by title, author, or subject, hiding the complexity of the physical organization.

### Basic Implementation:
```java
// DAO interface
public interface UserDAO {
    void save(User user);
    User findById(String id);
    List<User> findAll();
    void update(User user);
    void delete(String id);
}

// Concrete DAO implementation
public class UserDAOImpl implements UserDAO {
    private Connection connection;
    
    public UserDAOImpl(Connection connection) {
        this.connection = connection;
    }
    
    public void save(User user) {
        String sql = "INSERT INTO users (id, name, email) VALUES (?, ?, ?)";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, user.getId());
            stmt.setString(2, user.getName());
            stmt.setString(3, user.getEmail());
            stmt.executeUpdate();
        } catch (SQLException e) {
            throw new DataAccessException("Failed to save user", e);
        }
    }
    
    public User findById(String id) {
        String sql = "SELECT * FROM users WHERE id = ?";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, id);
            ResultSet rs = stmt.executeQuery();
            if (rs.next()) {
                return mapResultSetToUser(rs);
            }
        } catch (SQLException e) {
            throw new DataAccessException("Failed to find user", e);
        }
        return null;
    }
    
    private User mapResultSetToUser(ResultSet rs) throws SQLException {
        return new User(
            rs.getString("id"),
            rs.getString("name"),
            rs.getString("email")
        );
    }
}
```

## 9.2 Repository Pattern

The Repository pattern provides a more object-oriented approach to data access, treating data as a collection of objects.

### When to Use:
- When you want to work with domain objects
- When you need to implement complex queries
- When you want to test business logic without database

### Real-World Analogy:
Think of a warehouse management system. Instead of directly accessing shelves, you use a warehouse manager (repository) who knows how to store, retrieve, and organize items based on your requests.

### Basic Implementation:
```java
// Repository interface
public interface UserRepository {
    void save(User user);
    Optional<User> findById(String id);
    List<User> findByEmail(String email);
    List<User> findAll();
    void delete(User user);
}

// JPA Repository implementation
@Repository
public class JpaUserRepository implements UserRepository {
    @PersistenceContext
    private EntityManager entityManager;
    
    public void save(User user) {
        if (user.getId() == null) {
            entityManager.persist(user);
        } else {
            entityManager.merge(user);
        }
    }
    
    public Optional<User> findById(String id) {
        User user = entityManager.find(User.class, id);
        return Optional.ofNullable(user);
    }
    
    public List<User> findByEmail(String email) {
        return entityManager.createQuery(
            "SELECT u FROM User u WHERE u.email = :email", User.class)
            .setParameter("email", email)
            .getResultList();
    }
    
    public List<User> findAll() {
        return entityManager.createQuery(
            "SELECT u FROM User u", User.class)
            .getResultList();
    }
    
    public void delete(User user) {
        entityManager.remove(user);
    }
}
```

## 9.3 Unit of Work Pattern

The Unit of Work pattern maintains a list of objects affected by a business transaction and coordinates writing out changes.

### When to Use:
- When you need to manage transactions across multiple operations
- When you want to batch database operations
- When you need to maintain consistency

### Real-World Analogy:
Think of a shopping cart checkout process. You add multiple items to your cart, and when you're ready to pay, all items are processed together as a single transaction.

### Basic Implementation:
```java
// Unit of Work interface
public interface UnitOfWork {
    void registerNew(Object entity);
    void registerDirty(Object entity);
    void registerDeleted(Object entity);
    void commit();
    void rollback();
}

// Simple Unit of Work implementation
public class SimpleUnitOfWork implements UnitOfWork {
    private Set<Object> newEntities = new HashSet<>();
    private Set<Object> dirtyEntities = new HashSet<>();
    private Set<Object> deletedEntities = new HashSet<>();
    private EntityManager entityManager;
    
    public SimpleUnitOfWork(EntityManager entityManager) {
        this.entityManager = entityManager;
    }
    
    public void registerNew(Object entity) {
        newEntities.add(entity);
    }
    
    public void registerDirty(Object entity) {
        dirtyEntities.add(entity);
    }
    
    public void registerDeleted(Object entity) {
        deletedEntities.add(entity);
    }
    
    public void commit() {
        try {
            entityManager.getTransaction().begin();
            
            // Process new entities
            for (Object entity : newEntities) {
                entityManager.persist(entity);
            }
            
            // Process dirty entities
            for (Object entity : dirtyEntities) {
                entityManager.merge(entity);
            }
            
            // Process deleted entities
            for (Object entity : deletedEntities) {
                entityManager.remove(entity);
            }
            
            entityManager.getTransaction().commit();
            
        } catch (Exception e) {
            entityManager.getTransaction().rollback();
            throw new DataAccessException("Failed to commit transaction", e);
        }
    }
    
    public void rollback() {
        entityManager.getTransaction().rollback();
    }
}
```

## 9.4 Identity Map Pattern

The Identity Map pattern ensures that each object is loaded only once and maintains a map of all loaded objects.

### When to Use:
- When you need to avoid duplicate objects
- When you want to ensure object identity
- When you need to optimize database access

### Real-World Analogy:
Think of a library's book tracking system. Each book has a unique barcode, and the system ensures that the same book isn't checked out twice or that you don't have duplicate records for the same book.

### Basic Implementation:
```java
// Identity Map
public class IdentityMap<T> {
    private Map<String, T> map = new HashMap<>();
    
    public void put(String id, T entity) {
        map.put(id, entity);
    }
    
    public T get(String id) {
        return map.get(id);
    }
    
    public boolean contains(String id) {
        return map.containsKey(id);
    }
    
    public void remove(String id) {
        map.remove(id);
    }
    
    public void clear() {
        map.clear();
    }
}

// Repository with Identity Map
public class UserRepositoryWithIdentityMap {
    private IdentityMap<User> identityMap = new IdentityMap<>();
    private UserDAO userDAO;
    
    public UserRepositoryWithIdentityMap(UserDAO userDAO) {
        this.userDAO = userDAO;
    }
    
    public User findById(String id) {
        if (identityMap.contains(id)) {
            return identityMap.get(id);
        }
        
        User user = userDAO.findById(id);
        if (user != null) {
            identityMap.put(id, user);
        }
        return user;
    }
    
    public void save(User user) {
        userDAO.save(user);
        identityMap.put(user.getId(), user);
    }
}
```

## 9.5 Lazy Load Pattern

The Lazy Load pattern delays loading of data until it's actually needed.

### When to Use:
- When you have large objects with optional data
- When you want to optimize performance
- When you need to reduce memory usage

### Real-World Analogy:
Think of a smart phone that only loads apps when you actually open them, rather than keeping all apps in memory at once.

### Basic Implementation:
```java
// Lazy load proxy
public class LazyUser implements User {
    private String id;
    private UserDAO userDAO;
    private User realUser;
    
    public LazyUser(String id, UserDAO userDAO) {
        this.id = id;
        this.userDAO = userDAO;
    }
    
    private User getRealUser() {
        if (realUser == null) {
            realUser = userDAO.findById(id);
        }
        return realUser;
    }
    
    public String getName() {
        return getRealUser().getName();
    }
    
    public String getEmail() {
        return getRealUser().getEmail();
    }
}

// Lazy collection
public class LazyUserList {
    private List<String> userIds;
    private UserDAO userDAO;
    private List<User> users;
    
    public LazyUserList(List<String> userIds, UserDAO userDAO) {
        this.userIds = userIds;
        this.userDAO = userDAO;
    }
    
    public List<User> getUsers() {
        if (users == null) {
            users = new ArrayList<>();
            for (String id : userIds) {
                users.add(userDAO.findById(id));
            }
        }
        return users;
    }
}
```

## 9.6 Query Object Pattern

The Query Object pattern encapsulates database queries as objects, making them reusable and testable.

### When to Use:
- When you have complex queries
- When you want to reuse query logic
- When you need to build queries dynamically

### Real-World Analogy:
Think of a search form on a website. Instead of writing a new search function each time, you create a reusable search object that can be configured with different criteria.

### Basic Implementation:
```java
// Query object interface
public interface Query<T> {
    List<T> execute();
    Query<T> where(String condition);
    Query<T> orderBy(String field);
    Query<T> limit(int count);
}

// SQL Query implementation
public class SqlQuery<T> implements Query<T> {
    private String baseQuery;
    private List<String> conditions = new ArrayList<>();
    private String orderByClause;
    private Integer limitCount;
    private Connection connection;
    private RowMapper<T> rowMapper;
    
    public SqlQuery(String baseQuery, Connection connection, RowMapper<T> rowMapper) {
        this.baseQuery = baseQuery;
        this.connection = connection;
        this.rowMapper = rowMapper;
    }
    
    public Query<T> where(String condition) {
        conditions.add(condition);
        return this;
    }
    
    public Query<T> orderBy(String field) {
        orderByClause = "ORDER BY " + field;
        return this;
    }
    
    public Query<T> limit(int count) {
        limitCount = count;
        return this;
    }
    
    public List<T> execute() {
        StringBuilder sql = new StringBuilder(baseQuery);
        
        if (!conditions.isEmpty()) {
            sql.append(" WHERE ").append(String.join(" AND ", conditions));
        }
        
        if (orderByClause != null) {
            sql.append(" ").append(orderByClause);
        }
        
        if (limitCount != null) {
            sql.append(" LIMIT ").append(limitCount);
        }
        
        // Execute query and map results
        // Implementation details...
        return new ArrayList<>();
    }
}

// Usage
Query<User> query = new SqlQuery<>("SELECT * FROM users", connection, userRowMapper);
List<User> users = query
    .where("age > 18")
    .where("status = 'active'")
    .orderBy("name")
    .limit(10)
    .execute();
```

## 9.7 Table Data Gateway Pattern

The Table Data Gateway pattern provides a single interface for accessing all rows in a database table.

### When to Use:
- When you need simple table access
- When you want to encapsulate SQL operations
- When you have a one-to-one mapping between tables and classes

### Real-World Analogy:
Think of a library's book catalog system where each table (fiction, non-fiction, reference) has its own dedicated librarian who knows how to find, add, or remove books from that specific section.

### Basic Implementation:
```java
// Table Data Gateway
public class UserTableGateway {
    private Connection connection;
    
    public UserTableGateway(Connection connection) {
        this.connection = connection;
    }
    
    public void insert(User user) {
        String sql = "INSERT INTO users (id, name, email) VALUES (?, ?, ?)";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, user.getId());
            stmt.setString(2, user.getName());
            stmt.setString(3, user.getEmail());
            stmt.executeUpdate();
        } catch (SQLException e) {
            throw new DataAccessException("Failed to insert user", e);
        }
    }
    
    public void update(User user) {
        String sql = "UPDATE users SET name = ?, email = ? WHERE id = ?";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, user.getName());
            stmt.setString(2, user.getEmail());
            stmt.setString(3, user.getId());
            stmt.executeUpdate();
        } catch (SQLException e) {
            throw new DataAccessException("Failed to update user", e);
        }
    }
    
    public void delete(String id) {
        String sql = "DELETE FROM users WHERE id = ?";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, id);
            stmt.executeUpdate();
        } catch (SQLException e) {
            throw new DataAccessException("Failed to delete user", e);
        }
    }
    
    public User findById(String id) {
        String sql = "SELECT * FROM users WHERE id = ?";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, id);
            ResultSet rs = stmt.executeQuery();
            if (rs.next()) {
                return mapResultSetToUser(rs);
            }
        } catch (SQLException e) {
            throw new DataAccessException("Failed to find user", e);
        }
        return null;
    }
}
```

## 9.8 Row Data Gateway Pattern

The Row Data Gateway pattern provides an object that acts as a gateway to a single record in a data source.

### When to Use:
- When you need to work with individual records
- When you want to encapsulate row-level operations
- When you have complex row-level logic

### Real-World Analogy:
Think of a personal assistant who handles all communication and tasks for one specific person, knowing all the details about that person's preferences and requirements.

### Basic Implementation:
```java
// Row Data Gateway
public class UserRowGateway {
    private String id;
    private String name;
    private String email;
    private Connection connection;
    private boolean loaded = false;
    
    public UserRowGateway(Connection connection) {
        this.connection = connection;
    }
    
    public void load(String id) {
        String sql = "SELECT * FROM users WHERE id = ?";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, id);
            ResultSet rs = stmt.executeQuery();
            if (rs.next()) {
                this.id = rs.getString("id");
                this.name = rs.getString("name");
                this.email = rs.getString("email");
                this.loaded = true;
            }
        } catch (SQLException e) {
            throw new DataAccessException("Failed to load user", e);
        }
    }
    
    public void save() {
        if (loaded) {
            update();
        } else {
            insert();
        }
    }
    
    private void insert() {
        String sql = "INSERT INTO users (id, name, email) VALUES (?, ?, ?)";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, id);
            stmt.setString(2, name);
            stmt.setString(3, email);
            stmt.executeUpdate();
            loaded = true;
        } catch (SQLException e) {
            throw new DataAccessException("Failed to insert user", e);
        }
    }
    
    private void update() {
        String sql = "UPDATE users SET name = ?, email = ? WHERE id = ?";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, name);
            stmt.setString(2, email);
            stmt.setString(3, id);
            stmt.executeUpdate();
        } catch (SQLException e) {
            throw new DataAccessException("Failed to update user", e);
        }
    }
    
    // Getters and setters
    public String getId() { return id; }
    public void setId(String id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
}
```

## 9.9 Active Record Pattern

The Active Record pattern combines data access and business logic in a single object.

### When to Use:
- When you have simple domain objects
- When you want to keep data and behavior together
- When you need rapid development

### Real-World Analogy:
Think of a smart home device that not only stores its settings but also knows how to save and load those settings from storage.

### Basic Implementation:
```java
// Active Record base class
public abstract class ActiveRecord {
    protected Connection connection;
    
    public ActiveRecord(Connection connection) {
        this.connection = connection;
    }
    
    public void save() {
        if (isNew()) {
            insert();
        } else {
            update();
        }
    }
    
    public void delete() {
        if (!isNew()) {
            String sql = "DELETE FROM " + getTableName() + " WHERE id = ?";
            try (PreparedStatement stmt = connection.prepareStatement(sql)) {
                stmt.setString(1, getId());
                stmt.executeUpdate();
            } catch (SQLException e) {
                throw new DataAccessException("Failed to delete record", e);
            }
        }
    }
    
    protected abstract String getTableName();
    protected abstract String getId();
    protected abstract boolean isNew();
    protected abstract void insert();
    protected abstract void update();
}

// User Active Record
public class User extends ActiveRecord {
    private String id;
    private String name;
    private String email;
    
    public User(Connection connection) {
        super(connection);
    }
    
    public User(Connection connection, String id, String name, String email) {
        super(connection);
        this.id = id;
        this.name = name;
        this.email = email;
    }
    
    protected String getTableName() {
        return "users";
    }
    
    protected String getId() {
        return id;
    }
    
    protected boolean isNew() {
        return id == null;
    }
    
    protected void insert() {
        String sql = "INSERT INTO users (id, name, email) VALUES (?, ?, ?)";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, id);
            stmt.setString(2, name);
            stmt.setString(3, email);
            stmt.executeUpdate();
        } catch (SQLException e) {
            throw new DataAccessException("Failed to insert user", e);
        }
    }
    
    protected void update() {
        String sql = "UPDATE users SET name = ?, email = ? WHERE id = ?";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, name);
            stmt.setString(2, email);
            stmt.setString(3, id);
            stmt.executeUpdate();
        } catch (SQLException e) {
            throw new DataAccessException("Failed to update user", e);
        }
    }
    
    // Getters and setters
    public String getId() { return id; }
    public void setId(String id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
}
```

## 9.10 Data Mapper Pattern

The Data Mapper pattern separates the in-memory object model from the database schema, providing a mapping layer between them.

### When to Use:
- When you have complex object models
- When you need to decouple objects from database schema
- When you want to support multiple data sources

### Real-World Analogy:
Think of a translator who converts between two languages, ensuring that the meaning is preserved even though the words and structure are different.

### Basic Implementation:
```java
// Data Mapper interface
public interface DataMapper<T> {
    T findById(String id);
    List<T> findAll();
    void insert(T entity);
    void update(T entity);
    void delete(T entity);
}

// User Data Mapper
public class UserDataMapper implements DataMapper<User> {
    private Connection connection;
    private UserMapper userMapper;
    
    public UserDataMapper(Connection connection) {
        this.connection = connection;
        this.userMapper = new UserMapper();
    }
    
    public User findById(String id) {
        String sql = "SELECT * FROM users WHERE id = ?";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, id);
            ResultSet rs = stmt.executeQuery();
            if (rs.next()) {
                return userMapper.mapResultSetToUser(rs);
            }
        } catch (SQLException e) {
            throw new DataAccessException("Failed to find user", e);
        }
        return null;
    }
    
    public List<User> findAll() {
        String sql = "SELECT * FROM users";
        List<User> users = new ArrayList<>();
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            ResultSet rs = stmt.executeQuery();
            while (rs.next()) {
                users.add(userMapper.mapResultSetToUser(rs));
            }
        } catch (SQLException e) {
            throw new DataAccessException("Failed to find users", e);
        }
        return users;
    }
    
    public void insert(User user) {
        String sql = "INSERT INTO users (id, name, email) VALUES (?, ?, ?)";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, user.getId());
            stmt.setString(2, user.getName());
            stmt.setString(3, user.getEmail());
            stmt.executeUpdate();
        } catch (SQLException e) {
            throw new DataAccessException("Failed to insert user", e);
        }
    }
    
    public void update(User user) {
        String sql = "UPDATE users SET name = ?, email = ? WHERE id = ?";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, user.getName());
            stmt.setString(2, user.getEmail());
            stmt.setString(3, user.getId());
            stmt.executeUpdate();
        } catch (SQLException e) {
            throw new DataAccessException("Failed to update user", e);
        }
    }
    
    public void delete(User user) {
        String sql = "DELETE FROM users WHERE id = ?";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, user.getId());
            stmt.executeUpdate();
        } catch (SQLException e) {
            throw new DataAccessException("Failed to delete user", e);
        }
    }
}

// Mapper class
public class UserMapper {
    public User mapResultSetToUser(ResultSet rs) throws SQLException {
        return new User(
            rs.getString("id"),
            rs.getString("name"),
            rs.getString("email")
        );
    }
}
```

This comprehensive coverage of database patterns provides the foundation for building robust, maintainable data access layers. Each pattern addresses specific data access challenges and offers different trade-offs in terms of complexity, performance, and maintainability.