from src.settings import DATA_PATH_ROOT
import os

os.makedirs(DATA_PATH_ROOT, exist_ok=True)

data_path = os.path.join(DATA_PATH_ROOT, "data.csv")
optimize_result = os.path.join(DATA_PATH_ROOT, "optimize_result.json")
optimize_trials = os.path.join(DATA_PATH_ROOT, "optuna_trials.csv")
in_sample_data_path = os.path.join(DATA_PATH_ROOT, "in_sample_data.csv")
out_sample_data_path = os.path.join(DATA_PATH_ROOT, "out_sample_data.csv")