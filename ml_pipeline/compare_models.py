import joblib
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

from ml_pipeline.config import ARTIFACTS_DIR, MODELS_DIR

X = joblib.load(ARTIFACTS_DIR / "embeddings.joblib")
y_kmeans = joblib.load(ARTIFACTS_DIR / "cluster_labels.joblib")

router = joblib.load(MODELS_DIR / "fast_router_model.joblib")

y_router = router.predict(X)

print(f"Agreement: {accuracy_score(y_kmeans, y_router):.4f}")

print("\nConfusion Matrix:")
print(confusion_matrix(y_kmeans, y_router))
print("\nClassification Report:")
print(classification_report(y_kmeans, y_router))