# Section 17 – Web Concurrency

## 17.1 HTTP Concurrency Models

HTTP concurrency models define how web servers handle multiple simultaneous requests efficiently. Understanding these models is crucial for building scalable web applications.

### Key Concepts
- **Request-Response Cycle**: Each HTTP request is processed independently
- **Connection Handling**: How servers manage multiple client connections
- **Resource Sharing**: Efficient sharing of server resources across requests
- **Load Distribution**: Spreading requests across multiple processing units

### Real-World Analogy
Think of a restaurant with multiple tables. The restaurant can serve many customers simultaneously by having multiple waiters, each handling different tables. The kitchen can prepare multiple orders in parallel, and the cashier can process payments while other customers are being served.

### Java Example
```java
// Simple HTTP server with thread pool
public class ConcurrentHttpServer {
    private final ExecutorService threadPool;
    private final ServerSocket serverSocket;
    
    public ConcurrentHttpServer(int port, int threadCount) throws IOException {
        this.serverSocket = new ServerSocket(port);
        this.threadPool = Executors.newFixedThreadPool(threadCount);
    }
    
    public void start() {
        while (true) {
            try {
                Socket clientSocket = serverSocket.accept();
                // Submit each request to thread pool
                threadPool.submit(new RequestHandler(clientSocket));
            } catch (IOException e) {
                System.err.println("Error accepting connection: " + e.getMessage());
            }
        }
    }
    
    private static class RequestHandler implements Runnable {
        private final Socket clientSocket;
        
        public RequestHandler(Socket clientSocket) {
            this.clientSocket = clientSocket;
        }
        
        @Override
        public void run() {
            try {
                // Process HTTP request
                BufferedReader in = new BufferedReader(
                    new InputStreamReader(clientSocket.getInputStream())
                );
                PrintWriter out = new PrintWriter(
                    clientSocket.getOutputStream(), true
                );
                
                String requestLine = in.readLine();
                System.out.println("Processing: " + requestLine);
                
                // Send response
                out.println("HTTP/1.1 200 OK");
                out.println("Content-Type: text/html");
                out.println();
                out.println("<h1>Hello from concurrent server!</h1>");
                
                clientSocket.close();
            } catch (IOException e) {
                System.err.println("Error handling request: " + e.getMessage());
            }
        }
    }
}
```

## 17.2 WebSocket Concurrency

WebSocket provides full-duplex communication between client and server, enabling real-time applications with persistent connections.

### Key Concepts
- **Persistent Connections**: Long-lived connections that stay open
- **Bidirectional Communication**: Both client and server can send messages
- **Event-Driven**: Messages trigger events asynchronously
- **Connection Management**: Handling multiple concurrent WebSocket connections

### Real-World Analogy
Think of a telephone conversation where both parties can talk and listen simultaneously. Unlike a walkie-talkie where only one person can speak at a time, a phone call allows natural conversation flow in both directions.

### Java Example
```java
// WebSocket server using Java WebSocket API
@ServerEndpoint("/websocket")
public class WebSocketServer {
    private static Set<Session> sessions = Collections.synchronizedSet(new HashSet<>());
    
    @OnOpen
    public void onOpen(Session session) {
        sessions.add(session);
        System.out.println("Client connected: " + session.getId());
        
        // Send welcome message
        try {
            session.getBasicRemote().sendText("Welcome to the chat!");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    
    @OnMessage
    public void onMessage(String message, Session session) {
        System.out.println("Message from " + session.getId() + ": " + message);
        
        // Broadcast message to all connected clients
        synchronized (sessions) {
            for (Session s : sessions) {
                if (s.isOpen()) {
                    try {
                        s.getBasicRemote().sendText(
                            "Client " + session.getId() + ": " + message
                        );
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }
            }
        }
    }
    
    @OnClose
    public void onClose(Session session) {
        sessions.remove(session);
        System.out.println("Client disconnected: " + session.getId());
    }
    
    @OnError
    public void onError(Session session, Throwable throwable) {
        System.err.println("WebSocket error: " + throwable.getMessage());
        sessions.remove(session);
    }
}
```

## 17.3 Server-Sent Events

Server-Sent Events (SSE) enable servers to push data to clients over a single HTTP connection, ideal for real-time updates.

### Key Concepts
- **Unidirectional**: Server pushes data to client
- **HTTP-based**: Uses standard HTTP protocol
- **Automatic Reconnection**: Built-in reconnection mechanism
- **Event Stream**: Continuous stream of events

### Real-World Analogy
Think of a news ticker that continuously scrolls information. The ticker (server) pushes new information to the display (client) without the display needing to ask for updates.

### Java Example
```java
// Server-Sent Events endpoint
@RestController
public class SSEController {
    private final Set<SseEmitter> emitters = Collections.synchronizedSet(new HashSet<>());
    
    @GetMapping(value = "/events", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public SseEmitter streamEvents() {
        SseEmitter emitter = new SseEmitter(Long.MAX_VALUE);
        emitters.add(emitter);
        
        emitter.onCompletion(() -> emitters.remove(emitter));
        emitter.onTimeout(() -> emitters.remove(emitter));
        emitter.onError((ex) -> emitters.remove(emitter));
        
        return emitter;
    }
    
    // Method to broadcast events to all clients
    public void broadcastEvent(String eventName, String data) {
        synchronized (emitters) {
            emitters.removeIf(emitter -> {
                try {
                    emitter.send(SseEmitter.event()
                        .name(eventName)
                        .data(data));
                    return false;
                } catch (Exception e) {
                    return true; // Remove failed emitters
                }
            });
        }
    }
    
    // Simulate periodic events
    @Scheduled(fixedRate = 5000)
    public void sendPeriodicUpdate() {
        String timestamp = LocalDateTime.now().toString();
        broadcastEvent("update", "Server time: " + timestamp);
    }
}
```

## 17.4 Web Workers

Web Workers enable JavaScript to run in background threads, preventing UI blocking during intensive computations.

### Key Concepts
- **Background Processing**: Run scripts in separate threads
- **Message Passing**: Communication between main thread and workers
- **No DOM Access**: Workers cannot access DOM directly
- **Shared Memory**: Optional shared memory for high-performance scenarios

### Real-World Analogy
Think of a construction site where the main contractor (main thread) coordinates work but delegates heavy tasks like concrete mixing (Web Worker) to specialized workers. The contractor can continue planning while workers handle intensive tasks.

### JavaScript Example
```javascript
// Main thread
const worker = new Worker('worker.js');

// Send data to worker
worker.postMessage({ numbers: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] });

// Listen for results
worker.onmessage = function(event) {
    console.log('Sum calculated:', event.data.result);
    console.log('Time taken:', event.data.time, 'ms');
};

// worker.js - Background worker
self.onmessage = function(event) {
    const numbers = event.data.numbers;
    const startTime = performance.now();
    
    // Intensive calculation
    let sum = 0;
    for (let i = 0; i < numbers.length; i++) {
        sum += numbers[i];
        // Simulate heavy computation
        for (let j = 0; j < 1000000; j++) {
            Math.random();
        }
    }
    
    const endTime = performance.now();
    
    // Send result back to main thread
    self.postMessage({
        result: sum,
        time: endTime - startTime
    });
};
```

## 17.5 Service Workers

Service Workers act as a proxy between web applications and the network, enabling offline functionality and background processing.

### Key Concepts
- **Network Interception**: Intercept and modify network requests
- **Offline Support**: Serve cached content when offline
- **Background Sync**: Perform tasks when connection is restored
- **Push Notifications**: Handle push messages even when app is closed

### Real-World Analogy
Think of a smart assistant that can work even when you're not around. It can handle incoming calls, take messages, and perform tasks in the background, then update you when you return.

### JavaScript Example
```javascript
// service-worker.js
const CACHE_NAME = 'my-app-cache-v1';
const urlsToCache = [
    '/',
    '/styles/main.css',
    '/scripts/main.js',
    '/images/logo.png'
];

// Install event - cache resources
self.addEventListener('install', function(event) {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(function(cache) {
                return cache.addAll(urlsToCache);
            })
    );
});

// Fetch event - serve from cache when offline
self.addEventListener('fetch', function(event) {
    event.respondWith(
        caches.match(event.request)
            .then(function(response) {
                // Return cached version or fetch from network
                return response || fetch(event.request);
            })
    );
});

// Background sync
self.addEventListener('sync', function(event) {
    if (event.tag === 'background-sync') {
        event.waitUntil(doBackgroundSync());
    }
});

function doBackgroundSync() {
    // Perform background tasks
    return fetch('/api/sync-data', {
        method: 'POST',
        body: JSON.stringify({ timestamp: Date.now() })
    });
}
```

## 17.6 Progressive Web Apps (PWA)

Progressive Web Apps combine the best of web and mobile apps, providing native-like experiences with web technologies.

### Key Concepts
- **Responsive Design**: Works on any device
- **App-like Experience**: Feels like a native app
- **Offline Capability**: Works without internet connection
- **Installable**: Can be installed on device home screen

### Real-World Analogy
Think of a hybrid vehicle that can run on both electricity and gasoline. A PWA is like a web application that can work like a traditional website but also function like a native mobile app when needed.

### JavaScript Example
```javascript
// PWA manifest and service worker integration
const manifest = {
    "name": "My Progressive Web App",
    "short_name": "MyPWA",
    "start_url": "/",
    "display": "standalone",
    "background_color": "#ffffff",
    "theme_color": "#000000",
    "icons": [
        {
            "src": "/icons/icon-192x192.png",
            "sizes": "192x192",
            "type": "image/png"
        },
        {
            "src": "/icons/icon-512x512.png",
            "sizes": "512x512",
            "type": "image/png"
        }
    ]
};

// Register service worker
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/sw.js')
            .then(function(registration) {
                console.log('SW registered: ', registration);
            })
            .catch(function(registrationError) {
                console.log('SW registration failed: ', registrationError);
            });
    });
}

// Install prompt
let deferredPrompt;
window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    
    // Show install button
    const installButton = document.getElementById('install-button');
    installButton.style.display = 'block';
    installButton.addEventListener('click', () => {
        deferredPrompt.prompt();
        deferredPrompt.userChoice.then((choiceResult) => {
            if (choiceResult.outcome === 'accepted') {
                console.log('User accepted the install prompt');
            }
            deferredPrompt = null;
        });
    });
});
```

## 17.7 Real-time Communication

Real-time communication enables instant data exchange between clients and servers, essential for chat applications, live updates, and collaborative tools.

### Key Concepts
- **Low Latency**: Minimal delay in message delivery
- **Bidirectional**: Both client and server can initiate communication
- **Scalability**: Handle thousands of concurrent connections
- **Reliability**: Ensure message delivery and ordering

### Real-World Analogy
Think of a walkie-talkie system used by emergency responders. When someone speaks, all other responders hear it immediately. The system is designed for instant, reliable communication in critical situations.

### Java Example
```java
// Real-time chat application using WebSocket
@Component
public class ChatService {
    private final Map<String, Set<WebSocketSession>> rooms = new ConcurrentHashMap<>();
    
    public void joinRoom(String roomId, WebSocketSession session) {
        rooms.computeIfAbsent(roomId, k -> ConcurrentHashMap.newKeySet())
              .add(session);
        
        // Notify others in room
        broadcastToRoom(roomId, "User joined the room", session);
    }
    
    public void leaveRoom(String roomId, WebSocketSession session) {
        Set<WebSocketSession> roomSessions = rooms.get(roomId);
        if (roomSessions != null) {
            roomSessions.remove(session);
            broadcastToRoom(roomId, "User left the room", session);
        }
    }
    
    public void sendMessage(String roomId, String message, WebSocketSession sender) {
        String senderName = getSenderName(sender);
        String formattedMessage = senderName + ": " + message;
        
        broadcastToRoom(roomId, formattedMessage, sender);
    }
    
    private void broadcastToRoom(String roomId, String message, WebSocketSession sender) {
        Set<WebSocketSession> roomSessions = rooms.get(roomId);
        if (roomSessions != null) {
            roomSessions.parallelStream()
                .filter(session -> session.isOpen() && !session.equals(sender))
                .forEach(session -> {
                    try {
                        session.sendMessage(new TextMessage(message));
                    } catch (IOException e) {
                        System.err.println("Error sending message: " + e.getMessage());
                    }
                });
        }
    }
    
    private String getSenderName(WebSocketSession session) {
        return (String) session.getAttributes().getOrDefault("username", "Anonymous");
    }
}
```

## 17.8 WebRTC Concurrency

WebRTC enables peer-to-peer communication directly between browsers, supporting video, audio, and data channels with minimal latency.

### Key Concepts
- **Peer-to-Peer**: Direct communication between browsers
- **Media Streams**: Real-time audio and video transmission
- **Data Channels**: Reliable and unreliable data transmission
- **NAT Traversal**: Handle network address translation

### Real-World Analogy
Think of a direct phone call between two people without going through a central switchboard. WebRTC is like having a direct line that allows immediate, high-quality communication between two parties.

### JavaScript Example
```javascript
// WebRTC peer-to-peer video chat
class VideoChat {
    constructor() {
        this.localStream = null;
        this.peerConnection = null;
        this.localVideo = document.getElementById('localVideo');
        this.remoteVideo = document.getElementById('remoteVideo');
    }
    
    async startCall() {
        try {
            // Get user media
            this.localStream = await navigator.mediaDevices.getUserMedia({
                video: true,
                audio: true
            });
            
            this.localVideo.srcObject = this.localStream;
            
            // Create peer connection
            this.peerConnection = new RTCPeerConnection({
                iceServers: [{ urls: 'stun:stun.l.google.com:19302' }]
            });
            
            // Add local stream to peer connection
            this.localStream.getTracks().forEach(track => {
                this.peerConnection.addTrack(track, this.localStream);
            });
            
            // Handle remote stream
            this.peerConnection.ontrack = (event) => {
                this.remoteVideo.srcObject = event.streams[0];
            };
            
            // Handle ICE candidates
            this.peerConnection.onicecandidate = (event) => {
                if (event.candidate) {
                    // Send candidate to remote peer
                    this.sendCandidate(event.candidate);
                }
            };
            
        } catch (error) {
            console.error('Error starting call:', error);
        }
    }
    
    async createOffer() {
        const offer = await this.peerConnection.createOffer();
        await this.peerConnection.setLocalDescription(offer);
        
        // Send offer to remote peer
        this.sendOffer(offer);
    }
    
    async handleOffer(offer) {
        await this.peerConnection.setRemoteDescription(offer);
        const answer = await this.peerConnection.createAnswer();
        await this.peerConnection.setLocalDescription(answer);
        
        // Send answer to remote peer
        this.sendAnswer(answer);
    }
    
    async handleAnswer(answer) {
        await this.peerConnection.setRemoteDescription(answer);
    }
    
    async handleCandidate(candidate) {
        await this.peerConnection.addIceCandidate(candidate);
    }
    
    // These methods would typically use WebSocket or other signaling
    sendOffer(offer) { /* Implementation */ }
    sendAnswer(answer) { /* Implementation */ }
    sendCandidate(candidate) { /* Implementation */ }
}
```

This comprehensive explanation covers all aspects of web concurrency, providing both theoretical understanding and practical examples to illustrate each concept.