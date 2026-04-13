# ============================================
# PROYECTO: Clustering en transporte masivo
# ============================================

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# ============================================
# 1. CARGAR DATOS
# ============================================

data = pd.read_csv('transporte.csv')

print("📊 Primeros datos:")
print(data.head())

# ============================================
# 2. PREPROCESAMIENTO
# ============================================

# Convertir variables categóricas a numéricas
data['metodo_pago'] = data['metodo_pago'].map({'tarjeta': 1, 'efectivo': 0})
data['ruta'] = data['ruta'].map({'A': 0, 'B': 1, 'C': 2})

# Seleccionar variables para el modelo
X = data[['edad', 'viajes_dia', 'hora_pico', 'tiempo_espera', 'ruta', 'metodo_pago']]

# Escalar datos (IMPORTANTE para K-Means)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ============================================
# 3. MÉTODO DEL CODO (ELBOW METHOD)
# ============================================

inercia = []

for k in range(1, 8):
    modelo = KMeans(n_clusters=k, random_state=42)
    modelo.fit(X_scaled)
    inercia.append(modelo.inertia_)

plt.figure()
plt.plot(range(1, 8), inercia, marker='o')
plt.title('Método del Codo')
plt.xlabel('Número de clusters')
plt.ylabel('Inercia')
plt.grid()
plt.show()

print("\n👉 Según el gráfico, elegimos K = 3")

# ============================================
# 4. MODELO K-MEANS
# ============================================

kmeans = KMeans(n_clusters=3, random_state=42)
data['cluster'] = kmeans.fit_predict(X_scaled)

print("\n📊 Datos con cluster asignado:")
print(data.head())

# ============================================
# 5. ANÁLISIS DE CLUSTERS
# ============================================

print("\n📈 Promedio por cluster:")
analisis = data.groupby('cluster').mean()
print(analisis)

# ============================================
# 6. VISUALIZACIÓN
# ============================================

plt.figure()
plt.scatter(data['edad'], data['viajes_dia'], c=data['cluster'])
plt.xlabel('Edad')
plt.ylabel('Viajes por día')
plt.title('Segmentación de usuarios')
plt.grid()
plt.show()

# ============================================
# 7. INTERPRETACIÓN AUTOMÁTICA
# ============================================

print("\n🧠 INTERPRETACIÓN:")

for i in range(3):
    grupo = analisis.loc[i]
    print(f"\nCluster {i}:")
    
    if grupo['viajes_dia'] >= 3:
        print("- Usuarios frecuentes del sistema de transporte")
    else:
        print("- Usuarios ocasionales")
    
    if grupo['hora_pico'] > 0.5:
        print("- Usan transporte en horas pico")
    else:
        print("- Usan transporte en horarios normales")
    
    if grupo['tiempo_espera'] > 8:
        print("- Experimentan mayor tiempo de espera")
    else:
        print("- Tienen tiempos de espera bajos")

print("\n✅ Análisis finalizado correctamente.")