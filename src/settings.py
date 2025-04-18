from src.data_accessing import collect_data_from_csv

# Market Making params
pre_optimization_params = {
    "order_size": 1,
    "spread": 0.2 / 100,
    "wait_time": 1800,  # in seconds
}

post_optimized_params = {
    "order_size": 1,
    "spread": 0.0001,
    "wait_time": 1800,  # in seconds
}

# In-sample and out-of-sample periods
in_sample_params = {
    "future_code": "VN30F1M",
    "START_DATE": "2024-12-01",
    "END_DATE": "2024-12-12",
}

out_sample_params = {
    "future_code": "VN30F1M",
    "START_DATE": "2024-11-03",
    "END_DATE": "2024-11-11",
}

in_sample_data = collect_data_from_csv(
    in_sample_params["future_code"],
    in_sample_params["START_DATE"],
    in_sample_params["END_DATE"]
)

out_sample_data = collect_data_from_csv(
    out_sample_params["future_code"],
    out_sample_params["START_DATE"],
    out_sample_params["END_DATE"]
)