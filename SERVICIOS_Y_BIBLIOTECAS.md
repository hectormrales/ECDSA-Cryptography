# 🔧 Servicios Criptográficos y Bibliotecas del Proyecto ECDSA

## 🛡️ SERVICIOS CRIPTOGRÁFICOS PROPORCIONADOS

### Análisis de Servicios de Seguridad

Este proyecto implementa **firma digital ECDSA**, que proporciona ciertos servicios criptográficos específicos. Aquí está el análisis detallado:

---

### ✅ 1. AUTENTICACIÓN

**¿Qué es?** Verificar que el mensaje proviene realmente de quien dice ser el emisor.

**¿Este proyecto lo ofrece?** ✅ **SÍ**

**¿Por qué lo ofrece?**
- La firma digital solo puede ser generada por quien posee la **llave privada**
- Cada usuario tiene una llave privada única (d) que solo él conoce
- La llave pública (Q) identifica al usuario de manera única
- Matemáticamente: Q = d·G (solo quien conoce 'd' puede generar firmas válidas)

**Ejemplo práctico:**
```
Alicia firma mensaje: "Transferir $100"
Firma = firmar(mensaje, llave_privada_alicia)

Betito verifica con llave_publica_alicia
✅ Si la firma es válida → Betito tiene certeza de que Alicia envió el mensaje
❌ Si usa llave de Candy → Verificación falla (no es Alicia)
```

**Garantía:** Basada en el problema ECDLP (logaritmo discreto en curvas elípticas) que es computacionalmente intratable.

---

### ✅ 2. INTEGRIDAD

**¿Qué es?** Garantizar que el mensaje no ha sido modificado desde que fue firmado.

**¿Este proyecto lo ofrece?** ✅ **SÍ**

**¿Por qué lo ofrece?**
- Se calcula el **hash SHA-256 del mensaje** antes de firmar
- Este hash se incluye dentro de la firma: `s = k⁻¹(H(mensaje) + r·d) mod q`
- Si el mensaje cambia aunque sea 1 bit → el hash cambia completamente
- La firma no verificará con un hash diferente

**Ejemplo práctico:**
```
Mensaje original: "Pagar $100 a Candy"
Hash: SHA-256("Pagar $100 a Candy") = z
Firma: (r, s) basada en z

Un atacante modifica:
Mensaje alterado: "Pagar $999 a Candy"
Hash nuevo: SHA-256("Pagar $999 a Candy") = z' ≠ z

Al verificar:
verificar(mensaje_alterado, firma_original, Q) → ❌ FALLA
```

**Garantía:** SHA-256 es resistente a colisiones (~2^128 operaciones para encontrar dos mensajes con el mismo hash).

---

### ✅ 3. NO REPUDIO (Non-Repudiation)

**¿Qué es?** El emisor no puede negar posteriormente que él firmó el mensaje.

**¿Este proyecto lo ofrece?** ✅ **SÍ**

**¿Por qué lo ofrece?**
- Solo Alicia posee su llave privada
- Solo ella puede generar firmas válidas con esa llave
- La firma es una **prueba matemática** de que Alicia firmó
- Alicia no puede decir "yo no firmé eso" porque la prueba criptográfica existe

**Ejemplo práctico:**
```
Alicia firma un contrato digital: "Acepto pagar $500"
Firma: (r, s)

Más tarde, Alicia intenta negar:
"Yo nunca firmé ese contrato"

Pero la firma es verificable:
verificar("Acepto pagar $500", (r,s), llave_publica_alicia) → ✅ VÁLIDA

Conclusión: Alicia SÍ firmó (tiene valor legal)
```

**Garantía:** 
- La firma solo pudo ser creada con la llave privada de Alicia
- Problema ECDLP hace imposible falsificar la firma
- **Requisito crítico:** La llave privada debe mantenerse secreta

**Valor legal:** Las firmas digitales tienen validez legal en muchos países (equivalente a firma manuscrita).

---

### ❌ 4. CONFIDENCIALIDAD

**¿Qué es?** Mantener el contenido del mensaje secreto, que solo el destinatario autorizado pueda leerlo.

**¿Este proyecto lo ofrece?** ❌ **NO**

**¿Por qué NO lo ofrece?**
- ECDSA es un esquema de **FIRMA**, no de **CIFRADO**
- El mensaje permanece en **texto plano** (sin cifrar)
- Cualquiera puede leer el mensaje original
- La firma solo prueba quién lo firmó y que no fue alterado

**Ejemplo práctico:**
```
Mensaje: "Información ultra secreta"  ← Cualquiera puede leerlo
Firma: (r=73, s=42)                    ← Solo prueba que Alicia lo firmó

❌ El contenido NO está protegido
✅ Solo está autenticado e íntegro
```

**Si necesitas confidencialidad:**
```
Solución: Combinar ECDSA con cifrado

1. Primero CIFRAR el mensaje:
   mensaje_cifrado = AES.encrypt(mensaje, clave_simetrica)

2. Luego FIRMAR el mensaje cifrado:
   firma = ECDSA.firmar(mensaje_cifrado, llave_privada)

Ahora tienes:
✅ Confidencialidad (por AES)
✅ Autenticación (por ECDSA)
✅ Integridad (por ECDSA)
✅ No repudio (por ECDSA)
```

**Algoritmos para confidencialidad:**
- AES (cifrado simétrico)
- RSA (cifrado asimétrico)
- ECIES (cifrado con curvas elípticas)

---

### ❌ 5. ANONIMATO

**¿Qué es?** Ocultar la identidad del emisor del mensaje.

**¿Este proyecto lo ofrece?** ❌ **NO**

**¿Por qué NO lo ofrece?**
- La **llave pública identifica al firmante**
- Cuando Betito verifica una firma, sabe exactamente QUIÉN firmó
- La verificación requiere la llave pública del firmante

**Ejemplo práctico:**
```
Betito recibe un mensaje firmado
Betito verifica con llave_publica_alicia → ✅ Válida
Conclusión: Betito SABE que Alicia firmó (no hay anonimato)

Betito verifica con llave_publica_candy → ❌ Inválida
Conclusión: No fue Candy quien firmó
```

**Si necesitas anonimato:**
- **Ring Signatures** (firmas de anillo) - firma válida pero no sabes quién del grupo firmó
- **Blind Signatures** (firmas ciegas) - firmante no ve el contenido
- **Zero-Knowledge Proofs** - probar algo sin revelar información

---

### ✅ 6. AUTENTICIDAD DEL ORIGEN DE DATOS

**¿Qué es?** Confirmar que los datos provienen de la fuente correcta.

**¿Este proyecto lo ofrece?** ✅ **SÍ**

**¿Por qué lo ofrece?**
- Es similar a autenticación, pero enfocado en los datos mismos
- La firma vincula el mensaje con la identidad del firmante
- No se puede reutilizar la firma para otro mensaje

**Ejemplo práctico:**
```
Alicia firma: "Documento A"
Firma_A = (r₁, s₁)

Un atacante intenta reutilizar la firma:
atacante usa Firma_A con "Documento B"

Verificación:
verificar("Documento B", Firma_A, llave_publica_alicia) → ❌ FALLA

Razón: La firma está vinculada criptográficamente al Documento A
       por medio del hash H(Documento A) incluido en la firma
```

---

### ⚠️ 7. PROTECCIÓN CONTRA ATAQUES DE REPLAY (Parcial)

**¿Qué es?** Evitar que un atacante capture una firma válida y la reutilice más tarde.

**¿Este proyecto lo ofrece?** ⚠️ **PARCIALMENTE**

**¿Por qué solo parcial?**
- ✅ La firma está vinculada al mensaje específico (hash único)
- ❌ NO incluye timestamps o números de secuencia
- ❌ Una firma antigua sigue siendo válida si el contexto no cambia

**Ejemplo de vulnerabilidad:**
```
Día 1:
Alicia firma: "Transferir $100 a Betito"
Firma: (r, s)

Día 30:
Un atacante interceptó la firma del día 1
Atacante reenvía: mensaje + firma (válidos del día 1)

Resultado: ✅ La firma sigue siendo válida
          El sistema no sabe que es un "replay"
```

**Cómo mejorar la protección:**
```python
# Incluir timestamp en el mensaje
mensaje = "Transferir $100 | Fecha: 2025-10-27 14:30:00"
firma = firmar(mensaje, llave_privada)

# O usar números de secuencia (nonce)
mensaje = "Transferir $100 | Nonce: 12345"
```

---

## 📊 TABLA RESUMEN DE SERVICIOS CRIPTOGRÁFICOS

| Servicio | ✅/❌ | ¿Por qué? | Mecanismo |
|----------|-------|----------|-----------|
| **Autenticación** | ✅ | Solo el poseedor de la llave privada puede firmar | Llave privada única + ECDLP |
| **Integridad** | ✅ | Hash SHA-256 detecta cualquier modificación | H(mensaje) incluido en firma |
| **No Repudio** | ✅ | Firma es prueba matemática no falsificable | ECDLP intratable + firma única |
| **Confidencialidad** | ❌ | ECDSA firma pero NO cifra | Mensaje en texto plano |
| **Anonimato** | ❌ | Llave pública identifica al firmante | Verificación revela identidad |
| **Autenticidad de Datos** | ✅ | Firma vinculada al mensaje específico | Hash único por mensaje |
| **Anti-Replay** | ⚠️ | Firma válida pero sin timestamp | Requiere implementar timestamps |

---

## 🎯 CASOS DE USO REALES

### Caso 1: Firma de Documento Legal ✅
```
Servicio: Autenticación + Integridad + No Repudio
Escenario: Alicia firma un contrato digital

1. Alicia firma: "Contrato de compra-venta..."
2. La firma prueba que Alicia lo firmó (autenticación)
3. La firma detecta modificaciones (integridad)
4. Alicia no puede negar haberlo firmado (no repudio)
5. Tiene valor legal en corte
```

### Caso 2: Verificación de Identidad ✅
```
Servicio: Autenticación
Escenario: Betito verifica que el mensaje es de Alicia

1. Betito recibe mensaje + firma
2. Verifica con llave pública de Alicia
3. Si válida → Confirma que Alicia lo envió
4. Previene suplantación de identidad
```

### Caso 3: Detección de Alteración ✅
```
Servicio: Integridad
Escenario: Detectar si alguien modificó el mensaje

1. Mensaje original: "Pagar $100"
2. Atacante modifica: "Pagar $999"
3. Verificación detecta el cambio
4. Sistema rechaza el mensaje alterado
```

### Caso 4: Transmisión Segura ❌ (Falta Confidencialidad)
```
Servicio: Confidencialidad NO disponible
Escenario: Enviar información sensible

1. Mensaje: "PIN: 1234"  ← Visible para todos
2. ECDSA solo firma, no cifra
3. Cualquiera puede leer el PIN
4. ❌ NO usar ECDSA solo para datos sensibles
5. ✅ Combinar con AES o RSA para cifrar
```

---

## 🔐 EXPLICACIÓN TÉCNICA DEL "POR QUÉ"

### ¿Por qué ECDSA proporciona Autenticación?

**Fundamento matemático:**
```
Llave privada: d (número secreto)
Llave pública: Q = d·G (punto en la curva)

Para firmar:
1. k = número aleatorio secreto
2. R = k·G
3. r = R.x mod q
4. s = k⁻¹(H(M) + r·d) mod q  ← Aquí se usa 'd' (llave privada)

Sin conocer 'd', es imposible calcular 's' correcto
Problema ECDLP: Dado Q y G, encontrar d es intratable
```

**En términos simples:**
- Solo quien tiene 'd' puede generar 's' válido
- Como solo Alicia tiene su 'd', solo ella puede crear firmas que verifiquen con su Q
- Esto autentica que Alicia es el origen

---

### ¿Por qué ECDSA proporciona Integridad?

**Fundamento matemático:**
```
Firma incluye el hash:
s = k⁻¹(H(mensaje) + r·d) mod q
              ↑
        Hash SHA-256

Si mensaje cambia:
- H(mensaje) cambia
- s calculado será diferente
- Verificación fallará

Verificación:
w = s⁻¹ mod q
u₁ = H(mensaje)·w mod q  ← Hash se vuelve a calcular
u₂ = r·w mod q
X = u₁·G + u₂·Q
Verificar: X.x == r

Si H(mensaje) cambió → u₁ cambió → X cambió → X.x ≠ r → ❌ Falla
```

**En términos simples:**
- El hash del mensaje está "cocido" dentro de la firma
- Cambiar el mensaje cambia el hash
- La firma ya no coincide con el nuevo hash
- Detección automática de modificación

---

### ¿Por qué ECDSA proporciona No Repudio?

**Fundamento matemático:**
```
Para generar firma válida se necesita:
1. Conocer 'd' (llave privada)
2. Resolver: s = k⁻¹(H(M) + r·d) mod q

Sin 'd' → Imposible generar 's' válido

Problema ECDLP garantiza que:
- No se puede derivar 'd' desde Q
- No se puede falsificar 's' sin 'd'
- Solo Alicia (quien posee 'd') pudo firmar
```

**En términos simples:**
- La firma solo pudo ser creada por quien tiene la llave privada
- Como la llave privada es secreta y única
- Solo Alicia pudo haberla creado
- Ella no puede negar haberla firmado (la prueba matemática existe)

---

### ¿Por qué ECDSA NO proporciona Confidencialidad?

**Fundamento matemático:**
```
Firma ECDSA:
Input: mensaje (texto plano), llave privada
Output: (r, s)

El mensaje NUNCA se transforma ni se cifra
Solo se firma:
  r = (k·G).x mod q
  s = k⁻¹(H(M) + r·d) mod q

Transmisión:
  Mensaje: "Hola mundo"  ← En texto plano (sin cifrar)
  Firma: (r, s)          ← Prueba de autenticidad
```

**En términos simples:**
- ECDSA es como un "sello" que se pone al mensaje
- El mensaje original sigue siendo legible
- Cualquiera puede leer "Hola mundo"
- El sello solo prueba que Alicia lo escribió

**Analogía:**
- Firma manuscrita en un documento → No oculta el texto, solo autentica
- Firma digital ECDSA → No oculta el mensaje, solo autentica

---

### ¿Por qué ECDSA NO proporciona Anonimato?

**Fundamento matemático:**
```
Verificación requiere la llave pública del firmante:

verificar(mensaje, (r,s), Q_alicia):
    w = s⁻¹ mod q
    u₁ = H(M)·w mod q
    u₂ = r·w mod q
    X = u₁·G + u₂·Q_alicia  ← Se usa Q_alicia específicamente
              ↑
    Identifica a Alicia

Si verificación pasa → Sabemos que fue Alicia
No hay forma de verificar sin saber quién firmó
```

**En términos simples:**
- Para verificar, necesitas saber quién supuestamente firmó
- Usas la llave pública de esa persona
- Si funciona, confirmas que esa persona firmó
- No hay forma de ocultar la identidad

---

## 📚 Bibliotecas Utilizadas

### 🌟 **CERO Dependencias Externas**

Una de las grandes ventajas del proyecto: **No requiere instalar NADA adicional.**

### Bibliotecas Estándar de Python

#### 1. **tkinter** - Interfaz Gráfica
```python
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
```

**¿Para qué?**
- Crear ventanas y elementos visuales
- Botones, campos de texto, pestañas
- Cuadros de diálogo (abrir/guardar archivos)
- Mensajes de confirmación/error

**¿Por qué?**
- ✅ Incluida en Python (no hay que instalar)
- ✅ Multiplataforma (Windows, Mac, Linux)
- ✅ Fácil de usar y aprender
- ✅ Suficiente para interfaces educativas

---

#### 2. **hashlib** - Funciones Hash Criptográficas
```python
import hashlib
```

**¿Para qué?**
- Calcular SHA-256 de mensajes
- Generar hash de 256 bits
- Asegurar integridad del mensaje

**Ejemplo de uso:**
```python
def hash_mensaje(self, mensaje: str) -> int:
    hash_bytes = hashlib.sha256(mensaje.encode('utf-8')).digest()
    hash_int = int.from_bytes(hash_bytes, byteorder='big')
    return hash_int % self.curva.q
```

**¿Por qué SHA-256?**
- ✅ Estándar industrial
- ✅ Usado en Bitcoin, TLS/SSL
- ✅ 256 bits de salida (seguro)
- ✅ Resistente a colisiones

---

#### 3. **secrets** - Generación Aleatoria Segura
```python
import secrets
```

**¿Para qué?**
- Generar llaves privadas aleatorias
- Generar nonce (k) para firmas
- Números criptográficamente seguros

**Ejemplo de uso:**
```python
def generar_llaves(self) -> Tuple[int, PuntoElliptico]:
    llave_privada = secrets.randbelow(self.curva.q - 1) + 1
    llave_publica = self.curva.multiplicar_escalar(llave_privada, self.curva.G)
    return llave_privada, llave_publica
```

**¿Por qué secrets y no random?**
- ✅ Criptográficamente seguro (CSPRNG)
- ✅ No predecible
- ✅ Adecuado para criptografía
- ❌ `random` es predecible (NO usar en crypto)

---

#### 4. **math** - Operaciones Matemáticas
```python
import math
```

**¿Para qué?**
- Algoritmo extendido de Euclides
- Cálculo de MCD (máximo común divisor)
- Inverso modular

**Ejemplo de uso:**
```python
def euclides_extendido(a: int, b: int) -> Tuple[int, int, int]:
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = euclides_extendido(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y
```

**Operaciones clave:**
- `math.gcd()` - Máximo común divisor
- Aritmética modular
- Inverso multiplicativo

---

#### 5. **typing** - Type Hints
```python
from typing import Tuple, Optional, List, Dict
```

**¿Para qué?**
- Documentar tipos de datos
- Mejorar legibilidad del código
- Ayuda al IDE con autocompletado
- Detectar errores antes de ejecutar

**Ejemplo:**
```python
def firmar(self, mensaje: str, llave_privada: int) -> Tuple[int, int]:
    # Retorna tupla (r, s)
    pass
```

---

#### 6. **sys** y **os** - Sistema Operativo
```python
import sys
import os
```

**¿Para qué?**
- Gestionar rutas de archivos
- Importar módulos correctamente
- Compatibilidad multiplataforma

**Ejemplo:**
```python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
```

---

## 📊 Comparación con Otras Implementaciones

### Nuestro Proyecto vs Alternativas

| Aspecto | Nuestro Proyecto | PyCryptodome | cryptography | OpenSSL |
|---------|------------------|--------------|--------------|---------|
| **Dependencias** | 0 ❌ | 1 📦 | 1 📦 | 1 📦 |
| **Instalación** | Ninguna ✅ | `pip install` | `pip install` | Compilar |
| **Educativo** | Sí ✅ | No ❌ | No ❌ | No ❌ |
| **Paso a paso** | Sí ✅ | No ❌ | No ❌ | No ❌ |
| **GUI** | Sí ✅ | No ❌ | No ❌ | No ❌ |
| **Producción** | No ❌ | Sí ✅ | Sí ✅ | Sí ✅ |
| **Curvas grandes** | Lento 🐌 | Rápido ⚡ | Rápido ⚡ | Rápido ⚡ |

### Ventajas de Usar Solo Bibliotecas Estándar

✅ **Sin complicaciones de instalación**
- No hay conflictos de versiones
- No hay problemas de dependencias
- Funciona inmediatamente

✅ **Portabilidad total**
- Cualquier sistema con Python funciona
- No depende de librerías de terceros
- No hay problemas de licencias

✅ **Código transparente**
- Todo el algoritmo visible
- Fácil de entender y modificar
- Perfecto para aprender

✅ **Mantenimiento simple**
- No hay que actualizar dependencias
- No hay vulnerabilidades de terceros
- Código autocontenido

---

## 🔍 Arquitectura del Servicio

### Estructura de Capas

```
┌─────────────────────────────────────┐
│     Capa de Presentación (GUI)      │
│         tkinter + widgets           │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      Capa de Lógica (ECDSA)         │
│  - Generación de llaves             │
│  - Firma de mensajes                │
│  - Verificación de firmas           │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   Capa Matemática (Curva Elíptica)  │
│  - Suma de puntos                   │
│  - Multiplicación escalar           │
│  - Inverso modular                  │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│  Capa de Utilidades (Crypto Básico) │
│  - hashlib (SHA-256)                │
│  - secrets (Aleatorio seguro)       │
│  - math (Aritmética modular)        │
└─────────────────────────────────────┘
```

---

## 💻 Requisitos del Sistema

### Mínimos

- **Python:** 3.7 o superior
- **RAM:** 50 MB
- **Disco:** 1 MB
- **SO:** Windows, Linux o macOS

### Verificar Instalación

```bash
# Verificar Python
python --version

# Verificar Tkinter (debe abrir ventana)
python -m tkinter

# Si falta Tkinter (raro):
# Ubuntu: sudo apt-get install python3-tk
# Fedora: sudo dnf install python3-tkinter
```

---

## 🎯 Servicios Específicos del Proyecto

### API Programática

Aunque tiene GUI, también puede usarse como biblioteca:

```python
from ecdsa_core import ECDSA, crear_curva_ejemplo

# Crear instancia
curva = crear_curva_ejemplo()
ecdsa = ECDSA(curva)

# Generar llaves
privada, publica = ecdsa.generar_llaves()

# Firmar
r, s = ecdsa.firmar("Hola mundo", privada)

# Verificar
valida = ecdsa.verificar("Hola mundo", r, s, publica)
```

### Servicios de Archivo

```python
# Exportar llave pública
exportar_llave_publica(publica, curva, "llave.txt")

# Importar llave pública
publica2, curva2 = importar_llave_publica("llave.txt")

# Guardar firma
with open("firma.txt", "w") as f:
    f.write(f"r={r}\ns={s}")
```

---

## 📝 Resumen Ejecutivo

### ¿Qué servicio ofrece?
**Sistema completo de firma digital ECDSA con interfaz gráfica educativa**

### ¿Qué bibliotecas usa?
**Solo bibliotecas estándar de Python (cero dependencias externas):**

1. **tkinter** - Interfaz gráfica
2. **hashlib** - Hash SHA-256
3. **secrets** - Aleatorio criptográfico
4. **math** - Operaciones matemáticas
5. **typing** - Type hints
6. **sys/os** - Utilidades de sistema

### ¿Por qué es especial?
- ✅ Sin dependencias externas
- ✅ Código 100% transparente
- ✅ Verificación paso a paso educativa
- ✅ Listo para ejecutar inmediatamente

### ¿Para quién es?
- 🎓 Estudiantes de criptografía
- 👨‍🏫 Profesores de seguridad
- 🔍 Cualquiera que quiera entender ECDSA
- 💻 Desarrolladores aprendiendo crypto

---

## 🚀 Ejemplo de Uso del Servicio

### Caso Real: Firma de Contrato Digital

```python
# 1. Alicia genera su identidad
alicia_ecdsa = ECDSA(crear_curva_ejemplo())
alicia_privada, alicia_publica = alicia_ecdsa.generar_llaves()

# 2. Alicia firma el contrato
contrato = "Acepto los términos del acuerdo XYZ"
r, s = alicia_ecdsa.firmar(contrato, alicia_privada)

# 3. Alicia envía a Betito:
#    - El contrato original
#    - La firma (r, s)
#    - Su llave pública

# 4. Betito verifica
betito_ecdsa = ECDSA(crear_curva_ejemplo())
es_valida = betito_ecdsa.verificar(contrato, r, s, alicia_publica)

if es_valida:
    print("✓ Firma válida - Alicia firmó el contrato")
else:
    print("✗ Firma inválida - Posible fraude")
```

---

**En resumen:** Un servicio de firma digital completo, usando solo lo que Python trae de fábrica. Simple, educativo y funcional. 🔐
