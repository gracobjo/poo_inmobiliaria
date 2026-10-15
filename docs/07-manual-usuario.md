# Manual de usuario

## 1. ¿Qué es esta aplicación?

**Sistema Inmobiliario POO** permite:

- A la **inmobiliaria (Agente)** gestionar viviendas, ventas, alquileres, resoluciones de contrato y solicitudes.
- Al **cliente** buscar pisos disponibles, pedir visitas, consultar sus contratos y comprobar si una renta es asumible.

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

### 4.1 Completar o cargar tu perfil

En **Tu perfil** rellena:

| Campo | Ejemplo | Notas |
|---|---|---|
| Nombre | Ana López | Obligatorio |
| DNI | 12345678Z | 8 dígitos + letra |
| Teléfono | 600111222 | Obligatorio |
| Ingresos €/mes | 2500 | Número > 0 |

- **Guardar perfil:** valida los datos y los persiste en SQLite.
- **Cargar perfil:** escribe tu DNI y pulsa el botón para recuperar un perfil ya guardado.

Si intentas solicitar una visita con el perfil vacío, la app te avisará de los campos que faltan.

### 4.2 Buscar viviendas

1. (Opcional) Escribe **Localidad**, **Precio min (€)** y/o **Precio max (€)**.
2. Pulsa **Buscar disponibles**.
3. Solo verás viviendas en estado **DISPONIBLE**.

Formatos de precio admitidos: `250000`, `250.000`, `250k` o cantidades cortas como `250` (se interpretan como miles de euros).

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

> **Me interesa alquilar** se bloquea si tus rentas vigentes ya alcanzan o superan el tope del 35 % de tus ingresos.

### 4.5 Comprobar la regla del 35 %

Sirve para saber si una renta mensual (adicional) es razonable respecto a tus ingresos **y a lo que ya tienes alquilado**.

1. Pulsa **Comprobar regla 35%**.
2. Revisa tope, renta ya comprometida y margen libre.
3. Indica la renta adicional que te planteas.
4. La app comprueba: `renta nueva + rentas vigentes ≤ ingresos × 0,35`.

### 4.6 Mis contratos y baja como inquilino

1. Pulsa **Mis contratos**.
2. Verás tarjetas con periodo, renta, fianza y estado de vigencia, más el resumen del 35 %.
3. En cada tarjeta, **Dar de baja el contrato…** abre un diálogo con causas de resolución por parte del **arrendatario** (y causas ajenas / mutuo acuerdo).

Causas del inquilino (resumen):

- Falta de reparaciones de habitabilidad
- Perturbación del uso pacífico por el propietario
- Desistimiento (art. 11 LAU): requiere al menos **6 meses** de contrato
- Mutuo acuerdo, pérdida de la finca o declaración de ruina

---

## 5. Guía del Agente

### 5.1 Inventario

La tabla muestra todas las viviendas (id, tipo, dirección, localidad, precio, m², habitaciones, estado) y el **valor de cartera**.

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
| **Reservar** | Bloquea la casa para un cliente (pide nombre, DNI, teléfono e ingresos) |
| **Liberar** | Cancela reserva o libera alquiler sin expediente formal |
| **Comprar (venta)** | Cierra venta (aplica impuesto AITP) |
| **Alquilar…** | Crea contrato (pide datos del inquilino) |
| **Ver contrato** | Detalle del contrato de una vivienda ALQUILADA |
| **Listar contratos** | Todos los alquileres vigentes en cartera |
| **Resolver contrato…** | Baja formal con causa LAU (iniciativa arrendador) |
| **Historial resoluciones** | Bajas ya registradas |
| **Decorar…** | Suma un coste de decoración al valor |
| **Reformar…** | Obra con IVA; pasa a EN_REFORMA |
| **Finalizar reforma** | Vuelve a DISPONIBLE |
| **Ver informe cartera** | Tarjetas por estado (cliente/fecha en reservas; inquilino en alquileres) |
| **Solicitudes de clientes** | Bandeja de visitas/interés |

### 5.3 bis Reservar (paso a paso)

1. Selecciona una vivienda **DISPONIBLE**.
2. **Reservar**.
3. Introduce los datos del cliente interesado.
4. Si el DNI ya existe en SQLite, puedes reutilizar ese perfil.
5. La casa pasa a **RESERVADA** y se guarda la fecha/hora de la reserva.

En el informe de cartera verás el cliente y cuándo se reservó.

### 5.4 Alquilar (paso a paso)

1. Selecciona una vivienda **DISPONIBLE**.
2. **Alquilar…**
3. Introduce nombre, DNI, teléfono, ingresos, renta y fianza.
4. Si el inquilino ya tiene contratos, la app muestra tope 35 %, renta comprometida y margen.
5. Si `renta nueva + rentas vigentes` supera el 35 % de los ingresos, la operación se rechaza.
6. Si es válida, la casa queda **ALQUILADA** y el contrato se guarda.

### 5.5 Resolver un contrato (arrendador / gestor)

1. Selecciona una vivienda **ALQUILADA** (o ábrela desde Ver/Listar contratos).
2. **Resolver contrato…** / **Dar de baja el contrato…**
3. Elige la causa (impagos, daños, obras no consentidas, necesidad del propietario, mutuo acuerdo, etc.).
4. Añade observaciones opcionales y confirma.

La vivienda pasa a **DISPONIBLE** y la resolución queda en el historial.

Notas de plazos simulados:

- **Necesidad del propietario:** mínimo **12 meses** de contrato.
- Las causas ajenas (mutuo acuerdo, ruina, pérdida de finca) están disponibles también para el arrendador.

### 5.6 Atender solicitudes

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

**¿Cómo recupero mi perfil al volver a entrar?**  
Escribe tu DNI y pulsa **Cargar perfil**.

**¿El DNI se puede cambiar después?**  
Puedes editar el formulario y volver a guardar (se actualiza/crea el cliente en SQLite). El DNI del objeto de dominio es de solo lectura una vez creado; al guardar se reconstruye la sesión con los valores del formulario.

**¿Necesito crear usuario y contraseña?**  
No en esta versión: eliges el perfil en la pantalla inicial.

**¿Liberar y Resolver contrato son lo mismo?**  
No. **Liberar** es una liberación rápida (reserva o alquiler). **Resolver contrato** registra causa legal, iniciativa y observaciones en el historial.

---

## 7. Glosario rápido

| Término | Significado |
|---|---|
| AITP | Impuesto aplicado en la compra (por defecto 10 %) |
| IVA reforma | 21 % sobre el coste de reforma |
| Regla 35 % | La renta acumulada no debería superar el 35 % de los ingresos |
| Renta comprometida | Suma de rentas de contratos vigentes del mismo DNI |
| Resolución | Baja formal de un contrato con causa (LAU) |
| Reserva | Bloqueo temporal de una vivienda a favor de un cliente (con fecha) |
| Solicitud | Petición del cliente (visita/compra/alquiler) pendiente de agente |
