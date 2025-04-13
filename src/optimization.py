from backtesting import MarketMaker, in_sample_params, out_sample_params, out_sample_data, in_sample_data
import optuna
from optuna.samplers import TPESampler


def optuna_objective(trial):
    spread = trial.suggest_float("spread", 0.00001, 0.02, step=0.00001)
    order_size = trial.suggest_int("order_size", 1, 10)
    wait_time = trial.suggest_int("wait_time", 60, 7200)

    model = MarketMaker(
        **in_sample_params,
        order_size=order_size,
        spread=spread,
        wait_time=wait_time,
        sample_data=in_sample_data,
    )

    result = model.run()

    if result is None:
        print("No historical data found")
        return float("-inf")

    return result["pnl"]


if __name__ == "__main__":
    # We set the seed for the sampler so that the process can be replicated later.
    sampler = TPESampler(seed=710)

    # Create study using the sampler to maximize the objective function
    study = optuna.create_study(sampler=sampler, direction='maximize')

    # Optimize objective function
    print("### Starting hyperparameter optimization... ###")
    study.optimize(optuna_objective, n_trials=15, show_progress_bar=True)

    # Show best trial results
    best_trial = study.best_trial
    print("\n### Best Trial Results ###")
    print(f"  Value (PnL): {best_trial.value}")
    print("  Parameters:")
    for key, value in best_trial.params.items():
        print(f"    {key}: {value}")

    # Run the algorithm with the best parameter sets through the out-sample period
    print("\n### Running on Out-of-Sample Data... ###")
    out_sample_model = MarketMaker(
        sample_data=out_sample_data,
        **out_sample_params,
        **best_trial.params
    )
    out_sample_results = out_sample_model.full_run()

    input("\nPress Enter to exit...")
