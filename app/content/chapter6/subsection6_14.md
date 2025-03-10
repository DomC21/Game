# 6.14 The Kelly Criterion (Advanced Sizing)

## Introduction
The Kelly Criterion is a mathematical formula that helps traders determine the optimal size for their positions based on the probability of success and the potential risk-reward ratio. Developed by John L. Kelly Jr. at Bell Labs in 1956, this approach has been adopted by professional gamblers, investors, and traders seeking to maximize long-term capital growth. This section explores the Kelly formula, its applications in trading, and important modifications for practical implementation.

## Understanding the Kelly Criterion

### The Basic Formula
The Kelly Criterion calculates the optimal percentage of your capital to risk on a single trade:

```
Kelly % = W - [(1 - W) / R]
```

Where:
- **W** = Winning probability (as a decimal)
- **R** = Win/loss ratio (average win ÷ average loss)
- **Kelly %** = Percentage of capital to risk on the trade

### Example Calculation
Suppose you have a trading strategy with:
- 60% win rate (W = 0.6)
- Average win of $300 (when you win)
- Average loss of $200 (when you lose)
- Win/loss ratio (R) = $300 ÷ $200 = 1.5

Applying the Kelly formula:
```
Kelly % = 0.6 - [(1 - 0.6) / 1.5]
Kelly % = 0.6 - [0.4 / 1.5]
Kelly % = 0.6 - 0.267
Kelly % = 0.333 or 33.3%
```

According to the Kelly Criterion, you should risk 33.3% of your capital on this trade to maximize long-term growth.

### Interpreting Kelly Results
The Kelly percentage represents the optimal fraction of your capital to risk on a single trade:

- **Positive Kelly %**: Indicates a positive expected value; you should take the trade
- **Zero Kelly %**: Indicates a break-even proposition; avoid the trade
- **Negative Kelly %**: Indicates a negative expected value; avoid the trade

The higher the Kelly percentage, the more favorable the opportunity, but also the more aggressive the position sizing.

## The Mathematics Behind Kelly

### Expected Value and Geometric Growth
The Kelly Criterion is designed to maximize the expected geometric growth rate of your capital over time, rather than simply maximizing expected value.

#### Expected Value
The expected value of a trade is calculated as:
```
EV = (W × Average Win) - [(1 - W) × Average Loss]
```

#### Geometric Growth Rate
The geometric growth rate accounts for the compounding effect of sequential trades:
```
G = (1 + r)^W × (1 - f)^(1-W)
```
Where:
- G = Geometric growth rate
- r = Return on winning trades
- f = Fraction lost on losing trades
- W = Winning probability

The Kelly Criterion finds the position size that maximizes this geometric growth rate.

### Derivation from Information Theory
Kelly originally derived his formula from information theory, specifically the concept of maximizing the expected logarithm of wealth. This approach accounts for the diminishing marginal utility of money and the asymmetric impact of gains and losses on a portfolio.

The mathematical derivation shows that maximizing the expected logarithm of wealth leads to the optimal growth strategy in the long run.

## Practical Applications in Trading

### Position Sizing with Kelly
To apply Kelly for position sizing:

1. Calculate the Kelly percentage using your strategy's win rate and win/loss ratio
2. Multiply your total capital by the Kelly percentage to determine the amount to risk
3. Calculate position size based on your stop-loss level

**Example:**
- Account size: $100,000
- Kelly percentage: 20%
- Amount to risk: $100,000 × 0.20 = $20,000
- Entry price: $50
- Stop-loss price: $45
- Risk per share: $5
- Position size: $20,000 ÷ $5 = 4,000 shares

### Portfolio Management with Kelly
For managing multiple positions:

1. Calculate the Kelly percentage for each trading opportunity
2. Adjust allocations based on correlations between positions
3. Ensure total portfolio risk remains within acceptable limits

When trading correlated assets, the optimal allocation is less than the individual Kelly percentages would suggest, as correlations increase overall portfolio risk.

### The Half-Kelly Approach
Many professional traders use "Half-Kelly" or even "Quarter-Kelly" sizing:

```
Half-Kelly % = Kelly % ÷ 2
```

**Rationale for Half-Kelly:**
- Reduces volatility and drawdowns significantly
- Still captures approximately 75% of the optimal growth rate
- Provides a margin of safety against estimation errors
- More psychologically manageable

### Fractional Kelly
More generally, you can use any fraction of the full Kelly:

```
Fractional Kelly % = f × Kelly %
```

Where f is the fraction (typically 0.25 to 0.5 for most traders).

The trade-off is between growth rate and volatility:
- Higher f = Higher growth rate but more volatility
- Lower f = Lower growth rate but less volatility

## Limitations and Challenges

### Estimation Errors
The Kelly formula is only as good as your inputs. Errors in estimating win rates or average win/loss amounts can lead to suboptimal or even dangerous position sizing.

#### Impact of Estimation Errors
- Overestimating win rate by just 10% can lead to significant overbetting
- Underestimating potential losses can result in excessive risk
- Small sample sizes can produce unreliable estimates

#### Mitigating Estimation Errors
- Use large sample sizes (100+ trades) for more reliable estimates
- Regularly update your estimates as new data becomes available
- Apply conservative adjustments to your inputs
- Use fractional Kelly to provide a margin of safety

### Volatility and Drawdowns
Full Kelly sizing can lead to extreme volatility and drawdowns:

- Theoretical maximum drawdown can exceed 50% even with positive expected value
- Psychological impact of large drawdowns can lead to abandoning the strategy
- Sequence of losses can significantly impact overall performance

### Non-Normal Return Distributions
The standard Kelly formula assumes a binary outcome (win or lose) with fixed payoffs. Real trading often involves:

- Multiple possible outcomes
- Skewed return distributions
- Fat-tailed distributions with extreme events
- Time-varying probabilities and payoffs

## Advanced Kelly Applications

### Continuous Kelly Formula
For non-binary outcomes or continuous return distributions:

```
f* = μ / σ²
```

Where:
- f* = Optimal fraction to invest
- μ = Expected excess return
- σ² = Variance of returns

This formula is applicable for normally distributed returns, such as those often assumed in stock market investments.

### Multiple Simultaneous Opportunities
When facing multiple uncorrelated trading opportunities simultaneously:

1. Calculate the Kelly percentage for each opportunity
2. Allocate capital to each opportunity according to its Kelly percentage
3. Ensure the total allocation doesn't exceed your risk tolerance

For correlated opportunities, matrix algebra is required to determine optimal allocations, accounting for the covariance between returns.

### Dynamic Kelly
In practice, market conditions change, affecting win rates and payoff ratios. Dynamic Kelly approaches:

1. Continuously update estimates based on recent market data
2. Adjust position sizing as market conditions evolve
3. Incorporate regime-switching models to adapt to different market environments
4. Use Bayesian methods to update probability estimates

## Implementing Kelly in Your Trading System

### Step 1: Gather Historical Data
Collect detailed statistics on your trading strategy:
- Win/loss ratio for each setup type
- Average win and average loss
- Distribution of returns
- Correlation between different setups

### Step 2: Calculate Base Kelly Percentage
Use the standard formula or appropriate variation based on your return distribution.

### Step 3: Apply Conservative Adjustments
- Use fractional Kelly (typically 25-50% of full Kelly)
- Round down estimates of win rates
- Round up estimates of potential losses
- Cap maximum position size regardless of Kelly calculation

### Step 4: Implement Position Sizing Rules
Create clear rules for:
- Maximum position size as a percentage of portfolio
- Maximum number of correlated positions
- Position size adjustments during drawdowns
- Regular recalibration of Kelly inputs

### Step 5: Monitor and Adjust
- Track actual performance against expected outcomes
- Update win rates and win/loss ratios based on recent results
- Adjust fractional Kelly based on drawdown experience
- Review and refine the system regularly

## Kelly vs. Other Position Sizing Methods

### Kelly vs. Fixed Percentage
- **Fixed Percentage**: Always risks the same percentage of capital (e.g., 2%)
- **Kelly**: Varies position size based on edge (expected value)
- **Advantage of Kelly**: Optimizes capital growth by betting more when edge is larger
- **Advantage of Fixed Percentage**: Simpler and more conservative

### Kelly vs. Fixed Dollar Amount
- **Fixed Dollar**: Always risks the same dollar amount regardless of account size
- **Kelly**: Scales with account size and edge
- **Advantage of Kelly**: Compounds capital more efficiently
- **Advantage of Fixed Dollar**: Easier to implement and psychologically simpler

### Kelly vs. Volatility-Based Sizing
- **Volatility-Based**: Adjusts position size based on market volatility
- **Kelly**: Adjusts based on edge (win rate and win/loss ratio)
- **Hybrid Approach**: Combine Kelly with volatility adjustment for more robust sizing

## Key Takeaways
- The Kelly Criterion calculates the optimal position size to maximize long-term capital growth
- The basic formula is Kelly % = W - [(1 - W) / R], where W is win probability and R is win/loss ratio
- Most professional traders use fractional Kelly (25-50% of full Kelly) to reduce volatility
- Estimation errors in win rates or payoff ratios can significantly impact Kelly calculations
- Advanced applications include continuous Kelly for non-binary outcomes and dynamic Kelly for changing market conditions
- Implementing Kelly requires careful data collection, conservative adjustments, and regular monitoring
- Kelly should be compared with other position sizing methods to determine the best approach for your trading style

## Mini-Quiz

### Question 1
If your trading strategy has a 55% win rate and a win/loss ratio of 1.2, what is the full Kelly percentage?
- A) 10%
- B) 22%
- C) 38.3%
- D) 55%

### Question 2
What is the primary advantage of using Half-Kelly instead of full Kelly sizing?
- A) It doubles your expected return
- B) It eliminates all risk of ruin
- C) It significantly reduces volatility while still capturing most of the optimal growth rate
- D) It works better for strategies with win rates below 50%

### Question 3
Which of the following is NOT a limitation of the Kelly Criterion?
- A) Sensitivity to estimation errors
- B) Potential for large drawdowns with full Kelly sizing
- C) Assumption of constant win rates and payoff ratios
- D) Inability to handle strategies with win rates above 60%

### Answer Key
1. B
2. C
3. D
