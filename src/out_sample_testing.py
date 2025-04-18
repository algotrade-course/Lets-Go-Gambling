from src.backtest import MarketMaker
from src.settings import *

if __name__ == "__main__":
    # Run the algorithm with the best parameter sets through the out-sample period
    print("\n### Running on Out-of-Sample Data... ###")
    out_sample_model = MarketMaker(
        sample_data=out_sample_data,
        **out_sample_params
    )
    out_sample_results = out_sample_model.full_run()