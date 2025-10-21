# Instrucciones Rápidas - Ejercicio de Firmas

## 📋 Resumen del Ejercicio

1. **Todos generan llaves** y exportan sus llaves públicas
2. **Alicia firma** `song.txt` con mensaje "Si acepto"
3. **Candy firma** `song.txt` con mensaje "No acepto" (intentando suplantar)
4. **Betito verifica** cuál firma es auténtica de Alicia

---

## 🚀 Pasos Rápidos

### PARTE 1: Preparación (5 minutos)

```bash
# Ejecutar la aplicación
python src/gui.py
```

**Para cada usuario (Betito, Alicia, Candy):**
1. Seleccionar usuario
2. Generar Nuevo Par de Llaves
3. Exportar Llave Pública → guardar como `llave_publica_[Nombre].txt`

---

### PARTE 2: Alicia firma (2 minutos)

1. Seleccionar **Alicia**
2. Pestaña **"Firmar Mensaje"**
3. Copiar contenido de `ejercicio_firmas/PLANTILLA_song_alicia.txt`
4. Firmar Mensaje
5. Guardar Firma → `firma_alicia.txt`

---

### PARTE 3: Candy firma (2 minutos)

1. Seleccionar **Candy**
2. Pestaña **"Firmar Mensaje"**
3. Copiar contenido de `ejercicio_firmas/PLANTILLA_song_candy.txt`
4. Firmar Mensaje
5. Guardar Firma → `firma_candy.txt`

---

### PARTE 4: Betito verifica (5 minutos)

**Verificar firma de Alicia:**
1. Seleccionar **Betito**
2. Pestaña **"Gestión de Llaves"**
3. Importar Llave Pública de Alicia
4. Pestaña **"Verificar Firma"**
5. Copiar mensaje de `PLANTILLA_song_alicia.txt`
6. Cargar `firma_alicia.txt`
7. Verificar → Resultado: ✓ **VÁLIDA**

**Verificar firma de Candy:**
1. Copiar mensaje de `PLANTILLA_song_candy.txt`
2. Cargar `firma_candy.txt`
3. Verificar con llave pública de Alicia → Resultado: ✗ **INVÁLIDA**

---

## ✅ Conclusión

- **song de Alicia** → Firma VÁLIDA → "Si acepto" → Este es el auténtico
- **song de Candy** → Firma INVÁLIDA → Intento de suplantación detectado

**¡El sistema funciona! La firma digital protege contra suplantación.** 🔒

---

## 📁 Archivos Necesarios

```
ejercicio_firmas/
├── PLANTILLA_song_alicia.txt    (mensaje de Alicia)
├── PLANTILLA_song_candy.txt     (mensaje de Candy)
└── llaves_publicas/             (aquí guardar las llaves públicas)
```

---

**Ver guía completa en:** `EJERCICIO_PRACTICO.md`
