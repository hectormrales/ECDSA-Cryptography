# 🎯 RESUMEN RÁPIDO - Práctica con la Profesora

## ✅ RESPUESTA CORTA

**"¿Va a funcionar?"**
→ **SÍ, PERFECTAMENTE** ✅

**"¿La firma son los parámetros a, b?"**
→ **NO. La firma son los números (r, s)** ❌→✅

---

## 📋 FLUJO EN 3 FASES

```
FASE 1: Alicia y Candy con profesora
  ├─ Generan llaves
  └─ Suben llaves públicas (.pem) a la web

FASE 2: Alicia y Candy firman
  ├─ Ambas firman la MISMA canción
  ├─ Alicia: firma legítima → (r=73, s=42)
  └─ Candy: intenta suplantar → (r=19, s=88)

FASE 3: Betito verifica
  ├─ Descarga llave pública de Alicia
  ├─ Verifica firma de Alicia → ✓ VÁLIDA
  └─ Verifica firma de Candy → ✗ INVÁLIDA
```

---

## 🔑 CONCEPTOS CLAVE

### ❌ ERROR: "¿La firma son parámetros a, b?"

**NO.** Esos son parámetros de la curva elíptica.

### ✅ CORRECTO: La firma es (r, s)

```
Firma = (r, s)

Ejemplo:
  r = 73
  s = 42
```

Estos números se calculan matemáticamente al firmar.

---

## 📁 ARCHIVOS DE LA PRÁCTICA

### Alicia sube a la web:
```
llave_publica_Alicia.pem
```

### Candy sube a la web:
```
llave_publica_Candy.pem
```

### Te envían:
```
firma_alicia.sig    ← Contiene (r=73, s=42)
firma_candy.sig     ← Contiene (r=19, s=88)
cancion.txt         ← La letra (mismo contenido para ambas)
```

---

## 🎯 LO QUE TÚ HACES (Betito)

1. **Descargar** `llave_publica_Alicia.pem` de la web
2. **Importar** en la app
3. **Verificar** `firma_alicia.sig` → ✓ VÁLIDA
4. **Verificar** `firma_candy.sig` (con llave de Alicia) → ✗ INVÁLIDA

---

## 💡 ¿POR QUÉ CANDY NO PUEDE SUPLANTAR?

```
Candy NO tiene llave privada de Alicia
    ↓
Candy firma con SU llave privada
    ↓
Genera números (r, s) DIFERENTES
    ↓
Al verificar con llave pública de Alicia
    ↓
✗ NO COINCIDE → INVÁLIDA
```

---

## 📊 COMPARACIÓN

| Elemento | Alicia | Candy |
|----------|--------|-------|
| **Mensaje** | "Imagine..." | "Imagine..." ← Mismo |
| **Llave privada** | d_alicia | d_candy ← Diferente |
| **Firma (r, s)** | (73, 42) | (19, 88) ← Diferente |
| **Verificación con llave de Alicia** | ✓ VÁLIDA | ✗ INVÁLIDA |

---

## 🎤 QUÉ DECIR A LA PROFESORA

**"La firma digital es el par de números (r, s). Cuando Candy intenta suplantar a Alicia, genera números diferentes porque no tiene la llave privada de Alicia. Al verificar con la llave pública de Alicia, el sistema detecta automáticamente que la firma de Candy es inválida."**

---

## ✅ CHECKLIST PRE-PRÁCTICA

- [ ] Entender que firma = (r, s), NO parámetros (a, b)
- [ ] Probar generar llaves (.pem)
- [ ] Probar firmar mensaje (.sig)
- [ ] Probar verificar firma válida
- [ ] Probar verificar firma inválida
- [ ] Archivos listos para la práctica

---

## 🎯 RESULTADO ESPERADO

```
┌──────────────────────────────────────┐
│      VERIFICACIÓN DE FIRMAS          │
├──────────────────────────────────────┤
│                                      │
│  firma_alicia.sig  → ✓ VÁLIDA       │
│  firma_candy.sig   → ✗ INVÁLIDA     │
│                                      │
│  🎯 Candy intentó suplantar pero     │
│     el sistema lo detectó            │
│                                      │
└──────────────────────────────────────┘
```

---

## 🚀 COMANDOS RÁPIDOS

```bash
# Ejecutar app
python src/gui.py

# Ver curva actual
python -c "from src.ecdsa_core import crear_curva_ejemplo; c=crear_curva_ejemplo(); print(f'p={c.p}')"

# Resultado esperado: p=97
```

---

**Tu práctica es profesional y realista. ¡Buena suerte!** 🎯✨
