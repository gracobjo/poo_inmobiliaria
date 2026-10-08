"""Interfaz gráfica dual Agente/Cliente con persistencia SQLite."""

from __future__ import annotations

import tkinter as tk
from datetime import date
from tkinter import messagebox, simpledialog, ttk
from typing import Any

from src.modelos.casa import Casa
from src.modelos.inquilino import Inquilino
from src.servicios.app_inmobiliaria import AppInmobiliaria
from src.utils.constantes import EstadoCasa


COLORES = {
    "fondo": "#F4F7F5",
    "panel": "#FFFFFF",
    "primario": "#0F3D3E",
    "acento": "#C45C26",
    "texto": "#1C2B2B",
    "suave": "#D9E5E2",
    "exito": "#2F6F4E",
}


class AppGrafica(tk.Tk):
    """Ventana principal con selección de rol y paneles Agente/Cliente."""

    def __init__(self, app: AppInmobiliaria | None = None) -> None:
        super().__init__()
        self.app = app or AppInmobiliaria()
        self.title("Sistema Inmobiliario POO")
        self.geometry("1040x680")
        self.minsize(920, 600)
        self.configure(bg=COLORES["fondo"])
        self._cliente_sesion: Inquilino | None = None

        self._configurar_estilo()
        self._contenedor = ttk.Frame(self, style="Fondo.TFrame")
        self._contenedor.pack(fill=tk.BOTH, expand=True)
        self.protocol("WM_DELETE_WINDOW", self._al_cerrar)
        self._mostrar_inicio()

    def _configurar_estilo(self) -> None:
        estilo = ttk.Style(self)
        try:
            estilo.theme_use("clam")
        except tk.TclError:
            pass
        estilo.configure("Fondo.TFrame", background=COLORES["fondo"])
        estilo.configure("Panel.TFrame", background=COLORES["panel"])
        estilo.configure(
            "Titulo.TLabel",
            background=COLORES["fondo"],
            foreground=COLORES["primario"],
            font=("Segoe UI Semibold", 22),
        )
        estilo.configure(
            "Sub.TLabel",
            background=COLORES["fondo"],
            foreground=COLORES["texto"],
            font=("Segoe UI", 11),
        )
        estilo.configure(
            "Panel.TLabel",
            background=COLORES["panel"],
            foreground=COLORES["texto"],
            font=("Segoe UI", 10),
        )
        estilo.configure(
            "Primario.TButton",
            font=("Segoe UI Semibold", 11),
            padding=10,
        )
        estilo.configure("Tool.TButton", font=("Segoe UI", 9), padding=6)

    def _limpiar(self) -> None:
        for hijo in self._contenedor.winfo_children():
            hijo.destroy()

    def _al_cerrar(self) -> None:
        self.app.cerrar()
        self.destroy()

    # ------------------------------------------------------------------
    # Pantalla de inicio
    # ------------------------------------------------------------------

    def _mostrar_inicio(self) -> None:
        self._limpiar()
        marco = ttk.Frame(self._contenedor, style="Fondo.TFrame", padding=40)
        marco.pack(fill=tk.BOTH, expand=True)

        ttk.Label(marco, text="Sistema Inmobiliario POO", style="Titulo.TLabel").pack(
            pady=(40, 8)
        )
        ttk.Label(
            marco,
            text="Elige tu perfil para continuar. Los datos se guardan en SQLite.",
            style="Sub.TLabel",
        ).pack(pady=(0, 28))

        botones = ttk.Frame(marco, style="Fondo.TFrame")
        botones.pack()
        ttk.Button(
            botones,
            text="Entrar como Agente",
            style="Primario.TButton",
            command=self._mostrar_agente,
        ).grid(row=0, column=0, padx=12, pady=8, ipadx=18)
        ttk.Button(
            botones,
            text="Entrar como Cliente",
            style="Primario.TButton",
            command=self._mostrar_cliente,
        ).grid(row=0, column=1, padx=12, pady=8, ipadx=18)

        ttk.Label(
            marco,
            text=f"Base de datos: {self.app.ruta_db}",
            style="Sub.TLabel",
        ).pack(side=tk.BOTTOM, pady=16)

    # ------------------------------------------------------------------
    # Panel Agente
    # ------------------------------------------------------------------

    def _mostrar_agente(self) -> None:
        self._limpiar()
        self.app.cargar()

        raiz = ttk.Frame(self._contenedor, style="Fondo.TFrame", padding=16)
        raiz.pack(fill=tk.BOTH, expand=True)

        cabecera = ttk.Frame(raiz, style="Fondo.TFrame")
        cabecera.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(cabecera, text="Backoffice · Agente", style="Titulo.TLabel").pack(
            side=tk.LEFT
        )
        ttk.Button(cabecera, text="Cambiar perfil", command=self._mostrar_inicio).pack(
            side=tk.RIGHT
        )

        cuerpo = ttk.Panedwindow(raiz, orient=tk.HORIZONTAL)
        cuerpo.pack(fill=tk.BOTH, expand=True)

        izq = ttk.Frame(cuerpo, style="Panel.TFrame", padding=10)
        der = ttk.Frame(cuerpo, style="Panel.TFrame", padding=10)
        cuerpo.add(izq, weight=3)
        cuerpo.add(der, weight=2)

        cols = ("id", "direccion", "localidad", "precio", "m2", "hab", "estado")
        self._tabla_agente = ttk.Treeview(izq, columns=cols, show="headings", height=18)
        encabezados = {
            "id": "ID",
            "direccion": "Dirección",
            "localidad": "Localidad",
            "precio": "Precio €",
            "m2": "m²",
            "hab": "Hab.",
            "estado": "Estado",
        }
        anchos = {"id": 40, "direccion": 180, "localidad": 90, "precio": 90, "m2": 50, "hab": 45, "estado": 100}
        for col in cols:
            self._tabla_agente.heading(col, text=encabezados[col])
            self._tabla_agente.column(col, width=anchos[col], anchor=tk.CENTER if col != "direccion" else tk.W)
        self._tabla_agente.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        scroll = ttk.Scrollbar(izq, orient=tk.VERTICAL, command=self._tabla_agente.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self._tabla_agente.configure(yscrollcommand=scroll.set)

        ttk.Label(der, text="Acciones", style="Panel.TLabel", font=("Segoe UI Semibold", 12)).pack(
            anchor=tk.W, pady=(0, 8)
        )
        acciones = [
            ("Nueva vivienda", self._agente_nueva),
            ("Reservar", self._agente_reservar),
            ("Liberar", self._agente_liberar),
            ("Comprar (venta)", self._agente_comprar),
            ("Alquilar…", self._agente_alquilar),
            ("Decorar…", self._agente_decorar),
            ("Reformar…", self._agente_reformar),
            ("Finalizar reforma", self._agente_fin_reforma),
            ("Ver informe cartera", self._agente_informe),
            ("Solicitudes de clientes", self._agente_solicitudes),
        ]
        for texto, comando in acciones:
            ttk.Button(der, text=texto, style="Tool.TButton", command=comando).pack(
                fill=tk.X, pady=3
            )

        self._lbl_valor = ttk.Label(der, text="", style="Panel.TLabel")
        self._lbl_valor.pack(anchor=tk.W, pady=(16, 0))
        self._refrescar_tabla_agente()

    def _refrescar_tabla_agente(self) -> None:
        self.app.cargar()
        for item in self._tabla_agente.get_children():
            self._tabla_agente.delete(item)
        for casa in self.app.gestion.propiedades:
            self._tabla_agente.insert(
                "",
                tk.END,
                iid=str(casa.id),
                values=(
                    casa.id,
                    casa.direccion,
                    casa.localidad,
                    f"{casa.precio:,.0f}",
                    f"{casa.metros_cuadrados:.0f}",
                    casa.habitaciones,
                    casa.estado.name,
                ),
            )
        self._lbl_valor.configure(
            text=(
                f"Propiedades: {len(self.app.gestion.propiedades)}\n"
                f"Valor cartera: {self.app.gestion.calcular_valor_cartera():,.2f} €"
            )
        )

    def _casa_seleccionada_agente(self) -> Casa | None:
        sel = self._tabla_agente.selection()
        if not sel:
            messagebox.showinfo("Selección", "Selecciona una vivienda en la tabla.")
            return None
        return self.app.obtener_casa(int(sel[0]))

    def _agente_nueva(self) -> None:
        datos = self._dialogo_nueva_casa()
        if not datos:
            return
        try:
            casa = Casa(**datos)
            self.app.agregar_casa(casa)
            self._refrescar_tabla_agente()
            messagebox.showinfo("Alta", f"Vivienda creada (id={casa.id}).")
        except (ValueError, TypeError) as error:
            messagebox.showerror("Error", str(error))

    def _dialogo_nueva_casa(self) -> dict[str, Any] | None:
        dialogo = tk.Toplevel(self)
        dialogo.title("Nueva vivienda")
        dialogo.transient(self)
        dialogo.grab_set()
        dialogo.configure(bg=COLORES["panel"])
        campos = {
            "direccion": tk.StringVar(),
            "codigo_postal": tk.StringVar(),
            "localidad": tk.StringVar(),
            "metros_cuadrados": tk.StringVar(value="70"),
            "precio": tk.StringVar(value="200000"),
            "habitaciones": tk.StringVar(value="2"),
        }
        etiquetas = [
            ("Dirección", "direccion"),
            ("Código postal", "codigo_postal"),
            ("Localidad", "localidad"),
            ("Metros cuadrados", "metros_cuadrados"),
            ("Precio €", "precio"),
            ("Habitaciones", "habitaciones"),
        ]
        for i, (label, clave) in enumerate(etiquetas):
            ttk.Label(dialogo, text=label, style="Panel.TLabel").grid(
                row=i, column=0, sticky=tk.W, padx=10, pady=6
            )
            ttk.Entry(dialogo, textvariable=campos[clave], width=36).grid(
                row=i, column=1, padx=10, pady=6
            )

        resultado: dict[str, Any] = {}

        def aceptar() -> None:
            try:
                resultado.update(
                    {
                        "direccion": campos["direccion"].get(),
                        "codigo_postal": campos["codigo_postal"].get(),
                        "localidad": campos["localidad"].get(),
                        "metros_cuadrados": float(campos["metros_cuadrados"].get()),
                        "precio": float(campos["precio"].get()),
                        "habitaciones": int(campos["habitaciones"].get()),
                    }
                )
                dialogo.destroy()
            except ValueError:
                messagebox.showerror("Error", "Revisa los valores numéricos.", parent=dialogo)

        ttk.Button(dialogo, text="Guardar", command=aceptar).grid(
            row=len(etiquetas), column=0, columnspan=2, pady=12
        )
        self.wait_window(dialogo)
        return resultado or None

    def _agente_reservar(self) -> None:
        casa = self._casa_seleccionada_agente()
        if casa is None:
            return
        try:
            casa.reservar()
            self.app.sincronizar(casa)
            self._refrescar_tabla_agente()
        except ValueError as error:
            messagebox.showerror("Error", str(error))

    def _agente_liberar(self) -> None:
        casa = self._casa_seleccionada_agente()
        if casa is None:
            return
        try:
            casa.liberar()
            self.app.sincronizar(casa)
            self._refrescar_tabla_agente()
        except ValueError as error:
            messagebox.showerror("Error", str(error))

    def _agente_comprar(self) -> None:
        casa = self._casa_seleccionada_agente()
        if casa is None:
            return
        try:
            total = casa.comprar()
            self.app.sincronizar(casa)
            self._refrescar_tabla_agente()
            messagebox.showinfo("Venta", f"Venta registrada. Total con AITP: {total:,.2f} €")
        except ValueError as error:
            messagebox.showerror("Error", str(error))

    def _agente_alquilar(self) -> None:
        casa = self._casa_seleccionada_agente()
        if casa is None:
            return
        try:
            nombre = simpledialog.askstring("Inquilino", "Nombre:", parent=self)
            dni = simpledialog.askstring("Inquilino", "DNI (8 dígitos + letra):", parent=self)
            telefono = simpledialog.askstring("Inquilino", "Teléfono:", parent=self)
            ingresos = simpledialog.askfloat("Inquilino", "Ingresos mensuales €:", parent=self, minvalue=1)
            renta = simpledialog.askfloat("Contrato", "Renta mensual €:", parent=self, minvalue=1)
            fianza = simpledialog.askfloat("Contrato", "Fianza €:", parent=self, minvalue=0)
            if None in (nombre, dni, telefono, ingresos, renta, fianza):
                return
            inquilino = Inquilino(nombre, dni, telefono, float(ingresos))
            casa.alquilar(
                inquilino,
                renta=float(renta),
                fianza=float(fianza),
                fecha_inicio=date.today(),
                meses=12,
            )
            self.app.sincronizar(casa)
            self._refrescar_tabla_agente()
            messagebox.showinfo("Alquiler", "Contrato creado y guardado en SQLite.")
        except (ValueError, TypeError) as error:
            messagebox.showerror("Error", str(error))

    def _agente_decorar(self) -> None:
        casa = self._casa_seleccionada_agente()
        if casa is None:
            return
        coste = simpledialog.askfloat("Decorar", "Coste €:", parent=self, minvalue=1)
        if coste is None:
            return
        try:
            total = casa.decorar(coste)
            self.app.sincronizar(casa)
            self._refrescar_tabla_agente()
            messagebox.showinfo("Decoración", f"Coste aplicado: {total:,.2f} €")
        except ValueError as error:
            messagebox.showerror("Error", str(error))

    def _agente_reformar(self) -> None:
        casa = self._casa_seleccionada_agente()
        if casa is None:
            return
        coste = simpledialog.askfloat("Reformar", "Coste base € (sin IVA):", parent=self, minvalue=1)
        if coste is None:
            return
        try:
            total = casa.reformar(coste)
            self.app.sincronizar(casa)
            self._refrescar_tabla_agente()
            messagebox.showinfo("Reforma", f"Coste con IVA: {total:,.2f} €")
        except ValueError as error:
            messagebox.showerror("Error", str(error))

    def _agente_fin_reforma(self) -> None:
        casa = self._casa_seleccionada_agente()
        if casa is None:
            return
        try:
            casa.finalizar_reforma()
            self.app.sincronizar(casa)
            self._refrescar_tabla_agente()
        except ValueError as error:
            messagebox.showerror("Error", str(error))

    def _agente_informe(self) -> None:
        informe = self.app.gestion.generar_informe_cartera()
        self._mostrar_texto("Informe de cartera", informe)

    def _agente_solicitudes(self) -> None:
        solicitudes = self.app.listar_solicitudes()
        if not solicitudes:
            messagebox.showinfo("Solicitudes", "No hay solicitudes registradas.")
            return
        lineas = []
        for s in solicitudes:
            lineas.append(
                f"#{s['id']} [{s['estado']}] {s['tipo']} — {s['nombre']} ({s['dni']})\n"
                f"  Vivienda: {s['direccion']} ({s['localidad']}) · {s['precio']:,.0f} €\n"
                f"  {s['mensaje'] or '(sin mensaje)'} · {s['fecha']}\n"
            )
        ventana = self._mostrar_texto("Solicitudes de clientes", "\n".join(lineas))
        ttk.Button(
            ventana,
            text="Marcar primera pendiente como ATENDIDA",
            command=lambda: self._atender_primera(ventana),
        ).pack(pady=6)

    def _atender_primera(self, ventana: tk.Toplevel) -> None:
        pendientes = self.app.listar_solicitudes(solo_pendientes=True)
        if not pendientes:
            messagebox.showinfo("Solicitudes", "No hay pendientes.", parent=ventana)
            return
        self.app.atender_solicitud(int(pendientes[0]["id"]))
        messagebox.showinfo("Solicitudes", f"Solicitud #{pendientes[0]['id']} atendida.", parent=ventana)
        ventana.destroy()
        self._agente_solicitudes()

    def _mostrar_texto(self, titulo: str, contenido: str) -> tk.Toplevel:
        ventana = tk.Toplevel(self)
        ventana.title(titulo)
        ventana.geometry("640x420")
        texto = tk.Text(ventana, wrap=tk.WORD, font=("Consolas", 10))
        texto.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        texto.insert(tk.END, contenido)
        texto.configure(state=tk.DISABLED)
        return ventana

    # ------------------------------------------------------------------
    # Panel Cliente
    # ------------------------------------------------------------------

    def _mostrar_cliente(self) -> None:
        self._limpiar()
        self.app.cargar()

        raiz = ttk.Frame(self._contenedor, style="Fondo.TFrame", padding=16)
        raiz.pack(fill=tk.BOTH, expand=True)

        cabecera = ttk.Frame(raiz, style="Fondo.TFrame")
        cabecera.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(cabecera, text="Portal · Cliente", style="Titulo.TLabel").pack(side=tk.LEFT)
        ttk.Button(cabecera, text="Cambiar perfil", command=self._mostrar_inicio).pack(
            side=tk.RIGHT
        )

        sesion = ttk.LabelFrame(raiz, text="Tu perfil", padding=10)
        sesion.pack(fill=tk.X, pady=(0, 10))
        self._cli_nombre = tk.StringVar(value=self._cliente_sesion.nombre if self._cliente_sesion else "")
        self._cli_dni = tk.StringVar(value=self._cliente_sesion.dni if self._cliente_sesion else "")
        self._cli_tel = tk.StringVar(value=self._cliente_sesion.telefono if self._cliente_sesion else "")
        self._cli_ingresos = tk.StringVar(
            value=str(int(self._cliente_sesion.ingresos)) if self._cliente_sesion else ""
        )
        for i, (label, var) in enumerate(
            [
                ("Nombre", self._cli_nombre),
                ("DNI", self._cli_dni),
                ("Teléfono", self._cli_tel),
                ("Ingresos €/mes", self._cli_ingresos),
            ]
        ):
            ttk.Label(sesion, text=label).grid(row=0, column=i * 2, padx=4, pady=4, sticky=tk.W)
            ttk.Entry(sesion, textvariable=var, width=16).grid(
                row=0, column=i * 2 + 1, padx=4, pady=4
            )
        ttk.Button(sesion, text="Guardar perfil", command=self._cliente_guardar_perfil).grid(
            row=0, column=8, padx=8
        )

        filtros = ttk.Frame(raiz, style="Fondo.TFrame")
        filtros.pack(fill=tk.X, pady=(0, 8))
        self._filtro_localidad = tk.StringVar()
        self._filtro_min = tk.StringVar()
        self._filtro_max = tk.StringVar()
        ttk.Label(filtros, text="Localidad").pack(side=tk.LEFT)
        ttk.Entry(filtros, textvariable=self._filtro_localidad, width=14).pack(
            side=tk.LEFT, padx=6
        )
        ttk.Label(filtros, text="Precio min").pack(side=tk.LEFT)
        ttk.Entry(filtros, textvariable=self._filtro_min, width=10).pack(side=tk.LEFT, padx=6)
        ttk.Label(filtros, text="Precio max").pack(side=tk.LEFT)
        ttk.Entry(filtros, textvariable=self._filtro_max, width=10).pack(side=tk.LEFT, padx=6)
        ttk.Button(filtros, text="Buscar disponibles", command=self._refrescar_tabla_cliente).pack(
            side=tk.LEFT, padx=8
        )

        cols = ("id", "direccion", "localidad", "precio", "m2", "hab", "eur_m2")
        self._tabla_cliente = ttk.Treeview(raiz, columns=cols, show="headings", height=14)
        for col, texto, ancho in [
            ("id", "ID", 40),
            ("direccion", "Dirección", 200),
            ("localidad", "Localidad", 100),
            ("precio", "Precio €", 100),
            ("m2", "m²", 60),
            ("hab", "Hab.", 50),
            ("eur_m2", "€/m²", 80),
        ]:
            self._tabla_cliente.heading(col, text=texto)
            self._tabla_cliente.column(col, width=ancho, anchor=tk.CENTER if col != "direccion" else tk.W)
        self._tabla_cliente.pack(fill=tk.BOTH, expand=True)

        acciones = ttk.Frame(raiz, style="Fondo.TFrame")
        acciones.pack(fill=tk.X, pady=10)
        ttk.Button(acciones, text="Ver detalle", command=self._cliente_detalle).pack(
            side=tk.LEFT, padx=4
        )
        ttk.Button(
            acciones, text="Solicitar visita", command=lambda: self._cliente_solicitud("VISITA")
        ).pack(side=tk.LEFT, padx=4)
        ttk.Button(
            acciones, text="Me interesa comprar", command=lambda: self._cliente_solicitud("COMPRA")
        ).pack(side=tk.LEFT, padx=4)
        ttk.Button(
            acciones, text="Me interesa alquilar", command=lambda: self._cliente_solicitud("ALQUILER")
        ).pack(side=tk.LEFT, padx=4)
        ttk.Button(
            acciones, text="Comprobar regla 35%", command=self._cliente_elegibilidad
        ).pack(side=tk.LEFT, padx=4)

        self._refrescar_tabla_cliente()

    def _cliente_guardar_perfil(self, *, silencioso: bool = False) -> bool:
        """Valida y guarda el perfil del cliente desde el formulario.

        Args:
            silencioso: Si es ``True``, no muestra el aviso de éxito.

        Returns:
            ``True`` si el perfil quedó guardado correctamente.
        """
        nombre = self._cli_nombre.get().strip()
        dni = self._cli_dni.get().strip()
        telefono = self._cli_tel.get().strip()
        ingresos_txt = self._cli_ingresos.get().strip()

        faltantes: list[str] = []
        if not nombre:
            faltantes.append("Nombre")
        if not dni:
            faltantes.append("DNI")
        if not telefono:
            faltantes.append("Teléfono")
        if not ingresos_txt:
            faltantes.append("Ingresos €/mes")
        if faltantes:
            messagebox.showwarning(
                "Perfil incompleto",
                "Antes de continuar, completa tu perfil:\n- " + "\n- ".join(faltantes),
            )
            return False

        try:
            ingresos = float(ingresos_txt.replace(",", "."))
        except ValueError:
            messagebox.showerror(
                "Perfil",
                "Ingresos €/mes debe ser un número (ej. 2500).",
            )
            return False

        try:
            self._cliente_sesion = Inquilino(
                nombre=nombre,
                dni=dni,
                telefono=telefono,
                ingresos=ingresos,
            )
        except (ValueError, TypeError) as error:
            messagebox.showerror("Perfil", str(error))
            return False

        if not silencioso:
            messagebox.showinfo("Perfil", f"Perfil listo: {self._cliente_sesion}")
        return True

    def _exigir_cliente(self) -> Inquilino | None:
        """Devuelve el cliente de sesión, intentando leer el formulario si hace falta."""
        # Siempre revalida el formulario para recoger cambios recientes.
        if not self._cliente_guardar_perfil(silencioso=True):
            return None
        return self._cliente_sesion

    def _refrescar_tabla_cliente(self) -> None:
        self.app.cargar()
        for item in self._tabla_cliente.get_children():
            self._tabla_cliente.delete(item)

        casas = self.app.gestion.listar_disponibles()
        loc = self._filtro_localidad.get().strip()
        if loc:
            casas = [c for c in casas if c.localidad.casefold() == loc.casefold()]
        try:
            pmin = float(self._filtro_min.get()) if self._filtro_min.get().strip() else None
            pmax = float(self._filtro_max.get()) if self._filtro_max.get().strip() else None
        except ValueError:
            messagebox.showerror("Filtro", "Precio mínimo/máximo no válidos.")
            return
        if pmin is not None:
            casas = [c for c in casas if c.precio >= pmin]
        if pmax is not None:
            casas = [c for c in casas if c.precio <= pmax]

        for casa in casas:
            self._tabla_cliente.insert(
                "",
                tk.END,
                iid=str(casa.id),
                values=(
                    casa.id,
                    casa.direccion,
                    casa.localidad,
                    f"{casa.precio:,.0f}",
                    f"{casa.metros_cuadrados:.0f}",
                    casa.habitaciones,
                    f"{casa.precio_m2:,.0f}",
                ),
            )

    def _casa_seleccionada_cliente(self) -> Casa | None:
        sel = self._tabla_cliente.selection()
        if not sel:
            messagebox.showinfo("Selección", "Selecciona una vivienda disponible.")
            return None
        return self.app.obtener_casa(int(sel[0]))

    def _cliente_detalle(self) -> None:
        casa = self._casa_seleccionada_cliente()
        if casa is None:
            return
        detalle = (
            f"{casa}\n\n"
            f"Precio/m²: {casa.precio_m2:,.2f} €\n"
            f"Estado: {casa.estado.name}\n"
            f"Rentabilidad estimada (renta 5% anual del precio / 12):\n"
            f"  {casa.calcular_rentabilidad(casa.precio * 0.05 / 12):.2f} % bruta anual"
        )
        messagebox.showinfo("Detalle", detalle)

    def _cliente_solicitud(self, tipo: str) -> None:
        cliente = self._exigir_cliente()
        casa = self._casa_seleccionada_cliente()
        if cliente is None or casa is None or casa.id is None:
            return
        if casa.estado != EstadoCasa.DISPONIBLE:
            messagebox.showwarning("No disponible", "Solo puedes solicitar viviendas disponibles.")
            return
        mensaje = simpledialog.askstring(
            "Mensaje",
            "Cuéntanos tu interés (opcional):",
            parent=self,
        )
        try:
            sid = self.app.crear_solicitud(casa.id, cliente, tipo, mensaje or "")
            messagebox.showinfo(
                "Solicitud enviada",
                f"Solicitud #{sid} ({tipo}) registrada. Un agente la verá en el backoffice.",
            )
        except ValueError as error:
            messagebox.showerror("Error", str(error))

    def _cliente_elegibilidad(self) -> None:
        cliente = self._exigir_cliente()
        if cliente is None:
            return
        renta = simpledialog.askfloat(
            "Regla del 35%",
            "Renta mensual que te planteas (€):",
            parent=self,
            minvalue=1,
        )
        if renta is None:
            return
        try:
            ok = cliente.puede_alquilar(renta)
            tope = cliente.ingresos * 0.35
            if ok:
                messagebox.showinfo(
                    "Elegibilidad",
                    f"Sí puedes plantearte esa renta.\nTope 35%: {tope:,.2f} €/mes.",
                )
            else:
                messagebox.showwarning(
                    "Elegibilidad",
                    f"La renta supera el 35% de tus ingresos.\nTope: {tope:,.2f} €/mes.",
                )
        except ValueError as error:
            messagebox.showerror("Error", str(error))


def ejecutar_app(ruta_db: str | None = None) -> None:
    """Punto de entrada de la interfaz gráfica."""
    app_datos = AppInmobiliaria(ruta_db=ruta_db) if ruta_db else AppInmobiliaria()
    ventana = AppGrafica(app_datos)
    ventana.mainloop()


if __name__ == "__main__":
    ejecutar_app()
