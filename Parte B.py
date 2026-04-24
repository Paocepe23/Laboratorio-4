"""
PARTE B: ANÁLISIS DE SEÑAL DE PACIENTE (REAL)
Procesamiento Digital de Señales - Laboratorio EMG
Universidad Militar Nueva Granada
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import butter, sosfiltfilt
from pathlib import Path

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

DATA_FILE         = Path("real.txt")   # ← CAMBIO: archivo en la misma carpeta
FS                = 1000
NUM_CONTRACCIONES = 5
COL_EMG           = 5
SKIP_ROWS         = 4   # ← CAMBIO: incluye # EndOfHeader

OUTPUT_DIR = Path("./resultados_parte_b")
OUTPUT_DIR.mkdir(exist_ok=True)

plt.style.use('seaborn-v0_8-darkgrid')

# ============================================================================
# PASO 1: CARGAR SEÑAL
# ============================================================================

print("PARTE B: ANÁLISIS DE SEÑAL DE PACIENTE (REAL)")

try:
    señal = np.loadtxt(
        DATA_FILE,
        skiprows=SKIP_ROWS,
        usecols=[COL_EMG],
        delimiter='\t'   # ← CAMBIO: datos separados por tab
    )
except FileNotFoundError:
    print(f"ERROR: No se encontró '{DATA_FILE}'. Verifica la ruta.")
    raise SystemExit(1)
except Exception as e:
    print(f"ERROR al cargar el archivo: {e}")
    raise SystemExit(1)

print(f"Muestras: {len(señal)} | Duración: {len(señal)/FS:.2f} s | "
      f"Min: {np.min(señal):.2f} | Max: {np.max(señal):.2f} | "
      f"Media: {np.mean(señal):.2f} | Desv.Est: {np.std(señal):.2f}")

# ============================================================================
# PASO 2: SEÑAL BRUTA
# ============================================================================

tiempo = np.arange(len(señal)) / FS

plt.figure(figsize=(14, 5))
plt.plot(tiempo, señal, linewidth=0.8, color='darkred', alpha=0.7)
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud (unidades ADC)')
plt.title('Señal EMG Real - Señal Bruta (sin filtrar)')
plt.tight_layout()
plt.savefig(OUTPUT_DIR / '01_señal_bruta.png', dpi=300, bbox_inches='tight')
plt.close()
print("Guardado: 01_señal_bruta.png")

# ============================================================================
# PASO 3: FILTRO PASA BANDA 20-450 Hz
# ============================================================================

nyquist = FS / 2
low     = 20  / nyquist
high    = 450 / nyquist

if high >= 1.0:
    high = 0.95
    print("AVISO: frecuencia alta ajustada a 0.95*Nyquist por límite físico.")

sos            = butter(4, [low, high], btype='bandpass', output='sos')
señal_filtrada = sosfiltfilt(sos, señal)

print("Filtro pasa banda aplicado: 20-450 Hz (Butterworth orden 4, sin desfase)")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)
ax1.plot(tiempo, señal, linewidth=0.8, color='lightcoral', label='Original')
ax2.plot(tiempo, señal_filtrada, linewidth=0.8, color='forestgreen', label='Filtrada 20-450 Hz')
ax1.set(ylabel='Amplitud (ADC)', title='Señal EMG Real - Original')
ax2.set(xlabel='Tiempo (s)', ylabel='Amplitud (ADC)', title='Señal EMG Real - Filtrada')
ax1.legend(); ax2.legend()
plt.tight_layout()
plt.savefig(OUTPUT_DIR / '02_comparacion_filtrado.png', dpi=300, bbox_inches='tight')
plt.close()
print("Guardado: 02_comparacion_filtrado.png")

# ============================================================================
# PASO 4: SEGMENTACIÓN
# ============================================================================

tam       = len(señal_filtrada) // NUM_CONTRACCIONES
segmentos = [
    señal_filtrada[i*tam : (i+1)*tam if i < NUM_CONTRACCIONES-1 else len(señal_filtrada)]
    for i in range(NUM_CONTRACCIONES)
]

for i, seg in enumerate(segmentos):
    print(f"  Contracción {i+1}: {len(seg)} muestras ({len(seg)/FS:.3f} s)")

fig, ax = plt.subplots(figsize=(14, 6))
colores = plt.cm.RdYlGn_r(np.linspace(0, 1, NUM_CONTRACCIONES))
for i, seg in enumerate(segmentos):
    ax.plot(np.arange(len(seg))/FS, seg, linewidth=1.2,
            label=f'Contracción {i+1}', color=colores[i], alpha=0.8)

ax.set(xlabel='Tiempo (s)', ylabel='Amplitud (ADC)',
       title='Contracciones Segmentadas (verde=inicial, rojo=fatiga)')
ax.legend(fontsize=9)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / '03_segmentos.png', dpi=300, bbox_inches='tight')
plt.close()
print("Guardado: 03_segmentos.png")

# ============================================================================
# PASO 5: MF Y MPF
# ============================================================================

def calcular_mf_mpf(segmento, fs):
    n        = len(segmento)
    freqs    = np.fft.fftfreq(n, 1/fs)
    potencia = np.abs(np.fft.fft(segmento)) ** 2

    idx_pos   = freqs > 0
    freqs     = freqs[idx_pos]
    potencia  = potencia[idx_pos]
    pot_total = np.sum(potencia)

    mf  = np.sum(freqs * potencia) / pot_total if pot_total > 0 else 0.0

    pot_acum = np.cumsum(potencia)
    idx_med  = np.where(pot_acum >= pot_total / 2)[0]
    mpf      = freqs[idx_med[0]] if len(idx_med) > 0 and pot_total > 0 else 0.0

    return mf, mpf, freqs, potencia


resultados = []
for i, seg in enumerate(segmentos):
    mf, mpf, _, _ = calcular_mf_mpf(seg, FS)
    resultados.append({'Contraccion': i+1, 'MF (Hz)': mf, 'MPF (Hz)': mpf})
    print(f"  Contracción {i+1}:  MF = {mf:.2f} Hz  |  MPF = {mpf:.2f} Hz")

df = pd.DataFrame(resultados)

# ============================================================================
# PASO 6: FFT
# ============================================================================

for i, seg in enumerate(segmentos):
    _, _, freqs, potencia = calcular_mf_mpf(seg, FS)
    potencia_db = 10 * np.log10(potencia / np.max(potencia) + 1e-10)

    plt.figure(figsize=(12, 5))
    plt.plot(freqs, potencia_db, linewidth=1, color='navy')
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Potencia (dB)')  # ← CAMBIO 1
    plt.title(f'Espectro FFT - Contracción {i+1}')
    plt.xlim([0, FS/2])
    plt.ylim([-80, 5])           # ← CAMBIO 2
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / f'04_fft_contraccion_{i+1:02d}.png', dpi=300)
    plt.close()

# ============================================================================
# PASO 7: ANÁLISIS
# ============================================================================

mf_vals  = df['MF (Hz)'].values
mpf_vals = df['MPF (Hz)'].values

cambio_mf  = ((mf_vals[-1]  - mf_vals[0])  / mf_vals[0])  * 100
cambio_mpf = ((mpf_vals[-1] - mpf_vals[0]) / mpf_vals[0]) * 100

if cambio_mf < -5 or cambio_mpf < -5:
    interpretacion = "FATIGA MUSCULAR DETECTADA."
else:
    interpretacion = "SIN FATIGA SIGNIFICATIVA."

print(interpretacion)

# ============================================================================
# PASO 8: GUARDADO
# ============================================================================

df.to_csv(OUTPUT_DIR / 'resultados_real.csv', index=False)

with open(OUTPUT_DIR / 'reporte_real.txt', 'w', encoding='utf-8') as f:
    f.write("PARTE B - ANÁLISIS DE SEÑAL REAL\n\n")
    f.write(df.to_string(index=False))
    f.write(f"\n\nMF cambio: {cambio_mf:.2f}%\n")
    f.write(f"MPF cambio: {cambio_mpf:.2f}%\n\n")
    f.write(interpretacion)

print("\nPARTE B COMPLETADA.")
