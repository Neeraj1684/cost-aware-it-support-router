import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import joblib
from ml_pipeline.config import DATA_DIR, ARTIFACTS_DIR

df = pd.read_csv(DATA_DIR / "aa_dataset-tickets-multi-lang-5-2-50-version.csv")

df['combined_text'] = "Subject: " + df['subject'].astype(str) + " | Body: " + df['body'].astype(str)

df = df.dropna(subset=['combined_text'])

print("Initializing local HuggingFace embedding model on GPU...")
embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

df_sample = df.sample(n=5000, random_state=42).copy()
print("Generating semantic embeddings for 5000 rows...")
embeddings = embedding_model.encode(df_sample['combined_text'].tolist(), show_progress_bar=True)
print(f"Embedding Matrix Shape: {embeddings.shape}")

inertia = []
K_range = range(2,11)

print("\nCalculating inertia for different cluster counts...")
for i in K_range:
    kmeans = KMeans(
        n_clusters = i,
        init = 'k-means++',
        random_state = 42,
        n_init = 10
    )

    kmeans.fit(embeddings)
    inertia.append(kmeans.inertia_)

# plt.figure(figsize=(10,6))
# plt.plot(K_range, inertia, 'bx-')
# plt.xlabel('Number of Clusters (k)')
# plt.ylabel('Inertia (Within-cluster Sum of Squares)')
# plt.title('Elbow Method For Optimal k')
# plt.show()

optimal_k = 5
kmeans = KMeans(
    n_clusters=optimal_k,
    init='k-means++',
    random_state=42,
    n_init=10
)
df_sample['cluster_label'] = kmeans.fit_predict(embeddings)

for cluster_id in range(optimal_k):
    print(f"\n--- INSPECTING CLUSTER {cluster_id} ---")
    sample_tickets = df_sample[df_sample['cluster_label'] == cluster_id]['combined_text'].head(3).tolist()
    for i, ticket in enumerate(sample_tickets):
        print(f"Sample {i+1}: {ticket[:150]}...")


validation_matrix = pd.crosstab(df_sample['cluster_label'], df_sample['queue'])
print("\n\n",validation_matrix)

print("\nSaving data artifacts for the supervised training pipeline...")
joblib.dump(embeddings, ARTIFACTS_DIR / "embeddings_5k.joblib")
joblib.dump(df_sample['cluster_label'].values, ARTIFACTS_DIR / "cluster_labels_5k.joblib")
print("Saved! You can now use train_router.py without regenerating embeddings.")