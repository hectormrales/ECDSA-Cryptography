# ECDSA - Firma Digital con Curvas Elípticas

Aplicación de escritorio para implementar el algoritmo de firma digital ECDSA (Elliptic Curve Digital Signature Algorithm) sobre curvas elípticas finitas.

**Autores:** Betito, Alicia, Candy

## Descripción

Esta aplicación permite:
- Generar pares de llaves pública/privada para cada usuario
- Firmar mensajes digitalmente usando ECDSA
- Verificar firmas digitales paso a paso
- Importar y exportar llaves en formato de texto
- Configurar diferentes curvas elípticas

## Requisitos

- Python 3.7 o superior
- Tkinter (incluido por defecto en Python)
- No se requieren dependencias externas

## Instalación

1. Clona o descarga este repositorio
2. Navega al directorio del proyecto:
```bash
cd ECDSA-Cryptography
```

## Uso

Para ejecutar la aplicación:

```bash
python src/gui.py
```

O en Windows:
```bash
py src/gui.py
```

## Estructura del Proyecto

```
ECDSA-Cryptography/
├── src/
│   ├── ecdsa_core.py    # Módulo principal con la implementación ECDSA
│   └── gui.py           # Interfaz gráfica con Tkinter
├── examples/
│   ├── ejemplo_verificacion.txt    # Ejemplo de verificación paso a paso
│   └── llaves_ejemplo/              # Llaves de ejemplo
├── README.md            # Este archivo
└── MANUAL.md           # Manual de usuario detallado
```

## Características Principales

### 1. Gestión de Llaves
- Generar nuevos pares de llaves para cada usuario (Betito, Alicia, Candy)
- Exportar llaves públicas para compartir
- Importar llaves públicas de otros usuarios
- Exportar/importar llaves privadas (con advertencia de seguridad)

### 2. Firma de Mensajes
- Firmar cualquier mensaje de texto
- Visualizar la firma generada (r, s)
- Guardar firmas en archivos

### 3. Verificación de Firmas
- Verificar firmas paso a paso según el algoritmo ECDSA
- Mostrar cada paso del proceso de verificación
- Soporte para hash manual (útil para ejemplos educativos)

### 4. Configuración de Curvas
- Curva de ejemplo incluida: y² = x³ + x + 10 (mod 11)
- Configuración de curvas personalizadas
- Visualización de parámetros de la curva

## Curva de Ejemplo

La aplicación incluye la curva del ejemplo educativo:

**Ecuación:** y² = x³ + x + 10 (mod 11)

**Parámetros:**
- p = 11 (primo del campo finito)
- a = 1 (coeficiente)
- b = 10 (coeficiente)
- G = (6, 1) (punto generador)
- q = 10 (orden del generador)

## Ejemplo de Verificación

El ejemplo de las imágenes adjuntas está incluido:
- Llave pública: Q = (9, 0)
- Hash del mensaje: H(M) = 9
- Firma: (r, s) = (4, 3)

Ver `examples/ejemplo_verificacion.txt` para los detalles completos.

## Seguridad

⚠️ **IMPORTANTE:**
- Esta es una implementación educativa
- La curva de ejemplo (p=11) es muy pequeña y NO es segura para uso en producción
- Para uso real, utiliza curvas estándar como secp256k1 o P-256
- Las llaves privadas deben mantenerse SIEMPRE en secreto

## Algoritmo ECDSA

### Generación de Llaves
1. Elegir un número aleatorio `d` en [1, q-1] → llave privada
2. Calcular `Q = d·G` → llave pública

### Firma
1. Calcular hash del mensaje: `z = H(M)`
2. Elegir número aleatorio `k` en [1, q-1]
3. Calcular `R = k·G`
4. `r = x_R mod q`
5. `s = k⁻¹(z + rd) mod q`
6. La firma es `(r, s)`

### Verificación
1. Verificar que `1 ≤ r, s ≤ q-1`
2. Calcular `w = s⁻¹ mod q`
3. Calcular `u₁ = zw mod q` y `u₂ = rw mod q`
4. Calcular `X = u₁G + u₂Q`
5. Verificar que `x_X ≡ r (mod q)`

## Documentación Adicional

Ver `MANUAL.md` para:
- Manual de usuario completo
- Ejemplos de uso paso a paso
- Explicación detallada del algoritmo
- Preguntas frecuentes

## Licencia

Este proyecto es de código abierto con fines educativos.

## Autores

- Betito
- Alicia
- Candy
