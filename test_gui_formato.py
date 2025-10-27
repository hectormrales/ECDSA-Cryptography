#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test simple para verificar el formato de firma en la GUI
"""

from src.ecdsa_core import *
import base64

print("="*60)
print("TEST DE FORMATO GUI")
print("="*60)

# Simular lo que hace la GUI al firmar
curva = crear_curva_ejemplo()
ecdsa = ECDSA(curva)

# Usar llave fija para evitar problemas aleatorios
d = 2
Q = curva.multiplicar_escalar(d, curva.G)

mensaje = "Prueba de firma desde GUI"
r, s = ecdsa.firmar(mensaje, d)

# Formato nuevo: solo mensaje + Base64
firma_texto = f"r={r}\ns={s}"
firma_base64 = base64.b64encode(firma_texto.encode('utf-8')).decode('utf-8')

resultado = f"{mensaje}\n{firma_base64}"

print("\n📝 FORMATO DE FIRMA GENERADO POR LA GUI:")
print("-" * 60)
print(resultado)
print("-" * 60)

# Simular lectura de firma (lo que hace cargar_firma)
print("\n📖 SIMULACIÓN DE CARGA DE FIRMA:")
print("-" * 60)

lineas = resultado.strip().split('\n')
if len(lineas) >= 2:
    mensaje_leido = '\n'.join(lineas[:-1])  # Todo excepto última línea
    firma_base64_leida = lineas[-1].strip()
    
    print(f"Mensaje leído: {mensaje_leido}")
    print(f"Base64 leída: {firma_base64_leida}")
    
    # Decodificar
    firma_decodificada = base64.b64decode(firma_base64_leida).decode('utf-8')
    print(f"\nFirma decodificada:")
    print(firma_decodificada)
    
    # Parsear r y s
    for linea in firma_decodificada.split('\n'):
        if linea.startswith('r='):
            r_leido = int(linea.split('=')[1].strip())
            print(f"r = {r_leido}")
        elif linea.startswith('s='):
            s_leido = int(linea.split('=')[1].strip())
            print(f"s = {s_leido}")
    
    # Verificar
    es_valido = ecdsa.verificar(mensaje_leido, (r_leido, s_leido), Q)
    print(f"\n✅ Firma válida: {es_valido}")
    
    assert r == r_leido, "Error: r no coincide"
    assert s == s_leido, "Error: s no coincide"
    assert es_valido, "Error: Firma no es válida"
    
    print("\n🎉 PASS - Formato GUI funciona correctamente")
    print("="*60)
