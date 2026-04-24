"""
PARTE A: ANÁLISIS DE SEÑAL EMULADA (SINTÉTICA) - VERSIÓN CORREGIDA
Procesamiento Digital de Señales - Laboratorio EMG
Universidad Militar Nueva Granada

"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

# ============================================================================
# CONFIGURACIÓN  ← AJUSTAR SEGÚN TUS DATOS
# ============================================================================

DATA_FILE        = Path(r"simulada.txt")  # Ruta al archivo .txt
FS               = 1000                  # Frecuencia de muestreo (Hz)
NUM_CONTRACCIONES = 5                   # Número de contracciones

OUTPUT_DIR = Path("./resultados_parte_a")
OUTPUT_DIR.mkdir(exist_ok=True)

plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.figsize'] = (14, 8)

# ============================================================================
# PASO 1: CARGAR SEÑAL
# ============================================================================

print("="*80)
print("PARTE A: ANÁLISIS DE SEÑAL EMULADA (SINTÉTICA)")
print("="*80)

try:
    señal = np.loadtxt(DATA_FILE)

except FileNotFoundError:
    print(f"ERROR: No se encontró '{DATA_FILE}'. Verifica la ruta.")
    raise SystemExit(1)
except Exception as e:
    print(f"ERROR al cargar archivo TXT: {e}")
    raise SystemExit(1)

# Asegurar que la señal sea 1D
señal = np.array(señal).flatten().astype(np.float64)

print(f"\n[PASO 1] Señal cargada:")
print(f"  Muestras: {len(señal)}")
print(f"  Duración: {len(señal)/FS:.2f} s")
print(f"  FS: {FS} Hz")
print(f"  Rango: [{np.min(señal):.4f}, {np.max(señal):.4f}]")
print(f"  Media: {np.mean(señal):.4f}")
print(f"  Desv.Est: {np.std(señal):.4f}")

# ============================================================================
# PASO 2: SEÑAL BRUTA
# ============================================================================

print(f"\n[PASO 2] Graficando señal bruta...")

tiempo = np.arange(len(señal)) / FS

plt.figure(figsize=(14, 5))
plt.plot(tiempo, señal, linewidth=0.8, color='steelblue')
plt.xlabel('Tiempo (s)', fontsize=11, fontweight='bold')
plt.ylabel('Amplitud (unidades ADC)', fontsize=11, fontweight='bold')
plt.title('PARTE A - Señal EMG Emulada - Señal Bruta', fontsize=12, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / '01_señal_bruta.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Guardado: 01_señal_bruta.png")

# ============================================================================
# PASO 3: SEGMENTAR EN CONTRACCIONES
# ============================================================================

print(f"\n[PASO 3] Segmentando en {NUM_CONTRACCIONES} contracciones...")

tam = len(señal) // NUM_CONTRACCIONES
segmentos = [
    señal[i*tam : (i+1)*tam if i < NUM_CONTRACCIONES-1 else len(señal)]
    for i in range(NUM_CONTRACCIONES)
]

for i, seg in enumerate(segmentos):
    print(f"  Contracción {i+1}: {len(seg):6d} muestras ({len(seg)/FS:6.3f} s)")

# ============================================================================
# PASO 4: SEGMENTOS SUPERPUESTOS
# ============================================================================

print(f"\n[PASO 4] Graficando segmentos superpuestos...")

fig, ax = plt.subplots(figsize=(14, 6))
colores = plt.cm.viridis(np.linspace(0, 1, NUM_CONTRACCIONES))

for i, seg in enumerate(segmentos):
    ax.plot(np.arange(len(seg))/FS, seg, linewidth=1.2,
            label=f'Contracción {i+1}', color=colores[i], alpha=0.8)

ax.set_xlabel('Tiempo (s)', fontsize=11, fontweight='bold')
ax.set_ylabel('Amplitud (unidades ADC)', fontsize=11, fontweight='bold')
ax.set_title('PARTE A - Contracciones Segmentadas', fontsize=12, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.legend(fontsize=9, loc='best')
plt.tight_layout()
plt.savefig(OUTPUT_DIR / '02_segmentos.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Guardado: 02_segmentos.png")

# ============================================================================
# PASO 5: CALCULAR FRECUENCIA MEDIA (MF) Y FRECUENCIA MEDIANA (MPF)
# ============================================================================

print(f"\n[PASO 5] Calculando MF (Frecuencia Media) y MPF (Frecuencia Mediana)...")

def calcular_mf_mpf(segmento, fs):
    """
    Calcula MF y MPF usando FFT
    
    MF  = Σ(frecuencia_i × potencia_i) / Σ(potencia_i)
    MPF = frecuencia donde se acumula 50% de potencia
    """
    n = len(segmento)
    freqs    = np.fft.fftfreq(n, 1/fs)
    potencia = np.abs(np.fft.fft(segmento)) ** 2

    # Solo frecuencias positivas
    idx_pos  = freqs > 0
    freqs    = freqs[idx_pos]
    potencia = potencia[idx_pos]
    pot_total = np.sum(potencia)

    # Frecuencia media
    mf  = np.sum(freqs * potencia) / pot_total if pot_total > 0 else 0.0

    # Frecuencia mediana
    pot_acum = np.cumsum(potencia)
    idx_med  = np.where(pot_acum >= pot_total / 2)[0]
    mpf = freqs[idx_med[0]] if len(idx_med) > 0 and pot_total > 0 else 0.0

    return mf, mpf, freqs, potencia

resultados = []
for i, seg in enumerate(segmentos):
    mf, mpf, _, _ = calcular_mf_mpf(seg, FS)
    resultados.append({'Contraccion': i+1, 'MF (Hz)': mf, 'MPF (Hz)': mpf})
    print(f"  Contracción {i+1}:  MF = {mf:8.2f} Hz  |  MPF = {mpf:8.2f} Hz")

df = pd.DataFrame(resultados)
print("\nTABLA DE RESULTADOS:")
print(df.to_string(index=False))

# ============================================================================
# PASO 6: EVOLUCIÓN DE MF Y MPF
# ============================================================================

print(f"\n[PASO 6] Graficando evolución de frecuencias...")

contracciones = df['Contraccion'].values
mf_vals  = df['MF (Hz)'].values
mpf_vals = df['MPF (Hz)'].values

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# MF
ax1.plot(contracciones, mf_vals, 'o-', linewidth=2.5, markersize=10, 
         color='steelblue', markerfacecolor='lightblue', markeredgewidth=2)
ax1.fill_between(contracciones, mf_vals, alpha=0.2, color='steelblue')
ax1.set_xlabel('Número de Contracción', fontsize=11, fontweight='bold')
ax1.set_ylabel('MF (Hz)', fontsize=11, fontweight='bold')
ax1.set_title('Evolución de Frecuencia Media (MF)', fontsize=12, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.set_xticks(contracciones)

# MPF
ax2.plot(contracciones, mpf_vals, 's-', linewidth=2.5, markersize=10, 
         color='coral', markerfacecolor='lightsalmon', markeredgewidth=2)
ax2.fill_between(contracciones, mpf_vals, alpha=0.2, color='coral')
ax2.set_xlabel('Número de Contracción', fontsize=11, fontweight='bold')
ax2.set_ylabel('MPF (Hz)', fontsize=11, fontweight='bold')
ax2.set_title('Evolución de Frecuencia Mediana (MPF)', fontsize=12, fontweight='bold')
ax2.grid(True, alpha=0.3)
ax2.set_xticks(contracciones)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / '03_evolucion_frecuencias.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Guardado: 03_evolucion_frecuencias.png ⭐")

# ============================================================================
# PASO 7: ESPECTROS FFT POR CONTRACCIÓN (ESCALA LOGARÍTMICA CORREGIDA)
# ============================================================================

print(f"\n[PASO 7] Generando espectros FFT (escala logarítmica en dB)...")

for i, seg in enumerate(segmentos):
    _, _, freqs, potencia = calcular_mf_mpf(seg, FS)
    
    # ✓ CONVERSIÓN A dB (ESCALA LOGARÍTMICA CORRECTA)
    potencia_db = 10 * np.log10(potencia / np.max(potencia) + 1e-10)

    fig, axes = plt.subplots(2, 1, figsize=(12, 8))
    
    # Espectro superior: escala dB (RECOMENDADO)
    axes[0].plot(freqs, potencia_db, linewidth=1, color='navy')
    axes[0].set_xlabel('Frecuencia (Hz)', fontsize=10, fontweight='bold')
    axes[0].set_ylabel('Potencia (dB)', fontsize=10, fontweight='bold')
    axes[0].set_title(f'Espectro FFT - Contracción Emulada {i+1} (Escala LOG: dB)', 
                      fontsize=11, fontweight='bold')
    axes[0].set_xlim([0, 500])
    axes[0].set_ylim([-80, 5])  # Rango dinámico típico
    axes[0].grid(True, alpha=0.3)
    
    # Espectro inferior: escala lineal (para comparación)
    axes[1].plot(freqs, potencia, linewidth=1, color='darkred')
    axes[1].set_xlabel('Frecuencia (Hz)', fontsize=10, fontweight='bold')
    axes[1].set_ylabel('Potencia (unidades²)', fontsize=10, fontweight='bold')
    axes[1].set_title(f'Espectro FFT - Contracción Emulada {i+1} (Escala LINEAL)', 
                      fontsize=11, fontweight='bold')
    axes[1].set_xlim([0, 500])
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    nombre = f'04_fft_contraccion_{i+1:02d}.png'
    plt.savefig(OUTPUT_DIR / nombre, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  ✓ Guardado: {nombre}")

# ============================================================================
# PASO 8: ANÁLISIS DE VARIACIÓN
# ============================================================================

print(f"\n[PASO 8] Análisis de variación de frecuencias...")

cambio_mf  = ((mf_vals[-1]  - mf_vals[0])  / mf_vals[0])  * 100 if mf_vals[0]  != 0 else 0
cambio_mpf = ((mpf_vals[-1] - mpf_vals[0]) / mpf_vals[0]) * 100 if mpf_vals[0] != 0 else 0

print(f"\n  Cambios en parámetros espectrales:")
print(f"  MF  : {mf_vals[0]:7.2f} Hz → {mf_vals[-1]:7.2f} Hz  ({cambio_mf:+7.2f}%)")
print(f"  MPF : {mpf_vals[0]:7.2f} Hz → {mpf_vals[-1]:7.2f} Hz  ({cambio_mpf:+7.2f}%)")
print(f"\n  Variabilidad (Desv. Est.):")
print(f"  MF  : ±{np.std(mf_vals):.2f} Hz")
print(f"  MPF : ±{np.std(mpf_vals):.2f} Hz")

# ============================================================================
# PASO 9: GUARDAR CSV Y REPORTE
# ============================================================================

print(f"\n[PASO 9] Guardando resultados...")

df.to_csv(OUTPUT_DIR / 'resultados_emulada.csv', index=False)
print("  ✓ Guardado: resultados_emulada.csv")

if abs(cambio_mf) < 5 and abs(cambio_mpf) < 5:
    interpretacion = ("Señal ESTABLE. Cambios mínimos (<5%), sin evidencia de fatiga.\n"
                     "Comportamiento esperado para señal emulada (sin variación).\n"
                     "Sirve como línea base para comparación con señal real.")
else:
    interpretacion = (f"Cambio detectable ({abs(cambio_mf):.1f}% en MF).\n"
                     "Posible variación controlada en el generador de señales.")

with open(OUTPUT_DIR / 'reporte_emulada.txt', 'w', encoding='utf-8') as f:
    f.write("="*80 + "\n")
    f.write("PARTE A - ANÁLISIS DE SEÑAL EMULADA\n")
    f.write("="*80 + "\n\n")
    f.write(f"FS: {FS} Hz | Duración: {len(señal)/FS:.2f} s | Contracciones: {NUM_CONTRACCIONES}\n\n")
    f.write("RESULTADOS:\n")
    f.write(df.to_string(index=False))
    f.write(f"\n\nCambios:\n")
    f.write(f"MF  : {mf_vals[0]:.2f} → {mf_vals[-1]:.2f} Hz ({cambio_mf:+.2f}%)\n")
    f.write(f"MPF : {mpf_vals[0]:.2f} → {mpf_vals[-1]:.2f} Hz ({cambio_mpf:+.2f}%)\n\n")
    f.write("INTERPRETACIÓN:\n")
    f.write(interpretacion + "\n\n")
    f.write("NOTA SOBRE LAS GRÁFICAS FFT:\n")
    f.write("Las gráficas FFT (04_fft_contraccion_*.png) se muestran en DOS escalas:\n")
    f.write("1. SUPERIOR (dB - escala logarítmica): RECOMENDADA para análisis\n")
    f.write("   - Muestra mejor el rango dinámico completo\n")
    f.write("   - Rango: -80 a 0 dB (estándar en procesamiento de bioseñales)\n")
    f.write("2. INFERIOR (lineal): Para comparación visual\n")
    f.write("   - Muestra la distribución de potencia sin logaritmo\n")

print("  ✓ Guardado: reporte_emulada.txt")

print("\n" + "="*80)
print("✓ PARTE A COMPLETADA EXITOSAMENTE")
print("="*80)
print(f"\nArchivos guardados en: {OUTPUT_DIR.absolute()}")
print(f"\nGráficas generadas:")
print(f"  1. 01_señal_bruta.png")
print(f"  2. 02_segmentos.png")
print(f"  3. 03_evolucion_frecuencias.png ⭐")
print(f"  4. 04_fft_contraccion_01.png ... 0{NUM_CONTRACCIONES}.png (ESCALA LOG CORREGIDA)")
print(f"\nDatos generados:")
print(f"  • resultados_emulada.csv")
print(f"  • reporte_emulada.txt")
print("="*80)
