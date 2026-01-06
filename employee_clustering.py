import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

df = pd.read_csv("data/employee_data.csv")

# Features
X = df.values

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Apply PCA
pca = PCA(n_components=1)
X_pca = pca.fit_transform(X_scaled)

print("Explained Variance Ratio:", pca.explained_variance_ratio_)

# Elbow Method
wcss = []
for k in range(1, 8):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X_pca)
    wcss.append(kmeans.inertia_)

plt.plot(range(1, 8), wcss, marker='o')
plt.xlabel("Number of Clusters (K)")
plt.ylabel("WCSS")
plt.title("Elbow Method")
plt.savefig("outputs/elbow_plot.png")
plt.close()

# Apply K-Means
kmeans = KMeans(n_clusters=3, random_state=42)
df["Cluster"] = kmeans.fit_predict(X_pca)

# Save clustered data
df.to_csv("outputs/clustered_employees.csv", index=False)

# Visualize clusters (1D)
y_dummy = np.zeros(len(X_pca))
plt.scatter(X_pca[:, 0], y_dummy, c=df["Cluster"], cmap="viridis")
plt.scatter(
    kmeans.cluster_centers_[:, 0],
    np.zeros(len(kmeans.cluster_centers_)),
    c="red",
    s=200,
    marker="X"
)
plt.xlabel("PCA Component 1")
plt.yticks([])
plt.title("Employee Work-Style Clustering (PCA + K-Means)")
plt.savefig("outputs/cluster_plot.png")
plt.close()