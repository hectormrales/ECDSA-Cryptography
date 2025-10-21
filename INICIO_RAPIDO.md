# Guía de Inicio Rápido - ECDSA

## Ejecutar la Aplicación

```bash
python src/gui.py
```

## Primeros Pasos

### 1. Generar tus llaves (primera vez)
1. Abre la aplicación
2. Ve a la pestaña **"Gestión de Llaves"**
3. Selecciona tu usuario (Betito, Alicia o Candy)
4. Clic en **"Generar Nuevo Par de Llaves"**
5. Clic en **"Exportar Llave Pública"** para compartirla

### 2. Firmar un mensaje
1. Ve a **"Firmar Mensaje"**
2. Escribe tu mensaje
3. Clic en **"Firmar Mensaje"**
4. Guarda la firma si quieres compartirla

### 3. Verificar una firma
1. Ve a **"Verificar Firma"**
2. Ingresa el mensaje original
3. Ingresa los valores r y s de la firma
4. Selecciona quién firmó
5. Clic en **"Verificar Firma (Paso a Paso)"**

## Probar el Ejemplo de las Imágenes

### Opción 1: Usar el script de prueba
```bash
python src/test_ecdsa.py
```

### Opción 2: En la interfaz gráfica

1. **Configurar la curva:**
   - Pestaña "Configurar Curva"
   - Clic en "Cargar Curva de Ejemplo (p=11)"
   - Clic en "Aplicar Curva"

2. **Importar llave pública del ejemplo:**
   - Pestaña "Gestión de Llaves"
   - Seleccionar usuario (ej: Betito)
   - Clic en "Importar Llave Pública"
   - Seleccionar: `examples/llaves_ejemplo/llave_publica_ejemplo.txt`

3. **Verificar la firma del ejemplo:**
   - Pestaña "Verificar Firma"
   - Mensaje: cualquier texto
   - Marcar: "Usar valor de hash manual H(M):"
   - Ingresar hash: **9**
   - Ingresar firma: r = **4**, s = **3**
   - Seleccionar el usuario con la llave importada
   - Clic en "Verificar Firma (Paso a Paso)"

4. **Resultado esperado:**
   ```
   Paso 1: w = 7
   Paso 2: u1 = 3, u2 = 8
   Paso 3: X = (4, 1)
   Paso 4: xX mod q = 4 = r
   
   ✓ La firma es VÁLIDA
   ```

## Estructura de Archivos

```
ECDSA-Cryptography/
├── src/
│   ├── ecdsa_core.py      # Módulo principal ECDSA
│   ├── gui.py             # Interfaz gráfica
│   └── test_ecdsa.py      # Script de pruebas
├── examples/
│   ├── ejemplo_verificacion.txt              # Explicación detallada
│   └── llaves_ejemplo/
│       ├── llave_publica_ejemplo.txt        # Llave Q=(9,0)
│       └── firma_ejemplo.txt                # Firma (4,3)
├── README.md              # Documentación general
└── MANUAL.md             # Manual de usuario completo
```

## Notas Importantes

### Sobre la Curva de Ejemplo (p=11, q=10)

⚠️ **Limitación conocida:** La curva del ejemplo es muy pequeña y tiene q=10 (no primo).

- Solo los valores 1, 3, 7, 9 tienen inverso módulo 10
- Esto puede causar que la generación de firmas aleatorias tarde o falle
- **Esto es normal y esperado** con curvas tan pequeñas
- En curvas reales (con q primo grande), este problema no existe

### Seguridad

⚠️ Esta implementación es **educativa**. Para uso en producción:
- Usar curvas estándar: secp256k1, P-256, Curve25519
- q debe ser un primo grande (256+ bits)
- Implementar protección contra ataques de canal lateral

## Ver Documentación Completa

- **README.md** - Visión general del proyecto
- **MANUAL.md** - Manual detallado con explicación del algoritmo
- **examples/ejemplo_verificacion.txt** - Ejemplo paso a paso

## Ayuda

Si algo no funciona:
1. Verifica que Python 3.7+ esté instalado
2. Ejecuta el script de prueba: `python src/test_ecdsa.py`
3. Consulta el MANUAL.md para más detalles

---

**Autores:** Betito, Alicia, Candy 🔐
