# Laboratorio-4
# Señales electromiográficas EMG 
# Objetivo.
Identificar y cuantificar los cambios en las características espectrales de una señal electromiográfica durante  la fatiga muscular mediante el procesamiento digital de señales.
## Obejtivos especificos.
Aplicar técnicas de filtrado digital para limpiar la señal EMG de ruidos y artefactos.
Implementar algoritmos para segmentar la señal en contracciones individuales y calcular la Frecuencia Media  y la Frecuencia Mediana.
Detectar la aparición de fatiga muscular mediante la observación del desplazamiento del espectro de potencia hacia las bajas frecuencias utilizando la Transformada Rápida de Fourier.
Comparar el comportamiento de una señal emulada (ideal) frente a una señal real capturada de un voluntario, analizando sus diferencias en el dominio de la frecuencia.
# Metodología del experimento.
El laboratorio se divide en tres fases:
## Parte A

En esta sección se trabaja con una señal EMG sintética generada artificialmente. Primero se carga la señal desde un archivo .txt y se visualiza en el dominio del tiempo. Luego, la señal se segmenta en varias contracciones simuladas de igual duración.

Posteriormente, para cada segmento se calculan la frecuencia media (MF) y la frecuencia mediana (MPF) mediante la Transformada de Fourier, lo que permite analizar el contenido frecuencial de la señal a lo largo de las contracciones.
### Diagrama de flujo
```mermaid
flowchart TD

A([Inicio])

%% CONFIG
A --> B[Configurar parametros FS NUM_CONTRACCIONES DATA_FILE]
B --> C[Crear OUTPUT_DIR mkdir]

%% CARGA
C --> D[/Abrir archivo simulada.txt con np.loadtxt/]
D --> E{¿Carga exitosa?}

E -- No --> F[/Error FileNotFound salir/]
F --> Z([Fin])

E -- Sí --> G[Convertir a array 1D flatten astype float64]

%% INFO
G --> H[/Print info señal len duracion min max media std/]

%% SEÑAL BRUTA
H --> I[Generar tiempo np.arange FS]
I --> J[Plot señal bruta]
J --> K[/Guardar PNG señal bruta/]

%% SEGMENTACIÓN
K --> L[Segmentar señal en NUM_CONTRACCIONES partes]

%% INFO SEGMENTOS
L --> M[/Print tamaño de cada segmento/]

%% VISUAL SEGMENTOS
M --> N[Plot segmentos superpuestos]
N --> O[/Guardar PNG segmentos/]

%% LOOP MF MPF
O --> P{¿Quedan segmentos?}

P -- Sí --> Q[Calcular MF y MPF con FFT]
Q --> R[Guardar resultados en lista]
R --> P

%% TABLA
P -- No --> S[Crear DataFrame]
S --> T[/Print tabla resultados/]

%% EVOLUCIÓN
T --> U[Extraer arrays MF y MPF]
U --> V[Plot evolucion MF y MPF]
V --> W[/Guardar PNG evolucion/]

%% FFT ESPECTROS
W --> X{¿Quedan segmentos?}

X -- Sí --> Y[Calcular FFT y potencia]
Y --> Y1[Convertir a dB log10]
Y1 --> Y2[Plot espectro]
Y2 --> Y3[/Guardar PNG FFT/]
Y3 --> X

%% ANÁLISIS
X -- No --> AA[Calcular cambio porcentual MF y MPF]
AA --> AB[/Print cambios y desviacion/]

%% INTERPRETACIÓN
AB --> AC{¿Cambio MF y MPF menor a 5%?}

AC -- Sí --> AD[Señal estable]
AC -- No --> AE[Posible variacion]

%% EXPORTACIÓN
AD --> AF[Guardar CSV]
AE --> AF

AF --> AG[Escribir reporte TXT]

AG --> Z([Fin])
```
## resultados 
<img width="4169" height="1766" alt="02_segmentos" src="https://github.com/user-attachments/assets/37e310a5-74c2-4ae2-be5a-1501619a108f" />
<img width="4169" height="1466" alt="01_señal_bruta" src="https://github.com/user-attachments/assets/e430f528-71b5-412c-a846-7d710ce34231" />
<img width="4169" height="1466" alt="03_evolucion_frecuencias" src="https://github.com/user-attachments/assets/56ef3f92-c0f9-493c-a3b5-7adef143c444" />
<img width="3569" height="1466" alt="04_fft_contraccion_01" src="https://github.com/user-attachments/assets/0fe36a40-a95f-41a1-90a6-f40c10a82bf5" />
<img width="3569" height="1466" alt="04_fft_contraccion_02" src="https://github.com/user-attachments/assets/ec1314f8-66a7-49b1-b545-081ce425c1d0" />
<img width="3569" height="1466" alt="04_fft_contraccion_03" src="https://github.com/user-attachments/assets/32ae142b-b09c-47c5-b566-390b5b8ccf0a" />
<img width="3569" height="1466" alt="04_fft_contraccion_04" src="https://github.com/user-attachments/assets/b4c2b496-07db-48b6-91b8-b7c0886d9728" />
<img width="3569" height="1466" alt="04_fft_contraccion_05" src="https://github.com/user-attachments/assets/3a8740cf-b140-45e3-adfc-4a0edda5be12" />


- Frecuencia de muestreo (FS): 1000 Hz  
- Duración: 20.00 s  
- Número de contracciones: 5  

| Contracción | MF (Hz)  | MPF (Hz) |
|------------|---------|----------|
| 1          | 1.3262  | 0.25     |
| 2          | 1.3262  | 0.25     |
| 3          | 1.0644  | 0.25     |
| 4          | 13.9032 | 7.50     |
| 5          | 14.0410 | 7.50     |


- **MF:** 1.33 → 14.04 Hz (**+958.76%**)  
- **MPF:** 0.25 → 7.50 Hz (**+2900.00%**)
- 
## Análisis – Parte A (Señal EMG emulada)

En la señal emulada se observa que las tres primeras contracciones presentan valores de frecuencia media (MF) muy bajos y prácticamente constantes (~1.06–1.33 Hz), así como una frecuencia mediana (MPF) fija en 0.25 Hz. Sin embargo, a partir de la cuarta contracción ocurre un incremento abrupto en ambas métricas, alcanzando valores cercanos a 14 Hz en MF y 7.5 Hz en MPF.

El aumento del 958.76% en MF y 2900% en MPF indica un cambio abrupto en el contenido frecuencial, lo cual no corresponde a un fenómeno de fatiga muscular.  En cambio, sugiere una modificación en la señal generada, como un cambio en la frecuencia base o en los parámetros del generador entre segmentos.

En conclusión, la señal emulada no representa adecuadamente el comportamiento fisiológico de la fatiga, sino que funciona como una referencia artificial en la que se evidencian inconsistencias en la generación de las contracciones.

## Parte B 

En esta parte se analiza una señal EMG real adquirida de un sujeto durante contracciones musculares repetidas. Inicialmente, la señal es cargada desde un archivo .txt y se aplica un filtro pasa banda (20–450 Hz) para eliminar ruido y artefactos.

Posteriormente, la señal filtrada se segmenta en contracciones individuales, sobre las cuales se calculan la frecuencia media (MF) y la frecuencia mediana (MPF, usada aquí como estimación de la frecuencia mediana). Además, se obtiene y grafica la Transformada de Fourier para cada segmento.

Finalmente, se analiza la evolución de estos parámetros, permitiendo identificar signos de fatiga muscular a partir del desplazamiento del contenido espectral hacia bajas frecuencias.
### Diagrama de flujo
```mermaid
flowchart TD

A([Inicio])

%% CONFIG
A --> B[Configurar parametros FS NUM_CONTRACCIONES DATA_FILE]
B --> C[Crear OUTPUT_DIR mkdir]

%% CARGA
C --> D[/Abrir archivo real.txt con np.loadtxt skiprows usecols delimiter/]
D --> E{¿Carga exitosa?}

E -- No --> F[/Error FileNotFound salir/]
F --> Z([Fin])

E -- Sí --> G[Señal cargada desde columna EMG]

%% INFO
G --> H[/Print info señal len duracion min max media std/]

%% SEÑAL BRUTA
H --> I[Generar tiempo np.arange FS]
I --> J[Plot señal bruta]
J --> K[/Guardar PNG señal bruta/]

%% FILTRADO
K --> L[Calcular nyquist FS dividido 2]
L --> M[Definir banda 20 a 450 Hz]
M --> N[Aplicar filtro butter orden 4 sosfiltfilt]

N --> O[Plot señal original vs filtrada]
O --> P[/Guardar PNG comparacion filtrado/]

%% SEGMENTACIÓN
P --> Q[Segmentar señal_filtrada en NUM_CONTRACCIONES partes]

%% INFO SEGMENTOS
Q --> R[/Print tamaño y duracion por segmento/]

%% VISUAL SEGMENTOS
R --> S[Plot segmentos superpuestos]
S --> T[/Guardar PNG segmentos/]

%% LOOP MF MPF
T --> U{¿Quedan segmentos?}

U -- Sí --> V[Calcular MF y MPF con FFT]
V --> W[Guardar resultados en lista]
W --> U

%% TABLA
U -- No --> X[Crear DataFrame]

%% FFT ESPECTROS
X --> Y{¿Quedan segmentos?}

Y -- Sí --> Y1[Calcular FFT y potencia]
Y1 --> Y2[Convertir a dB log10]
Y2 --> Y3[Plot espectro]
Y3 --> Y4[/Guardar PNG FFT/]
Y4 --> Y

%% ANÁLISIS
Y -- No --> Z1[Calcular cambio porcentual MF y MPF]

%% INTERPRETACIÓN
Z1 --> Z2{¿Disminucion mayor a 5%?}

Z2 -- Sí --> Z3[Fatiga muscular detectada]
Z2 -- No --> Z4[Sin fatiga significativa]

%% EXPORTACIÓN
Z3 --> Z5[Guardar CSV]
Z4 --> Z5

Z5 --> Z6[Escribir reporte TXT]

Z6 --> Z([Fin])
```
<img width="500" height="600" alt="WhatsApp Image 2026-04-16 at 8 07 42 PM" src="https://github.com/user-attachments/assets/13f2d3ca-aecb-453a-b402-6a32acd2b0cf" />

Obtencion de la señal en el laboratorio.

Adquisición de EMG sobre el antebrazo realizando contracciones repetidas hasta el fallo muscular.
##Resultados
<img width="4169" height="1465" alt="05_evolucion_frecuencias" src="https://github.com/user-attachments/assets/b5150d27-b1bd-4a4d-9e14-e7fb3a69be2b" />
<img width="3600" height="1500" alt="04_fft_contraccion_01" src="https://github.com/user-attachments/assets/13541170-3704-4f43-ae7b-3a269066c2cf" />
<img width="4169" height="1767" alt="03_segmentos" src="https://github.com/user-attachments/assets/939b74d0-7edf-451e-a1c7-4a6b71dd6799" />
<img width="4169" height="2366" alt="02_comparacion_filtrado" src="https://github.com/user-attachments/assets/abee5703-8e98-4a04-a1ef-85c50abf940e" />
<img width="4169" height="1467" alt="01_señal_bruta" src="https://github.com/user-attachments/assets/0ae4cbcf-df84-471a-b419-170b5a132bbc" />
<img width="3600" height="1500" alt="04_fft_contraccion_05" src="https://github.com/user-attachments/assets/90547a88-cd03-4b8f-a34f-3beb87b64f80" />
<img width="3600" height="1500" alt="04_fft_contraccion_04" src="https://github.com/user-attachments/assets/e1695f1c-eab8-40eb-a00e-54508a02b21e" />
<img width="3600" height="1500" alt="04_fft_contraccion_03" src="https://github.com/user-attachments/assets/f114f367-8911-4f83-8a6c-90984a755860" />
<img width="3600" height="1500" alt="04_fft_contraccion_02" src="https://github.com/user-attachments/assets/e52a904b-323d-4188-abb1-7b5f85a84f47" />

PARTE B - ANÁLISIS DE SEÑAL REAL

| Contracción | MF (Hz)   | MPF (Hz)  |
|------------|----------|-----------|
| 1          | 129.9207 | 115.5690  |
| 2          | 125.3367 | 111.8531  |
| 3          | 123.9684 | 109.6451  |
| 4          | 121.9557 | 107.3833  |
| 5          | 122.3006 | 108.6523  |


MF cambio: -5.87%
MPF cambio: -5.98%

## Análisis – Parte B (Señal EMG real)
En la señal real se observa una tendencia general decreciente tanto de la frecuencia media (MF) como de la frecuencia mediana (MPF) a lo largo de las contracciones:

MF: 129.9 → 122.3 Hz (−5.87%)
MPF: 115.6 → 108.7 Hz (−5.98%)

Según la guía, se debe analizar la tendencia de estas frecuencias y relacionarla con la fatiga muscular. La reducción observada es consistente en términos generales, lo que indica un desplazamiento del contenido espectral hacia frecuencias más bajas.

Desde el punto de vista fisiológico, este comportamiento se explica porque, durante la fatiga muscular:

Disminuye la velocidad de conducción de las fibras musculares
Se acumulan metabolitos como lactato y iones H⁺
Se reduce la eficiencia en la generación de potenciales de acción

Esto provoca una reducción de los componentes de alta frecuencia en la señal EMG y una mayor concentración de energía en frecuencias bajas.

Por lo tanto, la tendencia descendente en MF y MPF confirma la presencia de fatiga muscular, cumpliendo con lo esperado teóricamente y validando el uso de estas métricas como indicadores confiables de fatiga muscular.

## Parte C 

En esta sección se profundiza en el análisis en frecuencia de la señal EMG real utilizando la Transformada Rápida de Fourier (FFT). Se calcula el espectro de amplitud para cada contracción, identificando parámetros clave como:

Frecuencia media (MF)
Frecuencia mediana (MPF, usada aquí como estimación de la frecuencia mediana)
Frecuencia pico del espectro

Se comparan los espectros entre contracciones iniciales y finales para observar la evolución del contenido frecuencial.

Este análisis permite evidenciar el fenómeno de fatiga muscular a través del desplazamiento del espectro hacia frecuencias más bajas, lo cual está asociado a cambios fisiológicos en el músculo durante el esfuerzo prolongado.
### Diagrama de flujo
```mermaid
flowchart TD

A([Inicio])

%% CONFIG
A --> B[Configurar parametros FS NUM_CONTRACCIONES DATA_FILE]
B --> C[Crear OUTPUT_DIR mkdir]

%% CARGA
C --> D[/Abrir archivo real.txt con np.loadtxt skiprows usecols delimiter/]
D --> E{¿Carga exitosa?}

E -- No --> F[/Error FileNotFound salir/]
F --> Z([Fin])

E -- Sí --> G[Filtrar señal butter sosfiltfilt 20 a 450 Hz]

%% SEGMENTACIÓN
G --> H[Segmentar señal_filtrada en NUM_CONTRACCIONES partes]

%% LOOP FFT
H --> I{¿Quedan segmentos?}

I -- Sí --> J[Calcular FFT magnitud y potencia]
J --> K[Calcular MF MPF y Pico]

K --> L[Guardar resultados en lista]
L --> M[Guardar espectro en lista]

M --> N[Plot espectro con MF MPF y Pico]
N --> O[/Guardar PNG espectro/]

O --> I

%% TABLA
I -- No --> P[Crear DataFrame]

%% INFO
P --> Q[/Print desplazamiento espectral MF MPF Pico/]

%% EXPORTACIÓN
Q --> R[Guardar CSV]

R --> Z([Fin])
```
Aplicación de la FFT para comparar los espectros de amplitud entre las primeras contracciones "músculo fresco" y las últimas "músculo fatigado".

##Resultados

<img width="3600" height="1200" alt="01_espectro_contraccion_02" src="https://github.com/user-attachments/assets/b0ef8200-8931-43f0-b33e-e4946928fe5e" />
<img width="3600" height="1200" alt="01_espectro_contraccion_01" src="https://github.com/user-attachments/assets/366c4c2b-03e8-4c42-b49a-3eea5bbbc932" />
<img width="4768" height="1466" alt="04_evolucion_pico_mf_mpf" src="https://github.com/user-attachments/assets/97f50252-c56e-421a-8de8-ac4e503d9688" />
<img width="3869" height="1766" alt="03_espectros_superpuestos" src="https://github.com/user-attachments/assets/71520ed1-6c0b-426b-b4bc-4a42f31e235a" />
<img width="3869" height="1467" alt="02_comparacion_primera_ultima" src="https://github.com/user-attachments/assets/9bd4c179-360f-44dd-8690-e14cc3ee4190" />
<img width="<img width="3600" height="1200" alt="01_espectro_contraccion_04" src="https://github.com/user-attachments/assets/97032343-139b-41c9-a880-a1f8e7fd3f7a" />
<img width="3600" height="1200" alt="01_espectro_contraccion_03" src="https://github.com/user-attachments/assets/db47f947-3ca6-4b8d-b95b-e9b4c2800b9f" />
<img width=3600" height="1200" alt="01_espectro_contraccion_05" src="https://github.com/user-attachments/assets/657eecfc-d5e4-4950-b618-f516d8b61b5e" />

**Parámetros:**
- Frecuencia de muestreo (FS): 1000 Hz  
- Número de contracciones: 5  
- Filtro: Pasa banda 20–450 Hz (Butterworth orden 4)  


| Contracción | MF (Hz)   | MPF (Hz)  | Pico (Hz) |
|------------|----------|-----------|-----------|
| 1          | 129.9207 | 115.5690  | 82.6108   |
| 2          | 125.3367 | 111.8531  | 75.1252   |
| 3          | 123.9684 | 109.6451  | 76.9562   |
| 4          | 121.9557 | 107.3833  | 100.2747  |
| 5          | 122.3006 | 108.6523  | 89.4309   |


## Análisis – Parte C 

El análisis espectral permite observar con mayor detalle cómo cambia el contenido en frecuencia de la señal. Según la guía, se debe comparar espectros, identificar pérdida de altas frecuencias y analizar el desplazamiento del pico espectral.

En los resultados se evidencia:

Pico espectral: 82.6 → 89.4 Hz (+6.8 Hz)
MF: 129.9 → 122.3 Hz (−7.6 Hz)
MPF: 115.6 → 108.7 Hz (−6.9 Hz)

La disminución de MF y MPF evidencia un corrimiento espectral hacia frecuencias más bajas, característico de la fatiga muscular. Sin embargo, el comportamiento del pico espectral no sigue una tendencia monótona, por lo que resulta menos robusto como indicador en este caso.

Además:

El pico espectral presenta variaciones entre contracciones, sin una tendencia clara, lo que sugiere que no es un indicador consistente del proceso de fatiga en esta señal.
La disminución de MF y MPF refuerza que la energía de la señal se redistribuye hacia bajas frecuencias
La comparación entre la primera y última contracción evidencia una señal más “lenta” en términos espectrales

Fisiológicamente, esto se relaciona con:

Menor reclutamiento de fibras rápidas (tipo II)
Disminución de la sincronización neuromuscular
Reducción de la velocidad de conducción

En conclusión, el análisis FFT permite visualizar y cuantificar el fenómeno de fatiga de forma más clara, mostrando una reducción del contenido de alta frecuencia a medida que avanza el esfuerzo, lo cual valida el uso del análisis espectral como herramienta diagnóstica en EMG.

---

# Marco conceptual

## Fisiología.

La fatiga muscular se define como la disminución de la capacidad del músculo para generar fuerza o mantener una contracción eficaz. 
Durante el ejercicio intenso, se acumula lactato y disminuye el adenosín trifosfato (ATP).
El aumento de iones de hidrógeno reduce la velocidad de conducción de los potenciales de acción en las fibras musculares.
Para compensar la pérdida de fuerza, el sistema nervioso busca o une más unidades motoras, lo que inicialmente aumenta la amplitud de la señal 

## Electromiografía de Superficie 

Es una técnica no invasiva que registra la actividad eléctrica de los músculos desde la piel. 
La señal capturada es la suma de los potenciales de acción de las unidades motoras que ocurren durante la contracción.
## Procesamiento Espectral y Transformada de Fourier
Dado que la señal EMG en el tiempo parece ruido aleatorio, es necesario llevarla al dominio de la frecuencia mediante la Transformada Rápida de Fourier (FFT).
Frecuencia Media (MNF): Es el promedio estadístico del espectro de potencia de la señal.
Frecuencia Mediana (MDF): Es la frecuencia que divide el espectro de potencia en dos regiones con la misma cantidad de energía.

## Indicadores de Fatiga 

En el espectro medida que el músculo se fatiga, ocurre un desplazamiento del espectro hacia las bajas frecuencias. 
Esto se debe a la disminución de la velocidad de conducción.
Las fibras musculares se vuelven más lentas al transmitir impulsos eléctricos.

##Filtrado Digital

Para obtener una señal útil, se debe aplicar un filtro pasa banda con un rango de 20 a 450 Hz.
Punto de corte inferior (20 Hz) eliminando artefactos de movimiento y ruido de la línea base.
Punto de corte superior (450 Hz) eliminando ruido electrónico de alta frecuencia, conservando la energía útil de la señal muscular.

# Procedimiento

## PARTE A 

Captura de la Señal EmuladaEsta fase busca establecer un punto de comparación con una señal ideal que no presenta fatiga real.
Ajustar el generador de señales biológicas en modo EMG para simular cinco contracciones musculares voluntarias.
Capturar y almacenar los datos para el procesamiento digital.
Dividir la señal continua en las cinco contracciones individuales simuladas.
Determinar la Frecuencia Media (MNF).
Determinar la Frecuencia Mediana (MDF).
Tabular los resultados y graficar la evolución de las frecuencias para verificar su estabilidad.

## PARTE B 

Captura de la Señal de PacienteAquí es donde observarás el fenómeno fisiológico real de la fatiga.
Colocar electrodos de superficie sobre un grupo muscular en el antebrazo asegurando que la piel esté limpia y seca para reducir el ruido
Registrar la señal mientras el voluntario realiza contracciones repetidas hasta alcanzar la fatiga total o falla 
Aplicar un filtro pasa banda de 20-450 Hz para eliminar el ruido de la red eléctrica y artefactos de movimiento.
Dividir la señal total en el número exacto de contracciones realizadas.
Calcular la frecuencia media y mediana para cada una de estas contracciones
Graficar la evolución de MNF y MDF y discutir cómo se relacionan con la fisiología del músculo fatigado.

## PARTE C 

Análisis Espectral mediante FFTEn esta fase utilizarás herramientas matemáticas avanzadas para visualizar el cambio de energía en la señal.
Aplicar la FFT a cada una de las contracciones segmentadas de la señal real.
Graficar el espectro de amplitud (Frecuencia vs. Magnitud).
Comparar visualmente los espectros de las primeras contracciones frente a las últimas.
Calcular el desplazamiento del pico espectral hacia la izquierda (bajas frecuencias) debido al esfuerzo sostenido.

# Conclusiones

Se demostró que la aplicación de un filtro pasa banda (20–450 Hz) es indispensable para el procesamiento de señales EMG reales. Este proceso eliminó con éxito el ruido de baja frecuencia (artefactos de movimiento) y el ruido de alta frecuencia, permitiendo que el análisis espectral posterior se basara principalmente en la actividad electrofisiológica del músculo.

La Frecuencia Media (MF) y la Frecuencia Mediana (MPF, usada como estimación de la frecuencia mediana) resultaron ser indicadores robustos para la detección de la fatiga muscular. Se observó una tendencia general decreciente en ambos parámetros a medida que aumentaba el número de contracciones (MF: 129.9 → 122.3 Hz; MPF: 115.6 → 108.7 Hz), validando su uso como métricas objetivas para monitorear el agotamiento muscular.

Mediante el uso de la Transformada Rápida de Fourier (FFT), se evidenció el desplazamiento del espectro de potencia hacia las bajas frecuencias durante la progresión de la fatiga. Este cambio se atribuye fisiológicamente a la reducción de la velocidad de conducción de los potenciales de acción y a la acumulación de metabolitos, lo que afecta la dinámica de activación de las unidades motoras.

La comparación entre la señal emulada (Parte A) y la señal real (Parte B) permitió distinguir entre un comportamiento artificial y un proceso fisiológico dinámico. Mientras que la señal emulada presentó cambios abruptos e inconsistentes en el contenido frecuencial, la señal real mostró la tendencia esperada asociada a la fatiga muscular, lo que respalda la validez del procedimiento experimental.

Se concluye que, aunque las técnicas espectrales son altamente precisas, su implementación en escenarios no controlados (como entrenamientos de alto rendimiento) presenta desafíos técnicos significativos. Factores como el ruido ambiental, la sudoración (que altera la impedancia de los electrodos) y los movimientos bruscos requieren estrategias de filtrado más robustas y sistemas de adquisición adecuados para garantizar la fiabilidad del análisis de fatiga en tiempo real.

# Preguntas para la Discusión

## 1. ¿Cambian los valores de frecuencia media y mediana a medida que el músculo se acerca a la fatiga?

Sí. Se observa una disminución progresiva en ambos valores. Mientras que en una señal ideal estos valores permanecen casi constantes tras la estabilización inicial, en una señal real de paciente, la pendiente de caída de la frecuencia media es un indicador directo del ritmo de fatiga del grupo muscular evaluado.

## 2. ¿A qué podría atribuirse este cambio?

Se atribuye a dos factores principales:
La ralentización de los potenciales de acción por fatiga metabólica. 
La sincronización de las unidades motoras. Cuando el músculo se agota, las unidades motoras tienden a disparar de forma más rítmica y conjunta para intentar sostener la fuerza, lo que aumenta la energía en las frecuencias bajas del espectro.

## 3. ¿Cómo justifica el uso de la Transformada de Fourier en terapias de rehabilitación?

El uso de la FFT es fundamental porque permite cuantificar la recuperación muscular de manera objetiva. En rehabilitación, no basta con saber si el paciente siente fuerza el análisis espectral permite al clínico observar si el espectro de la señal está volviendo a rangos de frecuencia normales (altos), lo que indica que las fibras musculares rápidas están recuperando su funcionalidad y velocidad de conducción.

# Declaración de uso de herramientas de IA

Durante la elaboración de este laboratorio se utilizaron herramientas de inteligencia artificial basadas en modelos de lenguaje como apoyo en tareas de consulta, revisión de redacción y organización del código.

Estas herramientas se emplearon únicamente como asistencia técnica para estructuración del documento, aclaración de conceptos y verificación de implementaciones en Python.

Los diagramas de flujo fueron generados inicialmente mediante herramientas compatibles con Mermaid , y posteriormente ajustados para representar la lógica del programa.
---
# Cómo ejecutar el proyecto

Para ejecutar este laboratorio es necesario tener todos los archivos en una misma carpeta y contar con Python previamente instalado en el sistema.

> ⚠️ Todos los archivos deben estar en la misma carpeta para evitar errores de lectura de datos.

### 1. Estructura del proyecto

Asegúrate de que todos los archivos se encuentren en el mismo directorio:


``` id="treefix"
/Carpeta_designada
│
├── Parte A.py
├── Parte B.py
├── Parte C.py
├── simulada.txt
├── real.txt
└── (carpetas de resultados se generan automáticamente)
```
### 2. Instalación de dependencias

Los scripts utilizan las siguientes librerías de Python:

- numpy  
- matplotlib  
- pandas  
- scipy  

Instálalas ejecutando el siguiente comando en la terminal:


```bash
pip install numpy matplotlib pandas scipy
```

### 3. Ejecución de los scripts
Cada parte del laboratorio se ejecuta de forma independiente:

```bash
python "Parte A.py"
python "Parte B.py"
python "Parte C.py"
```
### 4. Resultados generados
Al ejecutar cada script, se crearán automáticamente carpetas con los resultados:
- `resultados_parte_a/`
- `resultados_parte_b/`
- `resultados_parte_c/`
En estas carpetas encontrarás:

Gráficas en formato .png
Tablas de resultados en .csv
Reportes en .txt

### 3. Notas importantes

- os nombres de los archivos de señal (simulada.txt y real.txt) están definidos directamente en los scripts.
Sin embargo, estos pueden modificarse fácilmente editando la variable DATA_FILE en cada archivo .py en caso de que se desee trabajar con otros datos.

- El proyecto está diseñado para trabajar con archivos `.txt` en formato **OpenSignals** (generados por BITalino):

  - `simulada.txt` → señal EMG emulada (Parte A)  
  - `real.txt` → señal EMG real (Partes B y C)  

  Estos archivos contienen encabezados con metadatos y datos tabulados por columnas.

  ⚠️ No cualquier archivo `.txt` es compatible. Si se utilizan otros formatos, será necesario modificar la forma en que se cargan los datos en el código.

Si ocurre un error de archivo no encontrado, verifica que:
Todos los archivos estén en la misma carpeta
El nombre del archivo coincida exactamente con el definido en DATA_FILE
Los scripts están configurados con una frecuencia de muestreo de 1000 Hz, la cual puede ajustarse directamente en el código si se utilizan señales con diferentes características.
---
