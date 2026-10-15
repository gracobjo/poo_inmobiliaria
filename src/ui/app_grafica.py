"""Interfaz gráfica dual Agente/Cliente con persistencia SQLite."""

from __future__ import annotations

import tkinter as tk
from datetime import date
from pathlib import Path
from tkinter import filedialog, messagebox, simpledialog, ttk
from typing import Any

from src.modelos.casa import Casa
from src.modelos.inquilino import Inquilino
from src.servicios.app_inmobiliaria import AppInmobiliaria
from src.utils.constantes import CausaResolucion, EstadoCasa, IniciativaResolucion
from src.utils.validadores import ValidadoresInmobiliarios


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
            "Pista.TLabel",
            background=COLORES["fondo"],
            foreground="#5A6A6A",
            font=("Segoe UI", 9),
        )
        estilo.configure(
            "Card.TFrame",
            background=COLORES["panel"],
            relief="solid",
            borderwidth=1,
        )
        estilo.configure(
            "Card.TLabelframe",
            background=COLORES["panel"],
            foreground=COLORES["primario"],
            font=("Segoe UI Semibold", 11),
        )
        estilo.configure(
            "Card.TLabelframe.Label",
            background=COLORES["panel"],
            foreground=COLORES["primario"],
            font=("Segoe UI Semibold", 11),
        )
        estilo.configure(
            "CardTitle.TLabel",
            background=COLORES["panel"],
            foreground=COLORES["primario"],
            font=("Segoe UI Semibold", 12),
        )
        estilo.configure(
            "CardMeta.TLabel",
            background=COLORES["panel"],
            foreground="#5A6A6A",
            font=("Segoe UI", 9),
        )
        estilo.configure(
            "CardKey.TLabel",
            background=COLORES["panel"],
            foreground="#5A6A6A",
            font=("Segoe UI", 9),
        )
        estilo.configure(
            "CardVal.TLabel",
            background=COLORES["panel"],
            foreground=COLORES["texto"],
            font=("Segoe UI", 10),
        )
        estilo.configure(
            "Ok.TLabel",
            background=COLORES["panel"],
            foreground=COLORES["exito"],
            font=("Segoe UI Semibold", 10),
        )
        estilo.configure(
            "Warn.TLabel",
            background=COLORES["panel"],
            foreground=COLORES["acento"],
            font=("Segoe UI Semibold", 10),
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

        cols = ("id", "tipo", "direccion", "localidad", "precio", "m2", "hab", "estado")
        self._tabla_agente = ttk.Treeview(izq, columns=cols, show="headings", height=18)
        encabezados = {
            "id": "ID",
            "tipo": "Tipo",
            "direccion": "Dirección",
            "localidad": "Localidad",
            "precio": "Precio €",
            "m2": "m²",
            "hab": "Hab.",
            "estado": "Estado",
        }
        anchos = {
            "id": 40,
            "tipo": 90,
            "direccion": 160,
            "localidad": 85,
            "precio": 85,
            "m2": 45,
            "hab": 40,
            "estado": 95,
        }
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
            ("Importar datos…", self._agente_importar),
            ("Reservar", self._agente_reservar),
            ("Liberar", self._agente_liberar),
            ("Comprar (venta)", self._agente_comprar),
            ("Alquilar…", self._agente_alquilar),
            ("Ver contrato", self._agente_ver_contrato),
            ("Listar contratos", self._agente_listar_contratos),
            ("Resolver contrato…", self._agente_resolver_contrato),
            ("Historial resoluciones", self._agente_historial_resoluciones),
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
                    casa.tipo_vivienda.name,
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

    def _agente_importar(self) -> None:
        """Abre el explorador de archivos e importa viviendas desde el fichero elegido."""
        ejemplos = Path(__file__).resolve().parents[2] / "data" / "ejemplos"
        ruta = filedialog.askopenfilename(
            parent=self,
            title="Seleccionar fichero de viviendas a importar",
            initialdir=str(ejemplos if ejemplos.is_dir() else Path.home()),
            filetypes=[
                ("CSV", "*.csv"),
                ("Texto / TSV", "*.txt;*.tsv"),
                ("JSON", "*.json"),
                ("Excel", "*.xlsx;*.xlsm"),
                ("Todos los archivos", "*.*"),
            ],
        )
        if not ruta:
            return
        try:
            resultado = self.app.importar_casas(ruta)
        except (ValueError, TypeError, FileNotFoundError, ImportError, OSError) as error:
            messagebox.showerror("Importación", str(error))
            return
        self._refrescar_tabla_agente()
        messagebox.showinfo(
            "Importación",
            f"Fichero:\n{ruta}\n\n{resultado.resumen()}",
        )


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
            nombre = simpledialog.askstring("Reserva", "Nombre del cliente:", parent=self)
            dni = simpledialog.askstring("Reserva", "DNI (8 dígitos + letra):", parent=self)
            telefono = simpledialog.askstring("Reserva", "Teléfono:", parent=self)
            ingresos = simpledialog.askfloat(
                "Reserva",
                "Ingresos mensuales €:",
                parent=self,
                minvalue=1,
            )
            if None in (nombre, dni, telefono, ingresos):
                return
            cliente = Inquilino(nombre, dni, telefono, float(ingresos))
            # Si ya existe el cliente en BD, reutiliza sus datos guardados.
            existente = self.app.obtener_cliente_por_dni(cliente.dni)
            if existente is not None:
                usar = messagebox.askyesno(
                    "Cliente existente",
                    f"Ya hay un cliente con DNI {existente.dni}:\n"
                    f"{existente.nombre} · {existente.telefono} · "
                    f"{existente.ingresos:,.0f} €/mes\n\n"
                    "¿Usar esos datos para la reserva?",
                    parent=self,
                )
                if usar:
                    cliente = existente
            reserva = casa.reservar(cliente)
            self.app.guardar_cliente(cliente)
            self.app.sincronizar(casa)
            self._refrescar_tabla_agente()
            messagebox.showinfo(
                "Reserva",
                f"Vivienda #{casa.id} reservada para {reserva.cliente.nombre} "
                f"({reserva.cliente.dni})\n"
                f"Fecha: {reserva.fecha.strftime('%d/%m/%Y %H:%M')}",
            )
        except (ValueError, TypeError) as error:
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
            self.app.cargar()
            inquilino = Inquilino(nombre, dni, telefono, float(ingresos))
            comprometida = self.app.renta_comprometida(inquilino.dni)
            disponible = max(inquilino.tope_renta - comprometida, 0.0)
            if comprometida > 0:
                seguir = messagebox.askokcancel(
                    "Regla del 35%",
                    f"El inquilino ya tiene {self._fmt_eur(comprometida, mensuales=True)} "
                    f"en contratos vigentes.\n"
                    f"Tope 35%: {self._fmt_eur(inquilino.tope_renta, mensuales=True)}\n"
                    f"Margen restante: {self._fmt_eur(disponible, mensuales=True)}\n\n"
                    "¿Continuar con este alquiler?",
                )
                if not seguir:
                    return
            casa.alquilar(
                inquilino,
                renta=float(renta),
                fianza=float(fianza),
                fecha_inicio=date.today(),
                meses=12,
                renta_ya_comprometida=comprometida,
            )
            self.app.sincronizar(casa)
            self._refrescar_tabla_agente()
            messagebox.showinfo("Alquiler", "Contrato creado y guardado en SQLite.")
        except (ValueError, TypeError) as error:
            messagebox.showerror("Error", str(error))

    @staticmethod
    def _fmt_fecha(valor: date) -> str:
        return valor.strftime("%d/%m/%Y")

    @staticmethod
    def _fmt_eur(valor: float, *, mensuales: bool = False) -> str:
        texto = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return f"{texto} €/mes" if mensuales else f"{texto} €"

    def _mostrar_ventana_contratos(
        self,
        titulo: str,
        casas: list[Casa],
        *,
        subtitulo: str = "",
        iniciativa_baja: IniciativaResolucion | None = None,
        al_resolver=None,
    ) -> tk.Toplevel:
        """Ventana con tarjetas de contratos (mejor UX que texto plano)."""
        ventana = tk.Toplevel(self)
        ventana.title(titulo)
        ventana.geometry("740x580")
        ventana.configure(bg=COLORES["fondo"])
        ventana.transient(self)

        marco = ttk.Frame(ventana, style="Fondo.TFrame", padding=16)
        marco.pack(fill=tk.BOTH, expand=True)

        ttk.Label(marco, text=titulo, style="Titulo.TLabel").pack(anchor=tk.W)
        texto_sub = subtitulo or f"{len(casas)} contrato{'s' if len(casas) != 1 else ''}"
        ttk.Label(marco, text=texto_sub, style="Sub.TLabel", wraplength=680, justify=tk.LEFT).pack(
            anchor=tk.W, pady=(2, 10)
        )

        canvas = tk.Canvas(marco, bg=COLORES["fondo"], highlightthickness=0)
        scroll = ttk.Scrollbar(marco, orient=tk.VERTICAL, command=canvas.yview)
        interior = ttk.Frame(canvas, style="Fondo.TFrame")
        interior.bind(
            "<Configure>",
            lambda _e: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        canvas_ventana = canvas.create_window((0, 0), window=interior, anchor=tk.NW)

        def _ajustar_ancho(event: object) -> None:
            canvas.itemconfigure(canvas_ventana, width=getattr(event, "width", 0))

        def _rueda(event: object) -> None:
            delta = int(getattr(event, "delta", 0))
            if delta:
                canvas.yview_scroll(-1 if delta > 0 else 1, "units")

        canvas.bind("<Configure>", _ajustar_ancho)
        canvas.bind("<Enter>", lambda _e: canvas.bind_all("<MouseWheel>", _rueda))
        canvas.bind("<Leave>", lambda _e: canvas.unbind_all("<MouseWheel>"))
        canvas.configure(yscrollcommand=scroll.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        for casa in casas:
            self._montar_tarjeta_contrato(
                interior,
                casa,
                iniciativa_baja=iniciativa_baja,
                ventana_padre=ventana,
                al_resolver=al_resolver,
            )

        ttk.Button(marco, text="Cerrar", command=ventana.destroy).pack(pady=(12, 0))
        return ventana

    def _montar_tarjeta_contrato(
        self,
        padre: ttk.Frame,
        casa: Casa,
        *,
        iniciativa_baja: IniciativaResolucion | None = None,
        ventana_padre: tk.Toplevel | None = None,
        al_resolver=None,
    ) -> None:
        """Dibuja una tarjeta visual para el contrato de ``casa``."""
        contrato = casa.contrato
        if contrato is None:
            return

        tarjeta = ttk.LabelFrame(
            padre,
            text=f"  {casa.direccion} · {casa.localidad}  ",
            style="Card.TLabelframe",
            padding=12,
        )
        tarjeta.pack(fill=tk.X, pady=6, padx=2)

        cabecera = ttk.Frame(tarjeta, style="Panel.TFrame")
        cabecera.pack(fill=tk.X)
        ttk.Label(
            cabecera,
            text=f"Vivienda #{casa.id}  ·  {casa.estado.name}",
            style="CardMeta.TLabel",
        ).pack(side=tk.LEFT)
        vigente = contrato.esta_vigente()
        ttk.Label(
            cabecera,
            text="VIGENTE" if vigente else "NO VIGENTE",
            style="Ok.TLabel" if vigente else "Warn.TLabel",
        ).pack(side=tk.RIGHT)

        cuerpo = ttk.Frame(tarjeta, style="Panel.TFrame")
        cuerpo.pack(fill=tk.X, pady=(10, 0))
        cuerpo.columnconfigure(1, weight=1)
        cuerpo.columnconfigure(3, weight=1)

        filas = [
            ("Periodo", f"{self._fmt_fecha(contrato.fecha_inicio)}  →  {self._fmt_fecha(contrato.fecha_fin)}"),
            ("Renta", self._fmt_eur(contrato.renta, mensuales=True)),
            ("Fianza", self._fmt_eur(contrato.fianza)),
            ("Pagado estimado", self._fmt_eur(contrato.calcular_total_pagado())),
            ("Inquilino", f"{contrato.inquilino.nombre}  ·  {contrato.inquilino.dni}"),
            (
                "Contacto",
                f"{contrato.inquilino.telefono}  ·  {self._fmt_eur(contrato.inquilino.ingresos, mensuales=True)}",
            ),
        ]
        for i, (clave, valor) in enumerate(filas):
            fila, col = divmod(i, 2)
            ttk.Label(cuerpo, text=clave, style="CardKey.TLabel").grid(
                row=fila, column=col * 2, sticky=tk.W, padx=(0, 8), pady=3
            )
            ttk.Label(cuerpo, text=valor, style="CardVal.TLabel").grid(
                row=fila, column=col * 2 + 1, sticky=tk.W, padx=(0, 16), pady=3
            )

        if iniciativa_baja is not None and casa.id is not None:
            acciones = ttk.Frame(tarjeta, style="Panel.TFrame")
            acciones.pack(fill=tk.X, pady=(12, 0))
            ttk.Button(
                acciones,
                text="Dar de baja el contrato…",
                style="Tool.TButton",
                command=lambda c=casa: self._dialogo_resolver_contrato(
                    c,
                    iniciativa_baja,
                    ventana_padre=ventana_padre,
                    al_resolver=al_resolver,
                ),
            ).pack(side=tk.RIGHT)

    def _dialogo_resolver_contrato(
        self,
        casa: Casa,
        iniciativa: IniciativaResolucion,
        *,
        ventana_padre: tk.Toplevel | None = None,
        al_resolver=None,
    ) -> None:
        """Diálogo para elegir causa LAU y confirmar la baja del contrato."""
        if casa.contrato is None or casa.id is None:
            messagebox.showinfo("Resolver contrato", "Esta vivienda no tiene contrato activo.")
            return

        dialogo = tk.Toplevel(self)
        dialogo.title(f"Resolver contrato · vivienda #{casa.id}")
        dialogo.geometry("640x420")
        dialogo.configure(bg=COLORES["fondo"])
        dialogo.transient(self)
        dialogo.grab_set()

        marco = ttk.Frame(dialogo, style="Fondo.TFrame", padding=16)
        marco.pack(fill=tk.BOTH, expand=True)

        ttk.Label(marco, text="Baja de contrato", style="Titulo.TLabel").pack(anchor=tk.W)
        ttk.Label(
            marco,
            text=(
                f"{casa.direccion} ({casa.localidad}) · "
                f"Iniciativa: {iniciativa.etiqueta}"
            ),
            style="Sub.TLabel",
            wraplength=600,
        ).pack(anchor=tk.W, pady=(4, 12))

        causas = CausaResolucion.para_iniciativa(iniciativa)
        mapa = {c.descripcion: c for c in causas}
        var_causa = tk.StringVar(value=causas[0].descripcion)
        var_obs = tk.StringVar()

        ttk.Label(marco, text="Causa de resolución", style="Sub.TLabel").pack(anchor=tk.W)
        combo = ttk.Combobox(
            marco,
            textvariable=var_causa,
            values=list(mapa.keys()),
            state="readonly",
            width=80,
        )
        combo.pack(fill=tk.X, pady=(4, 10))

        ttk.Label(marco, text="Observaciones (opcional)", style="Sub.TLabel").pack(anchor=tk.W)
        entrada_obs = ttk.Entry(marco, textvariable=var_obs)
        entrada_obs.pack(fill=tk.X, pady=(4, 16))

        def confirmar() -> None:
            causa = mapa[var_causa.get()]
            if not messagebox.askyesno(
                "Confirmar baja",
                "¿Confirmas la resolución del contrato?\n\n"
                f"Causa: {causa.descripcion}\n"
                "La vivienda pasará a DISPONIBLE.",
                parent=dialogo,
            ):
                return
            try:
                resolucion = self.app.resolver_contrato(
                    casa.id,
                    causa,
                    iniciativa,
                    observaciones=var_obs.get(),
                )
            except (ValueError, TypeError) as error:
                messagebox.showerror("Resolver contrato", str(error), parent=dialogo)
                return
            messagebox.showinfo(
                "Contrato resuelto",
                f"Baja registrada el {self._fmt_fecha(resolucion.fecha)}.\n"
                f"{resolucion.causa.descripcion}",
                parent=dialogo,
            )
            dialogo.destroy()
            if ventana_padre is not None and ventana_padre.winfo_exists():
                ventana_padre.destroy()
            if al_resolver is not None:
                al_resolver()
            elif hasattr(self, "_tabla_agente"):
                try:
                    self._refrescar_tabla_agente()
                except tk.TclError:
                    pass

        botones = ttk.Frame(marco, style="Fondo.TFrame")
        botones.pack(fill=tk.X)
        ttk.Button(botones, text="Cancelar", command=dialogo.destroy).pack(side=tk.RIGHT)
        ttk.Button(botones, text="Confirmar baja", command=confirmar).pack(side=tk.RIGHT, padx=8)

    def _agente_ver_contrato(self) -> None:
        casa = self._casa_seleccionada_agente()
        if casa is None:
            return
        if casa.contrato is None:
            messagebox.showinfo(
                "Contrato",
                f"La vivienda #{casa.id} no tiene contrato de arrendamiento.\n"
                "Selecciona una vivienda en estado ALQUILADA.",
            )
            return
        self._mostrar_ventana_contratos(
            f"Contrato · vivienda #{casa.id}",
            [casa],
            subtitulo=f"{casa.direccion} ({casa.localidad})",
            iniciativa_baja=IniciativaResolucion.ARRENDADOR,
            al_resolver=self._refrescar_tabla_agente,
        )

    def _agente_listar_contratos(self) -> None:
        self.app.cargar()
        contratos = self.app.listar_contratos()
        if not contratos:
            messagebox.showinfo("Contratos", "No hay contratos de arrendamiento registrados.")
            return
        casas = [casa for casa, _contrato in contratos]
        self._mostrar_ventana_contratos(
            "Contratos de arrendamiento",
            casas,
            subtitulo=f"{len(casas)} alquileres en cartera",
            iniciativa_baja=IniciativaResolucion.ARRENDADOR,
            al_resolver=self._refrescar_tabla_agente,
        )

    def _agente_resolver_contrato(self) -> None:
        casa = self._casa_seleccionada_agente()
        if casa is None:
            return
        if casa.contrato is None:
            messagebox.showinfo(
                "Resolver contrato",
                "Selecciona una vivienda ALQUILADA con contrato vigente.",
            )
            return
        self._dialogo_resolver_contrato(
            casa,
            IniciativaResolucion.ARRENDADOR,
            al_resolver=self._refrescar_tabla_agente,
        )

    def _agente_historial_resoluciones(self) -> None:
        filas = self.app.listar_resoluciones()
        if not filas:
            messagebox.showinfo("Historial", "No hay resoluciones de contrato registradas.")
            return
        lineas = [f"Historial de bajas ({len(filas)}):\n"]
        for r in filas:
            try:
                causa = CausaResolucion[r["causa"]].descripcion
            except KeyError:
                causa = r["causa"]
            try:
                iniciativa = IniciativaResolucion[r["iniciativa"]].etiqueta
            except KeyError:
                iniciativa = r["iniciativa"]
            fecha = date.fromisoformat(r["fecha_resolucion"])
            lineas.append(
                f"#{r['id']} · {self._fmt_fecha(fecha)} · vivienda #{r['casa_id']} "
                f"{r['direccion']} ({r['localidad']})\n"
                f"  {r['nombre']} ({r['dni']}) · {iniciativa}\n"
                f"  {causa}\n"
                f"  Obs.: {r['observaciones'] or '—'}\n"
            )
        self._mostrar_texto("Historial de resoluciones", "\n".join(lineas))

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
        self.app.cargar()
        self._mostrar_informe_cartera()

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

    def _mostrar_informe_cartera(self) -> tk.Toplevel:
        """Informe de cartera con resumen y tarjetas por vivienda."""
        casas = self.app.gestion.propiedades
        valor = self.app.gestion.calcular_valor_cartera()
        por_estado: dict[str, list[Casa]] = {}
        for casa in casas:
            por_estado.setdefault(casa.estado.name, []).append(casa)

        ventana = tk.Toplevel(self)
        ventana.title("Informe de cartera")
        ventana.geometry("780x620")
        ventana.configure(bg=COLORES["fondo"])
        ventana.transient(self)

        marco = ttk.Frame(ventana, style="Fondo.TFrame", padding=16)
        marco.pack(fill=tk.BOTH, expand=True)

        ttk.Label(marco, text="Informe de cartera", style="Titulo.TLabel").pack(anchor=tk.W)
        resumen = (
            f"{len(casas)} propiedades  ·  Valor total {self._fmt_eur(valor)}\n"
            + "  ·  ".join(f"{estado}: {len(lista)}" for estado, lista in sorted(por_estado.items()))
        )
        ttk.Label(marco, text=resumen, style="Sub.TLabel", wraplength=720, justify=tk.LEFT).pack(
            anchor=tk.W, pady=(4, 12)
        )

        canvas = tk.Canvas(marco, bg=COLORES["fondo"], highlightthickness=0)
        scroll = ttk.Scrollbar(marco, orient=tk.VERTICAL, command=canvas.yview)
        interior = ttk.Frame(canvas, style="Fondo.TFrame")
        interior.bind(
            "<Configure>",
            lambda _e: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        ventana_canvas = canvas.create_window((0, 0), window=interior, anchor=tk.NW)

        def _ajustar(event: object) -> None:
            canvas.itemconfigure(ventana_canvas, width=getattr(event, "width", 0))

        def _rueda(event: object) -> None:
            delta = int(getattr(event, "delta", 0))
            if delta:
                canvas.yview_scroll(-1 if delta > 0 else 1, "units")

        canvas.bind("<Configure>", _ajustar)
        canvas.bind("<Enter>", lambda _e: canvas.bind_all("<MouseWheel>", _rueda))
        canvas.bind("<Leave>", lambda _e: canvas.unbind_all("<MouseWheel>"))
        canvas.configure(yscrollcommand=scroll.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        orden = ["RESERVADA", "ALQUILADA", "DISPONIBLE", "EN_REFORMA", "VENDIDA"]
        estados = sorted(
            por_estado.keys(),
            key=lambda e: orden.index(e) if e in orden else 99,
        )
        for estado in estados:
            ttk.Label(
                interior,
                text=f"{estado} ({len(por_estado[estado])})",
                style="Titulo.TLabel",
            ).pack(anchor=tk.W, pady=(10, 4))
            for casa in por_estado[estado]:
                self._montar_tarjeta_informe(interior, casa)

        botones = ttk.Frame(marco, style="Fondo.TFrame")
        botones.pack(fill=tk.X, pady=(12, 0))
        ttk.Button(
            botones,
            text="Ver texto completo",
            command=lambda: self._mostrar_texto(
                "Informe de cartera (texto)",
                self.app.gestion.generar_informe_cartera(),
            ),
        ).pack(side=tk.LEFT)
        ttk.Button(botones, text="Cerrar", command=ventana.destroy).pack(side=tk.RIGHT)
        return ventana

    def _montar_tarjeta_informe(self, padre: ttk.Frame, casa: Casa) -> None:
        """Tarjeta de vivienda dentro del informe de cartera."""
        tarjeta = ttk.LabelFrame(
            padre,
            text=f"  #{casa.id} · {casa.direccion} · {casa.localidad}  ",
            style="Card.TLabelframe",
            padding=10,
        )
        tarjeta.pack(fill=tk.X, pady=4, padx=2)

        cabecera = ttk.Frame(tarjeta, style="Panel.TFrame")
        cabecera.pack(fill=tk.X)
        ttk.Label(
            cabecera,
            text=(
                f"{casa.tipo_vivienda.name}  ·  {casa.metros_cuadrados:.0f} m²  ·  "
                f"{casa.habitaciones} hab.  ·  {self._fmt_eur(casa.precio)}"
            ),
            style="CardMeta.TLabel",
        ).pack(side=tk.LEFT)
        estilo_estado = (
            "Warn.TLabel"
            if casa.estado == EstadoCasa.RESERVADA
            else "Ok.TLabel"
            if casa.estado == EstadoCasa.DISPONIBLE
            else "CardVal.TLabel"
        )
        ttk.Label(cabecera, text=casa.estado.name, style=estilo_estado).pack(side=tk.RIGHT)

        if casa.estado == EstadoCasa.RESERVADA:
            detalle = ttk.Frame(tarjeta, style="Panel.TFrame")
            detalle.pack(fill=tk.X, pady=(8, 0))
            if casa.reserva is not None:
                r = casa.reserva
                filas = [
                    ("Cliente", f"{r.cliente.nombre}  ·  {r.cliente.dni}"),
                    ("Teléfono", r.cliente.telefono),
                    ("Ingresos", self._fmt_eur(r.cliente.ingresos, mensuales=True)),
                    ("Reservada el", r.fecha.strftime("%d/%m/%Y %H:%M")),
                ]
            else:
                filas = [
                    (
                        "Aviso",
                        "Reserva sin cliente/fecha (registrada antes de guardar estos datos).",
                    )
                ]
            for i, (clave, valor) in enumerate(filas):
                ttk.Label(detalle, text=clave, style="CardKey.TLabel").grid(
                    row=i // 2, column=(i % 2) * 2, sticky=tk.W, padx=(0, 8), pady=2
                )
                ttk.Label(detalle, text=valor, style="CardVal.TLabel").grid(
                    row=i // 2, column=(i % 2) * 2 + 1, sticky=tk.W, padx=(0, 16), pady=2
                )
        elif casa.estado == EstadoCasa.ALQUILADA and casa.contrato is not None:
            c = casa.contrato
            detalle = ttk.Frame(tarjeta, style="Panel.TFrame")
            detalle.pack(fill=tk.X, pady=(8, 0))
            filas = [
                ("Inquilino", f"{c.inquilino.nombre}  ·  {c.inquilino.dni}"),
                ("Renta", self._fmt_eur(c.renta, mensuales=True)),
                (
                    "Periodo",
                    f"{self._fmt_fecha(c.fecha_inicio)} → {self._fmt_fecha(c.fecha_fin)}",
                ),
                ("Fianza", self._fmt_eur(c.fianza)),
            ]
            for i, (clave, valor) in enumerate(filas):
                ttk.Label(detalle, text=clave, style="CardKey.TLabel").grid(
                    row=i // 2, column=(i % 2) * 2, sticky=tk.W, padx=(0, 8), pady=2
                )
                ttk.Label(detalle, text=valor, style="CardVal.TLabel").grid(
                    row=i // 2, column=(i % 2) * 2 + 1, sticky=tk.W, padx=(0, 16), pady=2
                )

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
        botones_perfil = ttk.Frame(sesion)
        botones_perfil.grid(row=0, column=8, padx=8)
        ttk.Button(botones_perfil, text="Cargar perfil", command=self._cliente_cargar_perfil).pack(
            side=tk.LEFT, padx=(0, 4)
        )
        ttk.Button(botones_perfil, text="Guardar perfil", command=self._cliente_guardar_perfil).pack(
            side=tk.LEFT
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
        ttk.Label(filtros, text="Precio min (€)").pack(side=tk.LEFT)
        ttk.Entry(filtros, textvariable=self._filtro_min, width=12).pack(side=tk.LEFT, padx=6)
        ttk.Label(filtros, text="Precio max (€)").pack(side=tk.LEFT)
        ttk.Entry(filtros, textvariable=self._filtro_max, width=12).pack(side=tk.LEFT, padx=6)
        ttk.Button(filtros, text="Buscar disponibles", command=self._refrescar_tabla_cliente).pack(
            side=tk.LEFT, padx=8
        )
        ttk.Label(
            filtros,
            text="ej. 250000, 250.000 o 250k",
            style="Pista.TLabel",
        ).pack(side=tk.LEFT, padx=(4, 0))

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
        ttk.Button(acciones, text="Mis contratos", command=self._cliente_mis_contratos).pack(
            side=tk.LEFT, padx=4
        )

        self._refrescar_tabla_cliente()

    def _cliente_cargar_perfil(self) -> None:
        """Carga desde SQLite el cliente cuyo DNI está en el formulario."""
        dni = self._cli_dni.get().strip()
        if not dni:
            messagebox.showinfo(
                "Cargar perfil",
                "Escribe tu DNI (8 dígitos + letra, ej. 12345678Z) y pulsa Cargar perfil.",
            )
            return
        cliente = self.app.obtener_cliente_por_dni(dni)
        if cliente is None:
            messagebox.showwarning(
                "Cargar perfil",
                f"No hay ningún cliente guardado con DNI {dni.upper()}.\n"
                "Completa el formulario y pulsa Guardar perfil.",
            )
            return
        self._cliente_sesion = cliente
        self._cli_nombre.set(cliente.nombre)
        self._cli_dni.set(cliente.dni)
        self._cli_tel.set(cliente.telefono)
        ingresos = cliente.ingresos
        self._cli_ingresos.set(
            str(int(ingresos) if ingresos == int(ingresos) else ingresos)
        )
        messagebox.showinfo("Cargar perfil", f"Perfil cargado: {cliente}")

    def _cliente_guardar_perfil(self, *, silencioso: bool = False) -> bool:
        """Valida, crea la sesión y persiste el perfil del cliente en SQLite.

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
            if not silencioso:
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
            self.app.guardar_cliente(self._cliente_sesion)
        except (ValueError, TypeError) as error:
            messagebox.showerror("Perfil", str(error))
            return False

        if not silencioso:
            messagebox.showinfo(
                "Perfil",
                f"Perfil guardado en SQLite: {self._cliente_sesion}\n"
                "Podrás recuperarlo con Cargar perfil usando tu DNI.",
            )
        return True

    def _cliente_mis_contratos(self) -> None:
        """Muestra los contratos de arrendamiento del cliente de sesión."""
        cliente = self._exigir_cliente()
        if cliente is None:
            return
        self.app.cargar()
        propios = [
            (casa, contrato)
            for casa, contrato in self.app.listar_contratos()
            if contrato.inquilino.dni == cliente.dni
        ]
        if not propios:
            messagebox.showinfo(
                "Mis contratos",
                f"No hay contratos de arrendamiento para {cliente.dni}.",
            )
            return
        casas = [casa for casa, _contrato in propios]
        comprometida = self.app.renta_comprometida(cliente.dni)
        tope = cliente.tope_renta
        margen = max(tope - comprometida, 0.0)
        aviso = (
            f"{cliente.nombre} · DNI {cliente.dni}\n"
            f"Rentas vigentes: {self._fmt_eur(comprometida, mensuales=True)}  ·  "
            f"Tope 35%: {self._fmt_eur(tope, mensuales=True)}  ·  "
            f"Margen: {self._fmt_eur(margen, mensuales=True)}"
        )
        if comprometida > tope:
            aviso += (
                "\n⚠ Las rentas actuales superan el 35% de tus ingresos; "
                "no se admitirán nuevos alquileres."
            )

        def _tras_baja() -> None:
            self._cliente_mis_contratos()

        self._mostrar_ventana_contratos(
            "Mis contratos",
            casas,
            subtitulo=aviso,
            iniciativa_baja=IniciativaResolucion.ARRENDATARIO,
            al_resolver=_tras_baja,
        )

    def _exigir_cliente(self) -> Inquilino | None:
        """Devuelve el cliente de sesión, intentando leer el formulario si hace falta."""
        # Siempre revalida el formulario para recoger cambios recientes.
        if not self._cliente_guardar_perfil(silencioso=True):
            return None
        return self._cliente_sesion

    @staticmethod
    def _parsear_filtro_precio(texto: str) -> float | None:
        """Interpreta el texto del filtro de precio en euros.

        Acepta formatos ES/EN y el sufijo ``k``. Las cantidades enteras
        menores de 1.000 se tratan como miles de euros (p. ej. ``250`` →
        ``250_000``), que es el uso habitual al buscar vivienda.
        """
        if not texto.strip():
            return None
        valor = ValidadoresInmobiliarios.parsear_importe(texto)
        if valor < 0:
            raise ValueError("El precio no puede ser negativo.")
        # 250 → 250000; 250.000 / 250k ya llegan como euros completos.
        if 0 < valor < 1000 and valor == int(valor):
            valor *= 1000
        return valor

    def _refrescar_tabla_cliente(self) -> None:
        self.app.cargar()
        for item in self._tabla_cliente.get_children():
            self._tabla_cliente.delete(item)

        casas = self.app.gestion.listar_disponibles()
        loc = self._filtro_localidad.get().strip()
        if loc:
            casas = [c for c in casas if c.localidad.casefold() == loc.casefold()]
        try:
            pmin = self._parsear_filtro_precio(self._filtro_min.get())
            pmax = self._parsear_filtro_precio(self._filtro_max.get())
        except (ValueError, TypeError):
            messagebox.showerror(
                "Filtro",
                "Precio mínimo/máximo no válidos.\n"
                "Usa euros completos (250000), formato ES (250.000) o miles (250 / 250k).",
            )
            return
        if pmin is not None and pmax is not None and pmin > pmax:
            messagebox.showerror("Filtro", "El precio mínimo no puede ser mayor que el máximo.")
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
        if tipo == "ALQUILER":
            self.app.cargar()
            comprometida = self.app.renta_comprometida(cliente.dni)
            if comprometida >= cliente.tope_renta:
                messagebox.showwarning(
                    "Regla del 35%",
                    "No puedes solicitar más alquileres: tus rentas vigentes "
                    f"({self._fmt_eur(comprometida, mensuales=True)}) ya alcanzan o "
                    f"superan el tope del 35% "
                    f"({self._fmt_eur(cliente.tope_renta, mensuales=True)}).",
                )
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
        self.app.cargar()
        comprometida = self.app.renta_comprometida(cliente.dni)
        tope = cliente.tope_renta
        margen = max(tope - comprometida, 0.0)
        renta = simpledialog.askfloat(
            "Regla del 35%",
            (
                f"Ingresos: {self._fmt_eur(cliente.ingresos, mensuales=True)}\n"
                f"Tope 35%: {self._fmt_eur(tope, mensuales=True)}\n"
                f"Ya comprometido: {self._fmt_eur(comprometida, mensuales=True)}\n"
                f"Margen libre: {self._fmt_eur(margen, mensuales=True)}\n\n"
                "Renta adicional que te planteas (€):"
            ),
            parent=self,
            minvalue=1,
        )
        if renta is None:
            return
        try:
            ok = cliente.puede_alquilar(renta, renta_ya_comprometida=comprometida)
            total = float(renta) + comprometida
            if ok:
                messagebox.showinfo(
                    "Elegibilidad",
                    f"Sí puedes plantearte esa renta adicional.\n\n"
                    f"Renta nueva: {self._fmt_eur(renta, mensuales=True)}\n"
                    f"Total acumulado: {self._fmt_eur(total, mensuales=True)}\n"
                    f"Tope 35%: {self._fmt_eur(tope, mensuales=True)}",
                )
            else:
                messagebox.showwarning(
                    "Elegibilidad",
                    f"No: el total superaría el 35% de tus ingresos.\n\n"
                    f"Renta nueva: {self._fmt_eur(renta, mensuales=True)}\n"
                    f"Ya comprometido: {self._fmt_eur(comprometida, mensuales=True)}\n"
                    f"Total: {self._fmt_eur(total, mensuales=True)}\n"
                    f"Tope 35%: {self._fmt_eur(tope, mensuales=True)}\n"
                    f"Margen libre: {self._fmt_eur(margen, mensuales=True)}",
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
