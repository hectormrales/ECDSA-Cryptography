# 🔧 Servicios y Bibliotecas del Proyecto ECDSA

## 🎯 ¿Qué Servicio Ofrece?

### Servicio Principal: **Sistema de Firma Digital ECDSA**

La aplicación ofrece un **servicio completo de criptografía de firma digital** que permite:

#### 1. 🔑 Gestión de Identidades Criptográficas
- **Generación de llaves:** Crear pares de llaves pública/privada
- **Almacenamiento:** Guardar llaves de forma segura
- **Import/Export:** Compartir llaves públicas entre usuarios
- **Multi-usuario:** Gestionar 3 identidades simultáneas

#### 2. ✍️ Servicio de Firma Digital
- **Firmar mensajes:** Crear firmas digitales únicas
- **Hash seguro:** SHA-256 para integridad del mensaje
- **Persistencia:** Guardar firmas en archivos
- **Formato legible:** Firmas en texto plano

#### 3. ✅ Verificación de Autenticidad
- **Verificación básica:** Validar si firma es correcta
- **Verificación educativa:** Mostrar paso a paso todo el proceso
- **Detección de fraude:** Identificar intentos de suplantación
- **Análisis matemático:** Explicar cada operación

#### 4. 🎓 Herramienta Educativa
- **Visualización:** Ver todo el proceso matemático
- **Interactividad:** Experimentar con diferentes parámetros
- **Curvas personalizadas:** Configurar curvas elípticas propias
- **Casos de uso:** Demostrar escenarios reales

### Casos de Uso Reales

```
✅ Autenticación de mensajes
✅ Firma de documentos digitales
✅ Verificación de identidad
✅ Detección de alteraciones
✅ Educación en criptografía
✅ Demostración de algoritmos
```

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
