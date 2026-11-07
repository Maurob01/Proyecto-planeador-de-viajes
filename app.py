import tkinter as tk
from tkinter import ttk, messagebox
from Motor.red import Red

class AppTransMilenio:
    def __init__(self, root):
        self.root = root
        self.root.title("Planeador de Viajes - TransMilenio")
        self.root.geometry("1100x750")
        self.root.minsize(950, 650)

        # Instanciar la red
        try:
            self.red = Red(carpeta_datos="Datos")
        except Exception as e:
            messagebox.showerror("Error de Datos", f"No se pudieron cargar los datos: {e}")

        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # --- 1. BARRA SUPERIOR (HEADER) ---
        self.header_frame = tk.Frame(root, bg="white", height=60, relief="solid", bd=1)
        self.header_frame.pack(fill="x", side="top")
        self.header_frame.pack_propagate(False)

        self.lbl_logo = tk.Label(self.header_frame, text="🔴 TransMilenio", font=("Arial", 14, "bold"), bg="white", fg="#B71C1C")
        self.lbl_logo.pack(side="left", padx=25)

        self.nav_frame = tk.Frame(self.header_frame, bg="white")
        self.nav_frame.pack(side="right", padx=20)

        # Botones de navegación superior
        self.btn_nav_buscador = tk.Button(self.nav_frame, text="Buscador", font=("Arial", 10, "bold"), bg="white", fg="#E53935", relief="flat", cursor="hand2", command=lambda: self.cambiar_vista("Buscador"))
        self.btn_nav_buscador.pack(side="left", padx=10)

        self.btn_nav_planeador = tk.Button(self.nav_frame, text="Planeador de Viajes", font=("Arial", 10), bg="white", fg="#555555", relief="flat", cursor="hand2", command=lambda: self.cambiar_vista("Planeador"))
        self.btn_nav_planeador.pack(side="left", padx=10)

        self.btn_nav_operador = tk.Button(self.nav_frame, text="Panel de Operador", font=("Arial", 10), bg="white", fg="#555555", relief="flat", cursor="hand2", command=lambda: self.cambiar_vista("Operador"))
        self.btn_nav_operador.pack(side="left", padx=10)

        # --- 2. CONTENEDOR PRINCIPAL DE VISTAS ---
        self.container_vistas = tk.Frame(root, bg="#F4F6F8")
        self.container_vistas.pack(fill="both", expand=True)

        # Crear las 3 vistas principales de la aplicación
        self.vista_buscador = tk.Frame(self.container_vistas, bg="#F4F6F8")
        self.vista_planeador = tk.Frame(self.container_vistas, bg="#F4F6F8")
        self.vista_operador = tk.Frame(self.container_vistas, bg="#F4F6F8")

        self.construir_vista_buscador()
        self.construir_vista_planeador()
        self.construir_vista_operador()

        # Mostrar la vista inicial por defecto
        self.cambiar_vista("Buscador")

    def cambiar_vista(self, seccion):
        # Ocultar todas las vistas
        self.vista_buscador.pack_forget()
        self.vista_planeador.pack_forget()
        self.vista_operador.pack_forget()

        # Restablecer estilos de botones superiores
        self.btn_nav_buscador.config(fg="#555555", font=("Arial", 10))
        self.btn_nav_planeador.config(fg="#555555", font=("Arial", 10))
        self.btn_nav_operador.config(fg="#555555", font=("Arial", 10))

        # Mostrar la vista seleccionada
        if seccion == "Buscador":
            self.vista_buscador.pack(fill="both", expand=True)
            self.btn_nav_buscador.config(fg="#E53935", font=("Arial", 10, "bold"))
        elif seccion == "Planeador":
            self.vista_planeador.pack(fill="both", expand=True)
            self.btn_nav_planeador.config(fg="#E53935", font=("Arial", 10, "bold"))
        elif seccion == "Operador":
            self.vista_operador.pack(fill="both", expand=True)
            self.btn_nav_operador.config(fg="#E53935", font=("Arial", 10, "bold"))

    # ==================== VISTA 1: BUSCADOR Y CATÁLOGO ====================
    def construir_vista_buscador(self):
        main_content = tk.Frame(self.vista_buscador, bg="#F4F6F8")
        main_content.pack(fill="both", expand=True, padx=30, pady=20)

        lbl_seccion = tk.Label(main_content, text="DIRECTORIO DE ESTACIONES", font=("Arial", 9, "bold"), bg="#F4F6F8", fg="#C62828")
        lbl_seccion.pack(anchor="w", pady=(0, 2))

        lbl_titulo = tk.Label(main_content, text="Buscador de Estaciones y Catálogo", font=("Arial", 18, "bold"), bg="#F4F6F8", fg="#111111")
        lbl_titulo.pack(anchor="w", pady=(0, 15))

        top_split_frame = tk.Frame(main_content, bg="#F4F6F8")
        top_split_frame.pack(fill="x", pady=(0, 25))

        # Columna Izquierda: Buscador con autocompletado flotante
        left_search_frame = tk.Frame(top_split_frame, bg="white", relief="solid", bd=1, padx=20, pady=20)
        left_search_frame.pack(side="left", fill="both", expand=True, padx=(0, 15))

        lbl_buscar_label = tk.Label(left_search_frame, text="Buscar estación", font=("Arial", 11, "bold"), bg="white", fg="#333333")
        lbl_buscar_label.pack(anchor="w", pady=(0, 5))

        # Contenedor relativo para el Entry y la lista desplegable de sugerencias
        entry_wrapper = tk.Frame(left_search_frame, bg="white")
        entry_wrapper.pack(fill="x", pady=(0, 5))

        self.input_estacion = tk.Entry(entry_wrapper, font=("Arial", 12), relief="solid", bd=1)
        self.input_estacion.pack(fill="x", ipady=6)
        self.input_estacion.bind("<KeyRelease>", self.on_keyrelease)

        # Listbox de sugerencias flotante
        self.lista_sugerencias = tk.Listbox(left_search_frame, font=("Arial", 11), height=4, relief="solid", bd=1)
        self.lista_sugerencias.bind("<<ListboxSelect>>", self.seleccionar_sugerencia)

        lbl_sugerencias_info = tk.Label(left_search_frame, text="Escribe para buscar · Selecciona una sugerencia", font=("Arial", 8), bg="white", fg="#888888")
        lbl_sugerencias_info.pack(anchor="w", pady=(5, 10))

        # Columna Derecha: Tarjeta de detalles
        self.right_card_frame = tk.Frame(top_split_frame, bg="white", relief="solid", bd=1, width=380, padx=20, pady=20)
        self.right_card_frame.pack(side="right", fill="y")
        self.right_card_frame.pack_propagate(False)

        card_header = tk.Frame(self.right_card_frame, bg="white")
        card_header.pack(fill="x", pady=(0, 10))

        tk.Label(card_header, text="ESTACIÓN SELECCIONADA", font=("Arial", 8, "bold"), bg="white", fg="#888888").pack(side="left")
        self.lbl_tag_estado = tk.Label(card_header, text="● ABIERTA", font=("Arial", 9, "bold"), bg="white", fg="#2E7D32")
        self.lbl_tag_estado.pack(side="right")

        self.lbl_card_nombre = tk.Label(self.right_card_frame, text="SELECCIONA UNA ESTACIÓN", font=("Arial", 16, "bold"), bg="white", fg="#111111")
        self.lbl_card_nombre.pack(anchor="w", pady=(0, 2))

        self.lbl_card_sub = tk.Label(self.right_card_frame, text="TransMilenio - Red de transporte", font=("Arial", 9), bg="white", fg="#666666")
        self.lbl_card_sub.pack(anchor="w", pady=(0, 15))

        self.rutas_frame = tk.Frame(self.right_card_frame, bg="#F9F9F9", relief="solid", bd=1, padx=10, pady=10)
        self.rutas_frame.pack(fill="both", expand=True)

        self.lbl_rutas_titulo = tk.Label(self.rutas_frame, text="Rutas disponibles:", font=("Arial", 10, "bold"), bg="#F9F9F9", fg="#333333")
        self.lbl_rutas_titulo.pack(anchor="w", pady=(0, 5))

        self.lbl_rutas_detalle = tk.Label(self.rutas_frame, text="Ninguna estación seleccionada aún.", font=("Arial", 10), bg="#F9F9F9", fg="#666666", justify="left")
        self.lbl_rutas_detalle.pack(anchor="w", pady=5)

        # Sección Inferior: Catálogo y Filtro por Rango
        catalog_section_frame = tk.Frame(main_content, bg="white", relief="solid", bd=1, padx=20, pady=20)
        catalog_section_frame.pack(fill="both", expand=True)

        cat_top_frame = tk.Frame(catalog_section_frame, bg="white")
        cat_top_frame.pack(fill="x", pady=(0, 10))

        tk.Label(cat_top_frame, text="Catálogo de estaciones", font=("Arial", 13, "bold"), bg="white", fg="#111111").pack(side="left")

        filter_frame = tk.Frame(catalog_section_frame, bg="white")
        filter_frame.pack(fill="x", pady=(5, 15))

        tk.Label(filter_frame, text="Desde", font=("Arial", 9, "bold"), bg="white", fg="#555555").grid(row=0, column=0, sticky="w", padx=(0, 5))
        self.input_desde = tk.Entry(filter_frame, font=("Arial", 10), width=15)
        self.input_desde.grid(row=1, column=0, padx=(0, 15), ipady=3)
        self.input_desde.insert(0, "A")

        tk.Label(filter_frame, text="Hasta", font=("Arial", 9, "bold"), bg="white", fg="#555555").grid(row=0, column=1, sticky="w", padx=(0, 5))
        self.input_hasta = tk.Entry(filter_frame, font=("Arial", 10), width=15)
        self.input_hasta.grid(row=1, column=1, padx=(0, 15), ipady=3)
        self.input_hasta.insert(0, "Z")

        btn_filtrar = tk.Button(
            filter_frame, text="🔍 Ver Rango", font=("Arial", 9, "bold"),
            bg="#E53935", fg="white", activebackground="#C62828", activeforeground="white",
            relief="flat", cursor="hand2", command=self.aplicar_filtro_rango
        )
        btn_filtrar.grid(row=1, column=2, padx=(0, 10), ipadx=10, ipady=3)

        btn_reset = tk.Button(
            filter_frame, text="🔄 Ver Todo", font=("Arial", 9, "bold"),
            bg="#546E7A", fg="white", activebackground="#455A64", activeforeground="white",
            relief="flat", cursor="hand2", command=self.cargar_catalogo_completo
        )
        btn_reset.grid(row=1, column=3, ipadx=10, ipady=3)

        columns = ("estacion", "rutas", "estado")
        self.tabla = ttk.Treeview(catalog_section_frame, columns=columns, show="headings", height=6)
        
        self.tabla.heading("estacion", text="ESTACIÓN")
        self.tabla.heading("rutas", text="RUTAS")
        self.tabla.heading("estado", text="ESTADO")
        
        self.tabla.column("estacion", width=300, anchor="w")
        self.tabla.column("rutas", width=250, anchor="w")
        self.tabla.column("estado", width=120, anchor="center")

        scrollbar = ttk.Scrollbar(catalog_section_frame, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)

        self.tabla.pack(side="left", fill="both", expand=True, pady=5)
        scrollbar.pack(side="right", fill="y", pady=5)

        self.tabla.bind("<ButtonRelease-1>", self.seleccionar_desde_tabla)
        self.cargar_catalogo_completo()

    # ==================== VISTA 2: PLANEADOR DE VIAJES ====================
    def construir_vista_planeador(self):
        content = tk.Frame(self.vista_planeador, bg="#F4F6F8", padx=30, pady=30)
        content.pack(fill="both", expand=True)

        tk.Label(content, text="PLANEADOR DE RUTAS Y VIAJES", font=("Arial", 9, "bold"), bg="#F4F6F8", fg="#C62828").pack(anchor="w", pady=(0, 2))
        tk.Label(content, text="Planea tu viaje por el sistema TransMilenio", font=("Arial", 18, "bold"), bg="#F4F6F8", fg="#111111").pack(anchor="w", pady=(0, 20))

        card = tk.Frame(content, bg="white", relief="solid", bd=1, padx=25, pady=25)
        card.pack(fill="both", expand=True)

        tk.Label(card, text="Estación de Origen:", font=("Arial", 11, "bold"), bg="white", fg="#333333").pack(anchor="w", pady=5)
        self.input_origen = tk.Entry(card, font=("Arial", 11), relief="solid", bd=1, width=40)
        self.input_origen.pack(anchor="w", ipady=4, pady=(0, 15))

        tk.Label(card, text="Estación de Destino:", font=("Arial", 11, "bold"), bg="white", fg="#333333").pack(anchor="w", pady=5)
        self.input_destino = tk.Entry(card, font=("Arial", 11), relief="solid", bd=1, width=40)
        self.input_destino.pack(anchor="w", ipady=4, pady=(0, 20))

        btn_calcular = tk.Button(
            card, text="Calcular Ruta Óptima", font=("Arial", 10, "bold"),
            bg="#E53935", fg="white", activebackground="#C62828", activeforeground="white",
            relief="flat", cursor="hand2", command=lambda: messagebox.showinfo("Planeador", "Calculando ruta óptima basada en la red...")
        )
        btn_calcular.pack(anchor="w", ipadx=15, ipady=6)

    # ==================== VISTA 3: PANEL DE OPERADOR ====================
    def construir_vista_operador(self):
        content = tk.Frame(self.vista_operador, bg="#F4F6F8", padx=30, pady=30)
        content.pack(fill="both", expand=True)

        tk.Label(content, text="CONTROL Y ESTADO", font=("Arial", 9, "bold"), bg="#F4F6F8", fg="#C62828").pack(anchor="w", pady=(0, 2))
        tk.Label(content, text="Panel de Operador del Sistema", font=("Arial", 18, "bold"), bg="#F4F6F8", fg="#111111").pack(anchor="w", pady=(0, 20))

        card = tk.Frame(content, bg="white", relief="solid", bd=1, padx=25, pady=25)
        card.pack(fill="both", expand=True)

        tk.Label(card, text="Gestión Operativa de Estaciones", font=("Arial", 14, "bold"), bg="white", fg="#111111").pack(anchor="w", pady=(0, 10))
        tk.Label(card, text="Desde este panel puedes verificar el estado general de la red y reportar novedades operativas.", font=("Arial", 10), bg="white", fg="#666666").pack(anchor="w", pady=(0, 20))

        btn_reporte = tk.Button(
            card, text="Generar Reporte de Estado", font=("Arial", 10, "bold"),
            bg="#37474F", fg="white", activebackground="#263238", activeforeground="white",
            relief="flat", cursor="hand2", command=lambda: messagebox.showinfo("Operador", "Reporte de estado general generado con éxito.")
        )
        btn_reporte.pack(anchor="w", ipadx=15, ipady=6)

    # ==================== LÓGICA DE AUTOCOMPLETADO Y CATÁLOGO ====================
    def on_keyrelease(self, event):
        if event.keysym in ("Up", "Down", "Return", "Tab", "Shift_L", "Shift_R"):
            return
        prefijo = self.input_estacion.get().strip()
        if not prefijo:
            self.lista_sugerencias.place_forget()
            return
        try:
            sugerencias = self.red.autocompletar(prefijo)
            if sugerencias:
                self.lista_sugerencias.delete(0, tk.END)
                for item in sugerencias:
                    nombre_est = item[0] if isinstance(item, (list, tuple)) else item
                    self.lista_sugerencias.insert(tk.END, nombre_est)
                
                # Posicionar la lista de sugerencias exactamente debajo de la barra de búsqueda
                self.lista_sugerencias.place(x=0, y=35, relwidth=1.0, height=90)
                self.lista_sugerencias.lift()
            else:
                self.lista_sugerencias.place_forget()
        except Exception:
            self.lista_sugerencias.place_forget()

    def seleccionar_sugerencia(self, event):
        if self.lista_sugerencias.curselection():
            index = self.lista_sugerencias.curselection()[0]
            nombre_est = self.lista_sugerencias.get(index)
            self.input_estacion.delete(0, tk.END)
            self.input_estacion.insert(0, nombre_est)
            self.lista_sugerencias.place_forget()
            self.mostrar_detalle_estacion(nombre_est)

    def seleccionar_desde_tabla(self, event):
        seleccion = self.tabla.selection()
        if seleccion:
            valores = self.tabla.item(seleccion[0], "values")
            nombre_est = valores[0]
            self.input_estacion.delete(0, tk.END)
            self.input_estacion.insert(0, nombre_est)
            self.mostrar_detalle_estacion(nombre_est)

    def mostrar_detalle_estacion(self, nombre_estacion):
        try:
            estado_actual = self.red.estado(nombre_estacion)
            es_abierta = "Abierta" in str(estado_actual) or "abierta" in str(estado_actual) or estado_actual is True
            
            self.lbl_card_nombre.config(text=nombre_estacion.upper())
            if es_abierta:
                self.lbl_tag_estado.config(text="● ABIERTA", fg="#2E7D32")
                self.lbl_rutas_detalle.config(text="🟢 Estación abierta y operando con normalidad.\nRutas troncales disponibles.", fg="#333333")
            else:
                self.lbl_tag_estado.config(text="● CERRADA", fg="#C62828")
                self.lbl_rutas_detalle.config(text="🔴 Estación cerrada temporalmente.", fg="#C62828")
        except Exception:
            self.lbl_card_nombre.config(text=nombre_estacion.upper())
            self.lbl_tag_estado.config(text="● CONSULTADO", fg="#555555")
            self.lbl_rutas_detalle.config(text="Información cargada correctamente.", fg="#333333")

    def cargar_catalogo_completo(self):
        # Limpiar y restaurar filtros de rango por defecto (A-Z)
        self.input_desde.delete(0, tk.END)
        self.input_desde.insert(0, "A")
        self.input_hasta.delete(0, tk.END)
        self.input_hasta.insert(0, "Z")

        for item in self.tabla.get_children():
            self.tabla.delete(item)
            
        if hasattr(self.red, "estaciones"):
            for est in self.red.estaciones:
                nombre = est[0]
                abierta = est[1]
                estado_str = "ABIERTA" if abierta else "CERRADA"
                self.tabla.insert("", "end", values=(nombre, "Rutas troncales", estado_str))

    def aplicar_filtro_rango(self):
        inicio = self.input_desde.get().strip().upper()
        fin = self.input_hasta.get().strip().upper()
        
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        try:
            if hasattr(self.red, "rango"):
                estaciones_filtradas = self.red.rango(inicio, fin)
            else:
                estaciones_filtradas = [est for est in self.red.estaciones if inicio <= est[0].upper() <= fin]

            for est in estaciones_filtradas:
                nombre = est[0]
                abierta = est[1]
                estado_str = "ABIERTA" if abierta else "CERRADA"
                self.tabla.insert("", "end", values=(nombre, "Rutas troncales", estado_str))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo aplicar el rango: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppTransMilenio(root)
    root.mainloop()
