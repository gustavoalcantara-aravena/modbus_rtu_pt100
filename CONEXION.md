# Guía de Conexión - Sensor PT100

## 📌 Diagrama de Conexión

```
                    ┌─────────────────────┐
                    │   TRANSMISOR PT100  │
                    │     (Modbus RTU)    │
                    ├─────────────────────┤
    PT100           │  P+   P-   GND      │         USB-RS485
   (3 hilos)        │  │    │    │        │        ┌─────────┐
                    │  │    │    │        │   A ───┤         │
  ┌──────┐          │  │    │    │        ├────────┤ USB-485 ├──── PC
  │      │──Blanco──┼──┘    │    │        │   B ───┤         │
  │ PT100│──Rojo 1──┼───────┘    │        │        └─────────┘
  │      │──Rojo 2──┼────────────┘        │
  └──────┘          │                     │
                    │  A+   B-   VCC  GND │
                    └─────────────────────┘
                       │    │
                       └────┴──── Bus RS-485
```

---

## 🔌 Conexión del Sensor PT100 (3 hilos)

El sensor PT100 de 3 hilos tiene típicamente:
- **2 cables del mismo color** (rojos) → Van al mismo lado del elemento resistivo
- **1 cable de diferente color** (blanco) → Va al otro lado

### Conexión correcta:

| Terminal Transmisor | Cable PT100 | Descripción |
|---------------------|-------------|-------------|
| **P+** | Blanco | Señal positiva |
| **P-** | Rojo 1 | Señal negativa |
| **GND** | Rojo 2 | Compensación de cable |

> ⚠️ **IMPORTANTE**: Los dos cables rojos NO van juntos. Uno va a P- y otro a GND para compensar la resistencia del cable.

---

## 🔗 Conexión RS-485

El bus RS-485 utiliza comunicación diferencial con dos líneas:

| Terminal Transmisor | Terminal USB-485 | Descripción |
|---------------------|------------------|-------------|
| **A+** | A (o D+) | Línea diferencial + |
| **B-** | B (o D-) | Línea diferencial - |
| **GND** | GND (opcional) | Referencia común |

---

## ⚡ Alimentación

El transmisor PT100 típicamente requiere:
- **Voltaje**: 12-24V DC
- **Consumo**: < 50mA

Verificar especificaciones del modelo utilizado.

---

## 🔧 Verificación de Conexión

### 1. Verificar puerto USB
```bash
ls -la /dev/ttyUSB*
```
Debe aparecer `/dev/ttyUSB0` (o similar).

### 2. Verificar permisos
```bash
sudo usermod -a -G dialout $USER
```
(Requiere cerrar sesión y volver a entrar)

### 3. Ejecutar diagnóstico
```bash
python3 diagnostico_pt100.py
```

### Valores esperados:
- **Registro 0**: Temperatura × 10 (ej: 267 = 26.7°C)
- **Registro 1**: Resistencia × 10 (ej: 1097 = 109.7Ω a 25°C)

---

## ❌ Problemas Comunes

### "No se pudo conectar"
- Verificar que el cable USB esté conectado
- Verificar que el puerto sea `/dev/ttyUSB0`
- Verificar alimentación del transmisor

### Temperatura incorrecta (muy negativa)
- Los cables del PT100 están mal conectados
- Revisar la conexión de 3 hilos según la tabla anterior

### Valor constante que no cambia
- El sensor puede estar desconectado
- Verificar continuidad de los cables

### Resistencia muy baja (~90Ω en vez de ~110Ω)
- Conexión de 3 hilos incorrecta
- Los cables de compensación no están bien conectados

---

## 📐 Teoría del Sensor RTD PT100

### Principio de Funcionamiento

Los sensores RTD (Resistance Temperature Detector) se basan en el **principio físico de la variación de la resistencia eléctrica de los metales con la temperatura**. Este fenómeno se debe a que:

1. **A nivel atómico**: Cuando la temperatura aumenta, los átomos del metal vibran con mayor amplitud
2. **Efecto en los electrones**: Estas vibraciones dificultan el movimiento de los electrones de conducción
3. **Resultado macroscópico**: Mayor resistencia al paso de la corriente eléctrica

### Ecuación de Callendar-Van Dusen

Este comportamiento se describe mediante:

```
R(T) = R₀ × [1 + A×T + B×T² + C×(T-100)×T³]
```

Donde:
- **R(T)**: Resistencia a temperatura T
- **R₀**: Resistencia a 0°C (100Ω para PT100)
- **A** = 3.9083 × 10⁻³ °C⁻¹
- **B** = -5.775 × 10⁻⁷ °C⁻²
- **C** = -4.183 × 10⁻¹² °C⁻⁴ (solo para T < 0°C)

**Aproximación lineal** (para uso práctico):
```
R(T) ≈ R₀ × (1 + α × T)
```
Donde **α = 0.00385 Ω/Ω/°C**

### ¿Por qué Platino?

| Propiedad | Ventaja |
|-----------|---------|
| Estabilidad química | No se oxida ni corroe |
| Linealidad | Relación R-T casi lineal |
| Repetibilidad | Misma respuesta ciclo tras ciclo |
| Rango amplio | -200°C a +850°C |
| Alta precisión | Hasta ±0.1°C |

### Tabla de Resistencia vs Temperatura

El sensor **PT100** tiene una resistencia de **100Ω a 0°C**.

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

### Configuraciones de Conexión

```
2 HILOS                 3 HILOS                 4 HILOS
─────────               ─────────               ─────────

  ┌───┐                   ┌───┐                   ┌───┐
──┤RTD├──               ──┤RTD├──               ──┤RTD├──
  └───┘                   └─┬─┘                   └─┬─┘
    │                       │                       │
    │                       └── Compensación        └── I+, I-, V+, V-

Error: Alto              Error: Medio             Error: Mínimo
(incluye R cables)       (compensa R cables)      (elimina R cables)
```

### Acondicionamiento de Señal

El transmisor PT100 a Modbus realiza:

1. **Excitación**: Aplica corriente constante (~1mA) al RTD
2. **Medición**: Mide el voltaje resultante (V = I × R)
3. **Compensación**: Corrige error por resistencia de cables
4. **Linealización**: Aplica ecuación de Callendar-Van Dusen
5. **Conversión A/D**: Digitaliza el valor
6. **Comunicación**: Transmite via Modbus RTU

### Comparación con otros sensores

| Característica | RTD (PT100) | Termopar | Termistor |
|----------------|-------------|----------|-----------|
| Precisión | ±0.1°C | ±1°C | ±0.2°C |
| Rango | -200 a +850°C | -200 a +2000°C | -50 a +150°C |
| Linealidad | Excelente | Buena | Pobre |
| Costo | Medio-Alto | Bajo | Bajo |
| Estabilidad | Excelente | Buena | Regular |

---

## 👤 Autor

**Gustavo Alcántara Aravena**

Laboratorio de Comunicaciones y Redes Industriales
