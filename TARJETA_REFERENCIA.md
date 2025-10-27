# 🔐 Análisis Criptográfico Completo - Proyecto ECDSA

**Documento técnico sobre algoritmos, bibliotecas y servicios de seguridad**

---

## 📚 ALGORITMOS CRIPTOGRÁFICOS UTILIZADOS

### 1. ECDSA (Elliptic Curve Digital Signature Algorithm)

**Tipo:** Algoritmo de firma digital asimétrico  
**Estándar:** FIPS 186-4, ANSI X9.62, SEC 1  
**Familia:** Criptografía de curvas elípticas (ECC)

**Implementación en el proyecto:**
```python
# Archivo: src/ecdsa_core.py
class ECDSA:
    def firmar(self, mensaje, llave_privada):
        # 1. Hash del mensaje
        z = hash_mensaje(mensaje) mod q
        # 2. Generar k aleatorio
        k = secrets.randbelow(q-1) + 1
        # 3. R = k·G
        R = multiplicar_escalar(k, G)
        # 4. r = R.x mod q
        r = R.x mod q
        # 5. s = k⁻¹(z + r·d) mod q
        s = inverso_modular(k) * (z + r*d) mod q
        return (r, s)
```

**Seguridad basada en:**
- Problema del logaritmo discreto en curvas elípticas (ECDLP)
- Inviable computacionalmente encontrar `d` dado `Q = d·G`

---

### 2. SHA-256 (Secure Hash Algorithm 256-bit)

**Tipo:** Función hash criptográfica  
**Estándar:** FIPS 180-4  
**Familia:** SHA-2 (diseñada por NSA)

**Implementación:**
```python
import hashlib

def hash_mensaje(self, mensaje: str) -> int:
    # Calcular SHA-256
    hash_bytes = hashlib.sha256(mensaje.encode('utf-8')).digest()
    # Convertir a entero
    hash_int = int.from_bytes(hash_bytes, byteorder='big')
    # Reducir módulo q
    return hash_int % self.curva.q
```

**Propiedades:**
- **Entrada:** Cualquier tamaño
- **Salida:** 256 bits (32 bytes)
- **Resistencia a colisiones:** ~2^128 operaciones
- **Resistencia a preimagen:** ~2^256 operaciones
- **Uso en ECDSA:** Convertir mensaje arbitrario a número en [0, q-1]

---

### 3. Aritmética Modular sobre Curvas Elípticas

**Algoritmos implementados:**

#### a) Suma de Puntos
```python
def sumar_puntos(P, Q):
    if P.es_infinito: return Q
    if Q.es_infinito: return P
    
    if P.x == Q.x:
        if P.y == Q.y:
            # Duplicación: P = Q
            m = (3*P.x² + a) * inverso(2*P.y) mod p
        else:
            # P + (-P) = ∞
            return PuntoInfinito
    else:
        # Suma general
        m = (Q.y - P.y) * inverso(Q.x - P.x) mod p
    
    x = m² - P.x - Q.x mod p
    y = m(P.x - x) - P.y mod p
    return Punto(x, y)
```

#### b) Multiplicación Escalar (Double-and-Add)
```python
def multiplicar_escalar(k, P):
    """Calcula k·P eficientemente"""
    resultado = PuntoInfinito
    temporal = P
    
    while k > 0:
        if k & 1:  # Si bit es 1
            resultado = sumar_puntos(resultado, temporal)
        temporal = sumar_puntos(temporal, temporal)  # Duplicar
        k >>= 1
    
    return resultado
```

**Complejidad:** O(log k) operaciones

#### c) Inverso Modular (Algoritmo Extendido de Euclides)
```python
def inverso_modular(a, m):
    """Encuentra x tal que a·x ≡ 1 (mod m)"""
    def euclides_extendido(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = euclides_extendido(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
    gcd, x, _ = euclides_extendido(a % m, m)
    if gcd != 1:
        raise ValueError(f"{a} no tiene inverso módulo {m}")
    return (x % m + m) % m
```

**Complejidad:** O(log min(a, m))

---

## 🔧 BIBLIOTECAS CRIPTOGRÁFICAS

### 1. `hashlib` - Hashing Criptográfico

**Origen:** Biblioteca estándar de Python  
**Backend:** OpenSSL (en la mayoría de sistemas)

**Funciones usadas:**
```python
import hashlib

# SHA-256
hashlib.sha256(datos).digest()      # Retorna bytes
hashlib.sha256(datos).hexdigest()   # Retorna hex string
```

**Algoritmos disponibles en hashlib:**
- SHA-1 (obsoleto, no usado)
- SHA-256 ✅ (usado en nuestro proyecto)
- SHA-384, SHA-512
- MD5 (obsoleto, no usado)
- BLAKE2b, BLAKE2s

**Por qué SHA-256:**
- ✅ Estándar industrial actual
- ✅ Balance perfecto seguridad/velocidad
- ✅ Usado en Bitcoin, TLS, certificados
- ✅ No ha sido roto (a 2025)

---

### 2. `secrets` - Generación Aleatoria Segura (CSPRNG)

**Origen:** Biblioteca estándar Python 3.6+  
**Tipo:** Cryptographically Secure Pseudo-Random Number Generator

**Funciones usadas:**
```python
import secrets

# Generar número aleatorio en [0, n)
secrets.randbelow(n)

# Generar bytes aleatorios
secrets.token_bytes(32)

# Generar token hexadecimal
secrets.token_hex(16)
```

**Fuentes de entropía por OS:**
- **Windows:** `CryptGenRandom()` (BCrypt API)
- **Linux:** `/dev/urandom` (getrandom syscall)
- **macOS:** `/dev/urandom`

**Vs random (NO seguro):**
```python
# ❌ NUNCA usar para criptografía
import random
random.randint(1, 100)  # Predecible con Mersenne Twister

# ✅ SIEMPRE usar para criptografía
import secrets
secrets.randbelow(100)  # Impredecible, criptográficamente seguro
```

---

### 3. `base64` - Codificación

**Origen:** Biblioteca estándar de Python  
**Estándar:** RFC 4648

**Funciones usadas:**
```python
import base64

# Codificar
base64.b64encode(bytes_data)  # bytes → base64 string

# Decodificar
base64.b64decode(base64_string)  # base64 → bytes originales
```

**Características:**
- Alfabeto: A-Z, a-z, 0-9, +, /
- Padding: `=` para alineación a múltiplos de 4
- Expansión: 33% (4 caracteres por cada 3 bytes)

**Uso en el proyecto:**
- Codificar parámetros de llaves en ASCII seguro
- Formato profesional compatible con PEM
- Evitar problemas de encoding en archivos de texto

---

### 4. `math` - Operaciones Matemáticas

**Origen:** Biblioteca estándar de Python

**Funciones usadas:**
```python
import math

# Máximo común divisor (algoritmo de Euclides)
math.gcd(a, b)

# Usado para verificar si 'a' tiene inverso mod m
if math.gcd(a, m) == 1:
    # Tiene inverso
```

**Algoritmo GCD:**
```python
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a
```

---

## 🛡️ SERVICIOS DE SEGURIDAD PROPORCIONADOS

### 1. ✅ AUTENTICACIÓN

**Definición:** Verificar que el mensaje proviene de quien dice ser

**Mecanismo:**
- Firma solo puede generarse con llave privada única
- Llave pública identifica al firmante
- Verificación confirma la identidad

**Implementación:**
```python
# Alicia firma
firma = ecdsa.firmar(mensaje, llave_privada_alicia)

# Betito verifica con llave pública de Alicia
if ecdsa.verificar(mensaje, firma, llave_publica_alicia):
    print("Mensaje auténtico de Alicia")
```

**Garantía matemática:**
- Problema ECDLP computacionalmente intratable
- Solo Alicia puede generar firmas válidas con su llave privada

---

### 2. ✅ INTEGRIDAD

**Definición:** Detectar cualquier modificación del mensaje

**Mecanismo:**
- SHA-256 produce hash único del mensaje
- Hash se incluye en el cálculo de la firma
- Cualquier cambio invalida la firma

**Implementación:**
```python
# Firma incluye hash
z = SHA-256(mensaje) mod q
s = k⁻¹(z + r·d) mod q

# Verificación recalcula hash
z' = SHA-256(mensaje_recibido) mod q
# Si mensaje cambió → z' ≠ z → verificación falla
```

**Ejemplo:**
```python
mensaje_original = "Transferir $100"
firma = firmar(mensaje_original, d)

# Atacante modifica
mensaje_alterado = "Transferir $1000"

# Verificación detecta modificación
verificar(mensaje_alterado, firma, Q)  # → False ❌
```

**Propiedades de SHA-256 garantizan:**
- Cambiar 1 bit → hash completamente diferente
- Imposible encontrar colisión (mismo hash)

---

### 3. ✅ NO REPUDIO (Non-Repudiation)

**Definición:** El firmante no puede negar haber firmado

**Mecanismo:**
- Solo el poseedor de la llave privada puede firmar
- Firma es prueba criptográfica de autoría
- Terceros pueden verificar con llave pública

**Implementación:**
```python
# Alicia firma contrato
contrato = "Acepto pagar $500"
firma_alicia = firmar(contrato, llave_privada_alicia)

# Más tarde Alicia intenta negar
# Pero cualquiera puede verificar:
if verificar(contrato, firma_alicia, llave_publica_alicia):
    print("Alicia SÍ firmó - No puede negar")
```

**Valor legal:**
- Firmas digitales ECDSA tienen validez legal en muchos países
- Equivalente a firma manuscrita
- Prueba no falsificable

**Requisito crítico:**
- Llave privada debe mantenerse secreta
- Si se expone, pierde valor de no repudio

---

### 4. ✅ DETECCIÓN DE FALSIFICACIONES

**Definición:** Identificar intentos de suplantación de identidad

**Mecanismo:**
- Imposible generar firma válida sin llave privada
- ECDLP es computacionalmente intratable

**Implementación:**
```python
# Candy intenta suplantar a Alicia
mensaje = "Transferir fondos"

# Candy firma con SU llave privada
firma_candy = firmar(mensaje, llave_privada_candy)

# Betito verifica con llave pública de ALICIA
resultado = verificar(mensaje, firma_candy, llave_publica_alicia)
# → False ❌ (detecta suplantación)
```

**Protecciones:**
- Cada llave privada genera firmas únicas
- Matemáticamente imposible imitar sin la llave
- Sistema detecta automáticamente intentos de fraude

---

### 5. ❌ NO PROPORCIONA: CONFIDENCIALIDAD

**Definición:** Mantener el contenido del mensaje secreto

**Por qué ECDSA NO cifra:**
- ECDSA es un esquema de FIRMA, no de CIFRADO
- El mensaje permanece en texto plano
- Solo prueba quién lo firmó, no lo oculta

**Ejemplo:**
```python
mensaje = "Información sensible"  # ← Visible para todos
firma = firmar(mensaje, d)        # ← Solo añade firma

# Cualquiera puede leer "Información sensible"
# La firma solo prueba que Alicia lo firmó
```

**Si necesitas confidencialidad:**
Combinar con cifrado:
```python
# 1. Cifrar mensaje (ej: AES, RSA)
mensaje_cifrado = cifrar(mensaje, llave_simetrica)

# 2. Luego firmar
firma = firmar(mensaje_cifrado, llave_privada)

# Ahora tienes: confidencialidad + autenticación
```

**Alternativas para confidencialidad:**
- AES (cifrado simétrico)
- RSA (cifrado asimétrico)
- ECIES (cifrado con curvas elípticas)

---

### 6. ❌ NO PROPORCIONA: ANONIMATO

**Definición:** Ocultar la identidad del firmante

**Por qué ECDSA NO es anónimo:**
- Llave pública identifica al firmante
- Verificación revela quién firmó

**Ejemplo:**
```python
# Verificación exitosa identifica a Alicia
verificar(mensaje, firma, llave_publica_alicia) → True
# ↑ Betito sabe que ALICIA firmó
```

**Si necesitas anonimato:**
- Ring Signatures (firmas de anillo)
- Blind Signatures (firmas ciegas)
- Zero-Knowledge Proofs (pruebas de conocimiento cero)

---

## 📊 TABLA COMPARATIVA DE SERVICIOS

| Servicio | Proporcionado | Algoritmo/Técnica | Garantía |
|----------|---------------|-------------------|----------|
| **Autenticación** | ✅ Sí | ECDSA + Llave privada única | Computacional (ECDLP difícil) |
| **Integridad** | ✅ Sí | SHA-256 + ECDSA | Colisión SHA-256 intratable |
| **No Repudio** | ✅ Sí | ECDSA (firma no falsificable) | ECDLP + llave privada secreta |
| **Detección Fraude** | ✅ Sí | Verificación criptográfica | Matemática (imposible sin llave) |
| **Confidencialidad** | ❌ No | N/A | No implementado |
| **Anonimato** | ❌ No | N/A | Llave pública identifica |
| **Resistencia Replay** | ⚠️ Parcial | Hash único por mensaje | Requiere timestamps |
| **Forward Secrecy** | ❌ No | N/A | Llave privada única |

---

## 🔐 MODELO DE AMENAZAS

### Amenazas Mitigadas ✅

1. **Suplantación de identidad**
   - Atacante: Candy pretende ser Alicia
   - Mitigación: Firma de Candy no verifica con Q_alicia
   - Probabilidad de éxito: ~0% (ECDLP intratable)

2. **Modificación de mensaje**
   - Atacante: Altera "pagar $100" → "pagar $1000"
   - Mitigación: Cambio en hash invalida firma
   - Probabilidad de éxito: ~0% (colisión SHA-256)

3. **Repudio**
   - Atacante: Alicia niega haber firmado
   - Mitigación: Firma es prueba criptográfica
   - Probabilidad de éxito: 0% (con llave privada secreta)

4. **Firma falsa**
   - Atacante: Intenta crear firma sin llave privada
   - Mitigación: ECDLP computacionalmente intratable
   - Probabilidad de éxito: ~2^-128 (curvas seguras)

### Amenazas NO Mitigadas ❌

1. **Robo de llave privada**
   - Si atacante obtiene la llave privada de Alicia
   - Puede firmar como Alicia
   - Mitigación: Protección física, HSM, contraseñas

2. **Ataque de replay**
   - Atacante reutiliza firma válida antigua
   - Si contexto no cambia, firma sigue siendo válida
   - Mitigación: Timestamps, nonces, sequence numbers

3. **Man-in-the-Middle en distribución de llaves**
   - Atacante intercepta llave pública
   - Sustituye con su propia llave
   - Mitigación: PKI, certificados, canales autenticados

4. **Análisis de canal lateral**
   - Timing attacks, power analysis
   - Pueden revelar información sobre llave privada
   - Mitigación: Implementación constante en tiempo

---

## 🎓 COMPARACIÓN CON ESTÁNDARES

### Nuestro Proyecto vs Bitcoin (secp256k1)

| Aspecto | Nuestro Proyecto | Bitcoin |
|---------|------------------|---------|
| **Curva** | y²=x³+2x+3 (mod 97) | y²=x³+7 (mod p) |
| **Primo p** | 97 | 2^256 - 2^32 - 977 |
| **Bits seguridad** | ~6.6 bits | ~128 bits |
| **Hash** | SHA-256 ✅ | SHA-256 ✅ |
| **Algoritmo** | ECDSA ✅ | ECDSA ✅ |
| **Formato llaves** | PEM híbrido | DER comprimido |
| **Propósito** | Educativo | Producción |
| **Resistencia** | Segundos (fuerza bruta) | Billones de años |

**Similitudes importantes:**
- ✅ Mismo algoritmo ECDSA
- ✅ Mismo hash SHA-256
- ✅ Misma estructura matemática
- ✅ Mismos principios de seguridad

**Diferencia clave:**
- Tamaño de la curva (educativa vs segura)

---

## 📚 REFERENCIAS Y ESTÁNDARES

### Estándares Implementados

1. **FIPS 186-4** - Digital Signature Standard
   - Especifica ECDSA
   - https://csrc.nist.gov/publications/fips

2. **FIPS 180-4** - Secure Hash Standard
   - Especifica SHA-256
   - https://csrc.nist.gov/publications/fips

3. **RFC 4648** - Base64 Encoding
   - https://tools.ietf.org/html/rfc4648

4. **SEC 1** - Elliptic Curve Cryptography
   - http://www.secg.org/sec1-v2.pdf

5. **ANSI X9.62** - Public Key Cryptography for Financial Services

### Bibliografía Técnica

- **"Handbook of Applied Cryptography"** - Menezes, van Oorschot, Vanstone
- **"Guide to Elliptic Curve Cryptography"** - Hankerson, Menezes, Vanstone
- **NIST SP 800-186** - Discrete Log-based Crypto Recommendations

---

## 🎯 RESUMEN EJECUTIVO

### Algoritmos Criptográficos

1. **ECDSA** - Firma digital (asimétrico)
2. **SHA-256** - Hash criptográfico
3. **Euclides Extendido** - Inverso modular
4. **Double-and-Add** - Multiplicación escalar

### Bibliotecas Criptográficas

1. **hashlib** - SHA-256 (backend OpenSSL)
2. **secrets** - CSPRNG del sistema operativo
3. **base64** - Codificación RFC 4648
4. **math** - GCD (algoritmo de Euclides)

### Servicios de Seguridad

✅ **Proporciona:**
- Autenticación (verificar identidad)
- Integridad (detectar modificaciones)
- No repudio (prueba legal)
- Detección de falsificaciones

❌ **No proporciona:**
- Confidencialidad (mensaje en claro)
- Anonimato (firmante identificado)

---

**Este proyecto implementa criptografía de clase industrial con bibliotecas estándar de Python, adaptada para propósitos educativos.** 🔐
