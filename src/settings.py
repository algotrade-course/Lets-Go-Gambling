# Market Making params
pre_optimization_params = {
    "order_size": 1,
    "spread": 0.2 / 100,
    "wait_time": 1800,  # in seconds
}

data_params = {
    "future_code": "VN30F1M",
    "START_DATE": "2024-11-01",
    "END_DATE": "2024-11-30",
}

# In-sample and out-of-sample periods (remember to adjust limit if you use csv)
in_sample_params = {
    "future_code": "VN30F1M",
    "START_DATE": "2024-11-01",
    "END_DATE": "2024-11-06",
}

out_sample_params = {
    "future_code": "VN30F1M",
    "START_DATE": "2024-11-09",
    "END_DATE": "2024-11-16",
}

DATA_PATH_ROOT = "data/"
