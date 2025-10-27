#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para generar archivos de demostración en formato Base64 puro
"""

from src.ecdsa_core import *
import base64

print("Generando archivos de demostración...")

# Crear curva y generar llaves
curva = crear_curva_ejemplo()
ecdsa = ECDSA(curva)
d, Q = ecdsa.generar_llaves()

# Exportar llaves
exportar_llave_publica(Q, curva, 'demo_public.pem')
print("✅ Llave pública: demo_public.pem")

exportar_llave_privada(d, curva, 'demo_private.pem')
print("✅ Llave privada: demo_private.pem")

# Crear firma
mensaje = "Hola mundo, esto es una prueba de ECDSA"
r, s = ecdsa.firmar(mensaje, d)

# Guardar firma en formato simple: mensaje + Base64
firma_texto = f"r={r}\ns={s}"
firma_base64 = base64.b64encode(firma_texto.encode()).decode()
contenido_firma = f"{mensaje}\n{firma_base64}"

with open('demo_firma.sig', 'w', encoding='utf-8') as f:
    f.write(contenido_firma)

print("✅ Firma: demo_firma.sig")
print("\n" + "="*60)
print("FORMATO DE LOS ARCHIVOS GENERADOS:")
print("="*60)

print("\n📄 demo_public.pem:")
with open('demo_public.pem', 'r') as f:
    print(f.read())

print("\n📄 demo_private.pem:")
with open('demo_private.pem', 'r') as f:
    print(f.read())

print("\n📄 demo_firma.sig:")
with open('demo_firma.sig', 'r') as f:
    print(f.read())

print("\n✅ Formato minimalista implementado correctamente")
print("   - Solo PEM headers + Base64 en llaves")
print("   - Solo mensaje + Base64 en firmas")
