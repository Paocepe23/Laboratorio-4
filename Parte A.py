"""
PARTE A: ANÁLISIS DE SEÑAL EMULADA (SINTÉTICA)
Procesamiento Digital de Señales - Laboratorio EMG
Universidad Militar Nueva Granada
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import h5py
from pathlib import Path

# ============================================================================
# CONFIGURACIÓN  ← AJUSTAR SEGÚN TUS DATOS
# ============================================================================

DATA_FILE        = Path(r"opensiseñalda.h5")  # Ruta al archivo .h5
FS               = 1000                        # Frecuencia de muestreo (Hz)
NUM_CONTRACCIONES = 5                          # Número de contracciones

OUTPUT_DIR = Path("./resultados_parte_a")
OUTPUT_DIR.mkdir(exist_ok=True)

plt.style.use('seaborn-v0_8-darkgrid')

# ============================================================================
# PASO 1: CARGAR SEÑAL
# ============================================================================

print("PARTE A: ANÁLISIS DE SEÑAL EMULADA")

try:
    with h5py.File(DATA_FILE, 'r') as f:
        # Estructura OpenSignals: <MAC> → raw → channel_1
        mac   = list(f.keys())[0]
        datos = np.array(f[mac]['raw']['channel_1'])  # shape (92850, 1), uint32
        señal = datos.flatten().astype(np.float64)    # convertir a float para operar

except FileNotFoundError:
    print(f"ERROR: No se encontró '{DATA_FILE}'. Verifica la ruta.")
    raise SystemExit(1)
except Exception as e:
    print(f"ERROR al cargar HDF5: {e}")
    raise SystemExit(1)


print(f"Muestras: {len(señal)} | Duración: {len(señal)/FS:.2f} s | "
      f"Min: {np.min(señal):.4f} | Max: {np.max(señal):.4f} | "
      f"Media: {np.mean(señal):.4f} | Desv.Est: {np.std(señal):.4f}")

# ============================================================================
# PASO 2: SEÑAL BRUTA
# ============================================================================

tiempo = np.arange(len(señal)) / FS

plt.figure(figsize=(14, 5))
plt.plot(tiempo, señal, linewidth=0.8, color='steelblue')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud (unidades ADC)')
plt.title('Señal EMG Emulada - Señal Bruta')
plt.tight_layout()
plt.savefig(OUTPUT_DIR / '01_señal_bruta.png', dpi=300, bbox_inches='tight')
plt.close()
print("Guardado: 01_señal_bruta.png")

# ============================================================================
# PASO 3: SEGMENTAR EN CONTRACCIONES (divisiones iguales)
# ============================================================================

tam = len(señal) // NUM_CONTRACCIONES
segmentos = [
    señal[i*tam : (i+1)*tam if i < NUM_CONTRACCIONES-1 else len(señal)]
    for i in range(NUM_CONTRACCIONES)
]

for i, seg in enumerate(segmentos):
    print(f"  Contracción {i+1}: {len(seg)} muestras ({len(seg)/FS:.3f} s)")

# ============================================================================
# PASO 4: SEGMENTOS SUPERPUESTOS
# ============================================================================

fig, ax = plt.subplots(figsize=(14, 6))
colores = plt.cm.viridis(np.linspace(0, 1, NUM_CONTRACCIONES))

for i, seg in enumerate(segmentos):
    ax.plot(np.arange(len(seg))/FS, seg, linewidth=1.2,
            label=f'Contracción {i+1}', color=colores[i], alpha=0.8)

ax.set_xlabel('Tiempo (s)')
ax.set_ylabel('Amplitud (unidades ADC)')
ax.set_title('Contracciones Segmentadas')
ax.legend(fontsize=9)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / '02_segmentos.png', dpi=300, bbox_inches='tight')
plt.close()
print("Guardado: 02_segmentos.png")

# ============================================================================
# PASO 5: FRECUENCIA MEDIA (MF) Y FRECUENCIA MEDIANA (MPF) VÍA FFT
# ============================================================================

def calcular_mf_mpf(segmento, fs):
    n = len(segmento)
    freqs    = np.fft.fftfreq(n, 1/fs)
    potencia = np.abs(np.fft.fft(segmento)) ** 2

    idx_pos  = freqs > 0
    freqs    = freqs[idx_pos]
    potencia = potencia[idx_pos]
    pot_total = np.sum(potencia)

    mf  = np.sum(freqs * potencia) / pot_total if pot_total > 0 else 0.0

    pot_acum = np.cumsum(potencia)
    idx_med  = np.where(pot_acum >= pot_total / 2)[0]
    mpf = freqs[idx_med[0]] if len(idx_med) > 0 and pot_total > 0 else 0.0

    return mf, mpf, freqs, potencia


resultados = []
for i, seg in enumerate(segmentos):
    mf, mpf, _, _ = calcular_mf_mpf(seg, FS)
    resultados.append({'Contraccion': i+1, 'MF (Hz)': mf, 'MPF (Hz)': mpf})
    print(f"  Contracción {i+1}:  MF = {mf:.2f} Hz  |  MPF = {mpf:.2f} Hz")

df = pd.DataFrame(resultados)
print("\nTABLA DE RESULTADOS:")
print(df.to_string(index=False))

# ============================================================================
# PASO 6: EVOLUCIÓN DE MF Y MPF
# ============================================================================

contracciones = df['Contraccion'].values
mf_vals  = df['MF (Hz)'].values
mpf_vals = df['MPF (Hz)'].values

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

ax1.plot(contracciones, mf_vals, 'o-', linewidth=2, markersize=8, color='steelblue')
ax1.fill_between(contracciones, mf_vals, alpha=0.2, color='steelblue')
ax1.set(xlabel='Contracción', ylabel='MF (Hz)', title='Evolución Frecuencia Media (MF)')
ax1.set_xticks(contracciones)

ax2.plot(contracciones, mpf_vals, 's-', linewidth=2, markersize=8, color='coral')
ax2.fill_between(contracciones, mpf_vals, alpha=0.2, color='coral')
ax2.set(xlabel='Contracción', ylabel='MPF (Hz)', title='Evolución Frecuencia Mediana (MPF)')
ax2.set_xticks(contracciones)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / '03_evolucion_frecuencias.png', dpi=300, bbox_inches='tight')
plt.close()
print("Guardado: 03_evolucion_frecuencias.png")

# ============================================================================
# PASO 7: ESPECTROS FFT POR CONTRACCIÓN
# ============================================================================

for i, seg in enumerate(segmentos):
    _, _, freqs, potencia = calcular_mf_mpf(seg, FS)
    potencia_db = 10 * np.log10(potencia / np.max(potencia) + 1e-10)

    plt.figure(figsize=(12, 5))
    plt.plot(freqs, potencia_db, linewidth=1, color='navy')
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Potencia (dB normalizada)')
    plt.title(f'Espectro FFT - Contracción {i+1}')
    plt.xlim([0, FS/2])
    plt.tight_layout()
    nombre = f'04_fft_contraccion_{i+1:02d}.png'
    plt.savefig(OUTPUT_DIR / nombre, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Guardado: {nombre}")

# ============================================================================
# PASO 8: ANÁLISIS DE VARIACIÓN
# ============================================================================

cambio_mf  = ((mf_vals[-1]  - mf_vals[0])  / mf_vals[0])  * 100 if mf_vals[0]  != 0 else 0
cambio_mpf = ((mpf_vals[-1] - mpf_vals[0]) / mpf_vals[0]) * 100 if mpf_vals[0] != 0 else 0

print(f"\nMF  : {mf_vals[0]:.2f} Hz → {mf_vals[-1]:.2f} Hz  ({cambio_mf:+.2f} %)")
print(f"MPF : {mpf_vals[0]:.2f} Hz → {mpf_vals[-1]:.2f} Hz  ({cambio_mpf:+.2f} %)")
print(f"Desv. Est. MF: ±{np.std(mf_vals):.2f} Hz  |  MPF: ±{np.std(mpf_vals):.2f} Hz")

# ============================================================================
# PASO 9: GUARDAR CSV Y REPORTE
# ============================================================================

df.to_csv(OUTPUT_DIR / 'resultados_emulada.csv', index=False)
print("Guardado: resultados_emulada.csv")

if abs(cambio_mf) < 5 and abs(cambio_mpf) < 5:
    interpretacion = "Señal ESTABLE. Cambios mínimos, sin evidencia de fatiga muscular.\nComportamiento esperado para señal emulada. Sirve como línea base."
else:
    interpretacion = f"Cambio detectable ({abs(cambio_mf):.1f}% en MF). Posible variación en el generador."

with open(OUTPUT_DIR / 'reporte_emulada.txt', 'w', encoding='utf-8') as f:
    f.write("PARTE A - ANÁLISIS DE SEÑAL EMULADA\n\n")
    f.write(f"FS: {FS} Hz | Duración: {len(señal)/FS:.2f} s | Contracciones: {NUM_CONTRACCIONES}\n\n")
    f.write(df.to_string(index=False))
    f.write(f"\n\nMF : {mf_vals[0]:.2f} → {mf_vals[-1]:.2f} Hz ({cambio_mf:+.2f}%)\n")
    f.write(f"MPF: {mpf_vals[0]:.2f} → {mpf_vals[-1]:.2f} Hz ({cambio_mpf:+.2f}%)\n\n")
    f.write(interpretacion + "\n")

print("Guardado: reporte_emulada.txt")
print("\nPARTE A COMPLETADA. Resultados en:", OUTPUT_DIR.absolute())