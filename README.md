# Plutus Project Template

Template repository of a Plutus Project.

This templte project sturcture also specifies how to store and structure the source code and report of a standard Plutus Project.

This `README.md` file serves as an example how a this will look like in a standard Plutus project. Below listed out the sample section.

## Abstract
- Summarize the project: motivation, methods, findings, etc.
- This project is for ALGOTRADE course, we use a simple Market Making stratergy and apply the first 7 steps in Algotrade. We found out that even after optimizing, the simple method is not good enough for the real market

## Introduction

In this project, we aim to develop and optimize a **Market Making strategy** using historical trading data from the **VN30F1M futures market**. Market Making is a common algorithmic trading strategy that involves continuously quoting buy and sell prices to profit from the bid-ask spread.

Despite the simplicity of Market Making as a trading strategy, determining the optimal configuration for parameters such as **spread size**, **order volume**, and **timing intervals** is hard. Bad parameters can lead to poor performance, high inventory risk, and potential losses. The key problem, therefore, is:

> **How can we find the optimal set of Market Making parameters that maximize profit and minimize risk on the VN30F1M futures market?**

#### Method

To solve this problem, we try to implemented a `MarketMaker` algorithm that accepts tunable parameters:

- `spread`: the distance from the mid-price at which to place quotes  
- `order_size`: the volume of each order  
- `wait_time`: the time interval between order refreshes

We used **Optuna** get the best parameters for in-sample-data

#### Results

- For the **in-sample data**, the strategy produced a **positive PnL**.
- However, for the **out-of-sample data**, the strategy still result in a **negative PnL**.
- The current parameters still cannot handle a rising or falling market well

## Related Work (or Background)
- Prerequisite reading if the audience needs knowledge before exploring the project.
- Optional

## Trading (Algorithm) Hypotheses
- Describe the Trading Hypotheses
- Step 1 of the Nine-Step

## Data
- Data source - algotradeDB
- Data type - 
- Data period
- How to get the input data? 
- In Src/backtesting, there are parameters that you can adjust
- in_sample_params: for getting in_sample_data
- out_sample_params: for getting out_sample_data
- market_making: for running MarketMaker within backtesting.py itself, this shouldn't affect optimization
- How to store the output data?
- i don't actually store them yet, i just print them out

### Data collection
- Step 2 of the Nine-Step
### Data Processing
- Step 3 of the Nine-Step

## Implementation
### Environment Setup
1. Set up python virtual environment
```bash
python -m venv venv
source venv/bin/activate # for Linux/MacOS
.\venv\Scripts\activate.bat # for Windows command line
.\venv\Scripts\Activate.ps1 # for Windows PowerShell
```
2. Install the required packages
```bash
pip install -r requirements.txt
```
3. (OPTIONAL) Create `.env` file in the root directory of the project and fill in the required information. The `.env` file is used to store environment variables that are used in the project. The following is an example of a `.env` file:
```env
DB_NAME=<database name>
DB_USER=<database user name>
DB_PASSWORD=<database password>
DB_HOST=<host name or IP address>
DB_PORT=<database port>
```
**Note:** Skip this step if you decide to use the provided data files on Google Drive (option 1).

## In-sample Backtesting
- Describe the In-sample Backtesting step
    - Parameters
    - Data
- Step 4 of the Nine-Step
### In-sample Backtesting Result
- Brieftly shown the result: table, image, etc.
- Has link to the In-sample Backtesting Report

## Optimization
- Library: Optuna
- Sampler: `TPESampler`
- Number of trials: 5000
- Optimization objective: 
```math
  0.8 \cdot \text{SR\_score} + 0.2 \cdot \text{MDD\_score}
```
Where:
  - `sharpe` varies from 0 to 1 as SR varies from 0 to 3.0.
  - `MDD_score` varies from 0 to 1 as MDD varies from -20% to -5%.
  - Check out [optimize.py](src/optimize.py) for more details.
### Optimization Result
- Brieftly shown the result: table, image, etc.
- Has link to the Optimization Report

## Out-of-sample Backtesting
- Describe the Out-of-sample Backtesting step
    - Parameter
    - Data
- Step 6 of th Nine-Step
### Out-of-sample Backtesting Reuslt
- Brieftly shown the result: table, image, etc.
- Has link to the Out-of-sample Backtesting Report

## Paper Trading
- Describe the Paper Trading step
- Step 7 of the Nine-Step
- Optional
### Optimization Result
- Brieftly shown the result: table, image, etc.
- Has link to the Paper Trading Report


## Conclusion
- What is the conclusion?
- Optional

## Reference
- All the reference goes here.

## Other information
- Link to the Final Report (Paper) should be somewhere in the `README.md` file.
- Please make sure this file is relatively easy to follow.
