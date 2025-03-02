import numpy as np
from typing import List

def sharpe_ratio(
    period_returns: List[float],
    risk_free_return: float
) -> float:
    r"""Returns the Sharpe Ratio. Formula (in LaTeX):
    .. math::
        Sharpe = \frac{R_x - R_f}{\sigma_{R_x}}

    Args:
        period_returns (List): The list of annual returns of the portfolio.
        risk_free_return: The risk-free return rate.
    
    Returns:
        Sharpe ratio of the portfolio.

    Raises:
        ValueError: If the input of annual_returns is None or an empty list.
    """
    # Your function should raise an error if the annual_returns is None or an empty list.
    # YOUR CODE HERE
    if not period_returns:
        raise ValueError("period_returns cannot be None or an empty list")
        
    average_return = sum(period_returns) / len(period_returns)
    std_dev = np.std(period_returns, ddof = 1)
    sharpe = (average_return - risk_free_return) / std_dev
    return sharpe

def maximum_drawdown(period_returns: List[float]) -> float:
    """Returns the Maximum Drawdown (MDD) of the portfolio.

    Args:
        period_returns (List of float): The period returns of the portfolio.

    Returns:
        The Maximum Drawdown (MDD) of the portfolio.

    Raises:
        ValueError when:
        - The period_returns is None or empty
        - The period_returns and benchmark_returns should not contain the value 1 (meaning all the capital of the portfolio is lost)
    """
    # Your function should raise ValueError according to the docstrings
    # Initial and peak asset
    peak = 1
    cur_asset = 1
    
    # YOUR CODE HERE
    if period_returns is None:
        raise ValueError("period_returns cannot be None")
    
    if not period_returns:
        raise ValueError("period_returns cannot be empty")

    if 1 in period_returns :
        raise ValueError("period_returns should not contain the value 1")

    MDD = 0; 
    for ret in period_returns:
        cur_asset *= 1 + ret
        peak = max(peak, cur_asset)
        drawdown = (cur_asset - peak) / peak
        MDD = min(MDD, drawdown)
    return MDD

