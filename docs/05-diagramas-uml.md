# Diagramas UML

Los diagramas usan [Mermaid](https://mermaid.js.org/). Se visualizan en GitHub, VS Code/Cursor (vista previa Markdown) o [mermaid.live](https://mermaid.live).

---

## 1. Diagrama de clases (dominio + servicios)

```mermaid
classDiagram
  direction TB

  class EstadoCasa {
    <<enumeration>>
    DISPONIBLE
    RESERVADA
    VENDIDA
    ALQUILADA
    EN_REFORMA
  }

  class TipoOperacion {
    <<enumeration>>
    VENTA
    ALQUILER
    REFORMA
    DECORACION
  }

  class ValidadoresInmobiliarios {
    <<utility>>
    +es_positivo(valor) bool
    +es_string_no_vacio(texto) bool
    +es_cp_valido(cp) bool
    +es_fecha_valida(fecha) bool
  }

  class Inquilino {
    +nombre: str
    -_dni: str
    +telefono: str
    -_ingresos: float
    +dni: str
    +ingresos: float
    +puede_alquilar(renta) bool
  }

  class Contrato {
    -_inquilino: Inquilino
    -_fecha_inicio: date
    -_fecha_fin: date
    -_renta: float
    -_fianza: float
    +calcular_total_pagado(hasta) float
    +esta_vigente(en_fecha) bool
  }

  class Casa {
    +total_casas: int$
    +impuesto_aitp: float$
    +iva_reforma: float$
    -_id: int
    -_direccion: str
    -_precio: float
    -_estado: EstadoCasa
    -_contrato: Contrato
    -_historial: TipoOperacion[*]
    +reservar()
    +liberar()
    +comprar() float
    +alquilar(...) Contrato
    +decorar(coste) float
    +reformar(coste) float
    +calcular_rentabilidad(renta) float
    +desde_diccionario(datos)$ Casa
    +cambiar_impuesto_aitp(x)$
    +calcular_precio_m2(p,m2)$ float
    +comparar_inversion(a,b)$ Casa
  }

  class GestionInmobiliaria {
    -_propiedades: Casa[*]
    +agregar_propiedad(casa)
    +listar_disponibles() Casa[*]
    +listar_por_localidad(loc) Casa[*]
    +buscar_por_precio(min,max) Casa[*]
    +calcular_valor_cartera() float
    +generar_informe_cartera() str
  }

  class AppInmobiliaria {
    +gestion: GestionInmobiliaria
    +ruta_db: Path
    +cargar()
    +agregar_casa(casa) Casa
    +sincronizar(casa)
    +crear_solicitud(...) int
    +listar_solicitudes(...) dict[*]
  }

  class Database {
    +ruta: Path
    +conexion: Connection
    +cerrar()
  }

  class RepositorioInmobiliario {
    +listar_casas() Casa[*]
    +guardar_casa(casa) Casa
    +guardar_cliente(cli) int
    +crear_solicitud(...) int
  }

  class AppGrafica {
    +app: AppInmobiliaria
    -_cliente_sesion: Inquilino
    +_mostrar_inicio()
    +_mostrar_agente()
    +_mostrar_cliente()
  }

  Casa --> EstadoCasa
  Casa --> TipoOperacion
  Casa --> Contrato : 0..1
  Casa ..> Inquilino : alquilar()
  Contrato --> Inquilino
  Casa ..> ValidadoresInmobiliarios
  Inquilino ..> ValidadoresInmobiliarios
  Contrato ..> ValidadoresInmobiliarios
  GestionInmobiliaria o-- Casa
  AppInmobiliaria --> GestionInmobiliaria
  AppInmobiliaria --> RepositorioInmobiliario
  RepositorioInmobiliario --> Database
  RepositorioInmobiliario ..> Casa
  AppGrafica --> AppInmobiliaria
  AppGrafica ..> Inquilino
```

---

## 2. Diagrama de estados — `Casa`

```mermaid
stateDiagram-v2
  [*] --> DISPONIBLE : alta
  DISPONIBLE --> RESERVADA : reservar()
  RESERVADA --> DISPONIBLE : liberar()
  DISPONIBLE --> VENDIDA : comprar()
  RESERVADA --> VENDIDA : comprar()
  DISPONIBLE --> ALQUILADA : alquilar()
  ALQUILADA --> DISPONIBLE : liberar()
  DISPONIBLE --> EN_REFORMA : reformar()
  ALQUILADA --> EN_REFORMA : reformar()
  RESERVADA --> EN_REFORMA : reformar()
  EN_REFORMA --> DISPONIBLE : finalizar_reforma()
  VENDIDA --> [*]
```

---

## 3. Diagrama de secuencia — Cliente solicita visita

```mermaid
sequenceDiagram
  actor Cliente
  participant UI as AppGrafica
  participant App as AppInmobiliaria
  participant Repo as RepositorioInmobiliario
  participant DB as SQLite

  Cliente->>UI: Solicitar visita
  UI->>UI: Validar perfil (nombre, DNI, tel, ingresos)
  alt Perfil incompleto
    UI-->>Cliente: Aviso "Perfil incompleto"
  else Perfil OK y casa seleccionada
    UI->>UI: Diálogo mensaje opcional
    UI->>App: crear_solicitud(casa_id, cliente, VISITA, msg)
    App->>Repo: guardar_cliente(cliente)
    Repo->>DB: INSERT/UPDATE clientes
    App->>Repo: crear_solicitud(...)
    Repo->>DB: INSERT solicitudes
    App-->>UI: id solicitud
    UI-->>Cliente: "Solicitud #id registrada"
  end
```

---

## 4. Diagrama de secuencia — Agente registra alquiler

```mermaid
sequenceDiagram
  actor Agente
  participant UI as AppGrafica
  participant Casa
  participant Inq as Inquilino
  participant App as AppInmobiliaria
  participant Repo as RepositorioInmobiliario

  Agente->>UI: Alquilar…
  UI->>UI: Pedir datos inquilino + renta + fianza
  UI->>Inq: new Inquilino(...)
  UI->>Casa: alquilar(inquilino, renta, fianza)
  Casa->>Inq: puede_alquilar(renta)
  alt No supera 35%
    Casa-->>UI: ValueError
    UI-->>Agente: Error
  else OK
    Casa->>Casa: crea Contrato, estado ALQUILADA
    UI->>App: sincronizar(casa)
    App->>Repo: guardar_casa(casa)
    Repo->>Repo: sincronizar contrato + cliente
    App->>App: cargar()
    UI-->>Agente: Contrato creado
  end
```

---

## 5. Diagrama de componentes

```mermaid
flowchart TB
  subgraph Presentacion
    MAIN[main.py]
    UI[AppGrafica]
    DEMO[demo_completa]
  end

  subgraph Aplicacion
    APP[AppInmobiliaria]
    GEST[GestionInmobiliaria]
  end

  subgraph Dominio
    CASA[Casa]
    CONT[Contrato]
    INQ[Inquilino]
    UTILS[constantes + validadores]
  end

  subgraph Infra
    REPO[RepositorioInmobiliario]
    DB[(SQLite inmobiliaria.db)]
  end

  MAIN --> UI
  MAIN -.-> DEMO
  UI --> APP
  DEMO --> CASA
  DEMO --> GEST
  APP --> GEST
  APP --> REPO
  GEST --> CASA
  CASA --> CONT
  CASA --> INQ
  CASA --> UTILS
  REPO --> DB
  REPO --> CASA
```

---

## 6. Modelo entidad-relación (persistencia)

```mermaid
erDiagram
  CASAS ||--o| CONTRATOS : tiene
  CLIENTES ||--o{ CONTRATOS : firma
  CASAS ||--o{ SOLICITUDES : recibe
  CLIENTES ||--o{ SOLICITUDES : envia

  CASAS {
    int id PK
    text direccion
    text codigo_postal
    text localidad
    real metros_cuadrados
    real precio
    int habitaciones
    text estado
    text historial
  }

  CLIENTES {
    int id PK
    text nombre
    text dni UK
    text telefono
    real ingresos
  }

  CONTRATOS {
    int id PK
    int casa_id FK
    int cliente_id FK
    text fecha_inicio
    text fecha_fin
    real renta
    real fianza
  }

  SOLICITUDES {
    int id PK
    int casa_id FK
    int cliente_id FK
    text tipo
    text mensaje
    text fecha
    text estado
  }
```

---

## 7. Diagrama de paquetes

```mermaid
flowchart LR
  ui[src.ui] --> servicios[src.servicios]
  servicios --> modelos[src.modelos]
  servicios --> persistencia[src.persistencia]
  persistencia --> modelos
  modelos --> utils[src.utils]
  ejemplos[ejemplos] --> modelos
  ejemplos --> servicios
  tests[tests] --> modelos
```
