# Section 16 – Number Theory & Mathematical Algorithms

## 16.1 Prime Number Algorithms

Prime numbers are fundamental in number theory and have applications in cryptography, hashing, and many other areas of computer science.

### Basic Prime Checking

```java
public class PrimeNumbers {
    // Check if a number is prime - O(√n)
    public static boolean isPrime(int n) {
        if (n <= 1) return false;
        if (n <= 3) return true;
        if (n % 2 == 0 || n % 3 == 0) return false;
        
        // Check divisors up to √n
        for (int i = 5; i * i <= n; i += 6) {
            if (n % i == 0 || n % (i + 2) == 0) {
                return false;
            }
        }
        
        return true;
    }
    
    // Check if a number is prime - optimized version
    public static boolean isPrimeOptimized(long n) {
        if (n <= 1) return false;
        if (n <= 3) return true;
        if (n % 2 == 0 || n % 3 == 0) return false;
        
        // Only check divisors of form 6k ± 1
        for (long i = 5; i * i <= n; i += 6) {
            if (n % i == 0 || n % (i + 2) == 0) {
                return false;
            }
        }
        
        return true;
    }
    
    // Find all prime numbers up to n using Sieve of Eratosthenes
    public static List<Integer> sieveOfEratosthenes(int n) {
        boolean[] isPrime = new boolean[n + 1];
        Arrays.fill(isPrime, true);
        isPrime[0] = isPrime[1] = false;
        
        for (int i = 2; i * i <= n; i++) {
            if (isPrime[i]) {
                // Mark all multiples of i as composite
                for (int j = i * i; j <= n; j += i) {
                    isPrime[j] = false;
                }
            }
        }
        
        List<Integer> primes = new ArrayList<>();
        for (int i = 2; i <= n; i++) {
            if (isPrime[i]) {
                primes.add(i);
            }
        }
        
        return primes;
    }
    
    // Time Complexity: O(n log log n)
    // Space Complexity: O(n)
}
```

### Segmented Sieve

```java
public class SegmentedSieve {
    // Find primes in range [low, high]
    public static List<Long> segmentedSieve(long low, long high) {
        int limit = (int) Math.sqrt(high) + 1;
        List<Integer> basePrimes = PrimeNumbers.sieveOfEratosthenes(limit);
        
        boolean[] isPrime = new boolean[(int) (high - low + 1)];
        Arrays.fill(isPrime, true);
        
        for (int prime : basePrimes) {
            long start = Math.max((long) prime * prime, (low + prime - 1) / prime * prime);
            
            for (long j = start; j <= high; j += prime) {
                isPrime[(int) (j - low)] = false;
            }
        }
        
        List<Long> primes = new ArrayList<>();
        for (long i = low; i <= high; i++) {
            if (isPrime[(int) (i - low)]) {
                primes.add(i);
            }
        }
        
        return primes;
    }
}
```

## 16.2 Greatest Common Divisor (GCD)

The GCD of two numbers is the largest number that divides both of them.

### Euclidean Algorithm

```java
public class GCD {
    // Recursive Euclidean algorithm
    public static int gcd(int a, int b) {
        if (b == 0) return a;
        return gcd(b, a % b);
    }
    
    // Iterative Euclidean algorithm
    public static int gcdIterative(int a, int b) {
        while (b != 0) {
            int temp = b;
            b = a % b;
            a = temp;
        }
        return a;
    }
    
    // Extended Euclidean algorithm - finds x, y such that ax + by = gcd(a, b)
    public static int[] extendedGcd(int a, int b) {
        if (b == 0) {
            return new int[]{a, 1, 0};
        }
        
        int[] result = extendedGcd(b, a % b);
        int gcd = result[0];
        int x = result[2];
        int y = result[1] - (a / b) * result[2];
        
        return new int[]{gcd, x, y};
    }
    
    // Least Common Multiple
    public static int lcm(int a, int b) {
        return Math.abs(a * b) / gcd(a, b);
    }
    
    // Time Complexity: O(log min(a, b))
    // Space Complexity: O(log min(a, b)) for recursive, O(1) for iterative
}
```

### Binary GCD Algorithm

```java
public class BinaryGCD {
    public static int binaryGcd(int a, int b) {
        if (a == 0) return b;
        if (b == 0) return a;
        
        // Find common factors of 2
        int shift = 0;
        while (((a | b) & 1) == 0) {
            a >>= 1;
            b >>= 1;
            shift++;
        }
        
        // Remove remaining factors of 2 from a
        while ((a & 1) == 0) {
            a >>= 1;
        }
        
        // Now a is odd
        do {
            // Remove remaining factors of 2 from b
            while ((b & 1) == 0) {
                b >>= 1;
            }
            
            // Now both a and b are odd
            if (a > b) {
                int temp = a;
                a = b;
                b = temp;
            }
            
            b = b - a;
        } while (b != 0);
        
        // Restore common factors of 2
        return a << shift;
    }
}
```

## 16.3 Modular Arithmetic

Modular arithmetic is essential for cryptography and many other applications.

### Basic Modular Operations

```java
public class ModularArithmetic {
    // Modular addition
    public static int modAdd(int a, int b, int mod) {
        return ((a % mod) + (b % mod)) % mod;
    }
    
    // Modular subtraction
    public static int modSubtract(int a, int b, int mod) {
        return ((a % mod) - (b % mod) + mod) % mod;
    }
    
    // Modular multiplication
    public static int modMultiply(int a, int b, int mod) {
        return ((a % mod) * (b % mod)) % mod;
    }
    
    // Modular exponentiation - O(log n)
    public static int modPow(int base, int exponent, int mod) {
        if (mod == 1) return 0;
        
        int result = 1;
        base = base % mod;
        
        while (exponent > 0) {
            if (exponent % 2 == 1) {
                result = (result * base) % mod;
            }
            exponent = exponent >> 1;
            base = (base * base) % mod;
        }
        
        return result;
    }
    
    // Modular inverse using extended Euclidean algorithm
    public static int modInverse(int a, int mod) {
        int[] gcdResult = GCD.extendedGcd(a, mod);
        int gcd = gcdResult[0];
        int x = gcdResult[1];
        
        if (gcd != 1) {
            throw new IllegalArgumentException("Modular inverse doesn't exist");
        }
        
        return (x % mod + mod) % mod;
    }
    
    // Chinese Remainder Theorem
    public static int chineseRemainder(int[] remainders, int[] moduli) {
        int n = remainders.length;
        int product = 1;
        
        for (int mod : moduli) {
            product *= mod;
        }
        
        int result = 0;
        
        for (int i = 0; i < n; i++) {
            int partialProduct = product / moduli[i];
            int inverse = modInverse(partialProduct, moduli[i]);
            result += remainders[i] * partialProduct * inverse;
        }
        
        return result % product;
    }
}
```

### Fermat's Little Theorem

```java
public class FermatsLittleTheorem {
    // If p is prime and a is not divisible by p, then a^(p-1) ≡ 1 (mod p)
    public static boolean fermatTest(int a, int p) {
        if (p <= 1) return false;
        if (p == 2) return true;
        if (a % p == 0) return false;
        
        return ModularArithmetic.modPow(a, p - 1, p) == 1;
    }
    
    // Fermat primality test (probabilistic)
    public static boolean isPrimeFermat(int n, int k) {
        if (n <= 1 || n == 4) return false;
        if (n <= 3) return true;
        
        Random random = new Random();
        
        for (int i = 0; i < k; i++) {
            int a = 2 + random.nextInt(n - 4);
            if (!fermatTest(a, n)) {
                return false;
            }
        }
        
        return true;
    }
}
```

## 16.4 Fast Exponentiation

Efficiently computing large powers modulo a number.

### Binary Exponentiation

```java
public class FastExponentiation {
    // Iterative binary exponentiation
    public static long modPow(long base, long exponent, long mod) {
        if (mod == 1) return 0;
        
        long result = 1;
        base = base % mod;
        
        while (exponent > 0) {
            if (exponent % 2 == 1) {
                result = (result * base) % mod;
            }
            exponent = exponent >> 1;
            base = (base * base) % mod;
        }
        
        return result;
    }
    
    // Recursive binary exponentiation
    public static long modPowRecursive(long base, long exponent, long mod) {
        if (exponent == 0) return 1;
        if (exponent == 1) return base % mod;
        
        long half = modPowRecursive(base, exponent / 2, mod);
        long result = (half * half) % mod;
        
        if (exponent % 2 == 1) {
            result = (result * base) % mod;
        }
        
        return result;
    }
    
    // Matrix exponentiation
    public static long[][] matrixPow(long[][] matrix, long exponent, long mod) {
        int n = matrix.length;
        long[][] result = new long[n][n];
        
        // Initialize result as identity matrix
        for (int i = 0; i < n; i++) {
            result[i][i] = 1;
        }
        
        while (exponent > 0) {
            if (exponent % 2 == 1) {
                result = matrixMultiply(result, matrix, mod);
            }
            matrix = matrixMultiply(matrix, matrix, mod);
            exponent = exponent >> 1;
        }
        
        return result;
    }
    
    private static long[][] matrixMultiply(long[][] a, long[][] b, long mod) {
        int n = a.length;
        long[][] result = new long[n][n];
        
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                for (int k = 0; k < n; k++) {
                    result[i][j] = (result[i][j] + (a[i][k] * b[k][j]) % mod) % mod;
                }
            }
        }
        
        return result;
    }
    
    // Time Complexity: O(log n)
    // Space Complexity: O(1) for iterative, O(log n) for recursive
}
```

## 16.5 Chinese Remainder Theorem

Solving systems of modular equations.

```java
public class ChineseRemainderTheorem {
    public static class Congruence {
        int remainder, modulus;
        
        public Congruence(int remainder, int modulus) {
            this.remainder = remainder;
            this.modulus = modulus;
        }
    }
    
    // Solve system of congruences
    public static int solveSystem(List<Congruence> congruences) {
        int n = congruences.size();
        int product = 1;
        
        for (Congruence c : congruences) {
            product *= c.modulus;
        }
        
        int result = 0;
        
        for (Congruence c : congruences) {
            int partialProduct = product / c.modulus;
            int inverse = ModularArithmetic.modInverse(partialProduct, c.modulus);
            result += c.remainder * partialProduct * inverse;
        }
        
        return result % product;
    }
    
    // Check if system has a solution
    public static boolean hasSolution(List<Congruence> congruences) {
        for (int i = 0; i < congruences.size(); i++) {
            for (int j = i + 1; j < congruences.size(); j++) {
                Congruence c1 = congruences.get(i);
                Congruence c2 = congruences.get(j);
                
                int gcd = GCD.gcd(c1.modulus, c2.modulus);
                if ((c1.remainder - c2.remainder) % gcd != 0) {
                    return false;
                }
            }
        }
        return true;
    }
}
```

## 16.6 Miller-Rabin Primality Test

A probabilistic primality test that's more reliable than Fermat's test.

```java
public class MillerRabinTest {
    // Miller-Rabin primality test
    public static boolean isPrime(long n, int k) {
        if (n <= 1 || n == 4) return false;
        if (n <= 3) return true;
        if (n % 2 == 0) return false;
        
        // Write n-1 as d * 2^r
        long d = n - 1;
        int r = 0;
        while (d % 2 == 0) {
            d /= 2;
            r++;
        }
        
        Random random = new Random();
        
        // Witness loop
        for (int i = 0; i < k; i++) {
            long a = 2 + random.nextLong() % (n - 4);
            long x = FastExponentiation.modPow(a, d, n);
            
            if (x == 1 || x == n - 1) continue;
            
            boolean composite = true;
            for (int j = 0; j < r - 1; j++) {
                x = (x * x) % n;
                if (x == n - 1) {
                    composite = false;
                    break;
                }
            }
            
            if (composite) return false;
        }
        
        return true;
    }
    
    // Deterministic version for small numbers
    public static boolean isPrimeDeterministic(long n) {
        if (n <= 1) return false;
        if (n <= 3) return true;
        if (n % 2 == 0) return false;
        
        int[] bases = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37};
        
        for (int a : bases) {
            if (a >= n) break;
            if (!millerRabinWitness(n, a)) {
                return false;
            }
        }
        
        return true;
    }
    
    private static boolean millerRabinWitness(long n, long a) {
        long d = n - 1;
        int r = 0;
        
        while (d % 2 == 0) {
            d /= 2;
            r++;
        }
        
        long x = FastExponentiation.modPow(a, d, n);
        
        if (x == 1 || x == n - 1) return true;
        
        for (int i = 0; i < r - 1; i++) {
            x = (x * x) % n;
            if (x == n - 1) return true;
        }
        
        return false;
    }
}
```

## 16.7 Pollard's Rho Algorithm

A factorization algorithm for finding non-trivial factors of composite numbers.

```java
public class PollardRho {
    // Pollard's rho algorithm for factorization
    public static long pollardRho(long n) {
        if (n % 2 == 0) return 2;
        
        Random random = new Random();
        long x = 2 + random.nextLong() % (n - 2);
        long y = x;
        long c = 1 + random.nextLong() % (n - 1);
        long d = 1;
        
        while (d == 1) {
            x = (FastExponentiation.modPow(x, 2, n) + c) % n;
            y = (FastExponentiation.modPow(y, 2, n) + c) % n;
            y = (FastExponentiation.modPow(y, 2, n) + c) % n;
            
            d = GCD.gcd(Math.abs(x - y), n);
        }
        
        return d;
    }
    
    // Complete factorization using Pollard's rho
    public static List<Long> factorize(long n) {
        List<Long> factors = new ArrayList<>();
        factorizeRecursive(n, factors);
        return factors;
    }
    
    private static void factorizeRecursive(long n, List<Long> factors) {
        if (n == 1) return;
        
        if (MillerRabinTest.isPrime(n, 10)) {
            factors.add(n);
            return;
        }
        
        long factor = pollardRho(n);
        factorizeRecursive(factor, factors);
        factorizeRecursive(n / factor, factors);
    }
    
    // Brent's variant of Pollard's rho
    public static long brentRho(long n) {
        if (n % 2 == 0) return 2;
        
        Random random = new Random();
        long y = 2 + random.nextLong() % (n - 2);
        long c = 1 + random.nextLong() % (n - 1);
        long m = 1 + random.nextLong() % (n - 1);
        
        long g = 1, r = 1, q = 1;
        
        while (g == 1) {
            long x = y;
            
            for (int i = 0; i < r; i++) {
                y = (FastExponentiation.modPow(y, 2, n) + c) % n;
            }
            
            int k = 0;
            while (k < r && g == 1) {
                long ys = y;
                
                for (int i = 0; i < Math.min(m, r - k); i++) {
                    y = (FastExponentiation.modPow(y, 2, n) + c) % n;
                    q = (q * Math.abs(x - y)) % n;
                }
                
                g = GCD.gcd(q, n);
                k += m;
            }
            
            r *= 2;
        }
        
        if (g == n) {
            do {
                ys = (FastExponentiation.modPow(ys, 2, n) + c) % n;
                g = GCD.gcd(Math.abs(x - ys), n);
            } while (g == 1);
        }
        
        return g;
    }
}
```

## 16.8 Cryptographic Algorithms

### RSA Algorithm

```java
public class RSA {
    private long n, e, d;
    
    public RSA(long p, long q) {
        if (!MillerRabinTest.isPrime(p, 10) || !MillerRabinTest.isPrime(q, 10)) {
            throw new IllegalArgumentException("p and q must be prime");
        }
        
        n = p * q;
        long phi = (p - 1) * (q - 1);
        
        // Choose e such that gcd(e, phi) = 1
        e = 65537; // Common choice
        while (GCD.gcd(e, phi) != 1) {
            e++;
        }
        
        // Calculate d such that ed ≡ 1 (mod phi)
        d = ModularArithmetic.modInverse((int) e, (int) phi);
    }
    
    public long encrypt(long message) {
        return FastExponentiation.modPow(message, e, n);
    }
    
    public long decrypt(long ciphertext) {
        return FastExponentiation.modPow(ciphertext, d, n);
    }
    
    public long getPublicKey() {
        return e;
    }
    
    public long getModulus() {
        return n;
    }
}
```

### Diffie-Hellman Key Exchange

```java
public class DiffieHellman {
    private long privateKey;
    private long publicKey;
    private long sharedSecret;
    
    public DiffieHellman(long privateKey, long prime, long generator) {
        this.privateKey = privateKey;
        this.publicKey = FastExponentiation.modPow(generator, privateKey, prime);
    }
    
    public long generateSharedSecret(long otherPublicKey, long prime) {
        this.sharedSecret = FastExponentiation.modPow(otherPublicKey, privateKey, prime);
        return sharedSecret;
    }
    
    public long getPublicKey() {
        return publicKey;
    }
    
    public long getSharedSecret() {
        return sharedSecret;
    }
}
```

### Elliptic Curve Cryptography (Simplified)

```java
public class EllipticCurve {
    private long a, b, p; // Curve parameters: y^2 = x^3 + ax + b (mod p)
    
    public EllipticCurve(long a, long b, long p) {
        this.a = a;
        this.b = b;
        this.p = p;
    }
    
    public static class Point {
        long x, y;
        boolean isInfinity;
        
        public Point(long x, long y) {
            this.x = x;
            this.y = y;
            this.isInfinity = false;
        }
        
        public Point() {
            this.isInfinity = true;
        }
    }
    
    public Point pointAddition(Point p1, Point p2) {
        if (p1.isInfinity) return p2;
        if (p2.isInfinity) return p1;
        
        if (p1.x == p2.x && p1.y == p2.y) {
            return pointDoubling(p1);
        }
        
        long slope = ((p2.y - p1.y) * ModularArithmetic.modInverse((int) (p2.x - p1.x), (int) p)) % p;
        if (slope < 0) slope += p;
        
        long x3 = (slope * slope - p1.x - p2.x) % p;
        if (x3 < 0) x3 += p;
        
        long y3 = (slope * (p1.x - x3) - p1.y) % p;
        if (y3 < 0) y3 += p;
        
        return new Point(x3, y3);
    }
    
    public Point pointDoubling(Point p) {
        if (p.isInfinity) return p;
        
        long slope = ((3 * p.x * p.x + a) * ModularArithmetic.modInverse((int) (2 * p.y), (int) this.p)) % p;
        if (slope < 0) slope += p;
        
        long x3 = (slope * slope - 2 * p.x) % p;
        if (x3 < 0) x3 += p;
        
        long y3 = (slope * (p.x - x3) - p.y) % p;
        if (y3 < 0) y3 += p;
        
        return new Point(x3, y3);
    }
    
    public Point scalarMultiply(Point p, long k) {
        Point result = new Point(); // Infinity point
        Point addend = p;
        
        while (k > 0) {
            if (k % 2 == 1) {
                result = pointAddition(result, addend);
            }
            addend = pointDoubling(addend);
            k = k >> 1;
        }
        
        return result;
    }
}
```

**Real-world Analogies:**
- **Prime Numbers:** Like the building blocks of all numbers - you can't break them down further
- **GCD:** Like finding the largest measuring stick that can evenly measure two lengths
- **Modular Arithmetic:** Like a clock that resets every 12 hours - 13 o'clock becomes 1 o'clock
- **Fast Exponentiation:** Like efficiently calculating compound interest over many years
- **Chinese Remainder Theorem:** Like solving a puzzle where you know the remainder when dividing by different numbers
- **Miller-Rabin Test:** Like a smart detective that can quickly determine if a number is prime with high confidence
- **Pollard's Rho:** Like finding the common factors between two numbers by following a trail
- **RSA Encryption:** Like having a public mailbox where anyone can drop messages, but only you have the key to open it
- **Diffie-Hellman:** Like two people agreeing on a secret color by mixing their own colors in public
- **Elliptic Curves:** Like drawing curves on a grid and using their properties for secure communication

Number theory and mathematical algorithms form the foundation of modern cryptography and are essential for secure communication, digital signatures, and many other applications in computer science.