from src.backtest import MarketMaker
import optuna
from optuna.samplers import TPESampler
from src.settings import *

def optuna_objective(trial):
    spread = trial.suggest_float("spread", 0.00001, 0.0002, step=0.00001)
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
    study.optimize(optuna_objective, n_trials=100, show_progress_bar=True)

    # Show best trial results
    best_trial = study.best_trial
    print("\n### Best Trial Results ###")
    print(f"  Value (PnL): {best_trial.value}")
    print("  Parameters:")
    for key, value in best_trial.params.items():
        print(f"    {key}: {value}")

    # Saving the post optimization params
    post_optimized_params = {
        "order_size": best_trial.params["order_size"],
        "spread": best_trial.params["spread"],
        "wait_time": best_trial.params["wait_time"],
    }

    input("\nPress Enter to exit...")
