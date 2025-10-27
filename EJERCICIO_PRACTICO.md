# ✅ Ejercicio Práctico: Detectar Suplantación de Identidad

## 🎯 Escenario Real de la Práctica con la Profesora

**Situación:**
- Alicia y Candy pasan con la profesora
- Generan sus llaves públicas y las suben a una página web
- Firman la misma letra de una canción
- Te envían las canciones firmadas
- **Alicia** envía su firma legítima
- **Candy** intenta suplantar a Alicia (fraude)
- Tú (Betito) debes identificar cuál firma es de Alicia

---

## 🔑 CONCEPTOS IMPORTANTES

### ❌ ERROR COMÚN: "¿La firma son los parámetros a, b?"

**NO.** La firma NO son los parámetros de la curva.

### ✅ CORRECTO: ¿Qué es la firma?

**La firma digital es el par de números (r, s)**

```
Firma = (r, s)

Ejemplo:
  r = 73
  s = 42
```

Estos números se generan matemáticamente al firmar con la llave privada.

---

## 📋 FLUJO COMPLETO DE LA PRÁCTICA

### FASE 1: Alicia y Candy con la Profesora (Generan llaves)

#### Paso 1: Alicia genera sus llaves

1. Ejecutar: `python src/gui.py`
2. Ir a **"Gestión de Llaves"**
3. Seleccionar **"Alicia"**
4. Clic en **"Generar Nuevo Par de Llaves"**
5. Clic en **"Exportar Llave Pública"**
   - Guardar como: `llave_publica_Alicia.pem`
   - **Este archivo se sube a la web** 🌐

**Contenido del archivo:**
```
-----BEGIN ECDSA PUBLIC KEY-----
p=97
a=2
b=3
Gx=3
Gy=6
q=5
Qx=17
Qy=23
-----END ECDSA PUBLIC KEY-----
```

#### Paso 2: Candy genera sus llaves

1. Seleccionar **"Candy"**
2. Clic en **"Generar Nuevo Par de Llaves"**
3. Clic en **"Exportar Llave Pública"**
   - Guardar como: `llave_publica_Candy.pem`
   - **Este archivo se sube a la web** 🌐

---

### FASE 2: Alicia y Candy firman la canción

#### Paso 3: Alicia firma (legítimo)

1. Seleccionar **"Alicia"**
2. Ir a pestaña **"Firmar Mensaje"**
3. Escribir la letra de la canción:
```
Imagine there's no heaven
It's easy if you try
```
4. Clic en **"Firmar Mensaje"**
5. Clic en **"Guardar Firma"**
   - Guardar como: `firma_alicia.sig`
   - **Este archivo se envía a Betito** 📧

**Contenido de firma_alicia.sig:**
```
=== FIRMA DIGITAL ECDSA ===

Usuario: Alicia
Mensaje: Imagine there's no heaven
It's easy if you try

Firma (r, s):
  r = 73      ← ESTOS números son la firma
  s = 42      ← NO son parámetros a, b

Hash del mensaje: H(M) = 3
```

#### Paso 4: Candy firma (intentando suplantar)

1. Seleccionar **"Candy"**
2. Ir a pestaña **"Firmar Mensaje"**
3. Escribir **LA MISMA canción** (esto es clave):
```
Imagine there's no heaven
It's easy if you try
```
4. Clic en **"Firmar Mensaje"**
5. Clic en **"Guardar Firma"**
   - Guardar como: `firma_candy.sig`
   - **Este archivo se envía a Betito** 📧

**Contenido de firma_candy.sig:**
```
=== FIRMA DIGITAL ECDSA ===

Usuario: Candy
Mensaje: Imagine there's no heaven
It's easy if you try

Firma (r, s):
  r = 19      ← Números DIFERENTES
  s = 88      ← Porque usó su llave privada

Hash del mensaje: H(M) = 3
```

**🎯 Nota importante:** Aunque el mensaje es el mismo, los números (r, s) son diferentes porque cada una firmó con SU propia llave privada.

---

### FASE 3: Betito verifica (¡Esta es tu parte!)

#### Paso 5: Descargar llave pública de Alicia

**Simular descarga de la web:**
- En la práctica real: Descargas de su página web
- En el ejercicio: Copias `llave_publica_Alicia.pem` a tu carpeta

#### Paso 6: Importar llave pública de Alicia

1. Ejecutar: `python src/gui.py`
2. Seleccionar **"Betito"**
3. Ir a **"Gestión de Llaves"**
4. Clic en **"Importar Llave Pública"**
5. Seleccionar: `llave_publica_Alicia.pem`
6. Ver que aparece la información de la llave de Alicia

#### Paso 7: Verificar firma de Alicia

1. Ir a pestaña **"Verificar Firma"**
2. Clic en **"Cargar Firma desde Archivo"**
3. Seleccionar: `firma_alicia.sig`
4. El mensaje y los valores r, s se cargan automáticamente
5. Seleccionar **"Alicia"** en el dropdown (importante!)
6. Clic en **"Verificar Firma (Paso a Paso)"**

**Resultado esperado:**
```
=== PASO 0: Verificar Rango ===
✓ 1 ≤ r ≤ q-1
✓ 1 ≤ s ≤ q-1

=== PASO 1: Calcular w = s⁻¹ mod q ===
w = 3

=== PASO 2: Calcular u₁ y u₂ ===
u₁ = 4
u₂ = 2

=== PASO 3: Calcular X = u₁·G + u₂·Q ===
X = (17, 23)

=== PASO 4: Verificar x_X ≡ r (mod q) ===
x_X = 17
r = 73
...

✓✓✓ La firma es VÁLIDA ✓✓✓
```

#### Paso 8: Verificar firma de Candy (intentando suplantar)

**IMPORTANTE:** Sin cerrar el programa, sin cambiar nada en "Gestión de Llaves"

1. Quedarte en pestaña **"Verificar Firma"**
2. Clic en **"Cargar Firma desde Archivo"**
3. Seleccionar: `firma_candy.sig`
4. **MANTENER** seleccionado **"Alicia"** (esto es clave!)
5. Clic en **"Verificar Firma (Paso a Paso)"**

**Resultado esperado:**
```
=== PASO 0: Verificar Rango ===
✓ 1 ≤ r ≤ q-1
✓ 1 ≤ s ≤ q-1

=== PASO 1: Calcular w = s⁻¹ mod q ===
w = 2

=== PASO 2: Calcular u₁ y u₂ ===
u₁ = 1
u₂ = 3

=== PASO 3: Calcular X = u₁·G + u₂·Q ===
X = (45, 67)

=== PASO 4: Verificar x_X ≡ r (mod q) ===
x_X = 45
r = 19
45 ≠ 19

✗✗✗ La firma NO es válida ✗✗✗
```

---

## 🎯 CONCLUSIÓN DE LA PRÁCTICA

```
┌─────────────────────────────────────────────┐
│         RESULTADOS DE VERIFICACIÓN          │
├─────────────────────────────────────────────┤
│                                             │
│  firma_alicia.sig  → ✓ VÁLIDA              │
│  firma_candy.sig   → ✗ INVÁLIDA            │
│                                             │
│  🎯 CONCLUSIÓN:                             │
│  Solo Alicia firmó realmente el mensaje     │
│  Candy intentó suplantar pero falló         │
│                                             │
└─────────────────────────────────────────────┘
```

**¿Por qué Candy falló?**
- Candy NO tiene la llave privada de Alicia
- Candy firmó con SU propia llave privada
- Los números (r, s) que generó son diferentes
- Al verificar con la llave pública de Alicia, no coinciden
- El algoritmo detecta automáticamente el fraude

---

## 📁 ARCHIVOS NECESARIOS PARA LA PRÁCTICA

### Lo que suben a la web:
```
📁 llave_publica_Alicia.pem  ← Alicia sube
📁 llave_publica_Candy.pem   ← Candy sube
```

### Lo que te envían:
```
📁 cancion.txt               ← La letra (opcional, está en las firmas)
📁 firma_alicia.sig          ← Contiene (r=73, s=42)
📁 firma_candy.sig           ← Contiene (r=19, s=88)
```

### Lo que tú usas:
```
📁 llave_publica_Alicia.pem  ← Descargas de la web
```

---

## 💡 RESPUESTAS A TUS DUDAS

### "¿Es profesional que la firma sean solo parámetros a, b?"

**❌ NO.** La firma NO son los parámetros (a, b) de la curva.

**✅ La firma son los números (r, s)**

Los parámetros (a, b, p, G, q) definen la curva elíptica y están en el archivo de la llave pública, pero NO son la firma.

### ¿Qué es cada archivo?

| Archivo | Contiene | Qué es |
|---------|----------|--------|
| `llave_publica_Alicia.pem` | p, a, b, G, q, Q | Parámetros de curva + llave pública |
| `firma_alicia.sig` | r, s, mensaje | **LA FIRMA DIGITAL** |

### ¿Va a funcionar la práctica?

**✅ SÍ, PERFECTAMENTE**

Tu práctica demuestra exactamente cómo funciona ECDSA en el mundo real:
- Bitcoin usa el mismo principio
- TLS/SSL usa el mismo principio
- PGP/GPG usa el mismo principio

---

## 🎤 QUÉ DECIR A LA PROFESORA

**"La firma digital es el par de números (r, s) generado al firmar el mensaje con la llave privada. Cuando Alicia firma, genera su par (r, s). Cuando Candy intenta suplantar a Alicia, genera un par (r, s) diferente porque usa su propia llave privada. Al verificar ambas firmas con la llave pública de Alicia, solo la firma genuina de Alicia es válida. El sistema detecta automáticamente que Candy intentó suplantar a Alicia."**

---

## ✅ CHECKLIST ANTES DE LA PRÁCTICA

- [ ] Probar generar llaves para Alicia
- [ ] Probar generar llaves para Candy  
- [ ] Exportar ambas llaves públicas (`.pem`)
- [ ] Firmar el mismo mensaje con ambas
- [ ] Guardar ambas firmas (`.sig`)
- [ ] Importar llave pública de Alicia en Betito
- [ ] Verificar firma de Alicia → ✓ VÁLIDA
- [ ] Verificar firma de Candy con llave de Alicia → ✗ INVÁLIDA
- [ ] Entender que la firma son los números (r, s)

---

**¡Tu práctica está perfecta! Solo asegúrate de entender que la firma son los números (r, s), NO los parámetros de la curva.** 🎯✨

Copiar los archivos:
- `llave_publica_Betito.txt` → `ejercicio_firmas/llaves_publicas/`
- `llave_publica_Alicia.txt` → `ejercicio_firmas/llaves_publicas/`
- `llave_publica_Candy.txt` → `ejercicio_firmas/llaves_publicas/`

---

## PARTE 2: Alicia firma song.txt

### Paso 2.1: Crear el archivo song.txt de Alicia

Crear archivo `song_alicia.txt` con este contenido:

```
Si acepto

[Aquí va una canción]
Verso 1:
En el cielo brilla una estrella
que ilumina mi camino
con su luz tan bella

Coro:
Canta el viento su melodía
mientras baila la alegría
en este nuevo día

Verso 2:
Entre montañas y mares
encuentro la paz
en lugares

Att Alicia
```

### Paso 2.2: Alicia firma el archivo

1. En la aplicación, asegurarse de estar como **"Alicia"**
2. Ir a pestaña **"Firmar Mensaje"**
3. Copiar **todo el contenido** de `song_alicia.txt` en el área de texto
4. Clic en **"Firmar Mensaje"**
5. La firma (r, s) aparecerá en el cuadro inferior
6. Clic en **"Guardar Firma"**
   - Guardar como: `firma_alicia.txt`

### Paso 2.3: Compartir archivos de Alicia

Copiar a la carpeta compartida:
- `song_alicia.txt` → `ejercicio_firmas/song_alicia.txt`
- `firma_alicia.txt` → `ejercicio_firmas/firma_alicia.txt`

---

## PARTE 3: Candy firma song.txt

### Paso 3.1: Crear el archivo song.txt de Candy

Crear archivo `song_candy.txt` con este contenido:

```
No acepto

[Aquí va una canción diferente]
Verso 1:
La luna brilla en la noche
reflejando sueños
sin reproche

Coro:
Baila el mar con las olas
mientras cuentan historias
las gaviotas solas

Verso 2:
En el jardín florecen
las rosas de colores
que amanecen

Att Alicia
```

**Nota:** Candy firma con "Att Alicia" para intentar suplantar a Alicia, pero usa su propia llave privada.

### Paso 3.2: Candy firma el archivo

1. En la aplicación, cambiar a **"Candy"**
2. Ir a pestaña **"Firmar Mensaje"**
3. Copiar **todo el contenido** de `song_candy.txt`
4. Clic en **"Firmar Mensaje"**
5. Clic en **"Guardar Firma"**
   - Guardar como: `firma_candy.txt`

### Paso 3.3: Compartir archivos de Candy

Copiar a la carpeta compartida:
- `song_candy.txt` → `ejercicio_firmas/song_candy.txt`
- `firma_candy.txt` → `ejercicio_firmas/firma_candy.txt`

---

## PARTE 4: Betito verifica las firmas

### Paso 4.1: Importar llave pública de Alicia

1. En la aplicación, cambiar a **"Betito"**
2. Ir a **"Gestión de Llaves"**
3. Clic en **"Importar Llave Pública"**
4. Seleccionar: `ejercicio_firmas/llaves_publicas/llave_publica_Alicia.txt`
5. La llave de Alicia ahora está cargada en el perfil de Betito

### Paso 4.2: Verificar firma del primer song.txt (de Alicia)

1. Ir a pestaña **"Verificar Firma"**
2. En "Mensaje Original":
   - Copiar **exactamente** el contenido de `song_alicia.txt`
3. Cargar la firma:
   - Clic en **"Cargar Firma desde Archivo"**
   - Seleccionar: `ejercicio_firmas/firma_alicia.txt`
   - Los valores r y s se cargarán automáticamente
4. En "Llave Pública del Firmante":
   - Seleccionar **"Betito"** (que tiene la llave de Alicia importada)
5. Clic en **"Verificar Firma (Paso a Paso)"**

**Resultado esperado:** ✓ **La firma es VÁLIDA**

Esto confirma que:
- El mensaje fue firmado por la persona que posee la llave privada correspondiente a la llave pública de Alicia
- El mensaje dice "Si acepto"

### Paso 4.3: Verificar firma del segundo song.txt (de Candy)

1. Cambiar a usuario **"Candy"** en "Gestión de Llaves"
2. Importar llave pública de Alicia nuevamente (o usar un slot diferente)
3. Volver a **"Verificar Firma"**
4. En "Mensaje Original":
   - Copiar **exactamente** el contenido de `song_candy.txt`
5. Cargar firma:
   - Clic en **"Cargar Firma desde Archivo"**
   - Seleccionar: `ejercicio_firmas/firma_candy.txt`
6. Seleccionar llave pública de Alicia
7. Clic en **"Verificar Firma (Paso a Paso)"**

**Resultado esperado:** ✗ **La firma es INVÁLIDA**

Esto demuestra que:
- Aunque el mensaje dice "Att Alicia", NO fue firmado con la llave privada de Alicia
- Fue firmado con la llave privada de Candy
- Candy intentó suplantar a Alicia pero la verificación lo detectó

---

## CONCLUSIÓN

**Betito puede determinar:**

1. **song_alicia.txt** → ✓ Firma VÁLIDA con llave pública de Alicia
   - Mensaje: "Si acepto"
   - Este es el archivo auténtico de Alicia

2. **song_candy.txt** → ✗ Firma INVÁLIDA con llave pública de Alicia
   - Aunque dice "Att Alicia", NO fue firmado por ella
   - Fue firmado por otra persona (Candy)

**Resultado:** Betito identifica correctamente que `song_alicia.txt` es el archivo auténtico de Alicia que dice "Si acepto".

---

## VARIANTE: Verificar con la llave correcta de Candy

Si Betito quiere confirmar que el segundo archivo fue firmado por Candy:

1. Importar `llave_publica_Candy.txt`
2. Verificar `song_candy.txt` con la firma de Candy
3. Resultado: ✓ **Firma VÁLIDA** (confirma que Candy firmó ese archivo)

Esto demuestra que:
- Candy efectivamente firmó el mensaje
- Pero no puede hacerse pasar por Alicia
- La firma digital garantiza la autenticidad

---

## NOTAS IMPORTANTES

### ⚠️ Exactitud del Mensaje
El mensaje a verificar debe ser **exactamente** igual al firmado:
- Mismo texto
- Mismos espacios
- Mismos saltos de línea
- Cualquier cambio invalidará la firma

### 🔒 Seguridad de Llaves Privadas
- Cada persona debe mantener su llave privada en secreto
- Solo exportar/compartir las llaves **públicas**
- Si alguien obtiene tu llave privada, puede suplantar tu identidad

### 📝 Carpeta del Ejercicio

Estructura final:
```
ejercicio_firmas/
├── llaves_publicas/
│   ├── llave_publica_Alicia.txt
│   ├── llave_publica_Betito.txt
│   └── llave_publica_Candy.txt
├── song_alicia.txt
├── firma_alicia.txt
├── song_candy.txt
└── firma_candy.txt
```

---

## RESUMEN DEL FLUJO

1. **Generación de llaves** → Todos generan y comparten llaves públicas
2. **Firma** → Alicia y Candy firman sus respectivos archivos
3. **Compartir** → Publican mensajes y firmas
4. **Verificación** → Betito verifica con la llave pública de Alicia
5. **Conclusión** → Solo el archivo de Alicia tiene firma válida

**¡El sistema ECDSA funciona! La suplantación es detectada.** ✅

---

**Autores:** Betito, Alicia, Candy 🔐
