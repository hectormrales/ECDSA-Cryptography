"""
Aplicación de escritorio para firma digital ECDSA
Interfaz gráfica con Tkinter

Autores: Betito, Alicia, Candy
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import sys
import os
import base64

# Agregar el directorio actual al path para importar ecdsa_core
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ecdsa_core import (
    CurvaEliptica, ECDSA, PuntoElliptico,
    exportar_llave_publica, importar_llave_publica,
    exportar_llave_privada, importar_llave_privada,
    crear_curva_ejemplo
)


class AplicacionECDSA:
    """
    Aplicación de escritorio para gestión de llaves y firmas ECDSA
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("ECDSA - Firma Digital con Curvas Elípticas")
        self.root.geometry("1000x750")
        
        # Variables de estado
        self.usuario_actual = tk.StringVar(value="Betito")
        self.usuarios = {
            "Betito": {"llave_privada": None, "llave_publica": None, "curva": None},
            "Alicia": {"llave_privada": None, "llave_publica": None, "curva": None},
            "Candy": {"llave_privada": None, "llave_publica": None, "curva": None}
        }
        
        # Curva por defecto (ejemplo de las imágenes)
        self.curva_defecto = crear_curva_ejemplo()
        
        # Configurar la interfaz
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea todos los elementos de la interfaz"""
        
        # Notebook (pestañas)
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Pestaña 1: Gestión de Llaves
        self.tab_llaves = ttk.Frame(notebook)
        notebook.add(self.tab_llaves, text="Gestión de Llaves")
        self.crear_tab_llaves()
        
        # Pestaña 2: Firmar Mensaje
        self.tab_firmar = ttk.Frame(notebook)
        notebook.add(self.tab_firmar, text="Firmar Mensaje")
        self.crear_tab_firmar()
        
        # Pestaña 3: Verificar Firma
        self.tab_verificar = ttk.Frame(notebook)
        notebook.add(self.tab_verificar, text="Verificar Firma")
        self.crear_tab_verificar()
        
        # Pestaña 4: Configurar Curva
        self.tab_curva = ttk.Frame(notebook)
        notebook.add(self.tab_curva, text="Configurar Curva")
        self.crear_tab_curva()
    
    def crear_tab_llaves(self):
        """Crea la pestaña de gestión de llaves"""
        
        # Frame superior: Selección de usuario
        frame_usuario = ttk.LabelFrame(self.tab_llaves, text="Seleccionar Usuario", padding=10)
        frame_usuario.pack(fill='x', padx=10, pady=10)
        
        for usuario in ["Betito", "Alicia", "Candy"]:
            rb = ttk.Radiobutton(frame_usuario, text=usuario, 
                                value=usuario, variable=self.usuario_actual,
                                command=self.actualizar_info_llaves)
            rb.pack(side='left', padx=20)
        
        # Frame medio: Información de llaves
        frame_info = ttk.LabelFrame(self.tab_llaves, text="Información de Llaves", padding=10)
        frame_info.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.texto_info_llaves = scrolledtext.ScrolledText(frame_info, height=15, width=80)
        self.texto_info_llaves.pack(fill='both', expand=True)
        
        # Frame inferior: Botones de acción
        frame_botones = ttk.Frame(self.tab_llaves, padding=10)
        frame_botones.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(frame_botones, text="Generar Nuevo Par de Llaves", 
                  command=self.generar_llaves).pack(side='left', padx=5)
        ttk.Button(frame_botones, text="Exportar Llave Pública", 
                  command=self.exportar_publica).pack(side='left', padx=5)
        ttk.Button(frame_botones, text="Exportar Llave Privada", 
                  command=self.exportar_privada).pack(side='left', padx=5)
        ttk.Button(frame_botones, text="Importar Llave Pública", 
                  command=self.importar_publica).pack(side='left', padx=5)
        ttk.Button(frame_botones, text="Importar Llave Privada", 
                  command=self.importar_privada).pack(side='left', padx=5)
        
        # Actualizar información inicial
        self.actualizar_info_llaves()
    
    def crear_tab_firmar(self):
        """Crea la pestaña de firma de mensajes"""
        
        # Frame superior: Usuario
        frame_usuario = ttk.LabelFrame(self.tab_firmar, text="Usuario que Firma", padding=10)
        frame_usuario.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(frame_usuario, textvariable=self.usuario_actual, 
                 font=('Arial', 12, 'bold')).pack()
        
        # Frame medio: Mensaje
        frame_mensaje = ttk.LabelFrame(self.tab_firmar, text="Mensaje a Firmar", padding=10)
        frame_mensaje.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.texto_mensaje_firmar = scrolledtext.ScrolledText(frame_mensaje, height=5, width=80)
        self.texto_mensaje_firmar.pack(fill='both', expand=True)
        
        # Frame inferior: Firma
        frame_firma = ttk.LabelFrame(self.tab_firmar, text="Firma Generada (r, s)", padding=10)
        frame_firma.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.texto_firma = scrolledtext.ScrolledText(frame_firma, height=8, width=80)
        self.texto_firma.pack(fill='both', expand=True)
        
        # Botones
        frame_botones = ttk.Frame(self.tab_firmar, padding=10)
        frame_botones.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(frame_botones, text="Firmar Mensaje", 
                  command=self.firmar_mensaje).pack(side='left', padx=5)
        ttk.Button(frame_botones, text="Guardar Firma", 
                  command=self.guardar_firma).pack(side='left', padx=5)
    
    def crear_tab_verificar(self):
        """Crea la pestaña de verificación de firmas"""
        
        # Frame: Mensaje
        frame_mensaje = ttk.LabelFrame(self.tab_verificar, text="Mensaje Original", padding=10)
        frame_mensaje.pack(fill='x', padx=10, pady=10)
        
        self.texto_mensaje_verificar = scrolledtext.ScrolledText(frame_mensaje, height=3, width=80)
        self.texto_mensaje_verificar.pack(fill='both', expand=True)
        
        # Frame: Firma
        frame_firma_ver = ttk.LabelFrame(self.tab_verificar, text="Firma (r, s)", padding=10)
        frame_firma_ver.pack(fill='x', padx=10, pady=10)
        
        frame_rs = ttk.Frame(frame_firma_ver)
        frame_rs.pack(fill='x')
        
        ttk.Label(frame_rs, text="r:").pack(side='left', padx=5)
        self.entry_r = ttk.Entry(frame_rs, width=20)
        self.entry_r.pack(side='left', padx=5)
        
        ttk.Label(frame_rs, text="s:").pack(side='left', padx=5)
        self.entry_s = ttk.Entry(frame_rs, width=20)
        self.entry_s.pack(side='left', padx=5)
        
        ttk.Button(frame_rs, text="Cargar Firma desde Archivo", 
                  command=self.cargar_firma).pack(side='left', padx=10)
        
        # Frame: Llave pública del firmante
        frame_llave = ttk.LabelFrame(self.tab_verificar, text="Llave Pública del Firmante", padding=10)
        frame_llave.pack(fill='x', padx=10, pady=10)
        
        self.var_firmante = tk.StringVar(value="Betito")
        for usuario in ["Betito", "Alicia", "Candy", "Otra (importar)"]:
            rb = ttk.Radiobutton(frame_llave, text=usuario, 
                                value=usuario, variable=self.var_firmante)
            rb.pack(side='left', padx=10)
        
        # Checkbox para usar hash manual
        self.var_hash_manual = tk.BooleanVar(value=False)
        frame_hash = ttk.Frame(self.tab_verificar)
        frame_hash.pack(fill='x', padx=10, pady=5)
        
        ttk.Checkbutton(frame_hash, text="Usar valor de hash manual H(M):", 
                       variable=self.var_hash_manual).pack(side='left', padx=5)
        self.entry_hash = ttk.Entry(frame_hash, width=20)
        self.entry_hash.pack(side='left', padx=5)
        ttk.Label(frame_hash, text="(Para ejemplos específicos)").pack(side='left')
        
        # Frame: Resultado
        frame_resultado = ttk.LabelFrame(self.tab_verificar, text="Resultado de la Verificación", padding=10)
        frame_resultado.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.texto_verificacion = scrolledtext.ScrolledText(frame_resultado, height=15, width=80)
        self.texto_verificacion.pack(fill='both', expand=True)
        
        # Botones
        frame_botones = ttk.Frame(self.tab_verificar, padding=10)
        frame_botones.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(frame_botones, text="Verificar Firma (Paso a Paso)", 
                  command=self.verificar_firma).pack(side='left', padx=5)
    
    def crear_tab_curva(self):
        """Crea la pestaña de configuración de curva"""
        
        frame_info = ttk.LabelFrame(self.tab_curva, text="Curva Elíptica Actual", padding=10)
        frame_info.pack(fill='x', padx=10, pady=10)
        
        self.texto_curva = scrolledtext.ScrolledText(frame_info, height=8, width=80)
        self.texto_curva.pack(fill='both', expand=True)
        
        # Frame de parámetros
        frame_params = ttk.LabelFrame(self.tab_curva, text="Configurar Nueva Curva", padding=10)
        frame_params.pack(fill='x', padx=10, pady=10)
        
        # Entradas para parámetros
        params = [
            ("Primo p:", "p"),
            ("Coeficiente a:", "a"),
            ("Coeficiente b:", "b"),
            ("Generador Gx:", "Gx"),
            ("Generador Gy:", "Gy"),
            ("Orden q:", "q")
        ]
        
        self.entries_curva = {}
        for i, (label, key) in enumerate(params):
            row = i // 2
            col = (i % 2) * 2
            
            ttk.Label(frame_params, text=label).grid(row=row, column=col, padx=5, pady=5, sticky='e')
            entry = ttk.Entry(frame_params, width=15)
            entry.grid(row=row, column=col+1, padx=5, pady=5, sticky='w')
            self.entries_curva[key] = entry
        
        # Botones
        frame_botones = ttk.Frame(self.tab_curva, padding=10)
        frame_botones.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(frame_botones, text="Cargar Curva de Ejemplo (p=11)", 
                  command=self.cargar_curva_ejemplo).pack(side='left', padx=5)
        ttk.Button(frame_botones, text="Aplicar Curva", 
                  command=self.aplicar_curva).pack(side='left', padx=5)
        
        # Mostrar curva actual
        self.actualizar_info_curva()
    
    def actualizar_info_llaves(self):
        """Actualiza la información de llaves del usuario seleccionado"""
        usuario = self.usuario_actual.get()
        info = self.usuarios[usuario]
        
        self.texto_info_llaves.delete(1.0, tk.END)
        
        texto = f"=== INFORMACIÓN DE LLAVES DE {usuario.upper()} ===\n\n"
        
        if info['curva']:
            texto += f"Curva: y² = x³ + {info['curva'].a}x + {info['curva'].b} (mod {info['curva'].p})\n"
            texto += f"Generador G = {info['curva'].G}\n"
            texto += f"Orden q = {info['curva'].q}\n\n"
        
        if info['llave_privada']:
            texto += f"Llave Privada (d): {info['llave_privada']}\n\n"
        else:
            texto += "Llave Privada: No generada\n\n"
        
        if info['llave_publica']:
            texto += f"Llave Pública (Q): {info['llave_publica']}\n"
            if info['curva']:
                texto += f"Verificación: Q está en la curva = {info['curva'].esta_en_curva(info['llave_publica'])}\n"
        else:
            texto += "Llave Pública: No generada\n"
        
        self.texto_info_llaves.insert(1.0, texto)
    
    def actualizar_info_curva(self):
        """Actualiza la información de la curva actual"""
        curva = self.curva_defecto
        
        texto = f"=== CURVA ELÍPTICA ACTUAL ===\n\n"
        texto += f"Ecuación: y² = x³ + {curva.a}x + {curva.b} (mod {curva.p})\n\n"
        texto += f"Parámetros:\n"
        texto += f"  • Primo p = {curva.p}\n"
        texto += f"  • Coeficiente a = {curva.a}\n"
        texto += f"  • Coeficiente b = {curva.b}\n"
        texto += f"  • Punto generador G = {curva.G}\n"
        texto += f"  • Orden de G: q = {curva.q}\n"
        
        self.texto_curva.delete(1.0, tk.END)
        self.texto_curva.insert(1.0, texto)
    
    def generar_llaves(self):
        """Genera un nuevo par de llaves para el usuario actual"""
        usuario = self.usuario_actual.get()
        
        # Usar la curva actual
        curva = self.curva_defecto
        ecdsa = ECDSA(curva)
        
        # Generar llaves
        llave_privada, llave_publica = ecdsa.generar_llaves()
        
        # Guardar en el usuario
        self.usuarios[usuario]['llave_privada'] = llave_privada
        self.usuarios[usuario]['llave_publica'] = llave_publica
        self.usuarios[usuario]['curva'] = curva
        
        self.actualizar_info_llaves()
        messagebox.showinfo("Éxito", f"Par de llaves generado exitosamente para {usuario}")
    
    def exportar_publica(self):
        """Exporta la llave pública del usuario actual"""
        usuario = self.usuario_actual.get()
        info = self.usuarios[usuario]
        
        if not info['llave_publica']:
            messagebox.showerror("Error", "No hay llave pública para exportar")
            return
        
        nombre_archivo = filedialog.asksaveasfilename(
            defaultextension=".pem",
            filetypes=[("Archivos PEM", "*.pem"), ("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")],
            initialfile=f"llave_publica_{usuario}.pem"
        )
        
        if nombre_archivo:
            exportar_llave_publica(info['llave_publica'], info['curva'], nombre_archivo)
            messagebox.showinfo("Éxito", f"Llave pública exportada a:\n{nombre_archivo}")
    
    def exportar_privada(self):
        """Exporta la llave privada del usuario actual"""
        usuario = self.usuario_actual.get()
        info = self.usuarios[usuario]
        
        if not info['llave_privada']:
            messagebox.showerror("Error", "No hay llave privada para exportar")
            return
        
        # Advertencia de seguridad
        respuesta = messagebox.askyesno(
            "Advertencia de Seguridad",
            "¡ADVERTENCIA!\n\n"
            "La llave privada debe mantenerse en secreto.\n"
            "Solo exporta si sabes lo que estás haciendo.\n\n"
            "¿Deseas continuar?"
        )
        
        if not respuesta:
            return
        
        nombre_archivo = filedialog.asksaveasfilename(
            defaultextension=".pem",
            filetypes=[("Archivos PEM", "*.pem"), ("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")],
            initialfile=f"llave_privada_{usuario}.pem"
        )
        
        if nombre_archivo:
            exportar_llave_privada(info['llave_privada'], info['curva'], nombre_archivo)
            messagebox.showinfo("Éxito", f"Llave privada exportada a:\n{nombre_archivo}")
    
    def importar_publica(self):
        """Importa una llave pública"""
        nombre_archivo = filedialog.askopenfilename(
            filetypes=[("Archivos PEM", "*.pem"), ("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        
        if nombre_archivo:
            try:
                llave_publica, curva = importar_llave_publica(nombre_archivo)
                
                usuario = self.usuario_actual.get()
                self.usuarios[usuario]['llave_publica'] = llave_publica
                self.usuarios[usuario]['curva'] = curva
                
                self.actualizar_info_llaves()
                messagebox.showinfo("Éxito", f"Llave pública importada para {usuario}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al importar llave pública:\n{e}")
    
    def importar_privada(self):
        """Importa una llave privada"""
        nombre_archivo = filedialog.askopenfilename(
            filetypes=[("Archivos PEM", "*.pem"), ("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        
        if nombre_archivo:
            try:
                llave_privada, curva = importar_llave_privada(nombre_archivo)
                
                usuario = self.usuario_actual.get()
                self.usuarios[usuario]['llave_privada'] = llave_privada
                self.usuarios[usuario]['curva'] = curva
                
                # Calcular llave pública
                ecdsa = ECDSA(curva)
                llave_publica = curva.multiplicar_escalar(llave_privada, curva.G)
                self.usuarios[usuario]['llave_publica'] = llave_publica
                
                self.actualizar_info_llaves()
                messagebox.showinfo("Éxito", f"Llave privada importada para {usuario}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al importar llave privada:\n{e}")
    
    def firmar_mensaje(self):
        """Firma un mensaje con la llave privada del usuario actual"""
        usuario = self.usuario_actual.get()
        info = self.usuarios[usuario]
        
        if not info['llave_privada']:
            messagebox.showerror("Error", f"{usuario} no tiene llave privada.\nGenera o importa una primero.")
            return
        
        mensaje = self.texto_mensaje_firmar.get(1.0, tk.END).strip()
        if not mensaje:
            messagebox.showerror("Error", "Por favor ingresa un mensaje para firmar")
            return
        
        try:
            ecdsa = ECDSA(info['curva'])
            r, s = ecdsa.firmar(mensaje, info['llave_privada'])
            
            # Formato simple: solo mensaje y firma en Base64
            firma_texto = f"r={r}\ns={s}"
            firma_base64 = base64.b64encode(firma_texto.encode('utf-8')).decode('utf-8')
            
            resultado = f"{mensaje}\n{firma_base64}"
            
            self.texto_firma.delete(1.0, tk.END)
            self.texto_firma.insert(1.0, resultado)
            
            messagebox.showinfo("Éxito", "Mensaje firmado exitosamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al firmar mensaje:\n{e}")
    
    def guardar_firma(self):
        """Guarda la firma actual en un archivo"""
        texto_firma = self.texto_firma.get(1.0, tk.END).strip()
        if not texto_firma:
            messagebox.showerror("Error", "No hay firma para guardar")
            return
        
        nombre_archivo = filedialog.asksaveasfilename(
            defaultextension=".sig",
            filetypes=[("Archivos de firma", "*.sig"), ("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")],
            initialfile="firma.sig"
        )
        
        if nombre_archivo:
            with open(nombre_archivo, 'w', encoding='utf-8') as f:
                f.write(texto_firma)
            messagebox.showinfo("Éxito", f"Firma guardada en:\n{nombre_archivo}")
    
    def cargar_firma(self):
        """Carga una firma desde un archivo"""
        nombre_archivo = filedialog.askopenfilename(
            filetypes=[("Archivos de firma", "*.sig"), ("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        
        if nombre_archivo:
            try:
                with open(nombre_archivo, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                
                lineas = contenido.strip().split('\n')
                
                # Formato nuevo: primera línea = mensaje, segunda línea = Base64
                if len(lineas) >= 2:
                    # Decodificar Base64 de la última línea
                    firma_base64 = lineas[-1].strip()
                    firma_decodificada = base64.b64decode(firma_base64).decode('utf-8')
                    
                    # Parsear r y s
                    for linea in firma_decodificada.split('\n'):
                        if linea.startswith('r='):
                            r = linea.split('=')[1].strip()
                            self.entry_r.delete(0, tk.END)
                            self.entry_r.insert(0, r)
                        elif linea.startswith('s='):
                            s = linea.split('=')[1].strip()
                            self.entry_s.delete(0, tk.END)
                            self.entry_s.insert(0, s)
                
                messagebox.showinfo("Éxito", "Firma cargada desde archivo")
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar firma:\n{e}")
    
    def verificar_firma(self):
        """Verifica una firma paso a paso"""
        mensaje = self.texto_mensaje_verificar.get(1.0, tk.END).strip()
        if not mensaje:
            messagebox.showerror("Error", "Por favor ingresa el mensaje original")
            return
        
        try:
            r = int(self.entry_r.get())
            s = int(self.entry_s.get())
        except ValueError:
            messagebox.showerror("Error", "r y s deben ser números enteros")
            return
        
        # Obtener llave pública del firmante
        firmante = self.var_firmante.get()
        
        if firmante == "Otra (importar)":
            messagebox.showinfo("Importar", "Por favor importa la llave pública del firmante en la pestaña 'Gestión de Llaves'")
            return
        
        info = self.usuarios[firmante]
        if not info['llave_publica']:
            messagebox.showerror("Error", f"{firmante} no tiene llave pública.\nImporta o genera una primero.")
            return
        
        try:
            ecdsa = ECDSA(info['curva'])
            
            # Verificar si usar hash manual
            hash_valor = None
            if self.var_hash_manual.get():
                try:
                    hash_valor = int(self.entry_hash.get())
                except ValueError:
                    messagebox.showerror("Error", "El valor de hash debe ser un número entero")
                    return
            
            # Verificar paso a paso
            pasos = ecdsa.verificar_paso_a_paso(mensaje, (r, s), info['llave_publica'], hash_valor)
            
            # Mostrar resultado
            resultado = f"=== VERIFICACIÓN DE FIRMA ECDSA PASO A PASO ===\n\n"
            resultado += f"Firmante: {firmante}\n"
            resultado += f"Mensaje: {mensaje}\n"
            resultado += f"Firma: (r={r}, s={s})\n\n"
            
            # Datos de la curva
            resultado += f"Curva: y² = x³ + {info['curva'].a}x + {info['curva'].b} (mod {info['curva'].p})\n"
            resultado += f"Generador G = {info['curva'].G}\n"
            resultado += f"Llave pública Q = {info['llave_publica']}\n"
            resultado += f"Orden q = {info['curva'].q}\n\n"
            
            resultado += "=" * 60 + "\n\n"
            
            # Mostrar cada paso
            for key in ['paso_0', 'hash', 'paso_1', 'paso_2', 'paso_3', 'paso_4']:
                if key in pasos:
                    paso = pasos[key]
                    resultado += f"{paso['titulo']}\n"
                    resultado += "-" * 60 + "\n"
                    
                    # Manejar diferentes formatos de explicación
                    if 'explicacion' in paso:
                        resultado += f"{paso['explicacion']}\n\n"
                    elif key == 'paso_2':
                        # paso_2 tiene u1_calculo y u2_calculo en vez de explicacion
                        resultado += f"{paso['u1_calculo']}\n"
                        resultado += f"{paso['u2_calculo']}\n\n"
                    else:
                        # Otros formatos si existen
                        resultado += "\n"
            
            # Resultado final
            resultado += "=" * 60 + "\n"
            resultado += f"RESULTADO FINAL: {pasos['resultado']['conclusion']}\n"
            resultado += "=" * 60 + "\n"
            
            self.texto_verificacion.delete(1.0, tk.END)
            self.texto_verificacion.insert(1.0, resultado)
            
            if pasos['resultado']['valido']:
                messagebox.showinfo("Verificación", "✓ La firma es VÁLIDA")
            else:
                messagebox.showwarning("Verificación", "✗ La firma es INVÁLIDA")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al verificar firma:\n{e}")
    
    def cargar_curva_ejemplo(self):
        """Carga los parámetros de la curva de ejemplo"""
        curva = crear_curva_ejemplo()
        
        self.entries_curva['p'].delete(0, tk.END)
        self.entries_curva['p'].insert(0, str(curva.p))
        
        self.entries_curva['a'].delete(0, tk.END)
        self.entries_curva['a'].insert(0, str(curva.a))
        
        self.entries_curva['b'].delete(0, tk.END)
        self.entries_curva['b'].insert(0, str(curva.b))
        
        self.entries_curva['Gx'].delete(0, tk.END)
        self.entries_curva['Gx'].insert(0, str(curva.G.x))
        
        self.entries_curva['Gy'].delete(0, tk.END)
        self.entries_curva['Gy'].insert(0, str(curva.G.y))
        
        self.entries_curva['q'].delete(0, tk.END)
        self.entries_curva['q'].insert(0, str(curva.q))
    
    def aplicar_curva(self):
        """Aplica los parámetros de curva ingresados"""
        try:
            p = int(self.entries_curva['p'].get())
            a = int(self.entries_curva['a'].get())
            b = int(self.entries_curva['b'].get())
            Gx = int(self.entries_curva['Gx'].get())
            Gy = int(self.entries_curva['Gy'].get())
            q = int(self.entries_curva['q'].get())
            
            self.curva_defecto = CurvaEliptica(p, a, b, (Gx, Gy), q)
            self.actualizar_info_curva()
            
            messagebox.showinfo("Éxito", "Curva actualizada exitosamente")
        except ValueError as e:
            messagebox.showerror("Error", f"Error en los parámetros:\n{e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear curva:\n{e}")


def main():
    """Función principal"""
    root = tk.Tk()
    app = AplicacionECDSA(root)
    root.mainloop()


if __name__ == "__main__":
    main()
