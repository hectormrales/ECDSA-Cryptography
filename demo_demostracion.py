#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demostración paso a paso de la verificación matemática de ECDSA
Muestra por qué P' = P usando valores reales
"""

from src.ecdsa_core import *
import base64

def imprimir_seccion(titulo):
    print("\n" + "="*70)
    print(f"  {titulo}")
    print("="*70)

def imprimir_paso(numero, titulo, contenido):
    print(f"\n{'─'*70}")
    print(f"📐 PASO {numero}: {titulo}")
    print(f"{'─'*70}")
    print(contenido)

def main():
    print("\n" + "🔬"*35)
    print(" "*15 + "DEMOSTRACIÓN MATEMÁTICA ECDSA")
    print("🔬"*35)
    
    imprimir_seccion("CONFIGURACIÓN INICIAL")
    
    # Crear curva
    curva = crear_curva_ejemplo()
    ecdsa = ECDSA(curva)
    
    print(f"\n📊 Parámetros de la Curva Elíptica:")
    print(f"   Ecuación: y² = x³ + {curva.a}x + {curva.b} (mod {curva.p})")
    print(f"   Módulo p = {curva.p}")
    print(f"   Coeficiente a = {curva.a}")
    print(f"   Coeficiente b = {curva.b}")
    print(f"   Generador G = {curva.G}")
    print(f"   Orden q = {curva.q}")
    
    # Generar llaves con valor fijo para reproducibilidad
    d = 2  # Llave privada
    Q = curva.multiplicar_escalar(d, curva.G)
    
    print(f"\n🔑 Llaves Criptográficas:")
    print(f"   Llave privada: d = {d}")
    print(f"   Llave pública: Q = d·G = {d}·{curva.G} = {Q}")
    
    # Mensaje a firmar
    mensaje = "Hola mundo"
    print(f"\n📝 Mensaje a firmar: '{mensaje}'")
    
    # ========================================================================
    # PROCESO DE FIRMA
    # ========================================================================
    
    imprimir_seccion("PROCESO DE FIRMA (GENERACIÓN)")
    
    # Calcular hash
    h = ecdsa.hash_mensaje(mensaje)
    print(f"\n🔢 Hash del mensaje:")
    print(f"   h = H('{mensaje}') mod {curva.q} = {h}")
    
    # Generar k (usamos valor fijo para reproducibilidad)
    k = 1  # Normalmente sería aleatorio
    print(f"\n🎲 Valor aleatorio k = {k}")
    print(f"   (En producción, k debe ser aleatorio y único)")
    
    # Calcular P = k·G
    P = curva.multiplicar_escalar(k, curva.G)
    print(f"\n📍 Punto P = k·G:")
    print(f"   P = {k}·{curva.G}")
    print(f"   P = {P}")
    
    # Calcular r
    r = P.x % curva.q
    print(f"\n🎯 Primera componente de la firma:")
    print(f"   r = x_P mod q")
    print(f"   r = {P.x} mod {curva.q}")
    print(f"   r = {r}")
    
    # Calcular k^(-1)
    k_inv = pow(k, -1, curva.q)
    print(f"\n🔄 Inverso modular de k:")
    print(f"   k⁻¹ = {k}⁻¹ mod {curva.q} = {k_inv}")
    print(f"   Verificación: {k} × {k_inv} = {(k * k_inv) % curva.q} mod {curva.q} ✓")
    
    # Calcular s
    s = (k_inv * (h + r * d)) % curva.q
    print(f"\n🔐 Segunda componente de la firma:")
    print(f"   s = k⁻¹(h + rd) mod q")
    print(f"   s = {k_inv} × ({h} + {r}×{d}) mod {curva.q}")
    print(f"   s = {k_inv} × ({h} + {r * d}) mod {curva.q}")
    print(f"   s = {k_inv} × {(h + r * d) % curva.q} mod {curva.q}")
    print(f"   s = {s}")
    
    print(f"\n✅ Firma generada: (r, s) = ({r}, {s})")
    
    # ========================================================================
    # PROCESO DE VERIFICACIÓN
    # ========================================================================
    
    imprimir_seccion("PROCESO DE VERIFICACIÓN")
    
    print(f"\n📥 Datos recibidos:")
    print(f"   Mensaje: '{mensaje}'")
    print(f"   Firma: (r, s) = ({r}, {s})")
    print(f"   Llave pública: Q = {Q}")
    
    # Calcular hash (mismo que en firma)
    h_verif = ecdsa.hash_mensaje(mensaje)
    print(f"\n🔢 Hash del mensaje:")
    print(f"   h = H('{mensaje}') mod {curva.q} = {h_verif}")
    
    # Calcular w = s^(-1)
    w = pow(s, -1, curva.q)
    print(f"\n🔄 Inverso de s:")
    print(f"   w = s⁻¹ mod q")
    print(f"   w = {s}⁻¹ mod {curva.q} = {w}")
    print(f"   Verificación: {s} × {w} = {(s * w) % curva.q} mod {curva.q} ✓")
    
    # Calcular u1
    u1 = (h_verif * w) % curva.q
    print(f"\n📊 Primer escalar u₁:")
    print(f"   u₁ = h × w mod q")
    print(f"   u₁ = {h_verif} × {w} mod {curva.q}")
    print(f"   u₁ = {u1}")
    
    # Calcular u2
    u2 = (r * w) % curva.q
    print(f"\n📊 Segundo escalar u₂:")
    print(f"   u₂ = r × w mod q")
    print(f"   u₂ = {r} × {w} mod {curva.q}")
    print(f"   u₂ = {u2}")
    
    # Calcular P' = u1·G + u2·Q
    print(f"\n🎯 Calcular punto P':")
    print(f"   P' = u₁·G + u₂·Q")
    print(f"   P' = {u1}·{curva.G} + {u2}·{Q}")
    
    # Calcular u1·G
    u1_G = curva.multiplicar_escalar(u1, curva.G)
    print(f"\n   Paso 1: u₁·G = {u1}·{curva.G} = {u1_G}")
    
    # Calcular u2·Q
    u2_Q = curva.multiplicar_escalar(u2, Q)
    print(f"   Paso 2: u₂·Q = {u2}·{Q} = {u2_Q}")
    
    # Sumar los puntos
    P_prima = curva.sumar_puntos(u1_G, u2_Q)
    print(f"   Paso 3: P' = u₁·G + u₂·Q = {u1_G} + {u2_Q}")
    print(f"   P' = {P_prima}")
    
    # Extraer r'
    r_prima = P_prima.x % curva.q
    print(f"\n🎯 Coordenada x de P':")
    print(f"   r' = x_P' mod q")
    print(f"   r' = {P_prima.x} mod {curva.q}")
    print(f"   r' = {r_prima}")
    
    # Verificar
    print(f"\n{'='*70}")
    if r_prima == r:
        print("✅ VERIFICACIÓN EXITOSA: r' = r")
        print(f"   {r_prima} = {r} ✓")
        print("\n   La firma es VÁLIDA - El mensaje fue firmado por el poseedor de d")
    else:
        print("❌ VERIFICACIÓN FALLIDA: r' ≠ r")
        print(f"   {r_prima} ≠ {r} ✗")
    print("="*70)
    
    # ========================================================================
    # DEMOSTRACIÓN ALGEBRAICA
    # ========================================================================
    
    imprimir_seccion("DEMOSTRACIÓN ALGEBRAICA: ¿Por qué P' = P?")
    
    imprimir_paso(1, "Expansión de P'", 
f"""   P' = u₁·G + u₂·Q
   P' = (h×w)·G + (r×w)·Q
   P' = ({h_verif}×{w})·G + ({r}×{w})·Q
   P' = {u1}·G + {u2}·Q""")
    
    imprimir_paso(2, "Sustituir Q = d·G",
f"""   Sabemos que Q = d·G = {d}·G
   
   P' = {u1}·G + {u2}·(d·G)
   P' = {u1}·G + ({u2}×{d})·G
   P' = {u1}·G + {(u2 * d) % curva.q}·G""")
    
    imprimir_paso(3, "Factorizar G",
f"""   P' = ({u1} + {(u2 * d) % curva.q})·G
   P' = {(u1 + u2 * d) % curva.q}·G
   P' = w(h + rd)·G
   P' = {w}×({h_verif} + {r}×{d})·G
   P' = {w}×{(h_verif + r * d) % curva.q}·G""")
    
    imprimir_paso(4, "Usar w = s⁻¹",
f"""   P' = s⁻¹(h + rd)·G
   P' = {s}⁻¹×{(h_verif + r * d) % curva.q}·G""")
    
    imprimir_paso(5, "Sustituir definición de s",
f"""   De la firma sabemos que:
   s = k⁻¹(h + rd)
   {s} = {k_inv}×({h} + {r}×{d})
   {s} = {k_inv}×{(h + r * d) % curva.q}
   
   Por lo tanto:
   h + rd = k×s
   {(h + r * d) % curva.q} = {k}×{s} = {(k * s) % curva.q} mod {curva.q}""")
    
    imprimir_paso(6, "Simplificar P'",
f"""   P' = s⁻¹(k×s)·G
   P' = (s⁻¹×s)×k·G
   P' = 1×k·G
   P' = k·G
   P' = {k}·G""")
    
    imprimir_paso(7, "Conclusión",
f"""   De la firma tenemos:
   P = k·G = {k}·{curva.G} = {P}
   
   De la verificación obtuvimos:
   P' = k·G = {k}·{curva.G} = {P_prima}
   
   Por lo tanto:
   ✅ P' = P = {P}
   ✅ x_P' = x_P = {P.x}
   ✅ r' = r = {r}
   
   ¡La verificación matemática es CORRECTA!""")
    
    # ========================================================================
    # PROPIEDADES UTILIZADAS
    # ========================================================================
    
    imprimir_seccion("PROPIEDADES DE CURVAS ELÍPTICAS UTILIZADAS")
    
    print("""
1️⃣  ASOCIATIVIDAD:
    (k₁ + k₂)·P = k₁·P + k₂·P
    Usada en: P' = u₁·G + u₂·Q = (u₁ + u₂d)·G

2️⃣  CONMUTATIVIDAD:
    k₁·(k₂·P) = k₂·(k₁·P) = (k₁k₂)·P
    Usada en: u₂·(d·G) = (u₂d)·G

3️⃣  INVERSOS MODULARES:
    Si w = s⁻¹, entonces s×w ≡ 1 (mod q)
    Usada en: s⁻¹×s = 1, simplifica P' = s⁻¹(ks)·G = k·G

4️⃣  PROBLEMA DEL LOGARITMO DISCRETO (DLP):
    Dado Q = d·G, es imposible encontrar d
    Garantiza: Seguridad del esquema

5️⃣  UNICIDAD DE k:
    Cada firma usa un k diferente y aleatorio
    Previene: Ataques de recuperación de clave
    """)
    
    # ========================================================================
    # VERIFICACIÓN CON VALORES INCORRECTOS
    # ========================================================================
    
    imprimir_seccion("CASO DE FALLO: Firma con Llave Incorrecta")
    
    print("\n🔧 Generando firma con llave privada incorrecta...")
    d_falsa = 3  # Llave privada incorrecta
    Q_falsa = curva.multiplicar_escalar(d_falsa, curva.G)
    
    print(f"   Llave privada falsa: d' = {d_falsa}")
    print(f"   Llave pública falsa: Q' = {Q_falsa}")
    
    # Firmar con llave falsa
    k_falso = 4
    P_falso = curva.multiplicar_escalar(k_falso, curva.G)
    r_falso = P_falso.x % curva.q
    k_falso_inv = pow(k_falso, -1, curva.q)
    s_falso = (k_falso_inv * (h + r_falso * d_falsa)) % curva.q
    
    print(f"   Firma falsa: (r', s') = ({r_falso}, {s_falso})")
    
    # Intentar verificar con llave pública original
    print(f"\n🔍 Intentando verificar con llave pública original Q = {Q}...")
    
    w_falso = pow(s_falso, -1, curva.q)
    u1_falso = (h * w_falso) % curva.q
    u2_falso = (r_falso * w_falso) % curva.q
    
    u1_G_falso = curva.multiplicar_escalar(u1_falso, curva.G)
    u2_Q_falso = curva.multiplicar_escalar(u2_falso, Q)
    P_prima_falso = curva.sumar_puntos(u1_G_falso, u2_Q_falso)
    r_prima_falso = P_prima_falso.x % curva.q
    
    print(f"   P' calculado = {P_prima_falso}")
    print(f"   r' = {r_prima_falso}")
    print(f"   r (de la firma) = {r_falso}")
    
    if r_prima_falso != r_falso:
        print(f"\n   ❌ VERIFICACIÓN FALLIDA: {r_prima_falso} ≠ {r_falso}")
        print("   ¡El sistema detecta correctamente firmas falsas!")
    else:
        print(f"\n   ⚠️  Casualidad: La firma pasó (probabilidad 1/{curva.q})")
    
    # ========================================================================
    # RESUMEN FINAL
    # ========================================================================
    
    imprimir_seccion("RESUMEN DE LA DEMOSTRACIÓN")
    
    print(f"""
📌 ECUACIÓN FUNDAMENTAL:

   Firma:        s = k⁻¹(h + rd)
   Verificación: P' = s⁻¹(h + rd)·G = k·G = P
   Resultado:    x_P' = x_P = r  ✓

🔑 PROPIEDADES CLAVE:

   • Asociatividad de suma de puntos
   • Conmutatividad de multiplicación escalar
   • Inversos modulares: s·s⁻¹ = 1
   • Logaritmo discreto: Q = d·G (d no recuperable)

🛡️  SEGURIDAD:

   • Basada en problema DLP de curvas elípticas
   • k debe ser aleatorio y único para cada firma
   • Hash criptográfico (SHA-256) resistente a colisiones

✅ RESULTADO:

   La verificación matemática demuestra que SOLO el poseedor
   de la llave privada d puede generar una firma válida que
   satisface la ecuación r' = r.

   ¡ECDSA es matemáticamente correcto y seguro! 🎓
    """)
    
    print("\n" + "🔬"*35 + "\n")

if __name__ == "__main__":
    main()
