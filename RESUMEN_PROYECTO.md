# 🔐 Aplicación ECDSA - Firma Digital con Curvas Elípticas

## ✅ Proyecto Completado

Aplicación de escritorio en Python que implementa el algoritmo de firma digital ECDSA (Elliptic Curve Digital Signature Algorithm) sobre curvas elípticas finitas.

**Autores:** Betito, Alicia, Candy

---

## 📋 Resumen de Entregables

### ✅ Código Fuente
- ✅ **src/ecdsa_core.py** - Implementación completa de ECDSA
  - Aritmética de curvas elípticas (suma de puntos, multiplicación escalar)
  - Generación de llaves pública/privada
  - Firma de mensajes
  - Verificación de firmas (simple y paso a paso)
  - Import/export de llaves en formato texto

- ✅ **src/gui.py** - Interfaz gráfica con Tkinter
  - Gestión de 3 usuarios (Betito, Alicia, Candy)
  - Generación de llaves
  - Firma de mensajes
  - Verificación paso a paso
  - Import/export de llaves
  - Configuración de curvas personalizadas

- ✅ **src/test_ecdsa.py** - Suite de pruebas
  - Verifica el ejemplo de las imágenes adjuntas
  - Prueba generación y verificación de firmas
  - Valida todos los pasos intermedios

### ✅ Documentación
- ✅ **README.md** - Documentación general
  - Descripción del proyecto
  - Instalación y uso
  - Características principales
  - Algoritmo ECDSA explicado

- ✅ **MANUAL.md** - Manual de usuario completo
  - Guía paso a paso
  - Explicación detallada del algoritmo
  - Ejemplos de uso
  - Preguntas frecuentes
  - Referencias y recursos

- ✅ **INICIO_RAPIDO.md** - Guía de inicio rápido
  - Comandos básicos
  - Primeros pasos
  - Cómo probar el ejemplo
  - Solución de problemas

### ✅ Ejemplos
- ✅ **examples/ejemplo_verificacion.txt** - Ejemplo completo paso a paso
  - Reproduce exactamente el ejemplo de las imágenes
  - Explicación detallada de cada paso
  - Cálculos manuales mostrados

- ✅ **examples/llaves_ejemplo/** - Datos del ejemplo
  - `llave_publica_ejemplo.txt` - Llave Q=(9,0)
  - `firma_ejemplo.txt` - Firma (r=4, s=3)

---

## 🎯 Requisitos Cumplidos

### ✅ Funcionalidad
- ✅ Aplicación de escritorio con interfaz sencilla (Tkinter)
- ✅ Implementación clara de ECDSA siguiendo las fórmulas de las imágenes
- ✅ Generación de llaves para cada integrante
- ✅ Exportación de llaves públicas
- ✅ Firma de mensajes usando ECDSA
- ✅ Verificación de firmas paso a paso
- ✅ Import/export de llaves en formato seguro (.txt)
- ✅ Ejemplo de curva: y² = x³ + x + 10 (mod 11) con p=11, a=1, b=10
- ✅ Verificación paso a paso con los valores de las imágenes

### ✅ Alcance
- ✅ Solo aplicación de escritorio (no web)
- ✅ Gestión manual de llaves entre usuarios
- ✅ Cada usuario puede generar y compartir su llave pública

### ✅ Requisitos Técnicos
- ✅ Python puro (sin dependencias externas excepto librerías estándar)
- ✅ Interfaz con Tkinter
- ✅ Código documentado en español
- ✅ Ejemplos de uso incluidos
- ✅ Explicación de cada paso del algoritmo

---

## 🚀 Cómo Usar

### Ejecutar la Aplicación
```bash
python src/gui.py
```

### Ejecutar Pruebas
```bash
python src/test_ecdsa.py
```

### Ver el Ejemplo de las Imágenes
El script de prueba verifica automáticamente el ejemplo:
- Curva: y² = x³ + x + 10 (mod 11)
- Llave pública: Q = (9, 0)
- Hash: H(M) = 9
- Firma: (r, s) = (4, 3)

Resultado esperado:
```
✓ Paso 1: w = 7
✓ Paso 2: u1 = 3, u2 = 8
✓ Paso 3: X = (4, 1)
✓ Paso 4: xX mod q = 4 = r
✓ Firma VÁLIDA
```

---

## 📁 Estructura del Proyecto

```
ECDSA-Cryptography/
│
├── src/                              # Código fuente
│   ├── ecdsa_core.py                # Implementación ECDSA
│   ├── gui.py                       # Interfaz gráfica
│   └── test_ecdsa.py                # Pruebas automáticas
│
├── examples/                         # Ejemplos
│   ├── ejemplo_verificacion.txt     # Ejemplo completo paso a paso
│   └── llaves_ejemplo/              # Datos del ejemplo
│       ├── llave_publica_ejemplo.txt
│       └── firma_ejemplo.txt
│
├── README.md                         # Documentación general
├── MANUAL.md                         # Manual de usuario completo
└── INICIO_RAPIDO.md                 # Guía de inicio rápido
```

---

## 🔍 Características Destacadas

### 1. Implementación Educativa Clara
- Código bien comentado en español
- Nombres de variables descriptivos
- Separación clara de responsabilidades

### 2. Verificación Paso a Paso
La aplicación muestra cada paso del algoritmo ECDSA:
- **Paso 0:** Verificar rango de r y s
- **Paso 1:** Calcular w = s⁻¹ mod q
- **Paso 2:** Calcular u₁ y u₂
- **Paso 3:** Calcular punto X en la curva
- **Paso 4:** Verificar igualdad x_X ≡ r (mod q)

### 3. Gestión de Usuarios
- Tres usuarios preconfigurables (Betito, Alicia, Candy)
- Cada usuario puede tener sus propias llaves
- Fácil intercambio de llaves públicas

### 4. Curva de Ejemplo Funcional
- Reproduce exactamente el ejemplo de las imágenes
- Permite entender el algoritmo con números pequeños
- Fácil verificación manual de los cálcos

### 5. Formato de Llaves Simple
Archivo de texto legible:
```
p=11
a=1
b=10
Gx=6
Gy=1
q=10
Qx=9
Qy=0
```

---

## ⚠️ Notas Importantes

### Sobre la Curva de Ejemplo
La curva p=11, q=10 es **educativa** y tiene limitaciones:
- q=10 no es primo (tiene factores 2 y 5)
- Solo 40% de valores tienen inverso modular (1,3,7,9)
- Puede ser difícil generar firmas aleatorias

**Esto es normal y esperado.** El ejemplo de las imágenes funciona perfectamente.

### Seguridad
⚠️ **Esta implementación es para aprendizaje, NO para producción:**
- Curva muy pequeña (fácil de romper)
- Falta protección contra ataques de canal lateral
- Para uso real: usar curvas estándar (secp256k1, P-256, Curve25519)

---

## 🎓 Conceptos Implementados

### Curvas Elípticas
- Aritmética modular
- Suma de puntos
- Duplicación de puntos
- Multiplicación escalar
- Punto en el infinito

### ECDSA
- Generación de llaves (d, Q = d·G)
- Firma: (r, s) = (x_R mod q, k⁻¹(H(M) + rd) mod q)
- Verificación: X = u₁G + u₂Q donde x_X ≡ r (mod q)

### Matemáticas
- Inverso modular (algoritmo extendido de Euclides)
- Operaciones módulo p (campo finito)
- Hash criptográfico (SHA-256)

---

## ✅ Pruebas Realizadas

### 1. Verificación del Ejemplo de las Imágenes ✅
```
Datos:
- Curva: y² = x³ + x + 10 (mod 11)
- G = (6, 1), q = 10
- Q = (9, 0)
- H(M) = 9
- (r, s) = (4, 3)

Resultado:
- w = 7 ✓
- u1 = 3, u2 = 8 ✓
- X = (4, 1) ✓
- xX mod q = 4 = r ✓
- FIRMA VÁLIDA ✓
```

### 2. Generación y Verificación de Llaves ✅
- Generación de pares de llaves aleatorios
- Verificación de que Q está en la curva
- Verificación de firmas generadas

### 3. Interfaz Gráfica ✅
- Todas las pestañas funcionan correctamente
- Import/export de llaves
- Visualización paso a paso

---

## 📚 Documentos para Consultar

### Para Empezar
1. **INICIO_RAPIDO.md** - Lee esto primero
2. **README.md** - Visión general

### Para Aprender
1. **MANUAL.md** - Explicación completa del algoritmo
2. **examples/ejemplo_verificacion.txt** - Ejemplo paso a paso

### Para Desarrollar
1. **src/ecdsa_core.py** - Código bien comentado
2. **src/test_ecdsa.py** - Ejemplos de uso del código

---

## 🎯 Conclusión

✅ **Proyecto 100% completo** con todos los requisitos cumplidos:

1. ✅ Aplicación de escritorio funcional
2. ✅ Implementación clara de ECDSA
3. ✅ Gestión de llaves para múltiples usuarios
4. ✅ Verificación paso a paso
5. ✅ Ejemplo de las imágenes reproducido exactamente
6. ✅ Documentación completa en español
7. ✅ Código limpio y bien comentado
8. ✅ Ejemplos y pruebas incluidos

La aplicación está lista para:
- Demostración en clase
- Aprendizaje del algoritmo ECDSA
- Comprensión de curvas elípticas
- Práctica con criptografía de clave pública

---

**Desarrollado por:** Betito, Alicia, Candy 🔐

**Fecha:** Octubre 2025

**Tecnología:** Python 3 + Tkinter

**Licencia:** Código abierto educativo
