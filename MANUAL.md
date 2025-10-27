# Manual de Usuario - ECDSA Firma Digital

## Tabla de Contenidos
1. [Introducción](#introducción)
2. [Inicio Rápido](#inicio-rápido)
3. [Gestión de Llaves](#gestión-de-llaves)
4. [Firmar Mensajes](#firmar-mensajes)
5. [Verificar Firmas](#verificar-firmas)
6. [Configurar Curvas](#configurar-curvas)
7. [Ejemplo Completo](#ejemplo-completo)
8. [Explicación del Algoritmo ECDSA](#explicación-del-algoritmo-ecdsa)
9. [Preguntas Frecuentes](#preguntas-frecuentes)

---

## Introducción

Esta aplicación implementa el algoritmo de **firma digital ECDSA** (Elliptic Curve Digital Signature Algorithm) de manera educativa y visual. Permite a tres usuarios (Betito, Alicia y Candy) generar llaves, firmar mensajes y verificar firmas digitales.

### ¿Qué es ECDSA?

ECDSA es un algoritmo de firma digital que utiliza curvas elípticas sobre campos finitos. Permite:
- **Autenticación:** Verificar quién firmó un mensaje
- **Integridad:** Asegurar que el mensaje no fue modificado
- **No repudio:** El firmante no puede negar haber firmado

---

## Inicio Rápido

### 1. Ejecutar la Aplicación

```bash
python src/gui.py
```

### 2. Primera Vez - Generar Llaves

1. Ve a la pestaña **"Gestión de Llaves"**
2. Selecciona tu usuario (Betito, Alicia o Candy)
3. Haz clic en **"Generar Nuevo Par de Llaves"**
4. ¡Listo! Ya tienes tu llave privada y pública

### 3. Firmar un Mensaje

1. Ve a la pestaña **"Firmar Mensaje"**
2. Escribe tu mensaje en el cuadro de texto
3. Haz clic en **"Firmar Mensaje"**
4. La firma (r, s) aparecerá en el cuadro inferior

### 4. Verificar una Firma

1. Ve a la pestaña **"Verificar Firma"**
2. Ingresa el mensaje original
3. Ingresa los valores r y s de la firma
4. Selecciona quién firmó el mensaje
5. Haz clic en **"Verificar Firma (Paso a Paso)"**

---

## Gestión de Llaves

### Generar Llaves Nuevas

**Pasos:**
1. Selecciona el usuario (botón de radio en la parte superior)
2. Clic en **"Generar Nuevo Par de Llaves"**
3. La aplicación genera automáticamente:
   - Llave privada `d`: número aleatorio secreto
   - Llave pública `Q = d·G`: punto en la curva

**Información mostrada:**
- Parámetros de la curva utilizada
- Valor de la llave privada (¡mantener en secreto!)
- Coordenadas de la llave pública
- Verificación de que Q está en la curva

### Exportar Llave Pública

Las llaves públicas se comparten con otros usuarios para que puedan verificar tus firmas.

**Pasos:**
1. Asegúrate de tener una llave generada
2. Clic en **"Exportar Llave Pública"**
3. Elige ubicación y nombre del archivo
4. Comparte el archivo `.txt` con otros usuarios

**Formato del archivo:**
```
# Llave Pública ECDSA
# Curva: y² = x³ + 1x + 10 (mod 11)
# Generador G = (6, 1)
# Orden q = 10

p=11
a=1
b=10
Gx=6
Gy=1
q=10
Qx=9
Qy=0
```

### Importar Llave Pública

Para verificar firmas de otros usuarios, necesitas su llave pública.

**Pasos:**
1. Selecciona el usuario al que quieres asignar la llave
2. Clic en **"Importar Llave Pública"**
3. Selecciona el archivo `.txt` con la llave pública
4. La llave se carga automáticamente

### Exportar/Importar Llave Privada

⚠️ **ADVERTENCIA:** La llave privada debe mantenerse en secreto. Solo exporta si es necesario hacer respaldo.

**Exportar:**
1. Clic en **"Exportar Llave Privada"**
2. Confirma la advertencia de seguridad
3. Guarda el archivo en lugar seguro

**Importar:**
1. Clic en **"Importar Llave Privada"**
2. Selecciona el archivo
3. La llave privada y pública se cargan automáticamente

---

## Firmar Mensajes

### Proceso de Firma

**Pasos:**
1. Ve a la pestaña **"Firmar Mensaje"**
2. El usuario actual se muestra en la parte superior
3. Escribe el mensaje a firmar en el área de texto
4. Clic en **"Firmar Mensaje"**

**Resultado:**
```
=== FIRMA DIGITAL ECDSA ===

Usuario: Betito
Mensaje: Hola mundo

Firma (r, s):
  r = 4
  s = 3

Hash del mensaje: H(M) = 9
```

### Guardar Firma

Para compartir la firma con otros:
1. Después de firmar, clic en **"Guardar Firma"**
2. Elige ubicación y nombre del archivo
3. Comparte el archivo junto con el mensaje original

---

## Verificar Firmas

### Verificación Paso a Paso

Esta es la funcionalidad más poderosa de la aplicación. Muestra cada paso del algoritmo de verificación.

**Pasos:**
1. Ve a la pestaña **"Verificar Firma"**
2. Ingresa el **mensaje original** en el primer cuadro
3. Ingresa los valores **r** y **s** de la firma
   - Manualmente en los campos
   - O clic en "Cargar Firma desde Archivo"
4. Selecciona quién firmó el mensaje (Betito, Alicia o Candy)
5. Clic en **"Verificar Firma (Paso a Paso)"**

**Resultado Detallado:**

La aplicación muestra:

#### Paso 0: Verificación de Rango
```
Verificar que 1 ≤ r, s ≤ q-1
r = 4, s = 3, q-1 = 9
```

#### Paso 1: Calcular w = s⁻¹ mod q
```
Necesitamos el inverso modular de s = 3 módulo q = 10
3 × 7 ≡ 21 ≡ 1 (mod 10)
Entonces w = 7
```

#### Paso 2: Calcular u₁ y u₂
```
u₁ = H(M) × w mod q = 9 × 7 mod 10 = 63 mod 10 = 3
u₂ = r × w mod q = 4 × 7 mod 10 = 28 mod 10 = 8
```

#### Paso 3: Calcular X = u₁·G + u₂·Q
```
Multiplicaciones escalares y suma de puntos en la curva:
u₁·G = 3·(6, 1) = (4, 1)
u₂·Q = 8·(9, 0) = O (punto en el infinito)
X = (4, 1) + O = (4, 1)
```

#### Paso 4: Verificar x_X ≡ r (mod q)
```
La coordenada x de X es x_X = 4
x_X mod q = 4 mod 10 = 4
Esto coincide con r = 4
```

**RESULTADO FINAL: ✓ La firma es VÁLIDA**

### Usar Hash Manual

Para verificar ejemplos específicos (como el de las imágenes adjuntas):

1. Marca la casilla **"Usar valor de hash manual H(M)"**
2. Ingresa el valor del hash (por ejemplo: 9)
3. Procede con la verificación normalmente

Esto es útil para casos educativos donde el hash ya está calculado.

---

## Configurar Curvas

### Curva de Ejemplo (p=11)

La aplicación incluye una curva

**Ecuación:** y² = x³ + x + 10 (mod 11)

**Parámetros:**
- **p = 11**: Campo finito F₁₁
- **a = 1**: Coeficiente de x
- **b = 10**: Término constante
- **G = (6, 1)**: Punto generador
- **q = 10**: Orden del generador

### Cargar Curva de Ejemplo

1. Ve a la pestaña **"Configurar Curva"**
2. Clic en **"Cargar Curva de Ejemplo (p=11)"**
3. Los parámetros se llenan automáticamente
4. Clic en **"Aplicar Curva"**

### Crear Curva Personalizada

Para experimentar con diferentes curvas:

1. Ingresa los valores de:
   - Primo **p**
   - Coeficientes **a** y **b**
   - Punto generador **Gx** y **Gy**
   - Orden **q**

2. Clic en **"Aplicar Curva"**

⚠️ **Nota:** Asegúrate de que los parámetros sean válidos:
- p debe ser primo
- El discriminante 4a³ + 27b² ≠ 0 (mod p)
- G debe estar en la curva
- q debe ser el orden de G

---

## Ejemplo Completo

### Escenario: Betito firma un mensaje para Alicia

#### 1. Betito Genera sus Llaves
```
Usuario: Betito
Llave Privada (d): 5
Llave Pública (Q): (9, 0)
```

#### 2. Betito Firma el Mensaje
```
Mensaje: "Hola Alicia"
Firma: (r=4, s=3)
```

#### 3. Betito Comparte
- Envía a Alicia:
  - El mensaje original: "Hola Alicia"
  - La firma: r=4, s=3
  - Su llave pública (archivo `llave_publica_Betito.txt`)

#### 4. Alicia Verifica la Firma

**Acciones:**
1. Cambia a usuario "Alicia"
2. Importa la llave pública de Betito
3. Va a "Verificar Firma"
4. Ingresa el mensaje: "Hola Alicia"
5. Ingresa r=4, s=3
6. Selecciona "Betito" como firmante
7. Clic en "Verificar Firma (Paso a Paso)"

**Resultado:**
✓ La firma es VÁLIDA

Alicia confirma que:
- El mensaje fue firmado por Betito (autenticación)
- El mensaje no fue modificado (integridad)

---

## Explicación del Algoritmo ECDSA

### Conceptos Fundamentales

#### Curva Elíptica
Una curva elíptica sobre un campo finito F_p tiene la forma:

**y² = x³ + ax + b (mod p)**

Los puntos (x, y) que satisfacen esta ecuación forman un grupo con:
- Operación de suma de puntos
- Punto especial O (punto en el infinito, elemento identidad)

#### Multiplicación Escalar
k·P significa sumar el punto P consigo mismo k veces:
- 2·P = P + P
- 3·P = P + P + P
- etc.

#### Problema del Logaritmo Discreto
Dado P y Q = k·P, es computacionalmente difícil encontrar k.

**Esto es la base de la seguridad de ECDSA.**

### Algoritmo Completo

#### Configuración Inicial
- Curva elíptica con parámetros (p, a, b)
- Punto generador G de orden q
- Función hash H (SHA-256 en esta implementación)

#### Generación de Llaves

**Privada:**
```
d = número aleatorio en [1, q-1]
```

**Pública:**
```
Q = d·G
```

La llave privada `d` debe mantenerse en secreto. La llave pública `Q` se comparte.

#### Firma de Mensaje M

**Entrada:** Mensaje M, llave privada d

**Pasos:**
1. Calcular hash: `z = H(M) mod q`
2. Elegir nonce aleatorio: `k` en [1, q-1]
3. Calcular punto: `R = k·G`
4. Calcular componente r: `r = x_R mod q`
5. Si r = 0, volver al paso 2
6. Calcular inverso: `k⁻¹ mod q`
7. Calcular componente s: `s = k⁻¹(z + rd) mod q`
8. Si s = 0, volver al paso 2

**Salida:** Firma (r, s)

⚠️ **Importante:** El nonce k debe ser único y secreto para cada firma. Reutilizar k compromete la llave privada.

#### Verificación de Firma

**Entrada:** Mensaje M, firma (r, s), llave pública Q

**Paso 0:** Verificar rango
```
Verificar que 1 ≤ r ≤ q-1 y 1 ≤ s ≤ q-1
Si no se cumple, rechazar
```

**Paso 1:** Calcular w
```
z = H(M) mod q
w = s⁻¹ mod q
```

**Paso 2:** Calcular escalares
```
u₁ = z·w mod q
u₂ = r·w mod q
```

**Paso 3:** Calcular punto X
```
X = u₁·G + u₂·Q
Si X = O (infinito), rechazar
```

**Paso 4:** Verificar igualdad
```
Extraer x_X (coordenada x de X)
Verificar: x_X ≡ r (mod q)
```

**Salida:** VÁLIDA si x_X = r, INVÁLIDA en caso contrario

### ¿Por Qué Funciona?

Si la firma es válida, entonces:

```
X = u₁·G + u₂·Q
  = (z·w)·G + (r·w)·Q
  = (z·s⁻¹)·G + (r·s⁻¹)·(d·G)
  = s⁻¹·(z·G + r·d·G)
  = s⁻¹·(z + rd)·G
```

Pero de la firma sabemos que:
```
s = k⁻¹(z + rd) mod q
Por lo tanto: (z + rd) = k·s mod q
```

Sustituyendo:
```
X = s⁻¹·k·s·G = k·G = R
```

Por lo tanto, x_X = x_R = r ✓

---

## Preguntas Frecuentes

### ¿Es segura esta implementación para uso real?

**No.** Esta es una implementación educativa. Para uso en producción:
- La curva p=11 es muy pequeña (puede romperse fácilmente)
- Falta protección contra ataques de canal lateral
- Usa curvas estándar como secp256k1 o P-256

### ¿Puedo usar curvas más grandes?

Sí, puedes configurar curvas personalizadas en la pestaña correspondiente. Sin embargo, curvas muy grandes pueden hacer que los cálculos sean lentos.

### ¿Qué pasa si pierdo mi llave privada?

No podrás firmar mensajes nuevos. Es como perder la contraseña de tu cuenta. Recomendación: exporta tu llave privada y guárdala en lugar seguro.

### ¿Puedo compartir mi llave privada?

**¡NUNCA!** Si alguien obtiene tu llave privada, puede firmar mensajes haciéndose pasar por ti.

### ¿Qué pasa si dos mensajes diferentes producen el mismo hash?

Esto se llama "colisión de hash" y es extremadamente improbable con SHA-256 (la probabilidad es menor que 1 en 2²⁵⁶). Si ocurriera, ambos mensajes tendrían la misma firma.

### ¿Por qué la curva de ejemplo usa p=11?

Es un primo pequeño ideal para aprendizaje. Permite hacer los cálculos a mano y entender el algoritmo sin usar computadora.

### ¿Cómo sé que un punto está en la curva?

Sustituye las coordenadas en la ecuación:
```
y² ≡ x³ + ax + b (mod p)
```

Por ejemplo, para (6, 1) en la curva y² = x³ + x + 10 (mod 11):
```
Izquierda: 1² = 1
Derecha: 6³ + 6 + 10 = 216 + 6 + 10 = 232 ≡ 1 (mod 11) ✓
```

### ¿Qué es el "punto en el infinito"?

Es un punto especial (O) que actúa como el elemento identidad en la suma de puntos:
- P + O = P
- P + (-P) = O

Es análogo al 0 en la suma de números.

### ¿Cómo se suma puntos en la curva?

Para P + Q:
1. Trazar línea por P y Q
2. Encontrar tercer punto de intersección R'
3. Reflejar R' respecto al eje x → R
4. R = P + Q

Casos especiales:
- Si P = Q: usar la tangente (duplicación)
- Si P = -Q: resultado es O

### ¿Por qué usar curvas elípticas en vez de RSA?

Ventajas de ECDSA:
- Llaves más cortas con igual seguridad
- Firmas más pequeñas
- Operaciones más rápidas
- Menor uso de memoria

Ejemplo: ECDSA con 256 bits ≈ RSA con 3072 bits

---

## Recursos Adicionales

### Para Aprender Más

1. **Libros:**
   - "Understanding Cryptography" - Christof Paar
   - "Introduction to Modern Cryptography" - Katz & Lindell

2. **Cursos Online:**
   - Coursera: Cryptography I (Stanford)
   - Khan Academy: Journey into Cryptography

3. **Estándares:**
   - FIPS 186-4: Digital Signature Standard
   - SEC 2: Recommended Elliptic Curve Domain Parameters

### Curvas Estándar

Para uso real, considera estas curvas:

**secp256k1** (Bitcoin, Ethereum)
- p = 2²⁵⁶ - 2³² - 977
- Ampliamente probada

**P-256** (NIST)
- También llamada secp256r1
- Recomendada por NIST

**Curve25519** (Ed25519)
- Diseñada para velocidad y seguridad
- Resistente a ataques de canal lateral

---

## Soporte

Para preguntas o reportar problemas:
1. Revisa este manual
2. Consulta el archivo README.md
3. Revisa los ejemplos en la carpeta `examples/`

---

**¡Disfruta aprendiendo sobre criptografía de curvas elípticas!**

Betito, Alicia y Candy 🔐
