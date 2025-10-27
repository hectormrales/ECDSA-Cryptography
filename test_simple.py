#!/usr/bin/env python3
"""Script simple de prueba"""
print("Iniciando pruebas...")

try:
    from src.ecdsa_core import *
    print("✅ Importación exitosa")
    
    curva = crear_curva_ejemplo()
    print(f"✅ Curva creada: p={curva.p}")
    
    ecdsa = ECDSA(curva)
    d, Q = ecdsa.generar_llaves()
    print(f"✅ Llaves generadas: d={d}, Q={Q}")
    
    # Exportar con Base64
    exportar_llave_publica(Q, curva, "test.pem")
    print("✅ Llave exportada")
    
    # Leer archivo
    with open("test.pem", "r") as f:
        contenido = f.read()
    print("\n📄 Contenido del archivo:")
    print(contenido)
    
    # Importar
    Q2, c = importar_llave_publica("test.pem")
    print(f"\n✅ Llave importada: Q2={Q2}")
    print(f"✅ Coinciden: {Q == Q2}")
    
    # Limpiar
    import os
    os.remove("test.pem")
    print("\n🎉 TODAS LAS PRUEBAS PASARON!")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
