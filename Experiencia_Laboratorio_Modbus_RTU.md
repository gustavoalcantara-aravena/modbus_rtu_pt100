# Experiencia de Laboratorio: Protocolo Modbus RTU

## Comunicaciones y Redes Industriales

---

## 📖 Introducción

En el ámbito de la **automatización industrial**, la comunicación entre dispositivos es fundamental para el control y monitoreo de procesos. Desde los primeros sistemas de control hasta las modernas plantas industriales 4.0, la necesidad de intercambiar datos de manera confiable ha impulsado el desarrollo de diversos protocolos de comunicación.

**Modbus**, desarrollado en 1979, se ha convertido en uno de los protocolos más utilizados en la industria debido a su simplicidad, robustez y carácter abierto. A pesar de tener más de cuatro décadas, sigue siendo ampliamente implementado y coexiste con tecnologías más modernas como Profinet, EtherNet/IP y OPC-UA.

### ¿Por qué estudiar Modbus?

1. **Relevancia industrial**: Millones de dispositivos en todo el mundo utilizan Modbus
2. **Base conceptual**: Los principios de Modbus aplican a otros protocolos industriales
3. **Accesibilidad**: Protocolo abierto, bien documentado y fácil de implementar
4. **Aplicación práctica**: Permite entender la comunicación real entre sensores y controladores

### Contexto de esta experiencia

En este laboratorio trabajaremos con un **sensor de temperatura PT100** conectado a través de un **transmisor Modbus RTU**. El PT100 es un sensor resistivo (RTD) ampliamente utilizado en la industria por su precisión y estabilidad. El transmisor convierte la señal del sensor en datos digitales que se transmiten mediante el protocolo Modbus sobre un bus RS-485.

La comunicación RS-485 fue elegida para entornos industriales por su capacidad de:
- Transmitir datos a **largas distancias** (hasta 1200 metros)
- Operar en ambientes con **ruido electromagnético**
- Conectar **múltiples dispositivos** en un mismo bus

### Arquitectura del sistema

```
┌─────────────┐     ┌─────────────────┐     ┌─────────────┐     ┌──────────┐
│   SENSOR    │────►│   TRANSMISOR    │────►│  ADAPTADOR  │────►│    PC    │
│   PT100     │     │  PT100-Modbus   │     │  USB-RS485  │     │ (Maestro)│
│ (Resistivo) │     │   (Esclavo)     │     │             │     │          │
└─────────────┘     └─────────────────┘     └─────────────┘     └──────────┘
                           │
                    Bus RS-485 (A+, B-)
```

El **PC actúa como maestro** Modbus, enviando solicitudes de lectura al transmisor (esclavo), que responde con el valor de temperatura medido por el sensor PT100.

### Importancia del modo RTU

Modbus puede operar en dos modos de transmisión:

| Característica | Modbus RTU | Modbus ASCII |
|----------------|------------|--------------|
| Formato de datos | Binario | Texto (hexadecimal) |
| Eficiencia | Mayor (menos bytes) | Menor (más bytes) |
| Delimitación | Silencio temporal | Caracteres especiales |
| Uso típico | Comunicación directa | Módems, radio |

El modo **RTU (Remote Terminal Unit)** es preferido en aplicaciones industriales directas por su mayor eficiencia en el uso del ancho de banda.

### Detección de errores

La integridad de los datos en comunicaciones industriales es crítica. Un error no detectado podría causar lecturas incorrectas o acciones no deseadas en un proceso. Modbus RTU utiliza **CRC-16 (Cyclic Redundancy Check)** para detectar errores de transmisión, garantizando que los datos recibidos sean idénticos a los enviados.

### RS-485 vs RS-232: ¿Por qué RS-485 en la industria?

En entornos industriales, la elección del medio físico de comunicación es crítica. Comparemos ambos estándares:

| Característica | RS-232 | RS-485 |
|----------------|--------|--------|
| Tipo de señal | Single-ended (referencia a tierra) | Diferencial (par trenzado) |
| Inmunidad al ruido | Baja | **Alta** |
| Distancia máxima | 15 metros | **1200 metros** |
| Dispositivos en bus | 1 (punto a punto) | **32-256** (multipunto) |
| Velocidad típica | Hasta 115 kbps | Hasta 10 Mbps |
| Entorno | Oficina, laboratorio | **Industrial, hostil** |

**RS-485 es preferido en la industria porque:**
1. La señal diferencial **cancela el ruido electromagnético** común en plantas industriales (motores, variadores, soldadoras)
2. Permite **largas distancias** sin repetidores
3. Soporta **múltiples dispositivos** en el mismo bus (topología multipunto)
4. Mayor **robustez** ante interferencias y variaciones de tierra

### Limitaciones de la arquitectura Maestro-Esclavo

Aunque simple y robusta, la arquitectura Maestro-Esclavo tiene limitaciones:

| Limitación | Descripción | Impacto |
|------------|-------------|---------|
| **Dependencia del maestro** | Si el maestro falla, todo el sistema se detiene | Punto único de fallo |
| **Sin comunicación entre esclavos** | Los esclavos no pueden intercambiar datos directamente | Requiere pasar por el maestro |
| **Polling secuencial** | El maestro consulta uno a uno | Latencia acumulativa |
| **Iniciativa unidireccional** | Los esclavos no pueden reportar eventos espontáneamente | No hay interrupciones |
| **Ancho de banda compartido** | Más esclavos = menos consultas por segundo a cada uno | Escalabilidad limitada |

**Alternativas modernas** como Modbus TCP/IP o protocolos basados en Ethernet permiten arquitecturas más flexibles (cliente-servidor, publicador-suscriptor).

### Escalabilidad: Múltiples sensores en el sistema

Una de las fortalezas de Modbus es su capacidad de escalar. El mismo bus RS-485 puede conectar hasta **247 dispositivos esclavos**, cada uno con una dirección única.

**Para agregar múltiples sensores PT100 al sistema actual:**

```
                         Bus RS-485 (A+, B-)
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        ▼                      ▼                      ▼
┌───────────────┐      ┌───────────────┐      ┌───────────────┐
│ Transmisor 1  │      │ Transmisor 2  │      │ Transmisor N  │
│  Dirección: 1 │      │  Dirección: 2 │      │  Dirección: N │
│    PT100-A    │      │    PT100-B    │      │    PT100-N    │
└───────────────┘      └───────────────┘      └───────────────┘
```

**Modificaciones necesarias en el software:**

1. **Configurar direcciones únicas** en cada transmisor (1, 2, 3, ...)
2. **Modificar el código Python** para consultar múltiples esclavos:
```python
esclavos = [1, 2, 3, 4, 5]  # Direcciones de los transmisores
for esclavo in esclavos:
    resultado = cliente.read_holding_registers(address=0, count=1, slave=esclavo)
    # Procesar temperatura de cada sensor
```
3. **Actualizar el dashboard** para mostrar múltiples lecturas simultáneas

### Mejoras potenciales para el Dashboard

El dashboard actual cumple su función educativa, pero podría mejorarse para uso profesional:

| Área | Mejora propuesta | Beneficio |
|------|------------------|-----------|
| **Alarmas** | Configurar umbrales de temperatura (mín/máx) con alertas visuales y sonoras | Detección temprana de anomalías |
| **Histórico** | Guardar datos en base de datos (SQLite, InfluxDB) | Análisis posterior, reportes |
| **Exportación** | Botón para descargar datos en CSV/Excel | Documentación, informes |
| **Multi-sensor** | Soporte para múltiples dispositivos Modbus | Monitoreo de planta completa |
| **Gráficos** | Agregar gráfico de resistencia del PT100 | Diagnóstico del sensor |
| **Configuración** | Panel para modificar parámetros Modbus sin editar código | Flexibilidad |
| **Autenticación** | Login de usuarios con roles | Seguridad en entorno real |
| **Responsive** | Optimizar para tablets y móviles | Acceso desde cualquier dispositivo |
| **API REST** | Exponer datos via API para integración con otros sistemas | Interoperabilidad |

---

## 📋 Objetivos

Al finalizar esta experiencia, el estudiante será capaz de:

1. **Comprender** el funcionamiento del protocolo Modbus RTU
2. **Identificar** la estructura de las tramas de comunicación
3. **Analizar** el intercambio de datos entre maestro y esclavo
4. **Interpretar** los datos recibidos de un sensor industrial
5. **Verificar** la integridad de la comunicación mediante CRC-16

---

## 🛠️ Equipamiento

### Hardware
- PC con sistema operativo Linux
- Adaptador USB a RS-485
- Transmisor de temperatura con salida Modbus RTU
- Sensor PT100 (3 hilos)
- Cables de conexión

### Software
- Python 3.x
- Dashboard Modbus RTU (proporcionado)
- Terminal de comandos

---

## 📚 Marco Teórico

### Historia del Protocolo Modbus

#### Origen y Evolución

**1979 - Nacimiento de Modbus**
- Desarrollado por **Modicon** (ahora Schneider Electric) en Andover, Massachusetts, USA
- Creado para comunicar sus controladores lógicos programables (PLC)
- Diseñado por el ingeniero **Dick Morley**, considerado el "padre del PLC"
- Objetivo: Protocolo simple, robusto y abierto para automatización industrial

**Década de 1980 - Adopción Industrial**
- Se convierte en estándar de facto en la industria
- Implementado por múltiples fabricantes de equipos industriales
- Versiones: Modbus RTU (binario) y Modbus ASCII (texto)

**1999 - Modbus TCP/IP**
- Adaptación del protocolo para redes Ethernet
- Encapsulación de tramas Modbus en paquetes TCP/IP
- Mayor velocidad y distancia de comunicación

**2004 - Modbus Organization**
- Schneider Electric transfiere los derechos a la Modbus Organization
- El protocolo se convierte oficialmente en **abierto y libre de regalías**
- Disponible en: [modbus.org](https://modbus.org)

**Actualidad**
- Más de **40 años** de uso continuo en la industria
- Millones de dispositivos instalados en todo el mundo
- Sigue siendo uno de los protocolos más utilizados en automatización
- Coexiste con protocolos modernos como Profinet, EtherNet/IP y OPC-UA

#### ¿Por qué Modbus sigue vigente?

| Característica | Beneficio |
|----------------|-----------|
| **Simplicidad** | Fácil de implementar y depurar |
| **Abierto** | Sin licencias ni regalías |
| **Documentado** | Especificaciones públicas y claras |
| **Interoperabilidad** | Dispositivos de diferentes fabricantes |
| **Robustez** | Probado en entornos industriales hostiles |
| **Bajo costo** | Hardware y software económicos |

---

### Protocolo Modbus RTU

#### Definición

**Modbus RTU** (Remote Terminal Unit) es el modo de transmisión binario del protocolo Modbus. Utiliza representación binaria compacta de los datos, lo que lo hace más eficiente que el modo ASCII.

#### Modelo OSI

Modbus RTU opera principalmente en las capas:

```
┌─────────────────────────────────────┐
│  Capa 7 - Aplicación                │ ← Protocolo Modbus
├─────────────────────────────────────┤
│  Capa 2 - Enlace de Datos           │ ← Trama RTU, CRC-16
├─────────────────────────────────────┤
│  Capa 1 - Física                    │ ← RS-485, RS-232
└─────────────────────────────────────┘
```

#### Arquitectura Maestro-Esclavo

```
                    ┌──────────────┐
                    │   MAESTRO    │
                    │  (Cliente)   │
                    └──────┬───────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
    ┌──────────┐     ┌──────────┐     ┌──────────┐
    │ ESCLAVO 1│     │ ESCLAVO 2│     │ ESCLAVO N│
    │ (Dir: 01)│     │ (Dir: 02)│     │ (Dir: XX)│
    └──────────┘     └──────────┘     └──────────┘
```

**Reglas de comunicación:**
- Solo el **maestro** puede iniciar transacciones
- Los **esclavos** solo responden cuando son consultados
- Cada esclavo tiene una **dirección única** (1-247)
- Dirección **0** = Broadcast (todos los esclavos, sin respuesta)

#### Características Técnicas

| Parámetro | Valor |
|-----------|-------|
| Modo de transmisión | Binario (RTU) |
| Medio físico | RS-485 (típico), RS-232 |
| Topología | Bus multipunto |
| Dispositivos máximos | 247 esclavos |
| Velocidades comunes | 9600, 19200, 38400, 115200 bps |
| Detección de errores | CRC-16 |
| Delimitación de trama | Silencio de 3.5 caracteres |

#### Capa Física: RS-485

**Características de RS-485:**
- Transmisión **diferencial** (inmune a ruido)
- Modo **half-duplex** (un par de cables)
- Distancia máxima: **1200 metros**
- Hasta **32 dispositivos** sin repetidores

```
Señal Diferencial RS-485:

     A+ ────────╲    ╱────────
                 ╲  ╱
                  ╲╱
                  ╱╲
                 ╱  ╲
     B- ────────╱    ╲────────

     Voltaje diferencial: |VA - VB| > 200mV
```

---

### Estructura de Trama RTU

```
┌─────────────┬──────────────┬────────────────┬─────────────┐
│  Dirección  │   Función    │     Datos      │   CRC-16    │
│   1 byte    │    1 byte    │    N bytes     │   2 bytes   │
└─────────────┴──────────────┴────────────────┴─────────────┘
     │              │               │               │
     │              │               │               └── Verificación de errores
     │              │               └── Parámetros variables
     │              └── Código de operación (01-FF)
     └── Dirección del esclavo (01-F7)
```

#### Delimitación de Tramas

Las tramas RTU se delimitan por **silencio** en la línea:

```
  ←─ 3.5T ─→                                    ←─ 3.5T ─→
  ┌────────┐┌────────────────────────────────────┐┌────────┐
  │SILENCIO││           TRAMA MODBUS             ││SILENCIO│
  └────────┘└────────────────────────────────────┘└────────┘

  T = Tiempo de un carácter = 11 bits / baudrate
  A 9600 bps: T = 1.15 ms, 3.5T = 4 ms
```

#### Códigos de Función

| Código | Función | Descripción |
|--------|---------|-------------|
| 0x01 | Read Coils | Leer salidas digitales |
| 0x02 | Read Discrete Inputs | Leer entradas digitales |
| **0x03** | **Read Holding Registers** | **Leer registros (usado en este lab)** |
| 0x04 | Read Input Registers | Leer registros de entrada |
| 0x05 | Write Single Coil | Escribir una salida digital |
| 0x06 | Write Single Register | Escribir un registro |
| 0x0F | Write Multiple Coils | Escribir múltiples salidas |
| 0x10 | Write Multiple Registers | Escribir múltiples registros |

#### CRC-16 (Cyclic Redundancy Check)

El CRC-16 detecta errores de transmisión:

- **Polinomio**: 0xA001 (reflejado)
- **Valor inicial**: 0xFFFF
- **Transmisión**: LSB primero

```
Algoritmo simplificado:

1. Inicializar CRC = 0xFFFF
2. Para cada byte del mensaje:
   a. XOR byte con CRC
   b. Para cada bit (8 veces):
      - Si bit 0 = 1: CRC = (CRC >> 1) XOR 0xA001
      - Si bit 0 = 0: CRC = CRC >> 1
3. Resultado: CRC de 16 bits
```

#### Códigos de Excepción (Errores)

Cuando ocurre un error, el esclavo responde con función + 0x80:

| Código | Nombre | Causa |
|--------|--------|-------|
| 0x01 | Illegal Function | Función no soportada |
| 0x02 | Illegal Data Address | Dirección de registro inválida |
| 0x03 | Illegal Data Value | Valor fuera de rango |
| 0x04 | Slave Device Failure | Error interno del dispositivo |

---

### Sensores RTD (Resistance Temperature Detector)

#### Principio de Funcionamiento

Los sensores RTD se basan en el **principio físico de la variación de la resistencia eléctrica de los metales con la temperatura**. Este fenómeno se debe a que:

1. **A nivel atómico**: Cuando la temperatura aumenta, los átomos del metal vibran con mayor amplitud
2. **Efecto en los electrones**: Estas vibraciones dificultan el movimiento de los electrones de conducción
3. **Resultado macroscópico**: Mayor resistencia al paso de la corriente eléctrica

Este comportamiento se describe mediante la ecuación de Callendar-Van Dusen:

```
R(T) = R₀ × [1 + A×T + B×T² + C×(T-100)×T³]
```

Donde:
- **R(T)**: Resistencia a temperatura T
- **R₀**: Resistencia a 0°C (100Ω para PT100)
- **A, B, C**: Coeficientes del material (para platino estándar IEC 60751)
  - A = 3.9083 × 10⁻³ °C⁻¹
  - B = -5.775 × 10⁻⁷ °C⁻²
  - C = -4.183 × 10⁻¹² °C⁻⁴ (solo para T < 0°C)

Para aplicaciones prácticas, se utiliza la aproximación lineal:

```
R(T) ≈ R₀ × (1 + α × T)
```

Donde **α = 0.00385 Ω/Ω/°C** es el coeficiente de temperatura.

#### ¿Por qué Platino?

El platino (Pt) es el material preferido para RTDs industriales debido a:

| Propiedad | Ventaja |
|-----------|---------|
| **Estabilidad química** | No se oxida ni corroe |
| **Linealidad** | Relación R-T casi lineal |
| **Repetibilidad** | Misma respuesta ciclo tras ciclo |
| **Rango amplio** | -200°C a +850°C |
| **Alta precisión** | Hasta ±0.1°C |

#### Sensor PT100

El **PT100** es un RTD de platino con:
- **PT**: Material = Platino
- **100**: Resistencia = 100Ω a 0°C

**Tabla de Resistencia vs Temperatura (PT100, α=0.00385):**

| Temperatura (°C) | Resistencia (Ω) |
|------------------|-----------------|
| -50 | 80.31 |
| -20 | 92.16 |
| 0 | 100.00 |
| 20 | 107.79 |
| 25 | 109.73 |
| 50 | 119.40 |
| 100 | 138.51 |
| 150 | 157.33 |
| 200 | 175.86 |

#### Configuraciones de Conexión

```
2 HILOS                 3 HILOS                 4 HILOS
─────────               ─────────               ─────────
                        
  ┌───┐                   ┌───┐                   ┌───┐
──┤RTD├──               ──┤RTD├──               ──┤RTD├──
  └───┘                   └─┬─┘                   └─┬─┘
    │                       │                       │
    │                       └── Compensación        └── I+ (corriente)
    │                                               └── I- (corriente)
                                                    └── V+ (voltaje)
                                                    └── V- (voltaje)

Error: Alto              Error: Medio             Error: Mínimo
(incluye R cables)       (compensa R cables)      (elimina R cables)
```

**Conexión a 3 hilos** (utilizada en este laboratorio):
- Dos cables van al mismo terminal del RTD
- Un cable va al terminal opuesto
- El transmisor mide la resistencia del cable y la compensa automáticamente

#### Acondicionamiento de Señal

El transmisor PT100 a Modbus realiza:

1. **Excitación**: Aplica una corriente constante (típicamente 1mA) al RTD
2. **Medición**: Mide el voltaje resultante (V = I × R)
3. **Compensación**: Corrige el error por resistencia de cables (3/4 hilos)
4. **Linealización**: Aplica la ecuación de Callendar-Van Dusen
5. **Conversión A/D**: Digitaliza el valor de temperatura
6. **Comunicación**: Transmite el dato via Modbus RTU

#### Ventajas y Desventajas del RTD

| Ventajas | Desventajas |
|----------|-------------|
| Alta precisión (±0.1°C) | Costo mayor que termopares |
| Excelente estabilidad | Respuesta más lenta |
| Buena linealidad | Requiere excitación externa |
| Repetible | Rango limitado vs termopar |
| No requiere compensación de unión fría | Sensible a vibraciones |

#### Comparación con otros sensores de temperatura

| Característica | RTD (PT100) | Termopar | Termistor |
|----------------|-------------|----------|-----------|
| Precisión | ±0.1°C | ±1°C | ±0.2°C |
| Rango | -200 a +850°C | -200 a +2000°C | -50 a +150°C |
| Linealidad | Excelente | Buena | Pobre |
| Costo | Medio-Alto | Bajo | Bajo |
| Respuesta | Media | Rápida | Rápida |
| Estabilidad | Excelente | Buena | Regular |

---

## 🔬 Procedimiento Experimental

### Parte 1: Preparación del Sistema

#### 1.1 Verificar conexiones físicas

1. Confirmar que el adaptador USB-RS485 está conectado
2. Verificar la conexión del sensor PT100 al transmisor:

| Terminal | Cable | Descripción |
|----------|-------|-------------|
| P+ | Blanco | Señal positiva |
| P- | Rojo 1 | Señal negativa |
| GND | Rojo 2 | Compensación |

3. Verificar la conexión RS-485:

| Transmisor | Adaptador USB |
|------------|---------------|
| A+ | A (D+) |
| B- | B (D-) |

#### 1.2 Verificar puerto serial

Ejecutar en terminal:
```bash
ls -la /dev/ttyUSB*
```

**Pregunta 1:** ¿Qué puerto serial detecta el sistema? Anótelo.

---

### Parte 2: Lectura Básica con Script Python

#### 2.1 Ejecutar lectura simple

```bash
cd /ruta/al/proyecto/Modbus
python3 leer_pt100.py
```

Observar la salida en consola durante 30 segundos.

**Pregunta 2:** Complete la siguiente tabla con 5 lecturas:

| Hora | Valor RAW | Temperatura (°C) |
|------|-----------|------------------|
| | | |
| | | |
| | | |
| | | |
| | | |

**Pregunta 3:** ¿Cuál es la relación matemática entre el valor RAW y la temperatura?

---

### Parte 3: Análisis con Dashboard Web

#### 3.1 Iniciar el Dashboard

```bash
python3 dashboard.py
```

Abrir en el navegador: **http://localhost:5000**

#### 3.2 Explorar la interfaz

Identificar las siguientes secciones del dashboard:

- [ ] Temperatura actual
- [ ] Indicador de tendencia (↑↓→)
- [ ] Estadísticas (mín, máx, promedio)
- [ ] Gráfico histórico
- [ ] Tramas Modbus TX/RX
- [ ] Configuración del sistema
- [ ] Estructura de trama RTU
- [ ] Registro de comunicaciones

#### 3.3 Cambiar entre modos de visualización

Hacer clic en el botón 🌙/☀️ para alternar entre Dark Mode y Light Mode.

---

### Parte 4: Análisis de Tramas Modbus

#### 4.1 Observar la trama de solicitud (TX)

En la sección "Comunicación Modbus en Vivo", observar la trama TX:

```
01 03 00 00 00 01 [CRC]
```

**Pregunta 4:** Complete el análisis de la trama de solicitud:

| Byte(s) | Valor Hex | Valor Decimal | Significado |
|---------|-----------|---------------|-------------|
| 1 | 01 | | |
| 2 | 03 | | |
| 3-4 | 00 00 | | |
| 5-6 | 00 01 | | |
| 7-8 | XX XX | | |

#### 4.2 Observar la trama de respuesta (RX)

Observar la trama RX que cambia con cada lectura:

```
01 03 02 XX XX [CRC]
```

**Pregunta 5:** Para una lectura de temperatura de 27.5°C, ¿cuál sería el valor hexadecimal en los bytes de datos?

Cálculo:
```
Temperatura × 10 = _____ (decimal)
Convertir a hexadecimal = 0x____
Byte alto = 0x__
Byte bajo = 0x__
```

#### 4.3 Verificar la conversión del dato

En la sección "Conversión del Dato", observar cómo se transforma:

```
0xXXXX → Decimal → Temperatura °C
```

**Pregunta 6:** Capture 3 ejemplos de conversión:

| Hex | Decimal | Temperatura |
|-----|---------|-------------|
| | | |
| | | |
| | | |

---

### Parte 5: Experimentos con Temperatura

#### 5.1 Respuesta a cambios de temperatura

1. Observar la temperatura estable (ambiente)
2. Tomar el sensor PT100 con la mano
3. Observar el cambio en el dashboard

**Pregunta 7:** 
- ¿Cuánto tiempo tarda en comenzar a subir la temperatura?
- ¿Cuál es la temperatura máxima alcanzada?
- ¿Cuánto tiempo tarda en estabilizarse al soltar el sensor?

#### 5.2 Análisis del gráfico histórico

Observar el gráfico durante el experimento anterior.

**Pregunta 8:** Dibuje o describa la forma de la curva de temperatura observada. ¿Qué tipo de respuesta representa (lineal, exponencial, etc.)?

---

### Parte 6: Análisis de la Configuración

#### 6.1 Parámetros de comunicación

Revisar la sección "Configuración Modbus RTU" del dashboard.

**Pregunta 9:** Complete los parámetros de comunicación:

| Parámetro | Valor |
|-----------|-------|
| Puerto Serial | |
| Velocidad (Baudrate) | |
| Bits de datos | |
| Paridad | |
| Bits de parada | |
| Dirección del esclavo | |
| Función Modbus | |
| Registro leído | |

#### 6.2 Cálculo de tiempo de transmisión

**Pregunta 10:** Calcule el tiempo teórico para transmitir una trama de solicitud (8 bytes) a 9600 bps:

```
Bits por carácter = 1 (start) + 8 (datos) + 1 (stop) = 10 bits
Tiempo por carácter = 10 / 9600 = _____ ms
Tiempo total (8 bytes) = _____ ms
```

---

### Parte 7: Códigos de Función Modbus

#### 7.1 Investigación

Revisar la sección "Protocolo Modbus RTU" del dashboard.

**Pregunta 11:** ¿Cuál es la diferencia entre las funciones 0x03 y 0x04?

**Pregunta 12:** Si quisiéramos escribir un valor en un registro del dispositivo, ¿qué código de función utilizaríamos?

---

### Parte 8: Detección de Errores

#### 8.1 CRC-16

**Pregunta 13:** ¿Qué significa CRC y cuál es su propósito en la comunicación Modbus?

**Pregunta 14:** ¿Qué sucedería si un bit de la trama se corrompe durante la transmisión?

---

## 📊 Tabla de Resultados

Complete la siguiente tabla resumen:

| Parámetro | Valor Observado |
|-----------|-----------------|
| Temperatura mínima registrada | |
| Temperatura máxima registrada | |
| Temperatura promedio | |
| Cantidad de lecturas realizadas | |
| Tiempo de respuesta aproximado | |
| Errores de comunicación observados | |

---

## 📝 Cuestionario Final

1. ¿Por qué se utiliza RS-485 en lugar de RS-232 para comunicaciones industriales?

2. ¿Cuál es la ventaja del modo RTU sobre el modo ASCII en Modbus?

3. ¿Qué limitaciones tiene la arquitectura Maestro-Esclavo?

4. ¿Cómo se podría modificar el sistema para leer múltiples sensores?

5. ¿Qué mejoras propondría para el dashboard?

---

## 📋 Informe de Laboratorio

El informe debe incluir:

1. **Portada** con datos del estudiante y fecha
2. **Objetivos** de la experiencia
3. **Marco teórico** (resumen)
4. **Desarrollo** con respuestas a todas las preguntas
5. **Capturas de pantalla** del dashboard (mínimo 3)
6. **Análisis de resultados**
7. **Conclusiones**
8. **Referencias bibliográficas**

---

## ⚠️ Precauciones

- No desconectar cables con el sistema energizado
- Manipular el sensor PT100 con cuidado
- No modificar la configuración del transmisor sin autorización
- Reportar cualquier anomalía al docente

---

## 📚 Referencias

- Modbus Application Protocol Specification V1.1b3
- TIA/EIA-485 Standard
- IEC 60751 (Sensores RTD)

---

## 👤 Autor

**Gustavo Alcántara Aravena**

Laboratorio de Comunicaciones y Redes Industriales
