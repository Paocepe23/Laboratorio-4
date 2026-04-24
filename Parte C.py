"""
PARTE C: ANÁLISIS ESPECTRAL MEDIANTE FFT
Procesamiento Digital de Señales - Laboratorio EMG
Universidad Militar Nueva Granada

Usa la misma señal real (.txt) de la Parte B, ya filtrada (20-450 Hz).
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import butter, sosfiltfilt
from pathlib import Path

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

DATA_FILE         = Path("real.txt")
FS                = 1000
NUM_CONTRACCIONES = 5
COL_EMG           = 5
SKIP_ROWS         = 4   # ← CORREGIDO

OUTPUT_DIR = Path("./resultados_parte_c")
OUTPUT_DIR.mkdir(exist_ok=True)

plt.style.use('seaborn-v0_8-darkgrid')

# ============================================================================
# PASO 1: CARGAR Y FILTRAR SEÑAL
# ============================================================================

print("PARTE C: ANÁLISIS ESPECTRAL MEDIANTE FFT")

try:
    señal = np.loadtxt(
        DATA_FILE,
        skiprows=SKIP_ROWS,
        usecols=[COL_EMG],
        delimiter='\t'   # ← CORREGIDO
    )
except FileNotFoundError:
    print(f"ERROR: No se encontró '{DATA_FILE}'. Verifica la ruta.")
    raise SystemExit(1)
except Exception as e:
    print(f"ERROR al cargar el archivo: {e}")
    raise SystemExit(1)

nyquist        = FS / 2
high           = min(450 / nyquist, 0.95)
sos            = butter(4, [20 / nyquist, high], btype='bandpass', output='sos')
señal_filtrada = sosfiltfilt(sos, señal)
print("Señal cargada y filtrada (20-450 Hz).")

# ============================================================================
# PASO 2: SEGMENTAR
# ============================================================================

tam       = len(señal_filtrada) // NUM_CONTRACCIONES
segmentos = [
    señal_filtrada[i*tam : (i+1)*tam if i < NUM_CONTRACCIONES-1 else len(señal_filtrada)]
    for i in range(NUM_CONTRACCIONES)
]

# ============================================================================
# PASO 3: FFT
# ============================================================================

def calcular_fft(segmento, fs):
    n        = len(segmento)
    freqs    = np.fft.fftfreq(n, 1/fs)
    magnitud = np.abs(np.fft.fft(segmento)) / n
    potencia = magnitud ** 2

    idx_pos  = freqs > 0
    freqs    = freqs[idx_pos]
    magnitud = magnitud[idx_pos]
    potencia = potencia[idx_pos]

    pot_total = np.sum(potencia)
    mf        = np.sum(freqs * potencia) / pot_total if pot_total > 0 else 0.0

    pot_acum = np.cumsum(potencia)
    idx_med  = np.where(pot_acum >= pot_total / 2)[0]
    mpf      = freqs[idx_med[0]] if len(idx_med) > 0 and pot_total > 0 else 0.0

    pico = freqs[np.argmax(magnitud)]

    return freqs, magnitud, mf, mpf, pico


espectros  = []
resultados = []

for i, seg in enumerate(segmentos):
    freqs, magnitud, mf, mpf, pico = calcular_fft(seg, FS)
    espectros.append((freqs, magnitud))
    resultados.append({'Contraccion': i+1, 'MF (Hz)': mf, 'MPF (Hz)': mpf, 'Pico (Hz)': pico})

    # CAMBIO 1: conversión a dB
    magnitud_db = 20 * np.log10(magnitud / np.max(magnitud) + 1e-10)

    plt.figure(figsize=(12, 4))
    plt.plot(freqs, magnitud_db, linewidth=1, color='navy')  # CAMBIO 2
    plt.axvline(pico, color='red', linestyle='--', label=f'Pico: {pico:.1f} Hz')
    plt.axvline(mf,   color='orange', linestyle='--', label=f'MF: {mf:.1f} Hz')
    plt.axvline(mpf,  color='green', linestyle='--', label=f'MPF: {mpf:.1f} Hz')
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Magnitud (dB)')  # CAMBIO 3
    plt.title(f'FFT - Contracción {i+1}')
    plt.xlim([0, FS/2])
    plt.ylim([-80, 5])  # CAMBIO 4
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / f'01_espectro_contraccion_{i+1:02d}.png', dpi=300)
    plt.close()

df = pd.DataFrame(resultados)

# ============================================================================
# PASO 4: DESPLAZAMIENTO
# ============================================================================

mf_vals   = df['MF (Hz)'].values
mpf_vals  = df['MPF (Hz)'].values
pico_vals = df['Pico (Hz)'].values

print("\nDESPLAZAMIENTO ESPECTRAL:")
print(f"Pico : {pico_vals[0]:.1f} → {pico_vals[-1]:.1f}")
print(f"MF   : {mf_vals[0]:.1f} → {mf_vals[-1]:.1f}")
print(f"MPF  : {mpf_vals[0]:.1f} → {mpf_vals[-1]:.1f}")

# ============================================================================
# PASO 5: GUARDAR
# ============================================================================

df.to_csv(OUTPUT_DIR / 'resultados_parte_c.csv', index=False)

print("\nPARTE C COMPLETADA.")
