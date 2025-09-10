# Section 14 - UI/UX Patterns

## 14.1 Model-View-Controller (MVC)

The MVC pattern separates user interface concerns into three interconnected components: Model (data), View (presentation), and Controller (logic).

### When to Use:
- When you need clear separation of concerns
- When you want to make applications more maintainable
- When you need to support multiple views of the same data

### Real-World Analogy:
Think of a restaurant: the Model is the kitchen (data and business logic), the View is the dining room (presentation), and the Controller is the waiter (coordinates between kitchen and dining room).

### Basic Implementation:
```java
// Model - represents data and business logic
public class User {
    private String id;
    private String name;
    private String email;
    
    public User(String id, String name, String email) {
        this.id = id;
        this.name = name;
        this.email = email;
    }
    
    // Getters and setters
    public String getId() { return id; }
    public String getName() { return name; }
    public String getEmail() { return email; }
}

// View - handles presentation
public class UserView {
    public void displayUser(User user) {
        System.out.println("User ID: " + user.getId());
        System.out.println("Name: " + user.getName());
        System.out.println("Email: " + user.getEmail());
    }
    
    public void displayError(String message) {
        System.err.println("Error: " + message);
    }
    
    public void displaySuccess(String message) {
        System.out.println("Success: " + message);
    }
}

// Controller - handles user input and coordinates
public class UserController {
    private UserService userService;
    private UserView userView;
    
    public UserController(UserService userService, UserView userView) {
        this.userService = userService;
        this.userView = userView;
    }
    
    public void createUser(String name, String email) {
        try {
            User user = userService.createUser(name, email);
            userView.displaySuccess("User created successfully");
            userView.displayUser(user);
        } catch (Exception e) {
            userView.displayError("Failed to create user: " + e.getMessage());
        }
    }
    
    public void getUser(String id) {
        try {
            User user = userService.getUser(id);
            userView.displayUser(user);
        } catch (Exception e) {
            userView.displayError("Failed to get user: " + e.getMessage());
        }
    }
}

// Service layer
public class UserService {
    private UserRepository userRepository;
    
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }
    
    public User createUser(String name, String email) throws Exception {
        User user = new User(UUID.randomUUID().toString(), name, email);
        userRepository.save(user);
        return user;
    }
    
    public User getUser(String id) throws Exception {
        return userRepository.findById(id);
    }
}
```

## 14.2 Model-View-Presenter (MVP)

The MVP pattern separates the view from the model through a presenter that handles all UI logic.

### When to Use:
- When you need better testability
- When you want to separate UI logic from view
- When you need to support multiple UI technologies

### Real-World Analogy:
Think of a TV show where the presenter (MVP presenter) acts as an intermediary between the audience (view) and the content (model), controlling what information is shown and how it's presented.

### Basic Implementation:
```java
// View interface
public interface UserView {
    void displayUser(User user);
    void displayError(String message);
    void displaySuccess(String message);
    String getUserName();
    String getUserEmail();
    void setUserName(String name);
    void setUserEmail(String email);
}

// Presenter
public class UserPresenter {
    private UserView view;
    private UserService userService;
    
    public UserPresenter(UserView view, UserService userService) {
        this.view = view;
        this.userService = userService;
    }
    
    public void onCreateUser() {
        String name = view.getUserName();
        String email = view.getUserEmail();
        
        if (name == null || name.trim().isEmpty()) {
            view.displayError("Name is required");
            return;
        }
        
        if (email == null || email.trim().isEmpty()) {
            view.displayError("Email is required");
            return;
        }
        
        try {
            User user = userService.createUser(name, email);
            view.displaySuccess("User created successfully");
            view.displayUser(user);
        } catch (Exception e) {
            view.displayError("Failed to create user: " + e.getMessage());
        }
    }
    
    public void onGetUser(String id) {
        try {
            User user = userService.getUser(id);
            view.displayUser(user);
        } catch (Exception e) {
            view.displayError("Failed to get user: " + e.getMessage());
        }
    }
}

// Concrete view implementation
public class SwingUserView implements UserView {
    private JTextField nameField;
    private JTextField emailField;
    private JTextArea outputArea;
    
    public SwingUserView() {
        initializeComponents();
    }
    
    private void initializeComponents() {
        JFrame frame = new JFrame("User Management");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setLayout(new BorderLayout());
        
        JPanel inputPanel = new JPanel(new GridLayout(2, 2));
        inputPanel.add(new JLabel("Name:"));
        nameField = new JTextField();
        inputPanel.add(nameField);
        inputPanel.add(new JLabel("Email:"));
        emailField = new JTextField();
        inputPanel.add(emailField);
        
        outputArea = new JTextArea(10, 30);
        outputArea.setEditable(false);
        
        frame.add(inputPanel, BorderLayout.NORTH);
        frame.add(new JScrollPane(outputArea), BorderLayout.CENTER);
        
        frame.pack();
        frame.setVisible(true);
    }
    
    public void displayUser(User user) {
        outputArea.append("User ID: " + user.getId() + "\n");
        outputArea.append("Name: " + user.getName() + "\n");
        outputArea.append("Email: " + user.getEmail() + "\n\n");
    }
    
    public void displayError(String message) {
        outputArea.append("Error: " + message + "\n\n");
    }
    
    public void displaySuccess(String message) {
        outputArea.append("Success: " + message + "\n\n");
    }
    
    public String getUserName() {
        return nameField.getText();
    }
    
    public String getUserEmail() {
        return emailField.getText();
    }
    
    public void setUserName(String name) {
        nameField.setText(name);
    }
    
    public void setUserEmail(String email) {
        emailField.setText(email);
    }
}
```

## 14.3 Model-View-ViewModel (MVVM)

The MVVM pattern uses data binding to connect the view and view model, reducing the need for manual UI updates.

### When to Use:
- When you need two-way data binding
- When you want to reduce boilerplate code
- When you need to support complex UI interactions

### Real-World Analogy:
Think of a smart home system where the view (your phone app) automatically updates when the view model (home state) changes, and vice versa. You don't need to manually refresh the app to see the current temperature.

### Basic Implementation:
```java
// ViewModel base class
public abstract class ViewModel {
    private List<PropertyChangeListener> listeners = new ArrayList<>();
    
    protected void firePropertyChange(String propertyName, Object oldValue, Object newValue) {
        for (PropertyChangeListener listener : listeners) {
            listener.propertyChange(new PropertyChangeEvent(this, propertyName, oldValue, newValue));
        }
    }
    
    public void addPropertyChangeListener(PropertyChangeListener listener) {
        listeners.add(listener);
    }
    
    public void removePropertyChangeListener(PropertyChangeListener listener) {
        listeners.remove(listener);
    }
}

// User ViewModel
public class UserViewModel extends ViewModel {
    private String name;
    private String email;
    private String errorMessage;
    private boolean isLoading;
    private UserService userService;
    
    public UserViewModel(UserService userService) {
        this.userService = userService;
    }
    
    public String getName() {
        return name;
    }
    
    public void setName(String name) {
        String oldValue = this.name;
        this.name = name;
        firePropertyChange("name", oldValue, name);
    }
    
    public String getEmail() {
        return email;
    }
    
    public void setEmail(String email) {
        String oldValue = this.email;
        this.email = email;
        firePropertyChange("email", oldValue, email);
    }
    
    public String getErrorMessage() {
        return errorMessage;
    }
    
    public void setErrorMessage(String errorMessage) {
        String oldValue = this.errorMessage;
        this.errorMessage = errorMessage;
        firePropertyChange("errorMessage", oldValue, errorMessage);
    }
    
    public boolean isLoading() {
        return isLoading;
    }
    
    public void setLoading(boolean loading) {
        boolean oldValue = this.isLoading;
        this.isLoading = loading;
        firePropertyChange("loading", oldValue, loading);
    }
    
    public void createUser() {
        setLoading(true);
        setErrorMessage(null);
        
        try {
            User user = userService.createUser(name, email);
            // Handle success
        } catch (Exception e) {
            setErrorMessage("Failed to create user: " + e.getMessage());
        } finally {
            setLoading(false);
        }
    }
}

// View with data binding
public class UserView {
    private UserViewModel viewModel;
    private JTextField nameField;
    private JTextField emailField;
    private JLabel errorLabel;
    private JButton createButton;
    private JProgressBar progressBar;
    
    public UserView(UserViewModel viewModel) {
        this.viewModel = viewModel;
        initializeComponents();
        bindToViewModel();
    }
    
    private void initializeComponents() {
        JFrame frame = new JFrame("User Management");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setLayout(new BorderLayout());
        
        JPanel inputPanel = new JPanel(new GridLayout(3, 2));
        inputPanel.add(new JLabel("Name:"));
        nameField = new JTextField();
        inputPanel.add(nameField);
        inputPanel.add(new JLabel("Email:"));
        emailField = new JTextField();
        inputPanel.add(emailField);
        inputPanel.add(new JLabel("Error:"));
        errorLabel = new JLabel();
        inputPanel.add(errorLabel);
        
        createButton = new JButton("Create User");
        progressBar = new JProgressBar();
        
        frame.add(inputPanel, BorderLayout.NORTH);
        frame.add(createButton, BorderLayout.CENTER);
        frame.add(progressBar, BorderLayout.SOUTH);
        
        frame.pack();
        frame.setVisible(true);
    }
    
    private void bindToViewModel() {
        // Bind view to view model
        nameField.addActionListener(e -> viewModel.setName(nameField.getText()));
        emailField.addActionListener(e -> viewModel.setEmail(emailField.getText()));
        createButton.addActionListener(e -> viewModel.createUser());
        
        // Bind view model to view
        viewModel.addPropertyChangeListener(e -> {
            switch (e.getPropertyName()) {
                case "name":
                    nameField.setText((String) e.getNewValue());
                    break;
                case "email":
                    emailField.setText((String) e.getNewValue());
                    break;
                case "errorMessage":
                    errorLabel.setText((String) e.getNewValue());
                    break;
                case "loading":
                    createButton.setEnabled(!(Boolean) e.getNewValue());
                    progressBar.setVisible((Boolean) e.getNewValue());
                    break;
            }
        });
    }
}
```

## 14.4 Presentation Model Pattern

The Presentation Model pattern encapsulates the state and behavior of a view, making it easier to test and maintain.

### When to Use:
- When you need to test UI logic
- When you want to separate view state from view
- When you need to support multiple views

### Real-World Analogy:
Think of a blueprint for a house. The blueprint (presentation model) contains all the specifications and rules, while the actual house (view) is built according to those specifications.

### Basic Implementation:
```java
// Presentation Model
public class UserPresentationModel {
    private String name;
    private String email;
    private String errorMessage;
    private boolean isValid;
    private UserService userService;
    
    public UserPresentationModel(UserService userService) {
        this.userService = userService;
        this.isValid = false;
    }
    
    public String getName() {
        return name;
    }
    
    public void setName(String name) {
        this.name = name;
        validate();
    }
    
    public String getEmail() {
        return email;
    }
    
    public void setEmail(String email) {
        this.email = email;
        validate();
    }
    
    public String getErrorMessage() {
        return errorMessage;
    }
    
    public boolean isValid() {
        return isValid;
    }
    
    private void validate() {
        if (name == null || name.trim().isEmpty()) {
            errorMessage = "Name is required";
            isValid = false;
        } else if (email == null || email.trim().isEmpty()) {
            errorMessage = "Email is required";
            isValid = false;
        } else if (!email.contains("@")) {
            errorMessage = "Invalid email format";
            isValid = false;
        } else {
            errorMessage = null;
            isValid = true;
        }
    }
    
    public void createUser() throws Exception {
        if (!isValid) {
            throw new ValidationException(errorMessage);
        }
        
        User user = userService.createUser(name, email);
        // Reset form
        name = null;
        email = null;
        validate();
    }
}

// View that uses presentation model
public class UserView {
    private UserPresentationModel presentationModel;
    private JTextField nameField;
    private JTextField emailField;
    private JLabel errorLabel;
    private JButton createButton;
    
    public UserView(UserPresentationModel presentationModel) {
        this.presentationModel = presentationModel;
        initializeComponents();
        bindToPresentationModel();
    }
    
    private void initializeComponents() {
        JFrame frame = new JFrame("User Management");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setLayout(new BorderLayout());
        
        JPanel inputPanel = new JPanel(new GridLayout(3, 2));
        inputPanel.add(new JLabel("Name:"));
        nameField = new JTextField();
        inputPanel.add(nameField);
        inputPanel.add(new JLabel("Email:"));
        emailField = new JTextField();
        inputPanel.add(emailField);
        inputPanel.add(new JLabel("Error:"));
        errorLabel = new JLabel();
        inputPanel.add(errorLabel);
        
        createButton = new JButton("Create User");
        
        frame.add(inputPanel, BorderLayout.NORTH);
        frame.add(createButton, BorderLayout.CENTER);
        
        frame.pack();
        frame.setVisible(true);
    }
    
    private void bindToPresentationModel() {
        nameField.addActionListener(e -> presentationModel.setName(nameField.getText()));
        emailField.addActionListener(e -> presentationModel.setEmail(emailField.getText()));
        createButton.addActionListener(e -> {
            try {
                presentationModel.createUser();
                nameField.setText("");
                emailField.setText("");
                errorLabel.setText("");
            } catch (Exception ex) {
                errorLabel.setText(ex.getMessage());
            }
        });
        
        // Update UI based on presentation model state
        Timer timer = new Timer(100, e -> {
            createButton.setEnabled(presentationModel.isValid());
            errorLabel.setText(presentationModel.getErrorMessage());
        });
        timer.start();
    }
}
```

## 14.5 Supervising Controller Pattern

The Supervising Controller pattern uses a controller to handle complex UI logic while the view handles simple data binding.

### When to Use:
- When you have complex UI logic
- When you want to keep the view simple
- When you need to coordinate multiple views

### Real-World Analogy:
Think of a supervisor at a construction site who oversees the work and makes complex decisions, while the workers (view) focus on their specific tasks and follow the supervisor's instructions.

### Basic Implementation:
```java
// Supervising Controller
public class UserSupervisingController {
    private UserView view;
    private UserService userService;
    private User currentUser;
    
    public UserSupervisingController(UserView view, UserService userService) {
        this.view = view;
        this.userService = userService;
        setupViewBindings();
    }
    
    private void setupViewBindings() {
        view.addCreateUserListener(this::handleCreateUser);
        view.addGetUserListener(this::handleGetUser);
        view.addUpdateUserListener(this::handleUpdateUser);
        view.addDeleteUserListener(this::handleDeleteUser);
    }
    
    private void handleCreateUser(String name, String email) {
        try {
            User user = userService.createUser(name, email);
            view.displayUser(user);
            view.showSuccess("User created successfully");
        } catch (Exception e) {
            view.showError("Failed to create user: " + e.getMessage());
        }
    }
    
    private void handleGetUser(String id) {
        try {
            User user = userService.getUser(id);
            currentUser = user;
            view.displayUser(user);
        } catch (Exception e) {
            view.showError("Failed to get user: " + e.getMessage());
        }
    }
    
    private void handleUpdateUser(String name, String email) {
        if (currentUser == null) {
            view.showError("No user selected");
            return;
        }
        
        try {
            currentUser.setName(name);
            currentUser.setEmail(email);
            userService.updateUser(currentUser);
            view.displayUser(currentUser);
            view.showSuccess("User updated successfully");
        } catch (Exception e) {
            view.showError("Failed to update user: " + e.getMessage());
        }
    }
    
    private void handleDeleteUser() {
        if (currentUser == null) {
            view.showError("No user selected");
            return;
        }
        
        try {
            userService.deleteUser(currentUser.getId());
            currentUser = null;
            view.clearUser();
            view.showSuccess("User deleted successfully");
        } catch (Exception e) {
            view.showError("Failed to delete user: " + e.getMessage());
        }
    }
}

// View interface
public interface UserView {
    void addCreateUserListener(BiConsumer<String, String> listener);
    void addGetUserListener(Consumer<String> listener);
    void addUpdateUserListener(BiConsumer<String, String> listener);
    void addDeleteUserListener(Runnable listener);
    void displayUser(User user);
    void clearUser();
    void showSuccess(String message);
    void showError(String message);
}
```

## 14.6 Passive View Pattern

The Passive View pattern makes the view completely passive, with all logic handled by the controller.

### When to Use:
- When you want maximum testability
- When you need to keep the view simple
- When you want to centralize all UI logic

### Real-World Analogy:
Think of a puppet show where the puppets (view) are completely passive and only move when the puppeteer (controller) pulls the strings. The puppets don't make any decisions on their own.

### Basic Implementation:
```java
// Passive View
public class PassiveUserView {
    private JTextField nameField;
    private JTextField emailField;
    private JTextArea outputArea;
    private JButton createButton;
    private JButton getButton;
    private JButton updateButton;
    private JButton deleteButton;
    
    public PassiveUserView() {
        initializeComponents();
    }
    
    private void initializeComponents() {
        JFrame frame = new JFrame("User Management");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setLayout(new BorderLayout());
        
        JPanel inputPanel = new JPanel(new GridLayout(2, 2));
        inputPanel.add(new JLabel("Name:"));
        nameField = new JTextField();
        inputPanel.add(nameField);
        inputPanel.add(new JLabel("Email:"));
        emailField = new JTextField();
        inputPanel.add(emailField);
        
        outputArea = new JTextArea(10, 30);
        outputArea.setEditable(false);
        
        JPanel buttonPanel = new JPanel(new FlowLayout());
        createButton = new JButton("Create");
        getButton = new JButton("Get");
        updateButton = new JButton("Update");
        deleteButton = new JButton("Delete");
        buttonPanel.add(createButton);
        buttonPanel.add(getButton);
        buttonPanel.add(updateButton);
        buttonPanel.add(deleteButton);
        
        frame.add(inputPanel, BorderLayout.NORTH);
        frame.add(new JScrollPane(outputArea), BorderLayout.CENTER);
        frame.add(buttonPanel, BorderLayout.SOUTH);
        
        frame.pack();
        frame.setVisible(true);
    }
    
    // Getters for controller to access view state
    public String getName() {
        return nameField.getText();
    }
    
    public String getEmail() {
        return emailField.getText();
    }
    
    // Setters for controller to update view
    public void setName(String name) {
        nameField.setText(name);
    }
    
    public void setEmail(String email) {
        emailField.setText(email);
    }
    
    public void appendOutput(String text) {
        outputArea.append(text + "\n");
    }
    
    public void clearOutput() {
        outputArea.setText("");
    }
    
    // Button getters for controller to add listeners
    public JButton getCreateButton() {
        return createButton;
    }
    
    public JButton getGetButton() {
        return getButton;
    }
    
    public JButton getUpdateButton() {
        return updateButton;
    }
    
    public JButton getDeleteButton() {
        return deleteButton;
    }
}

// Controller that handles all logic
public class PassiveUserController {
    private PassiveUserView view;
    private UserService userService;
    private User currentUser;
    
    public PassiveUserController(PassiveUserView view, UserService userService) {
        this.view = view;
        this.userService = userService;
        setupEventHandlers();
    }
    
    private void setupEventHandlers() {
        view.getCreateButton().addActionListener(e -> handleCreateUser());
        view.getGetButton().addActionListener(e -> handleGetUser());
        view.getUpdateButton().addActionListener(e -> handleUpdateUser());
        view.getDeleteButton().addActionListener(e -> handleDeleteUser());
    }
    
    private void handleCreateUser() {
        String name = view.getName();
        String email = view.getEmail();
        
        if (name == null || name.trim().isEmpty()) {
            view.appendOutput("Error: Name is required");
            return;
        }
        
        if (email == null || email.trim().isEmpty()) {
            view.appendOutput("Error: Email is required");
            return;
        }
        
        try {
            User user = userService.createUser(name, email);
            view.appendOutput("User created: " + user.getName() + " (" + user.getEmail() + ")");
            view.setName("");
            view.setEmail("");
        } catch (Exception e) {
            view.appendOutput("Error: Failed to create user - " + e.getMessage());
        }
    }
    
    private void handleGetUser() {
        // Implementation for getting user
    }
    
    private void handleUpdateUser() {
        // Implementation for updating user
    }
    
    private void handleDeleteUser() {
        // Implementation for deleting user
    }
}
```

## 14.7 Observer Pattern in UI

The Observer pattern allows UI components to be notified of changes in the underlying data model.

### When to Use:
- When you need to update multiple UI components
- When you want to decouple UI from data
- When you need to support dynamic UI updates

### Real-World Analogy:
Think of a news subscription service. When news is published, all subscribers are automatically notified and can update their displays accordingly.

### Basic Implementation:
```java
// Observer interface
public interface Observer {
    void update(Observable observable, Object arg);
}

// Observable interface
public interface Observable {
    void addObserver(Observer observer);
    void removeObserver(Observer observer);
    void notifyObservers();
    void notifyObservers(Object arg);
}

// User model that can be observed
public class UserModel implements Observable {
    private String name;
    private String email;
    private List<Observer> observers = new ArrayList<>();
    
    public String getName() {
        return name;
    }
    
    public void setName(String name) {
        String oldValue = this.name;
        this.name = name;
        notifyObservers(new PropertyChangeEvent(this, "name", oldValue, name));
    }
    
    public String getEmail() {
        return email;
    }
    
    public void setEmail(String email) {
        String oldValue = this.email;
        this.email = email;
        notifyObservers(new PropertyChangeEvent(this, "email", oldValue, email));
    }
    
    public void addObserver(Observer observer) {
        observers.add(observer);
    }
    
    public void removeObserver(Observer observer) {
        observers.remove(observer);
    }
    
    public void notifyObservers() {
        notifyObservers(null);
    }
    
    public void notifyObservers(Object arg) {
        for (Observer observer : observers) {
            observer.update(this, arg);
        }
    }
}

// UI component that observes the model
public class UserDisplayPanel extends JPanel implements Observer {
    private JLabel nameLabel;
    private JLabel emailLabel;
    private UserModel userModel;
    
    public UserDisplayPanel(UserModel userModel) {
        this.userModel = userModel;
        userModel.addObserver(this);
        initializeComponents();
    }
    
    private void initializeComponents() {
        setLayout(new GridLayout(2, 2));
        add(new JLabel("Name:"));
        nameLabel = new JLabel();
        add(nameLabel);
        add(new JLabel("Email:"));
        emailLabel = new JLabel();
        add(emailLabel);
        
        updateDisplay();
    }
    
    public void update(Observable observable, Object arg) {
        if (observable == userModel) {
            updateDisplay();
        }
    }
    
    private void updateDisplay() {
        nameLabel.setText(userModel.getName() != null ? userModel.getName() : "");
        emailLabel.setText(userModel.getEmail() != null ? userModel.getEmail() : "");
    }
}

// Property change event
public class PropertyChangeEvent {
    private Object source;
    private String propertyName;
    private Object oldValue;
    private Object newValue;
    
    public PropertyChangeEvent(Object source, String propertyName, Object oldValue, Object newValue) {
        this.source = source;
        this.propertyName = propertyName;
        this.oldValue = oldValue;
        this.newValue = newValue;
    }
    
    // Getters
    public Object getSource() { return source; }
    public String getPropertyName() { return propertyName; }
    public Object getOldValue() { return oldValue; }
    public Object getNewValue() { return newValue; }
}
```

## 14.8 Command Pattern in UI

The Command pattern encapsulates UI actions as objects, allowing for undo/redo functionality and action queuing.

### When to Use:
- When you need undo/redo functionality
- When you want to queue actions
- When you need to log user actions

### Real-World Analogy:
Think of a remote control that can store commands. You can program the remote to execute a series of commands, and it will execute them in sequence, allowing you to automate complex operations.

### Basic Implementation:
```java
// Command interface
public interface Command {
    void execute();
    void undo();
    String getDescription();
}

// Create user command
public class CreateUserCommand implements Command {
    private UserService userService;
    private String name;
    private String email;
    private User createdUser;
    
    public CreateUserCommand(UserService userService, String name, String email) {
        this.userService = userService;
        this.name = name;
        this.email = email;
    }
    
    public void execute() {
        try {
            createdUser = userService.createUser(name, email);
        } catch (Exception e) {
            throw new RuntimeException("Failed to create user", e);
        }
    }
    
    public void undo() {
        if (createdUser != null) {
            try {
                userService.deleteUser(createdUser.getId());
            } catch (Exception e) {
                throw new RuntimeException("Failed to undo user creation", e);
            }
        }
    }
    
    public String getDescription() {
        return "Create user: " + name;
    }
}

// Update user command
public class UpdateUserCommand implements Command {
    private UserService userService;
    private User originalUser;
    private User updatedUser;
    private User previousUser;
    
    public UpdateUserCommand(UserService userService, User updatedUser) {
        this.userService = userService;
        this.updatedUser = updatedUser;
    }
    
    public void execute() {
        try {
            originalUser = userService.getUser(updatedUser.getId());
            previousUser = new User(originalUser); // Create copy
            userService.updateUser(updatedUser);
        } catch (Exception e) {
            throw new RuntimeException("Failed to update user", e);
        }
    }
    
    public void undo() {
        if (previousUser != null) {
            try {
                userService.updateUser(previousUser);
            } catch (Exception e) {
                throw new RuntimeException("Failed to undo user update", e);
            }
        }
    }
    
    public String getDescription() {
        return "Update user: " + updatedUser.getName();
    }
}

// Command invoker
public class CommandInvoker {
    private List<Command> commandHistory = new ArrayList<>();
    private int currentIndex = -1;
    
    public void executeCommand(Command command) {
        command.execute();
        commandHistory.add(command);
        currentIndex++;
    }
    
    public void undo() {
        if (currentIndex >= 0) {
            Command command = commandHistory.get(currentIndex);
            command.undo();
            currentIndex--;
        }
    }
    
    public void redo() {
        if (currentIndex < commandHistory.size() - 1) {
            currentIndex++;
            Command command = commandHistory.get(currentIndex);
            command.execute();
        }
    }
    
    public List<String> getCommandHistory() {
        return commandHistory.stream()
            .map(Command::getDescription)
            .collect(Collectors.toList());
    }
}

// UI that uses commands
public class CommandBasedUserView extends JFrame {
    private CommandInvoker commandInvoker;
    private UserService userService;
    private JTextField nameField;
    private JTextField emailField;
    private JButton createButton;
    private JButton undoButton;
    private JButton redoButton;
    
    public CommandBasedUserView(CommandInvoker commandInvoker, UserService userService) {
        this.commandInvoker = commandInvoker;
        this.userService = userService;
        initializeComponents();
    }
    
    private void initializeComponents() {
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new BorderLayout());
        
        JPanel inputPanel = new JPanel(new GridLayout(2, 2));
        inputPanel.add(new JLabel("Name:"));
        nameField = new JTextField();
        inputPanel.add(nameField);
        inputPanel.add(new JLabel("Email:"));
        emailField = new JTextField();
        inputPanel.add(emailField);
        
        JPanel buttonPanel = new JPanel(new FlowLayout());
        createButton = new JButton("Create User");
        undoButton = new JButton("Undo");
        redoButton = new JButton("Redo");
        buttonPanel.add(createButton);
        buttonPanel.add(undoButton);
        buttonPanel.add(redoButton);
        
        add(inputPanel, BorderLayout.NORTH);
        add(buttonPanel, BorderLayout.SOUTH);
        
        createButton.addActionListener(e -> {
            String name = nameField.getText();
            String email = emailField.getText();
            Command command = new CreateUserCommand(userService, name, email);
            commandInvoker.executeCommand(command);
            nameField.setText("");
            emailField.setText("");
        });
        
        undoButton.addActionListener(e -> commandInvoker.undo());
        redoButton.addActionListener(e -> commandInvoker.redo());
        
        pack();
        setVisible(true);
    }
}
```

## 14.9 Strategy Pattern in UI

The Strategy pattern allows UI components to use different algorithms or behaviors interchangeably.

### When to Use:
- When you need different UI behaviors
- When you want to make UI components configurable
- When you need to support multiple UI themes

### Real-World Analogy:
Think of a camera with different shooting modes (portrait, landscape, night). The camera (UI component) can switch between different strategies (shooting modes) based on the situation.

### Basic Implementation:
```java
// Validation strategy interface
public interface ValidationStrategy {
    boolean validate(String input);
    String getErrorMessage();
}

// Email validation strategy
public class EmailValidationStrategy implements ValidationStrategy {
    private static final String EMAIL_REGEX = "^[A-Za-z0-9+_.-]+@(.+)$";
    private Pattern pattern = Pattern.compile(EMAIL_REGEX);
    
    public boolean validate(String input) {
        return input != null && pattern.matcher(input).matches();
    }
    
    public String getErrorMessage() {
        return "Invalid email format";
    }
}

// Name validation strategy
public class NameValidationStrategy implements ValidationStrategy {
    public boolean validate(String input) {
        return input != null && !input.trim().isEmpty() && input.length() >= 2;
    }
    
    public String getErrorMessage() {
        return "Name must be at least 2 characters long";
    }
}

// UI component that uses validation strategy
public class ValidatedTextField extends JTextField {
    private ValidationStrategy validationStrategy;
    private JLabel errorLabel;
    
    public ValidatedTextField(ValidationStrategy validationStrategy) {
        this.validationStrategy = validationStrategy;
        this.errorLabel = new JLabel();
        setupValidation();
    }
    
    private void setupValidation() {
        addFocusListener(new FocusAdapter() {
            public void focusLost(FocusEvent e) {
                validateInput();
            }
        });
    }
    
    private void validateInput() {
        String input = getText();
        if (validationStrategy.validate(input)) {
            errorLabel.setText("");
            setBorder(BorderFactory.createLineBorder(Color.GREEN));
        } else {
            errorLabel.setText(validationStrategy.getErrorMessage());
            setBorder(BorderFactory.createLineBorder(Color.RED));
        }
    }
    
    public void setValidationStrategy(ValidationStrategy strategy) {
        this.validationStrategy = strategy;
        validateInput();
    }
    
    public JLabel getErrorLabel() {
        return errorLabel;
    }
}

// Theme strategy interface
public interface ThemeStrategy {
    Color getBackgroundColor();
    Color getForegroundColor();
    Font getFont();
    Border getBorder();
}

// Light theme strategy
public class LightThemeStrategy implements ThemeStrategy {
    public Color getBackgroundColor() {
        return Color.WHITE;
    }
    
    public Color getForegroundColor() {
        return Color.BLACK;
    }
    
    public Font getFont() {
        return new Font("Arial", Font.PLAIN, 12);
    }
    
    public Border getBorder() {
        return BorderFactory.createLineBorder(Color.GRAY);
    }
}

// Dark theme strategy
public class DarkThemeStrategy implements ThemeStrategy {
    public Color getBackgroundColor() {
        return Color.DARK_GRAY;
    }
    
    public Color getForegroundColor() {
        return Color.WHITE;
    }
    
    public Font getFont() {
        return new Font("Arial", Font.PLAIN, 12);
    }
    
    public Border getBorder() {
        return BorderFactory.createLineBorder(Color.LIGHT_GRAY);
    }
}

// Themed UI component
public class ThemedPanel extends JPanel {
    private ThemeStrategy themeStrategy;
    
    public ThemedPanel(ThemeStrategy themeStrategy) {
        this.themeStrategy = themeStrategy;
        applyTheme();
    }
    
    public void setThemeStrategy(ThemeStrategy strategy) {
        this.themeStrategy = strategy;
        applyTheme();
    }
    
    private void applyTheme() {
        setBackground(themeStrategy.getBackgroundColor());
        setForeground(themeStrategy.getForegroundColor());
        setFont(themeStrategy.getFont());
        setBorder(themeStrategy.getBorder());
    }
}
```

## 14.10 Factory Pattern in UI

The Factory Pattern creates UI components based on configuration or user preferences.

### When to Use:
- When you need to create different types of UI components
- When you want to centralize UI component creation
- When you need to support multiple UI technologies

### Real-World Analogy:
Think of a car factory that can produce different types of vehicles (sedans, SUVs, trucks) based on customer orders. The factory knows how to create each type and can produce them on demand.

### Basic Implementation:
```java
// UI component factory interface
public interface UIComponentFactory {
    JComponent createComponent(String type, Map<String, Object> properties);
}

// Form field factory
public class FormFieldFactory implements UIComponentFactory {
    public JComponent createComponent(String type, Map<String, Object> properties) {
        switch (type.toLowerCase()) {
            case "textfield":
                return createTextField(properties);
            case "passwordfield":
                return createPasswordField(properties);
            case "combobox":
                return createComboBox(properties);
            case "checkbox":
                return createCheckBox(properties);
            case "radiobutton":
                return createRadioButton(properties);
            default:
                throw new IllegalArgumentException("Unknown component type: " + type);
        }
    }
    
    private JTextField createTextField(Map<String, Object> properties) {
        JTextField field = new JTextField();
        if (properties.containsKey("placeholder")) {
            field.setToolTipText((String) properties.get("placeholder"));
        }
        if (properties.containsKey("columns")) {
            field.setColumns((Integer) properties.get("columns"));
        }
        return field;
    }
    
    private JPasswordField createPasswordField(Map<String, Object> properties) {
        JPasswordField field = new JPasswordField();
        if (properties.containsKey("placeholder")) {
            field.setToolTipText((String) properties.get("placeholder"));
        }
        if (properties.containsKey("columns")) {
            field.setColumns((Integer) properties.get("columns"));
        }
        return field;
    }
    
    private JComboBox<String> createComboBox(Map<String, Object> properties) {
        JComboBox<String> comboBox = new JComboBox<>();
        if (properties.containsKey("options")) {
            String[] options = (String[]) properties.get("options");
            for (String option : options) {
                comboBox.addItem(option);
            }
        }
        return comboBox;
    }
    
    private JCheckBox createCheckBox(Map<String, Object> properties) {
        JCheckBox checkBox = new JCheckBox();
        if (properties.containsKey("text")) {
            checkBox.setText((String) properties.get("text"));
        }
        if (properties.containsKey("selected")) {
            checkBox.setSelected((Boolean) properties.get("selected"));
        }
        return checkBox;
    }
    
    private JRadioButton createRadioButton(Map<String, Object> properties) {
        JRadioButton radioButton = new JRadioButton();
        if (properties.containsKey("text")) {
            radioButton.setText((String) properties.get("text"));
        }
        if (properties.containsKey("selected")) {
            radioButton.setSelected((Boolean) properties.get("selected"));
        }
        return radioButton;
    }
}

// Form builder that uses the factory
public class FormBuilder {
    private UIComponentFactory componentFactory;
    private JPanel formPanel;
    
    public FormBuilder(UIComponentFactory componentFactory) {
        this.componentFactory = componentFactory;
        this.formPanel = new JPanel(new GridBagLayout());
    }
    
    public FormBuilder addField(String label, String type, Map<String, Object> properties) {
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(5, 5, 5, 5);
        
        // Add label
        gbc.gridx = 0;
        gbc.gridy = formPanel.getComponentCount() / 2;
        gbc.anchor = GridBagConstraints.EAST;
        formPanel.add(new JLabel(label + ":"), gbc);
        
        // Add component
        gbc.gridx = 1;
        gbc.anchor = GridBagConstraints.WEST;
        gbc.fill = GridBagConstraints.HORIZONTAL;
        gbc.weightx = 1.0;
        JComponent component = componentFactory.createComponent(type, properties);
        formPanel.add(component, gbc);
        
        return this;
    }
    
    public JPanel build() {
        return formPanel;
    }
}

// Usage example
public class UserFormBuilder {
    public static JPanel createUserForm() {
        FormFieldFactory factory = new FormFieldFactory();
        FormBuilder builder = new FormBuilder(factory);
        
        Map<String, Object> nameProperties = new HashMap<>();
        nameProperties.put("placeholder", "Enter your name");
        nameProperties.put("columns", 20);
        
        Map<String, Object> emailProperties = new HashMap<>();
        emailProperties.put("placeholder", "Enter your email");
        emailProperties.put("columns", 20);
        
        Map<String, Object> passwordProperties = new HashMap<>();
        passwordProperties.put("placeholder", "Enter your password");
        passwordProperties.put("columns", 20);
        
        Map<String, Object> roleProperties = new HashMap<>();
        roleProperties.put("options", new String[]{"Admin", "User", "Guest"});
        
        Map<String, Object> newsletterProperties = new HashMap<>();
        newsletterProperties.put("text", "Subscribe to newsletter");
        newsletterProperties.put("selected", false);
        
        return builder
            .addField("Name", "textfield", nameProperties)
            .addField("Email", "textfield", emailProperties)
            .addField("Password", "passwordfield", passwordProperties)
            .addField("Role", "combobox", roleProperties)
            .addField("Newsletter", "checkbox", newsletterProperties)
            .build();
    }
}
```

This comprehensive coverage of UI/UX patterns provides the foundation for building maintainable, testable, and flexible user interfaces. Each pattern addresses specific UI development challenges and offers different approaches to organizing and managing UI components.