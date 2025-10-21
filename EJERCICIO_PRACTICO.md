# Ejercicio Práctico: Firma y Verificación de song.txt

## Escenario del Ejercicio

1. **Los tres integrantes** generan sus llaves y suben sus llaves públicas
2. **Alicia** firma `song.txt` con el mensaje "Si acepto"
3. **Candy** firma `song.txt` con el mensaje "No acepto"
4. **Betito** verifica ambas firmas para identificar la firma auténtica de Alicia

---

## PARTE 1: Preparación - Generar Llaves

### Paso 1.1: Betito genera sus llaves

1. Ejecutar la aplicación: `python src/gui.py`
2. Ir a **"Gestión de Llaves"**
3. Seleccionar **"Betito"**
4. Clic en **"Generar Nuevo Par de Llaves"**
5. Clic en **"Exportar Llave Pública"**
   - Guardar como: `llave_publica_Betito.txt`
6. (Opcional) Clic en **"Exportar Llave Privada"** para respaldo
   - Guardar como: `llave_privada_Betito.txt`
   - ⚠️ Mantener este archivo seguro

### Paso 1.2: Alicia genera sus llaves

1. En la misma aplicación
2. Seleccionar **"Alicia"** (radio button)
3. Clic en **"Generar Nuevo Par de Llaves"**
4. Clic en **"Exportar Llave Pública"**
   - Guardar como: `llave_publica_Alicia.txt`
5. (Opcional) Exportar llave privada para respaldo

### Paso 1.3: Candy genera sus llaves

1. Seleccionar **"Candy"**
2. Clic en **"Generar Nuevo Par de Llaves"**
3. Clic en **"Exportar Llave Pública"**
   - Guardar como: `llave_publica_Candy.txt`
4. (Opcional) Exportar llave privada para respaldo

### Paso 1.4: "Subir" las llaves públicas

**En este ejercicio simulado:**
- Cada persona copia su archivo `llave_publica_*.txt` a una carpeta compartida
- En la vida real, cada uno subiría su llave pública a su página web

**Crear carpeta compartida:**
```bash
mkdir ejercicio_firmas
mkdir ejercicio_firmas/llaves_publicas
```

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
