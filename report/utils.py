import pickle
from pathlib import Path

# Absolute path to project root
project_root = Path(__file__).resolve().parents[1]

# Path to model file
model_path = project_root / "assets" / "model.pkl"

def load_model():
    with model_path.open('rb') as file:
        model = pickle.load(file)
    return model
