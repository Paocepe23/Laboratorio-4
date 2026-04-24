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
# CONFIGURACIÓN  ← AJUSTAR SEGÚN TUS DATOS (igual que Parte B)
# ============================================================================

DATA_FILE         = Path(r"opensiseñalda.txt")  # Mismo archivo .txt de Parte B
FS                = 1000
NUM_CONTRACCIONES = 5
COL_EMG           = 5
SKIP_ROWS         = 3

OUTPUT_DIR = Path("./resultados_parte_c")
OUTPUT_DIR.mkdir(exist_ok=True)

plt.style.use('seaborn-v0_8-darkgrid')

# ============================================================================
# PASO 1: CARGAR Y FILTRAR SEÑAL (igual que Parte B)
# ============================================================================

print("PARTE C: ANÁLISIS ESPECTRAL MEDIANTE FFT")

try:
    señal = np.loadtxt(DATA_FILE, skiprows=SKIP_ROWS, usecols=[COL_EMG])
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
# PASO 3: FFT POR CONTRACCIÓN — espectro de amplitud (frecuencia vs magnitud)
#         (guía C-a y C-b)
# ============================================================================

def calcular_fft(segmento, fs):
    n        = len(segmento)
    freqs    = np.fft.fftfreq(n, 1/fs)
    magnitud = np.abs(np.fft.fft(segmento)) / n   # amplitud normalizada
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

    pico = freqs[np.argmax(magnitud)]   # frecuencia del pico espectral (C-e)

    return freqs, magnitud, mf, mpf, pico


espectros  = []
resultados = []

for i, seg in enumerate(segmentos):
    freqs, magnitud, mf, mpf, pico = calcular_fft(seg, FS)
    espectros.append((freqs, magnitud))
    resultados.append({'Contraccion': i+1, 'MF (Hz)': mf, 'MPF (Hz)': mpf, 'Pico (Hz)': pico})
    print(f"  Contracción {i+1}:  MF={mf:.1f} Hz | MPF={mpf:.1f} Hz | Pico={pico:.1f} Hz")

    # Espectro individual con marcadores (C-b)
    plt.figure(figsize=(12, 4))
    plt.plot(freqs, magnitud, linewidth=1, color='navy')
    plt.axvline(pico, color='red',    linestyle='--', linewidth=1, label=f'Pico: {pico:.1f} Hz')
    plt.axvline(mf,   color='orange', linestyle='--', linewidth=1, label=f'MF: {mf:.1f} Hz')
    plt.axvline(mpf,  color='green',  linestyle='--', linewidth=1, label=f'MPF: {mpf:.1f} Hz')
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Magnitud (normalizada)')
    plt.title(f'Espectro de Amplitud FFT - Contracción {i+1}')
    plt.xlim([0, FS/2])
    plt.legend(fontsize=9)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / f'01_espectro_contraccion_{i+1:02d}.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  Guardado: 01_espectro_contraccion_{i+1:02d}.png")

df = pd.DataFrame(resultados)
print("\nTABLA DE RESULTADOS:")
print(df.to_string(index=False))

# ============================================================================
# PASO 4: COMPARACIÓN PRIMERA vs ÚLTIMA CONTRACCIÓN (guía C-c)
# ============================================================================

freqs_1, mag_1 = espectros[0]
freqs_n, mag_n = espectros[-1]

plt.figure(figsize=(13, 5))
plt.plot(freqs_1, mag_1, linewidth=1.2, color='steelblue', label='Contracción 1 (inicial)')
plt.plot(freqs_n, mag_n, linewidth=1.2, color='crimson',   label=f'Contracción {NUM_CONTRACCIONES} (final)')
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Magnitud (normalizada)')
plt.title('Comparación Espectral: Primera vs Última Contracción')
plt.xlim([0, FS/2])
plt.legend(fontsize=10)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / '02_comparacion_primera_ultima.png', dpi=300, bbox_inches='tight')
plt.close()
print("Guardado: 02_comparacion_primera_ultima.png")

# ============================================================================
# PASO 5: ESPECTROS SUPERPUESTOS (C-c y C-d)
# ============================================================================

colores = plt.cm.RdYlGn_r(np.linspace(0, 1, NUM_CONTRACCIONES))

plt.figure(figsize=(13, 6))
for i, (freqs, magnitud) in enumerate(espectros):
    plt.plot(freqs, magnitud, linewidth=1, color=colores[i],
             alpha=0.85, label=f'Contracción {i+1}')
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Magnitud (normalizada)')
plt.title('Espectros FFT Superpuestos — Evolución con Fatiga\n(verde=inicial  →  rojo=fatiga)')
plt.xlim([0, FS/2])
plt.legend(fontsize=9)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / '03_espectros_superpuestos.png', dpi=300, bbox_inches='tight')
plt.close()
print("Guardado: 03_espectros_superpuestos.png")

# ============================================================================
# PASO 6: EVOLUCIÓN DEL PICO ESPECTRAL, MF Y MPF (guía C-e)
# ============================================================================

contracciones = df['Contraccion'].values
mf_vals       = df['MF (Hz)'].values
mpf_vals      = df['MPF (Hz)'].values
pico_vals     = df['Pico (Hz)'].values

fig, axes = plt.subplots(1, 3, figsize=(16, 5))

for ax, vals, color, label in zip(
    axes,
    [mf_vals, mpf_vals, pico_vals],
    ['steelblue', 'coral', 'purple'],
    ['Frecuencia Media (MF)', 'Frecuencia Mediana (MPF)', 'Pico Espectral']
):
    ax.plot(contracciones, vals, 'o-', linewidth=2, markersize=8, color=color)
    ax.fill_between(contracciones, vals, alpha=0.15, color=color)
    ax.set(xlabel='Contracción', ylabel='Hz', title=f'Evolución {label}')
    ax.set_xticks(contracciones)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / '04_evolucion_pico_mf_mpf.png', dpi=300, bbox_inches='tight')
plt.close()
print("Guardado: 04_evolucion_pico_mf_mpf.png")

# ============================================================================
# PASO 7: DESPLAZAMIENTO DEL PICO ESPECTRAL (guía C-e)
# ============================================================================

desplazamiento_pico = pico_vals[-1] - pico_vals[0]
desplazamiento_mf   = mf_vals[-1]   - mf_vals[0]
desplazamiento_mpf  = mpf_vals[-1]  - mpf_vals[0]

print(f"\nDesplazamiento espectral (contracción 1 → {NUM_CONTRACCIONES}):")
print(f"  Pico : {pico_vals[0]:.1f} Hz → {pico_vals[-1]:.1f} Hz  ({desplazamiento_pico:+.1f} Hz)")
print(f"  MF   : {mf_vals[0]:.1f} Hz → {mf_vals[-1]:.1f} Hz  ({desplazamiento_mf:+.1f} Hz)")
print(f"  MPF  : {mpf_vals[0]:.1f} Hz → {mpf_vals[-1]:.1f} Hz  ({desplazamiento_mpf:+.1f} Hz)")

if desplazamiento_mf < 0 or desplazamiento_mpf < 0:
    print("\n  Desplazamiento hacia BAJAS frecuencias detectado.")
    print("  Consistente con fatiga muscular progresiva.")
else:
    print("\n  Sin desplazamiento significativo hacia bajas frecuencias.")

# ============================================================================
# PASO 8: GUARDAR CSV Y REPORTE
# ============================================================================

df.to_csv(OUTPUT_DIR / 'resultados_parte_c.csv', index=False)
print("Guardado: resultados_parte_c.csv")

with open(OUTPUT_DIR / 'reporte_parte_c.txt', 'w', encoding='utf-8') as f:
    f.write("PARTE C - ANÁLISIS ESPECTRAL MEDIANTE FFT\n\n")
    f.write(f"FS: {FS} Hz | Contracciones: {NUM_CONTRACCIONES}\n")
    f.write("Filtro pasa banda: 20-450 Hz (Butterworth orden 4)\n\n")
    f.write(df.to_string(index=False))
    f.write("\n\nDESPLAZAMIENTO ESPECTRAL:\n")
    f.write(f"  Pico : {pico_vals[0]:.1f} → {pico_vals[-1]:.1f} Hz ({desplazamiento_pico:+.1f} Hz)\n")
    f.write(f"  MF   : {mf_vals[0]:.1f} → {mf_vals[-1]:.1f} Hz ({desplazamiento_mf:+.1f} Hz)\n")
    f.write(f"  MPF  : {mpf_vals[0]:.1f} → {mpf_vals[-1]:.1f} Hz ({desplazamiento_mpf:+.1f} Hz)\n")

print("Guardado: reporte_parte_c.txt")
print("\nPARTE C COMPLETADA. Resultados en:", OUTPUT_DIR.absolute())