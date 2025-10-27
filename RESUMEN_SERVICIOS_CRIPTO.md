# 🎯 Resumen Rápido: Servicios Criptográficos

## Para usar en tu presentación o examen

---

## 🛡️ SERVICIOS CRIPTOGRÁFICOS

### ✅ 1. AUTENTICACIÓN
**¿Qué es?** Verificar la identidad del emisor

**¿Lo ofrece?** ✅ SÍ

**¿Por qué?**
- Solo quien tiene la llave privada puede firmar
- ECDLP hace imposible falsificar firmas
- La llave pública identifica al firmante

**Ejemplo:** Betito verifica que el mensaje es de Alicia, no de Candy

---

### ✅ 2. INTEGRIDAD
**¿Qué es?** Detectar modificaciones del mensaje

**¿Lo ofrece?** ✅ SÍ

**¿Por qué?**
- SHA-256 calcula hash del mensaje
- Hash se incluye en la firma: `s = k⁻¹(H(M) + r·d)`
- Cambiar 1 bit del mensaje → hash diferente → firma inválida

**Ejemplo:** Si atacante cambia "$100" por "$999", la firma falla

---

### ✅ 3. NO REPUDIO
**¿Qué es?** El firmante no puede negar haber firmado

**¿Lo ofrece?** ✅ SÍ

**¿Por qué?**
- Solo Alicia tiene su llave privada
- Solo ella puede crear firmas válidas
- La firma es prueba matemática
- Tiene valor legal

**Ejemplo:** Alicia no puede decir "yo no firmé ese contrato"

---

### ❌ 4. CONFIDENCIALIDAD
**¿Qué es?** Mantener el mensaje secreto

**¿Lo ofrece?** ❌ NO

**¿Por qué NO?**
- ECDSA FIRMA pero NO CIFRA
- El mensaje permanece en texto plano
- Cualquiera puede leerlo
- Solo prueba quién lo firmó

**Ejemplo:** Mensaje "Hola" es visible para todos

**Solución:** Combinar con AES o RSA para cifrar

---

### ❌ 5. ANONIMATO
**¿Qué es?** Ocultar quién firmó

**¿Lo ofrece?** ❌ NO

**¿Por qué NO?**
- La llave pública identifica al firmante
- Verificación requiere saber quién firmó

**Ejemplo:** Al verificar con Q_alicia, sabemos que Alicia firmó

---

## 📊 TABLA RÁPIDA

| Servicio | ✅/❌ | Razón Principal |
|----------|-------|-----------------|
| Autenticación | ✅ | Solo el dueño de llave privada puede firmar |
| Integridad | ✅ | Hash SHA-256 detecta modificaciones |
| No Repudio | ✅ | Firma no falsificable (ECDLP) |
| Confidencialidad | ❌ | ECDSA firma, NO cifra |
| Anonimato | ❌ | Llave pública identifica |

---

## 🎤 PARA TU PRESENTACIÓN

**Pregunta típica:** "¿Qué servicios de seguridad ofrece tu proyecto?"

**Respuesta modelo:**

> "El proyecto implementa firma digital ECDSA, que proporciona **tres servicios criptográficos principales:**
>
> 1. **Autenticación** - Verifica la identidad del firmante. Funciona porque solo quien posee la llave privada puede generar firmas válidas, y el problema ECDLP hace imposible falsificarlas.
>
> 2. **Integridad** - Detecta cualquier modificación del mensaje. Funciona porque calculamos SHA-256 del mensaje e incluimos este hash dentro de la firma. Si el mensaje cambia, el hash cambia y la firma se invalida.
>
> 3. **No repudio** - El firmante no puede negar haber firmado. Funciona porque la firma es una prueba matemática que solo pudo ser creada con la llave privada del firmante.
>
> **NO proporciona confidencialidad** porque ECDSA es un esquema de firma, no de cifrado. El mensaje permanece en texto plano. Si necesitáramos confidencialidad, deberíamos combinar ECDSA con un algoritmo de cifrado como AES."

---

## 💡 EJEMPLOS CONCRETOS

### Autenticación ✅
```
Alicia firma: "Hola"
Candy intenta suplantar: firma con su llave
Betito verifica con llave de Alicia
→ Firma de Candy FALLA
→ Sistema detecta que NO es Alicia
```

### Integridad ✅
```
Mensaje: "Pagar $100"
Firma: (r, s)
Atacante modifica: "Pagar $999"
Verificación: FALLA
→ Sistema detecta la alteración
```

### No Repudio ✅
```
Alicia firma contrato
Luego niega: "Yo no firmé"
Pero firma es verificable matemáticamente
→ Prueba que SÍ firmó
```

### Confidencialidad ❌
```
Mensaje: "PIN: 1234"
Firma: (r, s)
→ Cualquiera puede leer "PIN: 1234"
→ Solo está firmado, NO cifrado
```

---

## 🔐 FUNDAMENTO MATEMÁTICO SIMPLE

**Autenticación:**
```
s = k⁻¹(H(M) + r·d) mod q
              ↑
    Necesitas 'd' (llave privada)
    
Sin 'd' → No puedes calcular 's'
→ Solo Alicia (con su 'd') puede firmar
```

**Integridad:**
```
s = k⁻¹(H(M) + r·d) mod q
        ↑
   Hash del mensaje
   
Mensaje cambia → H(M) cambia → s inválido
→ Detecta modificaciones
```

**No Repudio:**
```
Verificación exitosa prueba que:
- Se usó la llave privada correcta
- Solo Alicia la tiene
- Ella no puede negar haberla usado
```

---

**¡Usa este documento como referencia rápida durante tu presentación!** 🚀
