# ECDSA - Firma Digital con Curvas Elípticas

**Estado:** ✅ Completamente funcional | **Tests:** 13/13 pasando | **Base64:** ✅ Implementado

Aplicación de escritorio para implementar el algoritmo de firma digital ECDSA (Elliptic Curve Digital Signature Algorithm) sobre curvas elípticas finitas.

**Autores:** Betito, Alicia, Candy

## Descripción

Esta aplicación permite:
- Generar pares de llaves pública/privada para cada usuario
- Firmar mensajes digitalmente usando ECDSA
- Verificar firmas digitales paso a paso
- Importar y exportar llaves en formato de texto
- Configurar diferentes curvas elípticas

## Requisitos

- Python 3.7 o superior
- Tkinter (incluido por defecto en Python)
- No se requieren dependencias externas

## Instalación

1. Clona o descarga este repositorio
2. Navega al directorio del proyecto:
```bash
cd ECDSA-Cryptography
```

## Uso

Para ejecutar la aplicación:

```bash
python src/gui.py
```

O en Windows:
```bash
py src/gui.py
```

## Estructura del Proyecto

```
ECDSA-Cryptography/
├── src/
│   ├── ecdsa_core.py    # Módulo principal con la implementación ECDSA
│   └── gui.py           # Interfaz gráfica con Tkinter
├── examples/
│   ├── ejemplo_verificacion.txt    # Ejemplo de verificación paso a paso
│   └── llaves_ejemplo/              # Llaves de ejemplo
├── README.md            # Este archivo
└── MANUAL.md           # Manual de usuario detallado
```

## Características Principales

### 1. Gestión de Llaves
- Generar nuevos pares de llaves para cada usuario (Betito, Alicia, Candy)
- **Exportar llaves en formato profesional (.pem con Base64)**
- Importar llaves públicas de otros usuarios
- Exportar/importar llaves privadas (con advertencia de seguridad)
- **Formato híbrido: números legibles + codificación Base64**

### 2. Firma de Mensajes
- Firmar cualquier mensaje de texto
- Visualizar la firma generada (r, s)
- **Guardar firmas en formato .sig con Base64**
- Formato dual: educativo y profesional

### 3. Verificación de Firmas
- Verificar firmas paso a paso según el algoritmo ECDSA
- Mostrar cada paso del proceso de verificación
- Soporte para hash manual (útil para ejemplos educativos)
- Compatible con formatos antiguos y nuevos

### 4. Configuración de Curvas
- **Curva profesional: y² = x³ + 2x + 3 (mod 97)**
- Configuración de curvas personalizadas
- Visualización de parámetros de la curva
- Módulo 9x más grande para mejor seguridad educativa

## Curva de Ejemplo

La aplicación incluye una curva profesional para propósitos educativos:

**Ecuación:** y² = x³ + 2x + 3 (mod 97)

**Parámetros:**
- p = 97 (primo del campo finito - 9x más grande que versiones anteriores)
- a = 2 (coeficiente)
- b = 3 (coeficiente)
- G = (3, 6) (punto generador)
- q = 5 (orden del generador)

**Ventajas:**
- Módulo más grande (p=97) para mejor demostración
- Valores numéricos de 2 dígitos (más realista)
- Formato profesional con codificación Base64
- Compatible con estándares de la industria

## Formatos de Archivo

### Llaves Públicas (.pem)
```
-----BEGIN ECDSA PUBLIC KEY-----
Format: ECDSA-Educational-v1
Encoding: Hybrid (Plain + Base64)

# Readable Format (Educational)
p=97
a=2
b=3
Gx=3
Gy=6
q=5
Qx=17
Qy=23

# Base64 Encoding (Professional)
cD05NwphPTIKYj0zCkd4PTMKR3k9NgpxPTUKUXg9MTcKUXk9MjM=
-----END ECDSA PUBLIC KEY-----
```

### Firmas Digitales (.sig)
```
=== FIRMA DIGITAL ECDSA ===

Usuario: Alicia
Mensaje: Si acepto

# Readable Format (Educational)
Firma (r, s):
  r = 73
  s = 42

Hash del mensaje: H(M) = 3

# Base64 Encoding (Professional)
cj03MwpzPTQy
```

**Formato Híbrido:**
- ✅ Números legibles para aprendizaje
- ✅ Base64 para estándares profesionales
- ✅ Compatible con sistemas antiguos
- ✅ Headers PEM estándar

## Ejemplo de Verificación

Ver `examples/ejemplo_verificacion.txt` para ejemplos detallados paso a paso.

Para la práctica con Alicia, Candy y Betito, consulta:
- `EJERCICIO_PRACTICO.md` - Escenario completo de la práctica
- `BASE64_IMPLEMENTADO.md` - Ejemplos de formato híbrido
- `ejercicio_firmas/` - Directorio con archivos de práctica

## Seguridad

⚠️ **IMPORTANTE:**
- Esta es una implementación educativa con propósitos de aprendizaje
- La curva actual (p=97) es más grande que versiones anteriores pero aún es pequeña
- **NO es segura para uso en producción**
- Para uso real, utiliza curvas estándar como:
  - **secp256k1** (usado en Bitcoin, Ethereum)
  - **P-256** (NIST, usado en TLS/SSL)
  - **Ed25519** (usado en SSH moderno)
- Las llaves privadas deben mantenerse SIEMPRE en secreto
- Formato Base64 incluido para demostrar estándares profesionales

## Mejoras Profesionales Implementadas

✅ **Módulo más grande:** p=97 (vs p=11 anterior)
✅ **Formato híbrido:** Números legibles + Base64
✅ **Extensiones estándar:** .pem para llaves, .sig para firmas
✅ **Headers PEM:** BEGIN/END como en producción
✅ **Compatible:** Lee formatos antiguos y nuevos
✅ **Educativo + Profesional:** Lo mejor de ambos mundos

## Algoritmo ECDSA

### Generación de Llaves
1. Elegir un número aleatorio `d` en [1, q-1] → llave privada
2. Calcular `Q = d·G` → llave pública

### Firma
1. Calcular hash del mensaje: `z = H(M)`
2. Elegir número aleatorio `k` en [1, q-1]
3. Calcular `R = k·G`
4. `r = x_R mod q`
5. `s = k⁻¹(z + rd) mod q`
6. La firma es `(r, s)`

### Verificación
1. Verificar que `1 ≤ r, s ≤ q-1`
2. Calcular `w = s⁻¹ mod q`
3. Calcular `u₁ = zw mod q` y `u₂ = rw mod q`
4. Calcular `X = u₁G + u₂Q`
5. Verificar que `x_X ≡ r (mod q)`

## Documentación Adicional

- **`MANUAL.md`** - Manual de usuario completo
- **`BASE64_IMPLEMENTADO.md`** - Ejemplos de formato híbrido con Base64
- **`EJERCICIO_PRACTICO.md`** - Escenario de práctica (Alicia, Candy, Betito)
- **`RESUMEN_CAMBIOS.md`** - Cambios de p=11 a p=97
- **`FORMATO_LLAVES_FIRMAS.md`** - Comparación de formatos
- **`GUIA_PRESENTACION.md`** - Guía para presentar el proyecto
- **`INICIO_RAPIDO.md`** - Quick start en español

## Licencia

Este proyecto es de código abierto con fines educativos.

## Autores

- Betito
- Alicia
- Candy
