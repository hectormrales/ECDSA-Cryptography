# 🔬 DEMOSTRACIÓN MATEMÁTICA: Verificación de Firmas ECDSA

## 📋 Índice
1. [Resumen del Proceso](#resumen)
2. [Demostración Paso a Paso](#demostracion)
3. [Propiedades Clave de Curvas Elípticas](#propiedades)
4. [Ejemplo Numérico Completo](#ejemplo)
5. [Conclusión](#conclusion)

---

## 🎯 Resumen del Proceso {#resumen}

### Parámetros del Sistema
- **Curva Elíptica:** $E: y^2 = x^3 + ax + b \pmod{p}$
- **Punto Generador:** $G$ (orden $q$)
- **Llave Privada:** $d$ (entero secreto, $1 \leq d < q$)
- **Llave Pública:** $Q = d \cdot G$ (punto en la curva)

### Proceso de Firma

**Firmar un mensaje $M$:**
1. Calcular $h = H(M)$ (hash del mensaje)
2. Generar $k$ aleatorio ($1 \leq k < q$)
3. Calcular $P = k \cdot G = (x_P, y_P)$
4. $r = x_P \bmod q$
5. $s = k^{-1}(h + rd) \bmod q$
6. **Firma:** $(r, s)$

### Proceso de Verificación

**Verificar firma $(r, s)$ del mensaje $M$:**
1. Calcular $h = H(M)$
2. Calcular $w = s^{-1} \bmod q$
3. Calcular $u_1 = hw \bmod q$
4. Calcular $u_2 = rw \bmod q$
5. Calcular $P' = u_1 \cdot G + u_2 \cdot Q$
6. **Verificar:** $x_{P'} \equiv r \pmod{q}$

---

## 🧮 DEMOSTRACIÓN: ¿Por qué $P' = P$? {#demostracion}

### 📝 Teorema a Demostrar

> **Si la firma $(r, s)$ fue generada correctamente con la llave privada $d$, entonces el punto $P'$ calculado en la verificación es igual al punto $P$ usado en la firma.**

### 🔍 Demostración Paso a Paso

#### **Paso 1: Expandir $P'$**

Por definición de verificación:
$$P' = u_1 \cdot G + u_2 \cdot Q$$

Sustituimos $u_1$ y $u_2$:
$$P' = (hw) \cdot G + (rw) \cdot Q$$

donde $w = s^{-1} \bmod q$

#### **Paso 2: Sustituir la Llave Pública**

Sabemos que $Q = d \cdot G$, entonces:
$$P' = (hw) \cdot G + (rw) \cdot (d \cdot G)$$

#### **Paso 3: Aplicar Propiedad Distributiva**

Por la propiedad asociativa de la multiplicación escalar en curvas elípticas:
$$P' = (hw) \cdot G + (rwd) \cdot G$$

Factorizamos $G$:
$$P' = (hw + rwd) \cdot G$$
$$P' = w(h + rd) \cdot G$$

#### **Paso 4: Sustituir $w = s^{-1}$**

$$P' = s^{-1}(h + rd) \cdot G$$

#### **Paso 5: Usar la Definición de $s$**

De la firma sabemos que:
$$s = k^{-1}(h + rd) \bmod q$$

Multiplicando ambos lados por $k$:
$$ks = h + rd \bmod q$$

Por lo tanto:
$$h + rd = ks \bmod q$$

#### **Paso 6: Sustituir en $P'$**

$$P' = s^{-1}(ks) \cdot G$$
$$P' = s^{-1} \cdot s \cdot k \cdot G$$

#### **Paso 7: Simplificar**

Como $s^{-1} \cdot s = 1 \bmod q$:
$$P' = k \cdot G$$

#### **Paso 8: Conclusión**

Pero $P = k \cdot G$ por definición en la firma, entonces:

$$\boxed{P' = P}$$

Por lo tanto:
$$\boxed{x_{P'} = x_P = r}$$

**¡La verificación funciona!** ✅

---

## 🔑 Propiedades Clave de Curvas Elípticas {#propiedades}

La demostración anterior se basa en estas propiedades fundamentales:

### 1. **Multiplicación Escalar**

Para un punto $P$ en la curva y un escalar $k$:
$$k \cdot P = \underbrace{P + P + \cdots + P}_{k \text{ veces}}$$

**Ejemplo:**
- $2 \cdot G = G + G$
- $3 \cdot G = G + G + G$

### 2. **Propiedad Asociativa**

$$(k_1 + k_2) \cdot P = k_1 \cdot P + k_2 \cdot P$$

**Ejemplo:**
$$(3 + 2) \cdot G = 5 \cdot G = 3 \cdot G + 2 \cdot G$$

### 3. **Propiedad Conmutativa**

$$k_1 \cdot (k_2 \cdot P) = k_2 \cdot (k_1 \cdot P) = (k_1 k_2) \cdot P$$

**Ejemplo:**
$$2 \cdot (3 \cdot G) = 3 \cdot (2 \cdot G) = 6 \cdot G$$

### 4. **Inversos Modulares**

Si $s \cdot w \equiv 1 \pmod{q}$, entonces $w = s^{-1}$

**Ejemplo:** Si $s = 3$ y $q = 5$:
- $s^{-1} = 2$ porque $3 \cdot 2 = 6 \equiv 1 \pmod{5}$

### 5. **Problema del Logaritmo Discreto**

Dado $Q = d \cdot G$, es computacionalmente imposible encontrar $d$:
- **Fácil:** $Q = d \cdot G$ (multiplicación)
- **Difícil:** Encontrar $d$ dado $Q$ y $G$ (logaritmo discreto)

Esta propiedad garantiza la **seguridad** del esquema.

---

## 📊 Ejemplo Numérico Completo {#ejemplo}

Usemos los parámetros de tu proyecto:

### Parámetros de la Curva
- **Curva:** $y^2 = x^3 + 2x + 3 \pmod{97}$
- **Generador:** $G = (3, 6)$
- **Orden:** $q = 5$
- **Llave Privada:** $d = 2$
- **Llave Pública:** $Q = 2 \cdot G$

### Calcular Llave Pública

$Q = 2 \cdot G = G + G$

Usando las fórmulas de suma de puntos en la curva:

$$Q = (80, 10)$$

### Firma del Mensaje "Hola"

**1. Hash del mensaje:**
$$h = H(\text{"Hola"}) \bmod 5 = 3$$

**2. Generar $k$ aleatorio:**
$$k = 4$$

**3. Calcular $P = k \cdot G$:**
$$P = 4 \cdot G = (80, 87)$$

**4. Calcular $r$:**
$$r = x_P \bmod q = 80 \bmod 5 = 0$$

⚠️ Si $r = 0$, se rechaza y se elige otro $k$. 

**Probemos con $k = 3$:**

$$P = 3 \cdot G = (80, 10)$$
$$r = 80 \bmod 5 = 0$$

**Probemos con $k = 1$:**

$$P = 1 \cdot G = (3, 6)$$
$$r = 3 \bmod 5 = 3$$

**5. Calcular $s$:**

Primero necesitamos $k^{-1} \bmod 5$:
- $k = 1$, entonces $k^{-1} = 1$

$$s = k^{-1}(h + rd) \bmod q$$
$$s = 1 \cdot (3 + 3 \cdot 2) \bmod 5$$
$$s = 1 \cdot (3 + 6) \bmod 5$$
$$s = 9 \bmod 5 = 4$$

**Firma generada:** $(r, s) = (3, 4)$

---

### Verificación de la Firma

**1. Hash del mensaje:**
$$h = 3$$ (mismo que antes)

**2. Calcular $w = s^{-1} \bmod q$:**

Necesitamos encontrar $w$ tal que $4w \equiv 1 \pmod{5}$

$$4 \cdot 4 = 16 \equiv 1 \pmod{5}$$

Por lo tanto: $w = 4$

**3. Calcular $u_1$:**
$$u_1 = hw \bmod q = 3 \cdot 4 \bmod 5 = 12 \bmod 5 = 2$$

**4. Calcular $u_2$:**
$$u_2 = rw \bmod q = 3 \cdot 4 \bmod 5 = 12 \bmod 5 = 2$$

**5. Calcular $P'$:**
$$P' = u_1 \cdot G + u_2 \cdot Q$$
$$P' = 2 \cdot G + 2 \cdot Q$$
$$P' = 2 \cdot (3, 6) + 2 \cdot (80, 10)$$

Necesitamos calcular estos puntos:
- $2 \cdot G = (80, 10)$
- $2 \cdot Q = 2 \cdot (80, 10) = (3, 91)$

$$P' = (80, 10) + (3, 91)$$

Usando fórmulas de suma de puntos:
$$P' = (3, 6)$$

**6. Verificar:**
$$x_{P'} = 3$$
$$r = 3$$

$$\boxed{x_{P'} = r \quad \checkmark}$$

**¡La firma es VÁLIDA!** ✅

---

### Verificación Algebraica Paso a Paso

Verifiquemos matemáticamente que $P' = P$:

$$P' = u_1 \cdot G + u_2 \cdot Q$$
$$P' = 2 \cdot G + 2 \cdot (2 \cdot G)$$
$$P' = 2 \cdot G + 4 \cdot G$$
$$P' = 6 \cdot G$$
$$P' = (6 \bmod 5) \cdot G = 1 \cdot G$$
$$P' = G = (3, 6)$$

Y de la firma:
$$P = k \cdot G = 1 \cdot G = (3, 6)$$

$$\boxed{P' = P = (3, 6)} \quad \checkmark$$

---

## 🎓 Demostración Alternativa (Más Formal) {#alternativa}

### Lema 1: Ley de Grupo en Curvas Elípticas

Los puntos de una curva elíptica forman un **grupo abeliano** bajo la operación de suma de puntos:

1. **Clausura:** Si $P, Q \in E$, entonces $P + Q \in E$
2. **Asociativa:** $(P + Q) + R = P + (Q + R)$
3. **Identidad:** Existe $\mathcal{O}$ (punto al infinito) tal que $P + \mathcal{O} = P$
4. **Inversos:** Para cada $P$ existe $-P$ tal que $P + (-P) = \mathcal{O}$
5. **Conmutativa:** $P + Q = Q + P$

### Lema 2: Homomorfismo de Multiplicación Escalar

La función $\phi_k: E \to E$ definida por $\phi_k(P) = k \cdot P$ es un homomorfismo de grupo:

$$\phi_k(P + Q) = \phi_k(P) + \phi_k(Q)$$
$$k(P + Q) = kP + kQ$$

### Teorema Principal: Corrección de ECDSA

**Enunciado:** 
> Si $(r, s)$ es una firma válida del mensaje $M$ con llave privada $d$, entonces la verificación con llave pública $Q = d \cdot G$ producirá $x_{P'} = r$.

**Demostración:**

Por definición de verificación:
$$P' = u_1 \cdot G + u_2 \cdot Q \quad \text{donde } u_1 = hs^{-1}, u_2 = rs^{-1}$$

Sustituyendo $Q = d \cdot G$:
$$P' = u_1 \cdot G + u_2 \cdot (d \cdot G)$$

Por el Lema 2 (homomorfismo):
$$P' = u_1 \cdot G + (u_2 d) \cdot G$$
$$P' = (u_1 + u_2 d) \cdot G$$

Sustituyendo $u_1$ y $u_2$:
$$P' = (hs^{-1} + rs^{-1}d) \cdot G$$
$$P' = s^{-1}(h + rd) \cdot G$$

De la firma sabemos que $s = k^{-1}(h + rd)$, entonces:
$$s^{-1} = k(h + rd)^{-1}$$

Pero también podemos escribir:
$$h + rd = ks$$

Por lo tanto:
$$P' = s^{-1}(ks) \cdot G = (s^{-1}s)k \cdot G = k \cdot G$$

Como $P = k \cdot G$ en la firma:
$$P' = P$$

Por lo tanto:
$$x_{P'} = x_P = r \quad \square$$

---

## 🔐 ¿Por qué es Seguro? {#seguridad}

### 1. **Problema del Logaritmo Discreto (DLP)**

Dado $Q = d \cdot G$, encontrar $d$ es computacionalmente imposible para curvas bien elegidas.

**Complejidad:** $O(\sqrt{q})$ con el mejor algoritmo conocido (Pollard's rho)

Para $q \approx 2^{256}$: $\sqrt{q} \approx 2^{128}$ operaciones (inviable)

### 2. **Aleatoriedad de $k$**

Cada firma usa un $k$ diferente y aleatorio:
- Si se reutiliza $k$, se puede recuperar la llave privada $d$
- Si $k$ es predecible, se puede recuperar $d$

**Ejemplo de ataque con $k$ reutilizado:**

Si dos mensajes $M_1, M_2$ se firman con el mismo $k$:
- $s_1 = k^{-1}(h_1 + rd)$
- $s_2 = k^{-1}(h_2 + rd)$

Entonces:
$$k = \frac{h_1 - h_2}{s_1 - s_2} \bmod q$$

Y con $k$, se puede recuperar $d$:
$$d = \frac{ks_1 - h_1}{r} \bmod q$$

### 3. **Hash Criptográfico**

El hash $h = H(M)$ debe ser:
- **Resistente a colisiones:** Difícil encontrar $M_1 \neq M_2$ con $H(M_1) = H(M_2)$
- **Preimagen:** Dado $h$, difícil encontrar $M$ tal que $H(M) = h$
- **Avalancha:** Cambio pequeño en $M$ cambia completamente $h$

---

## 📐 Propiedades Geométricas {#geometria}

### Suma de Puntos en la Curva

Para sumar dos puntos $P = (x_1, y_1)$ y $Q = (x_2, y_2)$:

**Caso 1: $P \neq Q$ (suma)**

$$\lambda = \frac{y_2 - y_1}{x_2 - x_1} \bmod p$$

$$x_3 = \lambda^2 - x_1 - x_2 \bmod p$$
$$y_3 = \lambda(x_1 - x_3) - y_1 \bmod p$$

$$P + Q = (x_3, y_3)$$

**Caso 2: $P = Q$ (duplicación)**

$$\lambda = \frac{3x_1^2 + a}{2y_1} \bmod p$$

$$x_3 = \lambda^2 - 2x_1 \bmod p$$
$$y_3 = \lambda(x_1 - x_3) - y_1 \bmod p$$

$$2P = (x_3, y_3)$$

### Interpretación Geométrica

La suma de puntos tiene una interpretación geométrica:
1. Trazar línea entre $P$ y $Q$
2. Encontrar tercer punto de intersección $R$ con la curva
3. Reflejar $R$ sobre eje $x$ para obtener $P + Q$

---

## 🧪 Verificación con tu Proyecto

Puedes verificar todo esto ejecutando:

```python
from src.ecdsa_core import *

# Crear curva
curva = crear_curva_ejemplo()
ecdsa = ECDSA(curva)

# Generar llaves
d = 2  # Llave privada
Q = curva.multiplicar_escalar(d, curva.G)

# Firmar
mensaje = "Hola"
r, s = ecdsa.firmar(mensaje, d)

# Verificar paso a paso
pasos = ecdsa.verificar_paso_a_paso(mensaje, (r, s), Q)

# Ver todos los pasos matemáticos
for paso in pasos.values():
    if 'titulo' in paso:
        print(f"\n{paso['titulo']}")
        print(paso.get('explicacion', ''))
```

---

## 🎯 Conclusión {#conclusion}

### Resumen de la Demostración

1. **Firma:** Se crea $s = k^{-1}(h + rd)$ usando la llave privada $d$
2. **Verificación:** Se calcula $P' = s^{-1}(h + rd) \cdot G$
3. **Simplificación:** $P' = s^{-1}(ks) \cdot G = k \cdot G = P$
4. **Resultado:** $x_{P'} = x_P = r$ ✅

### Propiedades Clave

| Propiedad | Función |
|-----------|---------|
| **Asociatividad** | Permite factorizar $(hw + rwd) \cdot G$ |
| **Conmutatividad** | Permite reordenar $u_1 \cdot G + u_2 \cdot Q$ |
| **Inversos Modulares** | $s \cdot s^{-1} = 1$ cancela términos |
| **Homomorfismo** | $k(P + Q) = kP + kQ$ permite distribuir |
| **DLP** | Hace imposible obtener $d$ desde $Q = d \cdot G$ |

### Seguridad

La seguridad de ECDSA se basa en:
- **DLP:** Problema del logaritmo discreto en curvas elípticas
- **Aleatoriedad:** $k$ único y aleatorio por cada firma
- **Hash:** SHA-256 u otro hash criptográfico robusto

### Aplicación Práctica

Tu proyecto implementa todo esto en:
- `src/ecdsa_core.py` - Matemática de curvas elípticas
- `src/gui.py` - Interfaz para firmar/verificar
- Tests - Verificación de corrección matemática

---

## 📚 Referencias

1. **NIST FIPS 186-4:** Digital Signature Standard (DSS)
2. **SEC 1:** Elliptic Curve Cryptography (Certicom)
3. **RFC 6979:** Deterministic Usage of DSA and ECDSA
4. **"Guide to Elliptic Curve Cryptography"** - Hankerson, Menezes, Vanstone

---

## 🔬 Ejercicio Propuesto

**Demuestra que si un atacante conoce dos firmas $(r, s_1)$ y $(r, s_2)$ del mismo mensaje pero con valores $s$ diferentes (error de implementación), puede recuperar la llave privada $d$.**

<details>
<summary>💡 Pista</summary>

Si $s_1 \neq s_2$ pero $r$ es igual, entonces se usaron valores $k_1 \neq k_2$ diferentes, pero ambos dieron el mismo $r$. Usa las ecuaciones:

$$s_1 = k_1^{-1}(h + rd)$$
$$s_2 = k_2^{-1}(h + rd)$$

Intenta eliminar $h$ y $d$ para encontrar una relación entre $k_1$ y $k_2$.
</details>

---

**¡Espero que esta demostración te ayude a entender profundamente cómo y por qué funciona ECDSA!** 🎓✨
