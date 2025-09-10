# Section 18 - Mobile Patterns

## 18.1 Mobile Architecture Patterns

Mobile architecture patterns provide structured approaches to building mobile applications that are scalable, maintainable, and performant.

### When to Use:
- When building mobile applications
- When you need to handle different screen sizes and orientations
- When you want to separate concerns in mobile apps

### Real-World Analogy:
Think of designing a mobile home that needs to be compact, efficient, and adaptable to different locations and weather conditions. Every component must be carefully planned to maximize space and functionality.

### Basic Implementation:
```kotlin
// MVVM pattern for mobile
class UserViewModel : ViewModel() {
    private val _users = MutableLiveData<List<User>>()
    val users: LiveData<List<User>> = _users
    
    private val _loading = MutableLiveData<Boolean>()
    val loading: LiveData<Boolean> = _loading
    
    fun loadUsers() {
        _loading.value = true
        userRepository.getUsers()
            .observeOn(AndroidSchedulers.mainThread())
            .subscribe(
                { users ->
                    _users.value = users
                    _loading.value = false
                },
                { error ->
                    _loading.value = false
                    // Handle error
                }
            )
    }
}

// Repository pattern
class UserRepository {
    private val apiService = ApiService.create()
    private val localDatabase = AppDatabase.getInstance()
    
    fun getUsers(): Observable<List<User>> {
        return apiService.getUsers()
            .doOnNext { users ->
                localDatabase.userDao().insertAll(users)
            }
            .onErrorResumeNext { error ->
                // Fallback to local data
                localDatabase.userDao().getAllUsers().toObservable()
            }
    }
}
```

## 18.2 Offline-First Patterns

Offline-first patterns ensure that mobile applications work seamlessly even when network connectivity is poor or unavailable.

### When to Use:
- When you need to provide functionality without internet
- When you want to improve user experience in poor network conditions
- When you need to sync data when connectivity is restored

### Real-World Analogy:
Think of a notebook that you can write in anywhere, even without internet. You can take notes, make changes, and when you get back to a place with internet, you can sync your notes with your digital system.

### Basic Implementation:
```kotlin
// Offline-first data manager
class OfflineFirstDataManager {
    private val localDatabase = AppDatabase.getInstance()
    private val syncManager = SyncManager()
    
    fun saveUser(user: User) {
        // Save locally first
        localDatabase.userDao().insert(user)
        
        // Try to sync with server
        syncManager.syncUser(user)
    }
    
    fun getUsers(): LiveData<List<User>> {
        return localDatabase.userDao().getAllUsers()
    }
    
    fun syncPendingChanges() {
        val pendingUsers = localDatabase.userDao().getPendingSyncUsers()
        pendingUsers.forEach { user ->
            syncManager.syncUser(user)
        }
    }
}

// Sync manager
class SyncManager {
    private val apiService = ApiService.create()
    
    fun syncUser(user: User) {
        apiService.saveUser(user)
            .subscribeOn(Schedulers.io())
            .observeOn(AndroidSchedulers.mainThread())
            .subscribe(
                { response ->
                    // Mark as synced
                    user.isSynced = true
                    localDatabase.userDao().update(user)
                },
                { error ->
                    // Keep as pending sync
                    user.isSynced = false
                    localDatabase.userDao().update(user)
                }
            )
    }
}
```

## 18.3 Sync Patterns

Sync patterns handle data synchronization between mobile devices and servers, ensuring data consistency across all platforms.

### When to Use:
- When you need to keep data synchronized across devices
- When you want to handle conflicts in data updates
- When you need to optimize sync performance

### Real-World Analogy:
Think of a shared document that multiple people can edit. When someone makes changes, those changes need to be synchronized with everyone else's version, and conflicts need to be resolved when two people edit the same part.

### Basic Implementation:
```kotlin
// Sync service
class SyncService {
    private val apiService = ApiService.create()
    private val localDatabase = AppDatabase.getInstance()
    
    fun syncData(): Completable {
        return Completable.fromAction {
            val lastSyncTime = getLastSyncTime()
            val localChanges = getLocalChangesSince(lastSyncTime)
            val serverChanges = getServerChangesSince(lastSyncTime)
            
            // Handle conflicts
            val conflicts = findConflicts(localChanges, serverChanges)
            resolveConflicts(conflicts)
            
            // Apply changes
            applyLocalChanges(localChanges)
            applyServerChanges(serverChanges)
            
            updateLastSyncTime(System.currentTimeMillis())
        }
    }
    
    private fun findConflicts(localChanges: List<Change>, serverChanges: List<Change>): List<Conflict> {
        val conflicts = mutableListOf<Conflict>()
        
        localChanges.forEach { localChange ->
            serverChanges.forEach { serverChange ->
                if (localChange.entityId == serverChange.entityId && 
                    localChange.timestamp > serverChange.timestamp) {
                    conflicts.add(Conflict(localChange, serverChange))
                }
            }
        }
        
        return conflicts
    }
    
    private fun resolveConflicts(conflicts: List<Conflict>) {
        conflicts.forEach { conflict ->
            // Use last-write-wins strategy
            if (conflict.localChange.timestamp > conflict.serverChange.timestamp) {
                // Keep local change
                applyLocalChange(conflict.localChange)
            } else {
                // Use server change
                applyServerChange(conflict.serverChange)
            }
        }
    }
}
```

## 18.4 Caching Patterns for Mobile

Caching patterns optimize mobile app performance by storing frequently accessed data locally.

### When to Use:
- When you need to improve app performance
- When you want to reduce network usage
- When you need to provide instant access to data

### Real-World Analogy:
Think of a library that keeps popular books on a nearby shelf for quick access, while less popular books are stored in the main collection. This way, you can get the books you need most often without walking to the main collection.

### Basic Implementation:
```kotlin
// Mobile cache manager
class MobileCacheManager {
    private val memoryCache = LruCache<String, Any>(50) // 50 items
    private val diskCache = DiskLruCache.open(cacheDir, 1, 1, 10 * 1024 * 1024) // 10MB
    
    fun <T> get(key: String, type: Class<T>): T? {
        // Try memory cache first
        val memoryValue = memoryCache.get(key)
        if (memoryValue != null) {
            return type.cast(memoryValue)
        }
        
        // Try disk cache
        val diskValue = getFromDiskCache(key, type)
        if (diskValue != null) {
            // Put back in memory cache
            memoryCache.put(key, diskValue)
            return diskValue
        }
        
        return null
    }
    
    fun put(key: String, value: Any) {
        // Put in memory cache
        memoryCache.put(key, value)
        
        // Put in disk cache asynchronously
        Completable.fromAction {
            putToDiskCache(key, value)
        }.subscribeOn(Schedulers.io())
        .subscribe()
    }
    
    private fun <T> getFromDiskCache(key: String, type: Class<T>): T? {
        return try {
            val snapshot = diskCache.get(key)
            snapshot?.getInputStream(0)?.use { inputStream ->
                val objectInputStream = ObjectInputStream(inputStream)
                type.cast(objectInputStream.readObject())
            }
        } catch (e: Exception) {
            null
        }
    }
    
    private fun putToDiskCache(key: String, value: Any) {
        try {
            val editor = diskCache.edit(key)
            editor?.newOutputStream(0)?.use { outputStream ->
                val objectOutputStream = ObjectOutputStream(outputStream)
                objectOutputStream.writeObject(value)
            }
            editor?.commit()
        } catch (e: Exception) {
            // Handle error
        }
    }
}
```

## 18.5 Navigation Patterns

Navigation patterns provide structured approaches to handling navigation flow in mobile applications.

### When to Use:
- When you need to manage complex navigation flows
- When you want to handle deep linking
- When you need to maintain navigation state

### Real-World Analogy:
Think of a GPS navigation system that knows how to get you from point A to point B, can handle detours, and remembers where you've been so you can go back if needed.

### Basic Implementation:
```kotlin
// Navigation manager
class NavigationManager {
    private val navigationStack = mutableListOf<NavigationItem>()
    private val listeners = mutableListOf<NavigationListener>()
    
    fun navigateTo(destination: NavigationDestination, data: Any? = null) {
        val item = NavigationItem(destination, data)
        navigationStack.add(item)
        notifyListeners(NavigationEvent.NAVIGATE, item)
    }
    
    fun goBack(): Boolean {
        if (navigationStack.size > 1) {
            navigationStack.removeAt(navigationStack.size - 1)
            val currentItem = navigationStack.last()
            notifyListeners(NavigationEvent.BACK, currentItem)
            return true
        }
        return false
    }
    
    fun replaceCurrent(destination: NavigationDestination, data: Any? = null) {
        if (navigationStack.isNotEmpty()) {
            navigationStack[navigationStack.size - 1] = NavigationItem(destination, data)
            notifyListeners(NavigationEvent.REPLACE, navigationStack.last())
        }
    }
    
    fun clearStack() {
        navigationStack.clear()
        notifyListeners(NavigationEvent.CLEAR, null)
    }
    
    private fun notifyListeners(event: NavigationEvent, item: NavigationItem?) {
        listeners.forEach { listener ->
            listener.onNavigationEvent(event, item)
        }
    }
}

// Navigation destination
sealed class NavigationDestination {
    object Home : NavigationDestination()
    object Profile : NavigationDestination()
    data class UserDetail(val userId: String) : NavigationDestination()
    data class Settings(val section: String) : NavigationDestination()
}
```

## 18.6 State Management Patterns

State management patterns help manage application state in a predictable and maintainable way.

### When to Use:
- When you need to manage complex application state
- When you want to ensure state consistency
- When you need to handle state changes across components

### Real-World Analogy:
Think of a control room that monitors and manages all the systems in a building. It keeps track of the current state of everything and can make changes when needed, ensuring everything works together properly.

### Basic Implementation:
```kotlin
// State management with Redux-like pattern
data class AppState(
    val user: User? = null,
    val isLoading: Boolean = false,
    val error: String? = null,
    val navigation: NavigationState = NavigationState()
)

sealed class Action {
    object LoadUser : Action()
    data class UserLoaded(val user: User) : Action()
    data class UserLoadFailed(val error: String) : Action()
    object ClearError : Action()
}

class StateManager {
    private val _state = MutableLiveData<AppState>()
    val state: LiveData<AppState> = _state
    
    private val currentState: AppState
        get() = _state.value ?: AppState()
    
    fun dispatch(action: Action) {
        val newState = reduce(currentState, action)
        _state.value = newState
    }
    
    private fun reduce(currentState: AppState, action: Action): AppState {
        return when (action) {
            is Action.LoadUser -> currentState.copy(isLoading = true, error = null)
            is Action.UserLoaded -> currentState.copy(
                user = action.user,
                isLoading = false,
                error = null
            )
            is Action.UserLoadFailed -> currentState.copy(
                isLoading = false,
                error = action.error
            )
            is Action.ClearError -> currentState.copy(error = null)
        }
    }
}

// State-aware component
class UserProfileFragment : Fragment() {
    private lateinit var stateManager: StateManager
    
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        
        stateManager.state.observe(viewLifecycleOwner) { state ->
            when {
                state.isLoading -> showLoading()
                state.error != null -> showError(state.error)
                state.user != null -> showUser(state.user)
            }
        }
    }
}
```

## 18.7 Performance Patterns

Performance patterns optimize mobile app performance to provide smooth user experience.

### When to Use:
- When you need to improve app responsiveness
- When you want to reduce memory usage
- When you need to optimize battery consumption

### Real-World Analogy:
Think of a race car that's been tuned for maximum performance. Every component has been optimized - the engine, suspension, aerodynamics - to ensure the car performs at its best while using fuel efficiently.

### Basic Implementation:
```kotlin
// Performance monitoring
class PerformanceMonitor {
    private val metrics = mutableMapOf<String, Long>()
    
    fun startTiming(operation: String) {
        metrics[operation] = System.currentTimeMillis()
    }
    
    fun endTiming(operation: String): Long {
        val startTime = metrics[operation] ?: return 0
        val duration = System.currentTimeMillis() - startTime
        metrics.remove(operation)
        return duration
    }
    
    fun logPerformance(operation: String, duration: Long) {
        if (duration > 1000) { // Log slow operations
            Log.w("Performance", "Slow operation: $operation took ${duration}ms")
        }
    }
}

// Lazy loading for images
class ImageLoader {
    private val cache = LruCache<String, Bitmap>(100)
    private val executor = Executors.newFixedThreadPool(4)
    
    fun loadImage(url: String, imageView: ImageView) {
        // Check cache first
        val cachedBitmap = cache.get(url)
        if (cachedBitmap != null) {
            imageView.setImageBitmap(cachedBitmap)
            return
        }
        
        // Load asynchronously
        executor.submit {
            try {
                val bitmap = loadBitmapFromUrl(url)
                cache.put(url, bitmap)
                
                // Update UI on main thread
                imageView.post {
                    imageView.setImageBitmap(bitmap)
                }
            } catch (e: Exception) {
                Log.e("ImageLoader", "Failed to load image: $url", e)
            }
        }
    }
    
    private fun loadBitmapFromUrl(url: String): Bitmap {
        val connection = URL(url).openConnection()
        connection.connectTimeout = 5000
        connection.readTimeout = 10000
        
        return BitmapFactory.decodeStream(connection.getInputStream())
    }
}
```

## 18.8 Security Patterns for Mobile

Security patterns protect mobile applications from various security threats and vulnerabilities.

### When to Use:
- When you need to protect sensitive data
- When you want to prevent unauthorized access
- When you need to comply with security regulations

### Real-World Analogy:
Think of a high-security vault with multiple layers of protection - biometric locks, security cameras, motion sensors, and armed guards. Each layer provides additional security to protect valuable contents.

### Basic Implementation:
```kotlin
// Mobile security manager
class MobileSecurityManager {
    private val keyStore = KeyStore.getInstance("AndroidKeyStore")
    private val cipher = Cipher.getInstance("AES/GCM/NoPadding")
    
    init {
        keyStore.load(null)
    }
    
    fun encryptData(data: String): EncryptedData {
        val key = getOrCreateKey("app_key")
        cipher.init(Cipher.ENCRYPT_MODE, key)
        
        val encryptedBytes = cipher.doFinal(data.toByteArray())
        val iv = cipher.iv
        
        return EncryptedData(encryptedBytes, iv)
    }
    
    fun decryptData(encryptedData: EncryptedData): String {
        val key = keyStore.getKey("app_key", null)
        cipher.init(Cipher.DECRYPT_MODE, key, GCMParameterSpec(128, encryptedData.iv))
        
        val decryptedBytes = cipher.doFinal(encryptedData.data)
        return String(decryptedBytes)
    }
    
    private fun getOrCreateKey(alias: String): SecretKey {
        if (!keyStore.containsAlias(alias)) {
            val keyGenerator = KeyGenerator.getInstance(KeyProperties.KEY_ALGORITHM_AES, "AndroidKeyStore")
            val keyGenParameterSpec = KeyGenParameterSpec.Builder(
                alias,
                KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT
            )
                .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
                .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
                .setUserAuthenticationRequired(false)
                .setRandomizedEncryptionRequired(true)
                .build()
            
            keyGenerator.init(keyGenParameterSpec)
            keyGenerator.generateKey()
        }
        
        return keyStore.getKey(alias, null) as SecretKey
    }
}

// Biometric authentication
class BiometricAuthManager {
    private val biometricManager = BiometricManager.from(context)
    
    fun authenticate(callback: (Boolean) -> Unit) {
        val executor = ContextCompat.getMainExecutor(context)
        val biometricPrompt = BiometricPrompt(fragment, executor, object : BiometricPrompt.AuthenticationCallback() {
            override fun onAuthenticationSucceeded(result: BiometricPrompt.AuthenticationResult) {
                callback(true)
            }
            
            override fun onAuthenticationError(errorCode: Int, errString: CharSequence) {
                callback(false)
            }
        })
        
        val promptInfo = BiometricPrompt.PromptInfo.Builder()
            .setTitle("Biometric Authentication")
            .setSubtitle("Use your fingerprint or face to authenticate")
            .setNegativeButtonText("Cancel")
            .build()
        
        biometricPrompt.authenticate(promptInfo)
    }
}
```

## 18.9 Cross-Platform Patterns

Cross-platform patterns enable code sharing between different mobile platforms while maintaining native performance.

### When to Use:
- When you need to support multiple platforms
- When you want to reduce development time
- When you need to maintain code consistency

### Real-World Analogy:
Think of a universal remote control that can work with different brands of TVs. It provides a common interface while adapting to the specific requirements of each device.

### Basic Implementation:
```kotlin
// Cross-platform service interface
interface PlatformService {
    fun getDeviceInfo(): DeviceInfo
    fun showNotification(title: String, message: String)
    fun openUrl(url: String)
}

// Platform-specific implementations
class AndroidPlatformService : PlatformService {
    override fun getDeviceInfo(): DeviceInfo {
        return DeviceInfo(
            platform = "Android",
            version = Build.VERSION.RELEASE,
            model = Build.MODEL
        )
    }
    
    override fun showNotification(title: String, message: String) {
        val notificationManager = context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        // Create and show notification
    }
    
    override fun openUrl(url: String) {
        val intent = Intent(Intent.ACTION_VIEW, Uri.parse(url))
        context.startActivity(intent)
    }
}

// Cross-platform business logic
class CrossPlatformApp {
    private val platformService: PlatformService
    
    fun initialize() {
        val deviceInfo = platformService.getDeviceInfo()
        Log.i("App", "Running on ${deviceInfo.platform} ${deviceInfo.version}")
    }
    
    fun handleUserAction(action: UserAction) {
        when (action.type) {
            ActionType.SHOW_NOTIFICATION -> {
                platformService.showNotification(action.title, action.message)
            }
            ActionType.OPEN_URL -> {
                platformService.openUrl(action.url)
            }
        }
    }
}
```

## 18.10 Progressive Web App Patterns

Progressive Web App patterns enable web applications to provide native app-like experiences on mobile devices.

### When to Use:
- When you want to provide app-like experience through web
- When you need to work across different platforms
- When you want to leverage web technologies

### Real-World Analogy:
Think of a website that behaves like a native app - it can be installed on your phone, works offline, sends notifications, and provides a smooth user experience, but it's built using web technologies.

### Basic Implementation:
```javascript
// Service Worker for offline functionality
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open('app-cache-v1').then(cache => {
            return cache.addAll([
                '/',
                '/index.html',
                '/styles.css',
                '/app.js',
                '/manifest.json'
            ]);
        })
    );
});

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request).then(response => {
            return response || fetch(event.request);
        })
    );
});

// Web App Manifest
{
    "name": "My Progressive Web App",
    "short_name": "MyPWA",
    "description": "A progressive web app example",
    "start_url": "/",
    "display": "standalone",
    "background_color": "#ffffff",
    "theme_color": "#000000",
    "icons": [
        {
            "src": "/icon-192.png",
            "sizes": "192x192",
            "type": "image/png"
        },
        {
            "src": "/icon-512.png",
            "sizes": "512x512",
            "type": "image/png"
        }
    ]
}

// Push notification handling
self.addEventListener('push', event => {
    const options = {
        body: event.data.text(),
        icon: '/icon-192.png',
        badge: '/badge-72.png',
        vibrate: [100, 50, 100],
        data: {
            dateOfArrival: Date.now(),
            primaryKey: 1
        }
    };
    
    event.waitUntil(
        self.registration.showNotification('Push Notification', options)
    );
});
```

This comprehensive coverage of mobile patterns provides the foundation for building robust, performant mobile applications. Each pattern addresses specific mobile development challenges and offers different approaches to creating excellent mobile user experiences.