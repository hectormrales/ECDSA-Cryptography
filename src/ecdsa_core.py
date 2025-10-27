"""
Módulo de criptografía ECDSA (Elliptic Curve Digital Signature Algorithm)
Implementación sobre curvas elípticas finitas: y² = x³ + ax + b (mod p)

Autores: Betito, Alicia, Candy
"""

import hashlib
import secrets
import math
import base64
from typing import Tuple, Optional, List, Dict


class PuntoElliptico:
    """Representa un punto en una curva elíptica o el punto en el infinito"""
    
    def __init__(self, x: Optional[int], y: Optional[int]):
        self.x = x
        self.y = y
        self.es_infinito = (x is None and y is None)
    
    def __eq__(self, otro):
        if not isinstance(otro, PuntoElliptico):
            return False
        return self.x == otro.x and self.y == otro.y
    
    def __repr__(self):
        if self.es_infinito:
            return "O (punto en el infinito)"
        return f"({self.x}, {self.y})"


class CurvaEliptica:
    """
    Curva elíptica sobre un campo finito F_p
    Ecuación: y² = x³ + ax + b (mod p)
    """
    
    def __init__(self, p: int, a: int, b: int, G: Tuple[int, int], q: int):
        """
        Args:
            p: Primo que define el campo finito F_p
            a, b: Coeficientes de la curva
            G: Punto generador (x, y)
            q: Orden del punto generador G
        """
        self.p = p
        self.a = a
        self.b = b
        self.G = PuntoElliptico(G[0], G[1])
        self.q = q
        
        # Verificar que el discriminante no sea cero
        discriminante = (4 * a**3 + 27 * b**2) % p
        if discriminante == 0:
            raise ValueError("La curva es singular (discriminante = 0)")
    
    def esta_en_curva(self, punto: PuntoElliptico) -> bool:
        """Verifica si un punto está en la curva"""
        if punto.es_infinito:
            return True
        
        izquierda = (punto.y ** 2) % self.p
        derecha = (punto.x ** 3 + self.a * punto.x + self.b) % self.p
        return izquierda == derecha
    
    def inverso_modular(self, a: int, m: int) -> int:
        """
        Calcula el inverso modular de a módulo m usando el algoritmo extendido de Euclides
        Devuelve x tal que (a * x) ≡ 1 (mod m)
        """
        if a < 0:
            a = (a % m + m) % m
        
        # Algoritmo extendido de Euclides
        def egcd(a, b):
            if a == 0:
                return b, 0, 1
            gcd, x1, y1 = egcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd, x, y
        
        gcd, x, _ = egcd(a, m)
        if gcd != 1:
            raise ValueError(f"No existe inverso modular de {a} módulo {m}")
        return (x % m + m) % m
    
    def sumar_puntos(self, P: PuntoElliptico, Q: PuntoElliptico) -> PuntoElliptico:
        """
        Suma dos puntos en la curva elíptica
        """
        # Casos especiales con el punto en el infinito
        if P.es_infinito:
            return Q
        if Q.es_infinito:
            return P
        
        # Si P = -Q, el resultado es O (punto en el infinito)
        if P.x == Q.x and (P.y + Q.y) % self.p == 0:
            return PuntoElliptico(None, None)
        
        # Calcular la pendiente
        if P == Q:
            # Duplicación de punto: λ = (3x² + a) / (2y)
            numerador = (3 * P.x ** 2 + self.a) % self.p
            denominador = (2 * P.y) % self.p
        else:
            # Suma de puntos diferentes: λ = (y₂ - y₁) / (x₂ - x₁)
            numerador = (Q.y - P.y) % self.p
            denominador = (Q.x - P.x) % self.p
        
        # Calcular el inverso modular del denominador
        denominador_inv = self.inverso_modular(denominador, self.p)
        pendiente = (numerador * denominador_inv) % self.p
        
        # Calcular las coordenadas del punto resultado
        x_r = (pendiente ** 2 - P.x - Q.x) % self.p
        y_r = (pendiente * (P.x - x_r) - P.y) % self.p
        
        return PuntoElliptico(x_r, y_r)
    
    def multiplicar_escalar(self, k: int, P: PuntoElliptico) -> PuntoElliptico:
        """
        Multiplica un punto P por un escalar k usando el método de duplicación y suma
        Calcula k·P
        """
        if k == 0:
            return PuntoElliptico(None, None)
        
        if k < 0:
            # Para k negativo, usar -k·P = k·(-P)
            k = -k
            P = PuntoElliptico(P.x, (-P.y) % self.p)
        
        # Algoritmo de duplicación y suma (binary method)
        resultado = PuntoElliptico(None, None)  # Iniciar con O
        sumando = P
        
        while k > 0:
            if k & 1:  # Si el bit es 1
                resultado = self.sumar_puntos(resultado, sumando)
            sumando = self.sumar_puntos(sumando, sumando)  # Duplicar
            k >>= 1  # Shift derecha
        
        return resultado


class ECDSA:
    """
    Implementación del algoritmo de firma digital ECDSA
    """
    
    def __init__(self, curva: CurvaEliptica):
        self.curva = curva
    
    def generar_llaves(self) -> Tuple[int, PuntoElliptico]:
        """
        Genera un par de llaves (privada, pública)
        
        Returns:
            (d, Q) donde:
            - d: Llave privada (entero aleatorio en [1, q-1])
            - Q: Llave pública (punto Q = d·G)
        """
        # Generar llave privada aleatoria d en [1, q-1]
        d = secrets.randbelow(self.curva.q - 1) + 1
        
        # Calcular llave pública Q = d·G
        Q = self.curva.multiplicar_escalar(d, self.curva.G)
        
        return d, Q
    
    def hash_mensaje(self, mensaje: str) -> int:
        """
        Calcula el hash del mensaje y lo convierte a entero módulo q
        """
        # Usar SHA-256 para el hash
        hash_bytes = hashlib.sha256(mensaje.encode('utf-8')).digest()
        hash_int = int.from_bytes(hash_bytes, byteorder='big')
        
        # Reducir módulo q
        return hash_int % self.curva.q
    
    def firmar(self, mensaje: str, llave_privada: int, k: Optional[int] = None) -> Tuple[int, int]:
        """
        Firma un mensaje usando ECDSA
        
        Args:
            mensaje: Mensaje a firmar
            llave_privada: Llave privada d
            k: Nonce aleatorio (opcional, si no se proporciona se genera uno)
        
        Returns:
            (r, s): Firma digital
        """
        # Calcular hash del mensaje
        z = self.hash_mensaje(mensaje)
        
        max_intentos = 100
        intentos = 0
        
        while intentos < max_intentos:
            intentos += 1
            
            # Generar nonce aleatorio k si no se proporciona
            if k is None:
                k_actual = secrets.randbelow(self.curva.q - 1) + 1
            else:
                k_actual = k
            
            # Calcular punto R = k·G
            R = self.curva.multiplicar_escalar(k_actual, self.curva.G)
            
            # r = x_R mod q
            r = R.x % self.curva.q
            
            if r == 0:
                if k is not None:
                    raise ValueError("k inválido: r = 0")
                continue
            
            # Intentar calcular k^(-1) mod q
            try:
                k_inv = self.curva.inverso_modular(k_actual, self.curva.q)
            except ValueError:
                # k no tiene inverso modular (gcd(k, q) != 1), intentar con otro k
                if k is not None:
                    raise ValueError(f"k inválido: k={k_actual} no tiene inverso módulo q={self.curva.q}")
                continue
            
            # s = k^(-1) * (z + r * d) mod q
            s = (k_inv * (z + r * llave_privada)) % self.curva.q
            
            if s == 0:
                if k is not None:
                    raise ValueError("k inválido: s = 0")
                continue
            
            # Verificar que s tenga inverso modular (gcd(s, q) = 1)
            if math.gcd(s, self.curva.q) != 1:
                if k is not None:
                    raise ValueError(f"k inválido: s={s} no tiene inverso módulo q={self.curva.q}")
                continue
            
            return r, s
        
        raise RuntimeError(f"No se pudo generar firma después de {max_intentos} intentos")
    
    def verificar(self, mensaje: str, firma: Tuple[int, int], llave_publica: PuntoElliptico) -> bool:
        """
        Verifica una firma ECDSA
        
        Args:
            mensaje: Mensaje original
            firma: Tupla (r, s)
            llave_publica: Llave pública Q
        
        Returns:
            True si la firma es válida, False en caso contrario
        """
        r, s = firma
        
        # Paso 0: Verificar rango de r y s
        if not (1 <= r <= self.curva.q - 1) or not (1 <= s <= self.curva.q - 1):
            return False
        
        # Calcular hash del mensaje
        z = self.hash_mensaje(mensaje)
        
        # Paso 1: Calcular w = s^(-1) mod q
        try:
            w = self.curva.inverso_modular(s, self.curva.q)
        except ValueError:
            # s no tiene inverso modular, la firma es inválida
            return False
        
        # Paso 2: Calcular u₁ = z·w mod q y u₂ = r·w mod q
        u1 = (z * w) % self.curva.q
        u2 = (r * w) % self.curva.q
        
        # Paso 3: Calcular X = u₁·G + u₂·Q
        punto1 = self.curva.multiplicar_escalar(u1, self.curva.G)
        punto2 = self.curva.multiplicar_escalar(u2, llave_publica)
        X = self.curva.sumar_puntos(punto1, punto2)
        
        # Si X es el punto en el infinito, la firma es inválida
        if X.es_infinito:
            return False
        
        # Paso 4: Verificar que x_X ≡ r (mod q)
        return (X.x % self.curva.q) == r
    
    def verificar_paso_a_paso(self, mensaje: str, firma: Tuple[int, int], 
                              llave_publica: PuntoElliptico, hash_valor: Optional[int] = None) -> Dict:
        """
        Verifica una firma ECDSA mostrando todos los pasos intermedios
        
        Args:
            mensaje: Mensaje original
            firma: Tupla (r, s)
            llave_publica: Llave pública Q
            hash_valor: Valor de hash pre-calculado (opcional, para ejemplos específicos)
        
        Returns:
            Diccionario con todos los pasos y el resultado final
        """
        r, s = firma
        pasos = {}
        
        # Paso 0: Verificar rango
        pasos['paso_0'] = {
            'titulo': 'Paso 0 - Verificar rango de r y s',
            'detalle': f'Verificar que 1 ≤ r, s ≤ q-1',
            'r': r,
            's': s,
            'q': self.curva.q,
            'rango_valido': (1 <= r <= self.curva.q - 1) and (1 <= s <= self.curva.q - 1),
            'explicacion': f'r = {r}, s = {s}, q-1 = {self.curva.q - 1}'
        }
        
        if not pasos['paso_0']['rango_valido']:
            pasos['resultado'] = {'valido': False, 'razon': 'r o s fuera de rango'}
            return pasos
        
        # Calcular hash
        if hash_valor is None:
            z = self.hash_mensaje(mensaje)
        else:
            z = hash_valor
        
        pasos['hash'] = {
            'titulo': 'Hash del mensaje',
            'mensaje': mensaje,
            'hash': z,
            'explicacion': f'H(M) = {z}'
        }
        
        # Paso 1: Calcular w = s^(-1) mod q
        w = self.curva.inverso_modular(s, self.curva.q)
        pasos['paso_1'] = {
            'titulo': 'Paso 1 - Calcular w = s⁻¹ mod q',
            's': s,
            'q': self.curva.q,
            'w': w,
            'verificacion': f'{s} × {w} ≡ {(s * w) % self.curva.q} ≡ 1 (mod {self.curva.q})',
            'explicacion': f'Necesitamos el inverso modular de s = {s} módulo q = {self.curva.q}\n'
                          f'Entonces w = {w}'
        }
        
        # Paso 2: Calcular u₁ y u₂
        u1 = (z * w) % self.curva.q
        u2 = (r * w) % self.curva.q
        pasos['paso_2'] = {
            'titulo': 'Paso 2 - Calcular u₁ = H(M)·w mod q  y  u₂ = r·w mod q',
            'u1_calculo': f'u₁ = {z} × {w} mod {self.curva.q} = {z * w} mod {self.curva.q} = {u1}',
            'u2_calculo': f'u₂ = {r} × {w} mod {self.curva.q} = {r * w} mod {self.curva.q} = {u2}',
            'u1': u1,
            'u2': u2
        }
        
        # Paso 3: Calcular X = u₁·G + u₂·Q
        punto1 = self.curva.multiplicar_escalar(u1, self.curva.G)
        punto2 = self.curva.multiplicar_escalar(u2, llave_publica)
        X = self.curva.sumar_puntos(punto1, punto2)
        
        pasos['paso_3'] = {
            'titulo': 'Paso 3 - Calcular el punto X = u₁·G + u₂·Q en la curva',
            'curva': f'y² = x³ + {self.curva.a}x + {self.curva.b} (mod {self.curva.p})',
            'G': str(self.curva.G),
            'Q': str(llave_publica),
            'u1': u1,
            'u2': u2,
            'u1G': str(punto1),
            'u2Q': str(punto2),
            'X': str(X),
            'explicacion': f'Multiplicaciones escalares y suma de puntos en la curva:\n'
                          f'u₁·G = {u1}·{self.curva.G} = {punto1}\n'
                          f'u₂·Q = {u2}·{llave_publica} = {punto2}\n'
                          f'X = {punto1} + {punto2} = {X}'
        }
        
        if X.es_infinito:
            pasos['resultado'] = {'valido': False, 'razon': 'X es el punto en el infinito'}
            return pasos
        
        # Paso 4: Verificar x_X ≡ r (mod q)
        x_X_mod_q = X.x % self.curva.q
        valido = (x_X_mod_q == r)
        
        pasos['paso_4'] = {
            'titulo': 'Paso 4 - Comprobar la igualdad de x_X mod q con r',
            'x_X': X.x,
            'q': self.curva.q,
            'x_X_mod_q': x_X_mod_q,
            'r': r,
            'igualdad': f'{x_X_mod_q} = {r}' if valido else f'{x_X_mod_q} ≠ {r}',
            'explicacion': f'La coordenada x de X es x_X = {X.x}\n'
                          f'x_X mod q = {X.x} mod {self.curva.q} = {x_X_mod_q}\n'
                          f'Esto {"coincide" if valido else "NO coincide"} con r = {r}'
        }
        
        pasos['resultado'] = {
            'valido': valido,
            'conclusion': '✓ La firma es VÁLIDA' if valido else '✗ La firma es INVÁLIDA'
        }
        
        return pasos


def crear_curva_ejemplo() -> CurvaEliptica:
    """
    Crea una curva elíptica de ejemplo más grande y realista:
    y² = x³ + 2x + 3 (mod 97)
    
    Nota: p=97 es un primo decente para demostración educativa
    (mucho más seguro que p=11, pero aún manejable para cálculos)
    """
    # Curva: y² = x³ + 2x + 3 (mod 97)
    # Generador G y orden q calculados para esta curva
    return CurvaEliptica(p=97, a=2, b=3, G=(3, 6), q=5)


def crear_curva_ejemplo_pequena() -> CurvaEliptica:
    """
    Crea la curva pequeña del ejemplo original (solo para referencia):
    y² = x³ + x + 10 (mod 11)
    G = (6, 1)
    q = 10
    
    ADVERTENCIA: Esta curva es SOLO educativa y MUY insegura.
    Usar crear_curva_ejemplo() en su lugar.
    """
    return CurvaEliptica(p=11, a=1, b=10, G=(6, 1), q=10)


def exportar_llave_publica(llave_publica: PuntoElliptico, curva: CurvaEliptica, 
                           nombre_archivo: str):
    """
    Exporta una llave pública en formato PEM profesional con Base64.
    Incluye tanto formato legible (educativo) como Base64 (profesional).
    """
    # Datos en formato legible
    datos_texto = (
        f"p={curva.p}\n"
        f"a={curva.a}\n"
        f"b={curva.b}\n"
        f"Gx={curva.G.x}\n"
        f"Gy={curva.G.y}\n"
        f"q={curva.q}\n"
        f"Qx={llave_publica.x}\n"
        f"Qy={llave_publica.y}"
    )
    
    # Codificar en Base64
    datos_base64 = base64.b64encode(datos_texto.encode('utf-8')).decode('utf-8')
    
    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        f.write("-----BEGIN ECDSA PUBLIC KEY-----\n")
        f.write(f"Format: ECDSA-Educational-v1\n")
        f.write(f"Encoding: Hybrid (Plain + Base64)\n")
        f.write(f"\n")
        f.write(f"# Readable Format (Educational)\n")
        f.write(f"p={curva.p}\n")
        f.write(f"a={curva.a}\n")
        f.write(f"b={curva.b}\n")
        f.write(f"Gx={curva.G.x}\n")
        f.write(f"Gy={curva.G.y}\n")
        f.write(f"q={curva.q}\n")
        f.write(f"Qx={llave_publica.x}\n")
        f.write(f"Qy={llave_publica.y}\n")
        f.write(f"\n")
        f.write(f"# Base64 Encoding (Professional)\n")
        f.write(f"{datos_base64}\n")
        f.write("-----END ECDSA PUBLIC KEY-----\n")


def importar_llave_publica(nombre_archivo: str) -> Tuple[PuntoElliptico, CurvaEliptica]:
    """
    Importa una llave pública desde un archivo en formato PEM.
    Compatible con formatos: antiguo (comentarios #), PEM simple, y PEM con Base64.
    
    Returns:
        (llave_publica, curva)
    """
    with open(nombre_archivo, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    datos = {}
    
    # Intentar decodificar Base64 si existe
    if "# Base64 Encoding" in contenido or "Base64:" in contenido:
        # Buscar la línea de Base64
        lineas_contenido = contenido.split('\n')
        for i, linea in enumerate(lineas_contenido):
            linea = linea.strip()
            # La línea Base64 debe venir después del header "# Base64 Encoding"
            if i > 0 and '# Base64' in lineas_contenido[i-1]:
                if linea and not linea.startswith('#') and not linea.startswith('-----'):
                    try:
                        # Decodificar Base64
                        datos_decodificados = base64.b64decode(linea).decode('utf-8')
                        # Parsear los datos decodificados
                        for dato_linea in datos_decodificados.split('\n'):
                            if '=' in dato_linea:
                                clave, valor = dato_linea.split('=', 1)
                                datos[clave] = int(valor)
                        break
                    except:
                        pass
    
    # Si no hay Base64 o falló, leer formato plano
    if not datos:
        for linea in contenido.split('\n'):
            linea = linea.strip()
            # Ignorar líneas vacías, comentarios, headers y metadatos
            if not linea or linea.startswith('#') or linea.startswith('-----') or linea.startswith('Format:') or linea.startswith('Encoding:'):
                continue
            if '=' in linea and ':' not in linea:
                partes = linea.split('=', 1)  # Split solo en el primer =
                if len(partes) == 2:
                    clave, valor = partes
                    try:
                        datos[clave] = int(valor)
                    except:
                        pass
    
    curva = CurvaEliptica(
        p=datos['p'],
        a=datos['a'],
        b=datos['b'],
        G=(datos['Gx'], datos['Gy']),
        q=datos['q']
    )
    
    llave_publica = PuntoElliptico(datos['Qx'], datos['Qy'])
    
    return llave_publica, curva


def exportar_llave_privada(llave_privada: int, curva: CurvaEliptica, nombre_archivo: str):
    """
    Exporta una llave privada en formato PEM profesional con Base64.
    ADVERTENCIA: Mantener este archivo seguro y privado.
    """
    # Datos en formato legible
    datos_texto = (
        f"p={curva.p}\n"
        f"a={curva.a}\n"
        f"b={curva.b}\n"
        f"Gx={curva.G.x}\n"
        f"Gy={curva.G.y}\n"
        f"q={curva.q}\n"
        f"d={llave_privada}"
    )
    
    # Codificar en Base64
    datos_base64 = base64.b64encode(datos_texto.encode('utf-8')).decode('utf-8')
    
    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        f.write("-----BEGIN ECDSA PRIVATE KEY-----\n")
        f.write(f"Format: ECDSA-Educational-v1\n")
        f.write(f"Encoding: Hybrid (Plain + Base64)\n")
        f.write(f"WARNING: Keep this file SECRET!\n")
        f.write(f"\n")
        f.write(f"# Readable Format (Educational)\n")
        f.write(f"p={curva.p}\n")
        f.write(f"a={curva.a}\n")
        f.write(f"b={curva.b}\n")
        f.write(f"Gx={curva.G.x}\n")
        f.write(f"Gy={curva.G.y}\n")
        f.write(f"q={curva.q}\n")
        f.write(f"d={llave_privada}\n")
        f.write(f"\n")
        f.write(f"# Base64 Encoding (Professional)\n")
        f.write(f"{datos_base64}\n")
        f.write("-----END ECDSA PRIVATE KEY-----\n")


def importar_llave_privada(nombre_archivo: str) -> Tuple[int, CurvaEliptica]:
    """
    Importa una llave privada desde un archivo en formato PEM.
    Compatible con formatos: antiguo (comentarios #), PEM simple, y PEM con Base64.
    
    Returns:
        (llave_privada, curva)
    """
    with open(nombre_archivo, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    datos = {}
    
    # Intentar decodificar Base64 si existe
    if "# Base64 Encoding" in contenido or "Base64:" in contenido:
        # Buscar la línea de Base64
        lineas_contenido = contenido.split('\n')
        for i, linea in enumerate(lineas_contenido):
            linea = linea.strip()
            # La línea Base64 debe venir después del header "# Base64 Encoding"
            if i > 0 and '# Base64' in lineas_contenido[i-1]:
                if linea and not linea.startswith('#') and not linea.startswith('-----'):
                    try:
                        # Decodificar Base64
                        datos_decodificados = base64.b64decode(linea).decode('utf-8')
                        # Parsear los datos decodificados
                        for dato_linea in datos_decodificados.split('\n'):
                            if '=' in dato_linea:
                                clave, valor = dato_linea.split('=', 1)
                                datos[clave] = int(valor)
                        break
                    except:
                        pass
    
    # Si no hay Base64 o falló, leer formato plano
    if not datos:
        for linea in contenido.split('\n'):
            linea = linea.strip()
            # Ignorar líneas vacías, comentarios, headers y metadatos
            if not linea or linea.startswith('#') or linea.startswith('-----') or linea.startswith('Format:') or linea.startswith('Encoding:') or linea.startswith('WARNING:'):
                continue
            if '=' in linea and ':' not in linea:
                partes = linea.split('=', 1)  # Split solo en el primer =
                if len(partes) == 2:
                    clave, valor = partes
                    try:
                        datos[clave] = int(valor)
                    except:
                        pass
    
    curva = CurvaEliptica(
        p=datos['p'],
        a=datos['a'],
        b=datos['b'],
        G=(datos['Gx'], datos['Gy']),
        q=datos['q']
    )
    
    llave_privada = datos['d']
    
    return llave_privada, curva
