# 3.19 Point and Figure Charting

## Introduction
Point and Figure (P&F) charting is one of the oldest forms of technical analysis, dating back to the late 1800s. Unlike time-based charts that plot price against time, P&F charts focus exclusively on price movements, filtering out minor fluctuations and the time element. This unique approach provides a clear visualization of supply and demand dynamics, making it easier to identify significant support and resistance levels, breakouts, and trend reversals. This subsection explores the principles of Point and Figure charting, its construction, interpretation, and practical applications in modern trading.

## Fundamentals of Point and Figure Charting

### Basic Principles
Point and Figure charting is built on several key principles that differentiate it from other charting methods:

1. **Price-Focused**: Only significant price movements are recorded, ignoring time
2. **Noise Reduction**: Minor price fluctuations are filtered out
3. **Trend Clarity**: Clear visualization of support, resistance, and trend direction
4. **Supply and Demand**: Direct representation of buying and selling pressure
5. **Pattern Recognition**: Distinctive patterns with high-probability outcomes

### Construction Elements
P&F charts consist of several basic elements:

**X-Columns and O-Columns:**
- **X-Columns**: Represent rising prices (demand exceeding supply)
- **O-Columns**: Represent falling prices (supply exceeding demand)
- Columns never contain both Xs and Os

**Box Size:**
- The minimum price movement required to add an X or O to the chart
- Typically set as a fixed value (e.g., $1) or percentage (e.g., 1%)
- Larger box sizes filter out more noise but may miss important movements
- Smaller box sizes provide more detail but may include more noise

**Reversal Amount:**
- The number of boxes price must move in the opposite direction to warrant a column change
- Typically 3 boxes (3-box reversal) is standard
- Larger reversal amounts create fewer columns and highlight major trends
- Smaller reversal amounts create more columns and show minor trends

**Scale:**
- Traditional P&F charts use an arithmetic scale
- Modern software often offers logarithmic scaling options
- Scale choice affects pattern formation and interpretation

## Constructing Point and Figure Charts

### Traditional Method
The traditional method of constructing P&F charts involves these steps:

1. **Determine Parameters:**
   - Select box size (e.g., $1, 0.5%, etc.)
   - Select reversal amount (typically 3 boxes)

2. **Plot Initial Column:**
   - If price is rising, plot Xs in a column
   - If price is falling, plot Os in a column
   - Continue adding Xs or Os in the same column as price continues in the same direction

3. **Handle Reversals:**
   - When price reverses by the reversal amount or more, start a new column
   - Move one column to the right and plot Os (if previous column was Xs) or Xs (if previous column was Os)
   - Begin the new column at a level that overlaps with the previous column by the amount of the reversal minus one

4. **Continue the Process:**
   - Add Xs or Os to the current column as price continues in the same direction
   - Create new columns when reversals occur
   - Ignore price movements smaller than the box size

### Modern Approaches
Modern P&F charting incorporates several enhancements:

**Dynamic Box Sizing:**
- ATR-based box sizes that adapt to market volatility
- Percentage-based box sizes that scale with price level
- Hybrid approaches combining fixed and percentage methods

**Time Stamps:**
- Adding dates to column changes to maintain some time reference
- Marking specific time periods (month/quarter ends) on the chart
- Creating hybrid charts that incorporate time elements

**Multiple Timeframe Analysis:**
- Using different box sizes and reversal amounts simultaneously
- Comparing patterns across different parameter settings
- Integrating signals from various P&F timeframes

## Reading Point and Figure Charts

### Trend Identification
P&F charts provide clear trend signals:

**Bullish Trend Signals:**
- Series of rising tops and bottoms (higher highs and higher lows)
- Columns of Xs exceeding previous X-column highs
- More and longer X-columns than O-columns
- Bullish patterns forming (triple top breakout, etc.)

**Bearish Trend Signals:**
- Series of declining tops and bottoms (lower highs and lower lows)
- Columns of Os exceeding previous O-column lows
- More and longer O-columns than X-columns
- Bearish patterns forming (triple bottom breakdown, etc.)

**Trend Lines:**
- **Bullish Support Line**: 45-degree line drawn from significant bottoms, rising one box for each column to the right
- **Bearish Resistance Line**: 45-degree line drawn from significant tops, falling one box for each column to the right
- Trend line breaks often signal potential trend changes

### Support and Resistance
P&F charts excel at identifying key support and resistance levels:

**Support Levels:**
- Previous column lows, especially those with multiple O-columns reaching the same level
- Bullish support trend lines
- Areas with multiple X-column bottoms at similar levels
- Congestion areas with multiple columns trading in a narrow range

**Resistance Levels:**
- Previous column highs, especially those with multiple X-columns reaching the same level
- Bearish resistance trend lines
- Areas with multiple O-column tops at similar levels
- Congestion areas with multiple columns trading in a narrow range

**Congestion Areas:**
- Horizontal trading ranges with multiple columns
- Often form rectangles on the chart
- Breakouts from congestion areas typically lead to significant moves
- Width of congestion can help project the extent of the subsequent move

## Point and Figure Patterns

### Bullish Patterns

**Double Top Breakout:**
- Formation: X-column rises to match the high of the previous X-column
- Signal: Bullish continuation or reversal
- Reliability: Moderate
- Target: Box size × number of columns in the pattern

**Triple Top Breakout:**
- Formation: X-column rises to match the high of two previous X-columns
- Signal: Strong bullish continuation or reversal
- Reliability: High
- Target: Box size × number of columns in the pattern

**Bullish Catapult:**
- Formation: Triple top breakout followed by a pullback and another breakout
- Signal: Very strong bullish continuation
- Reliability: Very high
- Target: Box size × number of columns in the pattern × 1.5

**Ascending Triple Top Breakout:**
- Formation: Triple top breakout where each column low is higher than the previous
- Signal: Strong bullish trend confirmation
- Reliability: Very high
- Target: Box size × number of columns in the pattern × 1.5

**Bullish Signal Reversed:**
- Formation: Bearish pattern that fails to follow through, with price reversing upward
- Signal: Potential trend change from bearish to bullish
- Reliability: Moderate to high
- Target: Varies based on the specific pattern

### Bearish Patterns

**Double Bottom Breakdown:**
- Formation: O-column falls to match the low of the previous O-column
- Signal: Bearish continuation or reversal
- Reliability: Moderate
- Target: Box size × number of columns in the pattern

**Triple Bottom Breakdown:**
- Formation: O-column falls to match the low of two previous O-columns
- Signal: Strong bearish continuation or reversal
- Reliability: High
- Target: Box size × number of columns in the pattern

**Bearish Catapult:**
- Formation: Triple bottom breakdown followed by a rally and another breakdown
- Signal: Very strong bearish continuation
- Reliability: Very high
- Target: Box size × number of columns in the pattern × 1.5

**Descending Triple Bottom Breakdown:**
- Formation: Triple bottom breakdown where each column high is lower than the previous
- Signal: Strong bearish trend confirmation
- Reliability: Very high
- Target: Box size × number of columns in the pattern × 1.5

**Bearish Signal Reversed:**
- Formation: Bullish pattern that fails to follow through, with price reversing downward
- Signal: Potential trend change from bullish to bearish
- Reliability: Moderate to high
- Target: Varies based on the specific pattern

### Continuation Patterns

**Bullish Triangle:**
- Formation: Series of columns with rising bottoms and flat tops
- Signal: Bullish continuation after consolidation
- Reliability: High
- Target: Height of the widest part of the triangle projected from the breakout point

**Bearish Triangle:**
- Formation: Series of columns with falling tops and flat bottoms
- Signal: Bearish continuation after consolidation
- Reliability: High
- Target: Height of the widest part of the triangle projected from the breakout point

**Bullish Flag:**
- Formation: Short consolidation after a strong upward move
- Signal: Bullish continuation
- Reliability: High
- Target: Length of the prior move added to the breakout point

**Bearish Flag:**
- Formation: Short consolidation after a strong downward move
- Signal: Bearish continuation
- Reliability: High
- Target: Length of the prior move subtracted from the breakout point

## Price Objectives and Targets

### Horizontal Count Method
The horizontal count is the most common method for calculating price targets in P&F charting:

**Calculation Steps:**
1. Identify a congestion area (horizontal formation)
2. Count the number of columns in the formation
3. Multiply the count by the box size
4. For bullish targets: Add the result to the breakout level
5. For bearish targets: Subtract the result from the breakdown level

**Example:**
- Congestion area with 10 columns
- Box size of $1
- Breakout level at $50
- Bullish target: $50 + (10 × $1) = $60

**Reliability Factors:**
- Wider formations generally produce more reliable targets
- Formations with more columns typically generate stronger moves
- Multiple counts from different formations can provide confirmation
- Targets should be adjusted based on nearby support/resistance levels

### Vertical Count Method
The vertical count provides an alternative method for calculating price targets:

**Calculation Steps:**
1. Identify the number of Xs or Os in the column that breaks out from a significant level
2. Multiply the count by the box size and the reversal amount
3. For bullish targets: Add the result to the lowest point in the breakout column
4. For bearish targets: Subtract the result from the highest point in the breakdown column

**Example:**
- Breakout column with 8 Xs
- Box size of $1
- Reversal amount of 3 boxes
- Lowest point in column at $45
- Bullish target: $45 + (8 × $1 × 3) = $69

**Reliability Factors:**
- More reliable in strongly trending markets
- Often produces more aggressive targets than horizontal counts
- Can be used in conjunction with horizontal counts for confirmation
- May need adjustment in volatile markets

## Trading Strategies Using Point and Figure

### Breakout Strategy
This strategy focuses on trading breakouts from significant P&F patterns:

**Entry Criteria:**
- Breakout above a triple top or breakdown below a triple bottom
- Confirmation from increasing volume (if available)
- Alignment with the longer-term trend
- No nearby resistance (for bullish trades) or support (for bearish trades)

**Stop-Loss Placement:**
- Below the lowest point of the pattern for bullish trades
- Above the highest point of the pattern for bearish trades
- Alternatively, use a reversal amount (e.g., 3-box reversal) from entry

**Target Setting:**
- Primary target: Horizontal count objective
- Secondary target: Vertical count objective
- Consider partial profit-taking at the first target

**Risk Management:**
- Risk no more than 1-2% of capital per trade
- Consider scaling into positions on pullbacks that hold support
- Trail stops as the trend develops

### Trend Line Strategy
This strategy trades breaks of significant P&F trend lines:

**Entry Criteria:**
- Break above a bearish resistance line or below a bullish support line
- Confirmation from a subsequent column (avoid false breaks)
- Pattern formation near the trend line break
- Alignment with larger timeframe signals

**Stop-Loss Placement:**
- Below the lowest recent column for bullish trades
- Above the highest recent column for bearish trades
- Alternatively, use a multiple of the box size (e.g., 3-5 boxes)

**Target Setting:**
- Initial target: Distance to the next significant support/resistance
- Secondary target: Horizontal count objective
- Final target: Major support/resistance levels

**Risk Management:**
- Use smaller position sizes for counter-trend trades
- Increase position size for trend-continuation signals
- Move stops to breakeven after the trade moves in your favor by the reversal amount

### Bullish Catapult Strategy
This strategy specifically targets the high-probability bullish catapult pattern:

**Entry Criteria:**
- Triple top breakout occurs
- Price pulls back but holds above a key support level
- Second breakout above the previous high
- Increasing volume on the second breakout (if available)

**Stop-Loss Placement:**
- Below the low of the pullback column
- Alternatively, below the bullish support line

**Target Setting:**
- Conservative target: 1.5 times the horizontal count
- Aggressive target: 2 times the horizontal count
- Consider trailing stops rather than fixed targets in strong trends

**Risk Management:**
- Higher position sizing justified by the pattern's high reliability
- Consider scaling in with partial positions at each stage of the pattern
- Trail stops more aggressively due to the pattern's strong momentum expectation

## Combining Point and Figure with Other Technical Tools

### P&F and Moving Averages
While traditional P&F charts don't include moving averages, modern approaches incorporate them:

**Applications:**
1. **Overlay MAs on P&F Charts**: Some software allows MA overlays on P&F charts
2. **MA Signals on Traditional Charts**: Use MA signals from time-based charts to confirm P&F patterns
3. **MA-Based Box Sizing**: Use moving averages to determine dynamic box sizes
4. **Trend Confirmation**: Use MA direction on time-based charts to confirm P&F trend signals

**Effective Combinations:**
- P&F breakouts confirmed by price crossing above/below key moving averages
- Moving average crossovers coinciding with P&F pattern completions
- P&F support/resistance levels aligning with moving average levels

### P&F and Relative Strength
Relative strength analysis is particularly effective with P&F charts:

**Approaches:**
1. **Relative Strength Charts**: Create P&F charts of one asset divided by another (e.g., stock vs. index)
2. **Bullish/Bearish Percent Charts**: Track percentage of stocks in an index showing P&F buy signals
3. **Sector Rotation Analysis**: Compare P&F patterns across different market sectors
4. **RS Ranking**: Rank stocks based on the strength of their P&F patterns

**Trading Applications:**
- Focus on stocks with bullish P&F patterns and positive relative strength
- Avoid stocks with bearish P&F patterns and negative relative strength
- Identify sector rotation through changes in relative strength P&F charts
- Use market breadth indicators based on P&F buy/sell signals

### P&F and Volume Analysis
While traditional P&F charts don't include volume, it can be incorporated:

**Integration Methods:**
1. **Volume Filters**: Only count price movements with above-average volume
2. **Confirmation**: Use volume from time-based charts to confirm P&F signals
3. **Volume-Based Box Sizing**: Adjust box size based on volume characteristics
4. **Volume Point and Figure**: Specialized P&F charts that incorporate volume

**Trading Applications:**
- Give more weight to P&F breakouts accompanied by high volume
- Be cautious of P&F signals occurring on unusually low volume
- Use volume trends from time-based charts to confirm P&F trend signals
- Consider volume patterns during congestion areas in P&F charts

## Advantages and Limitations of Point and Figure Charting

### Advantages
P&F charting offers several benefits over other charting methods:

1. **Noise Reduction**: Filters out minor price fluctuations
2. **Trend Clarity**: Provides clear visualization of support, resistance, and trend direction
3. **Pattern Recognition**: Distinctive patterns with high-probability outcomes
4. **Price Focus**: Concentrates on significant price movements rather than time
5. **Support/Resistance Identification**: Excellent for identifying key levels
6. **Target Projection**: Built-in methods for calculating price objectives
7. **Long-Term Perspective**: Effective for long-term trend analysis
8. **Versatility**: Applicable across all markets and timeframes

### Limitations
P&F charting also has several limitations:

1. **Time Element**: Removes time from the analysis, which can be important
2. **Parameter Sensitivity**: Results vary based on box size and reversal amount choices
3. **Learning Curve**: More difficult to learn than time-based charts
4. **Limited Adoption**: Less commonly used, resulting in fewer resources and tools
5. **Volume Exclusion**: Traditional P&F charts don't incorporate volume
6. **Subjectivity**: Pattern identification can be subjective
7. **Historical Data**: Requires more historical data for proper context
8. **Software Limitations**: Fewer software options compared to time-based charts

## Key Takeaways
- Point and Figure charting focuses exclusively on significant price movements, filtering out minor fluctuations and the time element
- P&F charts consist of columns of Xs (rising prices) and Os (falling prices), with the box size and reversal amount as key parameters
- These charts excel at identifying trends, support/resistance levels, and price targets
- Common P&F patterns include double/triple tops and bottoms, catapults, and triangles
- Price objectives can be calculated using horizontal count and vertical count methods
- P&F charts can be combined with other technical tools like moving averages, relative strength, and volume analysis
- Advantages include noise reduction, trend clarity, and pattern recognition
- Limitations include the removal of the time element and parameter sensitivity

## Quiz: Point and Figure Charting

### Question 1: What is the primary difference between Point and Figure charts and traditional time-based charts?
- A) Point and Figure charts use different symbols
- B) Point and Figure charts focus exclusively on price movements and filter out the time element
- C) Point and Figure charts cannot be used for short-term trading
- D) Point and Figure charts only work in trending markets

### Question 2: In Point and Figure charting, what does the "box size" represent?
- A) The physical size of each box on the chart
- B) The minimum price movement required to add an X or O to the chart
- C) The number of days between price changes
- D) The maximum number of Xs or Os in a single column

### Question 3: What is a "triple top breakout" in Point and Figure charting?
- A) When price rises above three previous highs on a time-based chart
- B) When an X-column rises to match the high of two previous X-columns
- C) When price makes three consecutive new highs
- D) When three X-columns reach the same price level

### Question 4: How is the horizontal count method used in Point and Figure charting?
- A) To count the number of days in a trend
- B) To measure the width of the chart
- C) To calculate price targets based on the number of columns in a congestion area
- D) To determine the box size

### Question 5: Which of the following is NOT an advantage of Point and Figure charting?
- A) Noise reduction
- B) Clear visualization of support and resistance
- C) Incorporation of volume analysis
- D) Distinctive patterns with high-probability outcomes

## Answer Key
1. B
2. B
3. B
4. C
5. C
