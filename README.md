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
## Fase A
Uso de un generador de señales biológicas para establecer una línea base de comportamiento ideal sin ruido.
## Fase B 
<img width="200" height="600" alt="WhatsApp Image 2026-04-16 at 8 07 42 PM" src="https://github.com/user-attachments/assets/13f2d3ca-aecb-453a-b402-6a32acd2b0cf" />

Obtencion de la señal en el laboratorio.

Adquisición de EMG sobre el antebrazo realizando contracciones repetidas hasta el fallo muscular.

## Fase C 
Aplicación de la FFT para comparar los espectros de amplitud entre las primeras contracciones "músculo fresco" y las últimas "músculo fatigado".
# Marco conceptual
##Fisiología.
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
#PARTE A - 
Captura de la Señal EmuladaEsta fase busca establecer un punto de comparación con una señal ideal que no presenta fatiga real.
Ajustar el generador de señales biológicas en modo EMG para simular cinco contracciones musculares voluntarias.
Capturar y almacenar los datos para el procesamiento digital.
Dividir la señal continua en las cinco contracciones individuales simuladas.
Determinar la Frecuencia Media (MNF).
Determinar la Frecuencia Mediana (MDF).
Tabular los resultados y graficar la evolución de las frecuencias para verificar su estabilidad.
#PARTE B 
Captura de la Señal de PacienteAquí es donde observarás el fenómeno fisiológico real de la fatiga.
Colocar electrodos de superficie sobre un grupo muscular en el antebrazo asegurando que la piel esté limpia y seca para reducir el ruido
Registrar la señal mientras el voluntario realiza contracciones repetidas hasta alcanzar la fatiga total o falla 
Aplicar un filtro pasa banda de 20-450 Hz para eliminar el ruido de la red eléctrica y artefactos de movimiento.
Dividir la señal total en el número exacto de contracciones realizadas.
Calcular la frecuencia media y mediana para cada una de estas contracciones
Graficar la evolución de MNF y MDF y discutir cómo se relacionan con la fisiología del músculo fatigado.
PARTE C 
Análisis Espectral mediante FFTEn esta fase utilizarás herramientas matemáticas avanzadas para visualizar el cambio de energía en la señal.
Aplicar la FFT a cada una de las contracciones segmentadas de la señal real.
Graficar el espectro de amplitud (Frecuencia vs. Magnitud).
Comparar visualmente los espectros de las primeras contracciones frente a las últimas.
Calcular el desplazamiento del pico espectral hacia la izquierda (bajas frecuencias) debido al esfuerzo sostenido.
# Conclusiones
Se demostró que la aplicación de un filtro pasa banda (20-450 Hz) es indispensable para el procesamiento de señales EMG reales. Este proceso eliminó con éxito 
el ruido de baja frecuencia (artefactos de movimiento) y el ruido de alta frecuencia, permitiendo que el análisis espectral posterior se basara únicamente en la 
actividad electrofisiológica del músculo.
La Frecuencia Media (MNF) y la Frecuencia Mediana (MDF) resultaron ser indicadores robustos para la detección de la fatiga muscular. 
Se observó una tendencia decreciente constante en ambos parámetros a medida que aumentaba el número de contracciones, validando su uso como métricas objetivas para monitorear el agotamiento muscular.
Mediante el uso de la Transformada Rápida de Fourier (FFT), se evidenció visualmente el desplazamiento del espectro de potencia hacia las bajas frecuencias durante la progresión de la fatiga. 
Este cambio se atribuye fisiológicamente a la reducción de la velocidad de conducción de los potenciales de acción y a la sincronización de las unidades motoras debido a la acumulación de metabolitos como el lactato.

La comparación entre la señal emulada (Parte A) y la señal de paciente (Parte B) permitió distinguir entre un comportamiento idealizado y un proceso fisiológico dinámico. 
Mientras que la señal emulada mantuvo valores de frecuencia estables, la señal real mostró la variabilidad natural y el decaimiento esperado, lo que confirma la calidad de la adquisición y el montaje experimental realizado.
Se concluye que, aunque las técnicas espectrales son altamente precisas, su implementación en escenarios no controlados (como entrenamientos de atletas de alto rendimiento) presenta desafíos técnicos significativos. Factores como el ruido ambiental, la sudoración (que altera la impedancia de los electrodos) y los movimientos bruscos requieren algoritmos de filtrado más avanzados y sensores inalámbricos para garantizar la fiabilidad del diagnóstico de fatiga en tiempo real.
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
