# 🎯 Resumen - Cómo Realizar el Ejercicio

## Tu Pregunta
> "¿Cómo hacer el ejercicio donde los tres integrantes suben su llave pública, Alicia firma 'Si acepto', Candy firma 'No acepto', y Betito verifica quién es realmente Alicia?"

## Respuesta Rápida

### Opción 1: Demostración Automática ⚡
```bash
python ejercicio_firmas/demo_ejercicio.py
```
Este script simula todo el proceso automáticamente.

### Opción 2: Paso a Paso Manual (Recomendado) 📝

#### **Paso 1: Generar Llaves** (todos)
```bash
python src/gui.py
```
- Cada usuario genera sus llaves
- Exportan llave pública
- "Suben" a su página web (en este caso, carpeta compartida)

#### **Paso 2: Alicia Firma**
1. Abrir `ejercicio_firmas/PLANTILLA_song_alicia.txt`
2. En la app, pestaña "Firmar Mensaje"
3. Copiar el mensaje completo
4. Firmar y guardar firma

#### **Paso 3: Candy Firma**
1. Abrir `ejercicio_firmas/PLANTILLA_song_candy.txt`
2. Firmar con su propia llave (intenta suplantar a Alicia)
3. Guardar firma

#### **Paso 4: Betito Verifica**
1. Importar llave pública de Alicia
2. Pestaña "Verificar Firma"
3. Verificar mensaje de Alicia → ✓ VÁLIDA
4. Verificar mensaje de Candy con llave de Alicia → ✗ INVÁLIDA

## Archivos Creados

✅ **`EJERCICIO_PRACTICO.md`** - Guía completa paso a paso (15 páginas)
✅ **`ejercicio_firmas/INSTRUCCIONES.md`** - Guía rápida
✅ **`ejercicio_firmas/demo_ejercicio.py`** - Demostración automática
✅ **`ejercicio_firmas/PLANTILLA_song_alicia.txt`** - Mensaje de Alicia
✅ **`ejercicio_firmas/PLANTILLA_song_candy.txt`** - Mensaje de Candy

## Resultado Esperado

```
Mensaje de Alicia + Firma de Alicia + Llave pública de Alicia
→ ✓ VÁLIDA (dice "Si acepto")

Mensaje de Candy + Firma de Candy + Llave pública de Alicia  
→ ✗ INVÁLIDA (intento de suplantación detectado)
```

**Conclusión:** Betito identifica que el mensaje auténtico de Alicia es el que dice "Si acepto".

## Documentación

📖 **Lee primero:** `ejercicio_firmas/INSTRUCCIONES.md` (versión corta)
📖 **Guía completa:** `EJERCICIO_PRACTICO.md` (versión detallada)

## ¡Listo para Usar! 🚀

Todos los archivos están creados y listos en la carpeta `ejercicio_firmas/`.

---

**Pregunta resuelta:** Sí, puedes hacer exactamente el ejercicio que describiste usando la aplicación que creé. Todo está documentado y funcionando. 🔐
