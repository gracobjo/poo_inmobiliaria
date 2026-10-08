# Manual de usuario

## 1. ¿Qué es esta aplicación?

**Sistema Inmobiliario POO** permite:

- A la **inmobiliaria (Agente)** gestionar viviendas, ventas, alquileres y solicitudes.
- Al **cliente** buscar pisos disponibles, pedir visitas y comprobar si una renta es asumible.

Los datos se guardan en el ordenador (archivo SQLite). No necesita internet.

## 2. Cómo abrir la aplicación

1. Abre una terminal en la carpeta del proyecto.
2. Ejecuta:

```bash
python main.py
```

3. Aparece la ventana **Sistema Inmobiliario POO**.

> Si ya tenías la app abierta mientras se actualizaba el código, ciérrala y ábrela de nuevo.

## 3. Pantalla de inicio

Verás dos botones:

| Botón | Para quién |
|---|---|
| **Entrar como Agente** | Personal de la inmobiliaria |
| **Entrar como Cliente** | Comprador o posible inquilino |

Puedes cambiar de perfil en cualquier momento con **Cambiar perfil**.

---

## 4. Guía del Cliente

### 4.1 Completar tu perfil (obligatorio para solicitar)

En **Tu perfil** rellena:

| Campo | Ejemplo | Notas |
|---|---|---|
| Nombre | Ana López | Obligatorio |
| DNI | 12345678Z | 8 dígitos + letra |
| Teléfono | 600111222 | Obligatorio |
| Ingresos €/mes | 2500 | Número > 0 |

Pulsa **Guardar perfil**.

Si intentas **Solicitar visita** con el perfil vacío, la app te avisará de los campos que faltan.

### 4.2 Buscar viviendas

1. (Opcional) Escribe **Localidad**, **Precio min** y/o **Precio max**.
2. Pulsa **Buscar disponibles**.
3. Solo verás viviendas en estado **DISPONIBLE**.

### 4.3 Ver una vivienda

1. Selecciona una fila de la tabla.
2. Pulsa **Ver detalle**.
3. Consulta dirección, precio/m² y una rentabilidad estimada.

### 4.4 Solicitar visita / interés

1. Selecciona la vivienda.
2. Pulsa:
   - **Solicitar visita**
   - **Me interesa comprar**
   - **Me interesa alquilar**
3. Escribe un mensaje opcional.
4. Confirma el aviso de solicitud registrada.

Un agente verá tu solicitud en el backoffice.

### 4.5 Comprobar la regla del 35 %

Sirve para saber si una renta mensual es razonable respecto a tus ingresos.

1. Pulsa **Comprobar regla 35%**.
2. Indica la renta mensual.
3. La app te dice si cumples la regla (`renta ≤ 35 % de ingresos`).

---

## 5. Guía del Agente

### 5.1 Inventario

La tabla muestra todas las viviendas (id, dirección, localidad, precio, m², habitaciones, estado) y el **valor de cartera**.

### 5.2 Alta de vivienda

1. **Nueva vivienda**
2. Completa dirección, CP, localidad, m², precio y habitaciones.
3. **Guardar**

### 5.2 bis Importar desde archivo (navegación al fichero)

1. En el panel Agente, pulsa **Importar datos…**
2. Se abre el **explorador de Windows** (carpeta inicial: `data/ejemplos`)
3. Navega y selecciona el fichero, por ejemplo **`casas_10_tipos.csv`** (12 viviendas de distintos tipos)
4. Acepta: verás un resumen y la tabla se actualiza (columna **Tipo**)

Formatos: `.csv`, `.txt`, `.json`, `.xlsx` (Excel requiere `pip install openpyxl`).

Guía detallada: [docs/09-importacion-datos.md](09-importacion-datos.md).

### 5.3 Operaciones sobre una vivienda seleccionada

| Botón | Cuándo usarlo |
|---|---|
| **Reservar** | Cliente interesado; bloquea la casa |
| **Liberar** | Cancela reserva o finaliza alquiler |
| **Comprar (venta)** | Cierra venta (aplica impuesto AITP) |
| **Alquilar…** | Crea contrato (pide datos del inquilino) |
| **Decorar…** | Suma un coste de decoración al valor |
| **Reformar…** | Obra con IVA; pasa a EN_REFORMA |
| **Finalizar reforma** | Vuelve a DISPONIBLE |
| **Ver informe cartera** | Resumen textual |
| **Solicitudes de clientes** | Bandeja de visitas/interés |

### 5.4 Alquilar (paso a paso)

1. Selecciona una vivienda **DISPONIBLE**.
2. **Alquilar…**
3. Introduce nombre, DNI, teléfono, ingresos, renta y fianza.
4. Si la renta supera el 35 % de los ingresos, la operación se rechaza.
5. Si es válida, la casa queda **ALQUILADA** y el contrato se guarda.

### 5.5 Atender solicitudes

1. **Solicitudes de clientes**
2. Revisa tipo (`VISITA`, `COMPRA`, `ALQUILER`), datos del cliente y mensaje.
3. Usa **Marcar primera pendiente como ATENDIDA** cuando la gestiones.

---

## 6. Preguntas frecuentes

**¿Dónde se guardan mis datos?**  
En `data/inmobiliaria.db` dentro de la carpeta del proyecto.

**¿Puedo borrar todo y empezar de cero?**  
Sí: cierra la app, elimina `data/inmobiliaria.db` y vuelve a abrirla (se regenera el ejemplo).

**¿Por qué no veo una casa como cliente?**  
Solo se listan las **DISPONIBLE**. Las alquiladas, vendidas o en reforma no aparecen en el portal cliente.

**¿El DNI se puede cambiar después?**  
En el perfil del cliente puedes editar los campos y volver a guardar. El DNI del modelo de dominio es de solo lectura una vez creado el objeto; al guardar perfil se crea/actualiza la sesión con los valores del formulario.

**¿Necesito crear usuario y contraseña?**  
No en esta versión: eliges el perfil en la pantalla inicial.

---

## 7. Glosario rápido

| Término | Significado |
|---|---|
| AITP | Impuesto aplicado en la compra (por defecto 10 %) |
| IVA reforma | 21 % sobre el coste de reforma |
| Regla 35 % | La renta no debería superar el 35 % de los ingresos |
| Solicitud | Petición del cliente (visita/compra/alquiler) pendiente de agente |
