# 📚 API Reference

Complete reference for the Sui DeFi Advisor API.

## SuiDeFiAdvisor Class

The main class that provides DeFi analysis functionality.

### Constructor

```python
SuiDeFiAdvisor()
```

Initializes the DeFi advisor with a Sui GraphQL client.

**Returns**: `SuiDeFiAdvisor` instance

**Raises**: 
- `Exception` if client initialization fails

**Example**:
```python
advisor = SuiDeFiAdvisor()
```

---

## Core Methods

### analyze_portfolio(address)

Analyzes a wallet's portfolio composition and risk profile.

**Parameters**:
- `address` (str): Sui wallet address to analyze (must start with '0x')

**Returns**: `Dict` containing:
```python
{
    "portfolio_summary": {
        "total_coin_types": int,      # Total number of coin balances
        "unique_coin_types": int,     # Number of unique coin types
        "objects_owned": int,         # Number of objects owned
        "risk_level": str            # "Low", "Medium", or "High"
    },
    "insights": List[str],           # Human-readable insights
    "coin_types": List[str],         # List of coin types (first 5)
    "recommendations": List[str]     # Personalized recommendations
}
```

**Example**:
```python
portfolio = advisor.analyze_portfolio("0x123...")
print(f"Risk Level: {portfolio['portfolio_summary']['risk_level']}")
for insight in portfolio['insights']:
    print(f"💡 {insight}")
```

---

### get_staking_opportunities()

Finds staking opportunities and provides gas cost analysis.

**Parameters**: None

**Returns**: `Dict` containing:
```python
{
    "top_validators": List[Dict],     # Validator information (future)
    "gas_cost_analysis": {
        "current_gas_price": int,     # Current gas price
        "recommendation": str         # Gas timing recommendation
    },
    "recommendations": List[str]      # Staking recommendations
}
```

**Example**:
```python
staking = advisor.get_staking_opportunities()
for rec in staking['recommendations']:
    print(f"🎯 {rec}")
```

---

### generate_report(address)

Generates a comprehensive DeFi analysis report.

**Parameters**:
- `address` (str): Sui wallet address to analyze

**Returns**: `str` - Formatted report text

**Example**:
```python
report = advisor.generate_report("0x123...")
print(report)
```

---

## Internal Methods

These methods are used internally but can be accessed if needed.

### _analyze_portfolio_data(balances_result, objects_result)

Processes raw blockchain data into portfolio insights.

**Parameters**:
- `balances_result`: Result from `GetAllCoinBalances` query
- `objects_result`: Result from `GetObjectsOwnedByAddress` query

**Returns**: `Dict` - Portfolio analysis data

---

### _analyze_staking_data(validators_result, gas_result)

Processes validator and gas data into staking recommendations.

**Parameters**:
- `validators_result`: Result from `GetValidatorsApy` query
- `gas_result`: Result from `GetReferenceGasPrice` query

**Returns**: `Dict` - Staking analysis data

---

### _generate_recommendations(coin_count, coin_types)

Generates personalized recommendations based on portfolio composition.

**Parameters**:
- `coin_count` (int): Number of coin balances
- `coin_types` (List[str]): List of coin types in portfolio

**Returns**: `List[str]` - List of recommendations

---

## Data Structures

### Portfolio Summary

```python
{
    "total_coin_types": int,      # Total coin balance entries
    "unique_coin_types": int,     # Unique coin types
    "objects_owned": int,         # NFTs and other objects
    "risk_level": str            # Risk assessment
}
```

### Risk Levels

| Level | Criteria | Description |
|-------|----------|-------------|
| `"High"` | 0-1 coin types | Empty or single-asset portfolio |
| `"Medium"` | 2-3 coin types | Limited diversification |
| `"Low"` | 4+ coin types | Well-diversified portfolio |

### Insight Types

| Category | Example |
|----------|---------|
| Portfolio Status | `"⚠️ Empty portfolio - consider acquiring some SUI tokens"` |
| Diversification | `"📊 Limited diversification - consider adding more asset types"` |
| Objects | `"🎨 You own 5 objects (NFTs/DeFi positions)"` |
| Staking | `"💰 Consider staking your SUI tokens for passive income"` |

### Recommendation Categories

| Stage | Recommendations |
|-------|----------------|
| **Beginner** (0 coins) | Start with SUI tokens, learn ecosystem |
| **Limited** (1-2 coins) | Diversify, start staking |
| **Diversified** (3+ coins) | Rebalance, yield farming, advanced strategies |

---

## Error Handling

### Common Errors

```python
# Client initialization failure
{
    "error": "Client not initialized"
}

# Network or query failure
{
    "error": "Analysis failed: [specific error message]"
}

# Invalid address format
{
    "error": "Portfolio analysis failed: [validation error]"
}
```

### Error Handling Example

```python
advisor = SuiDeFiAdvisor()
result = advisor.analyze_portfolio("0x123...")

if "error" in result:
    print(f"❌ Error: {result['error']}")
else:
    print(f"✅ Analysis complete: {result['portfolio_summary']}")
```

---

## Usage Patterns

### Basic Analysis

```python
# Simple portfolio check
advisor = SuiDeFiAdvisor()
portfolio = advisor.analyze_portfolio(address)
risk = portfolio['portfolio_summary']['risk_level']
```

### Batch Analysis

```python
# Analyze multiple addresses
addresses = ["0x123...", "0x456...", "0x789..."]
results = {}

for addr in addresses:
    results[addr] = advisor.analyze_portfolio(addr)
```

### Custom Analysis

```python
# Extend functionality
class MyAdvisor(SuiDeFiAdvisor):
    def custom_analysis(self, address):
        base_analysis = self.analyze_portfolio(address)
        # Add custom logic
        return enhanced_analysis
```

---

## PySui Integration

### GraphQL Queries Used

| Method | PySui Query | Purpose |
|--------|-------------|---------|
| `analyze_portfolio()` | `GetAllCoinBalances` | Get coin balances |
| `analyze_portfolio()` | `GetObjectsOwnedByAddress` | Get owned objects |
| `get_staking_opportunities()` | `GetValidatorsApy` | Get validator info |
| `get_staking_opportunities()` | `GetReferenceGasPrice` | Get gas prices |

### Client Configuration

```python
# How the client is configured internally
cfg = PysuiConfiguration(group_name=PysuiConfiguration.SUI_GQL_RPC_GROUP)
client = SyncGqlClient(pysui_config=cfg, write_schema=False)
```

---

## Extension Examples

### Custom Risk Assessment

```python
class AdvancedAdvisor(SuiDeFiAdvisor):
    def advanced_risk_analysis(self, address):
        portfolio = self.analyze_portfolio(address)
        
        # Custom risk factors
        risk_factors = {
            "concentration": self._analyze_concentration(portfolio),
            "volatility": self._analyze_volatility(portfolio),
            "liquidity": self._analyze_liquidity(portfolio)
        }
        
        return {
            "portfolio": portfolio,
            "advanced_risk": risk_factors,
            "composite_score": self._calculate_composite_risk(risk_factors)
        }
```

### Yield Tracking

```python
class YieldTracker(SuiDeFiAdvisor):
    def track_yield_opportunities(self, address):
        portfolio = self.analyze_portfolio(address)
        staking = self.get_staking_opportunities()
        
        # Calculate potential yields
        yield_potential = self._calculate_yield_potential(portfolio, staking)
        
        return {
            "current_portfolio": portfolio,
            "yield_opportunities": yield_potential,
            "optimization_suggestions": self._suggest_optimizations(yield_potential)
        }
```

### Multi-Timeframe Analysis

```python
class TimeframeAnalyzer(SuiDeFiAdvisor):
    def analyze_trends(self, address, timeframes=['1d', '7d', '30d']):
        results = {}
        
        for timeframe in timeframes:
            # Historical analysis would go here
            results[timeframe] = self._analyze_timeframe(address, timeframe)
        
        return {
            "address": address,
            "timeframe_analysis": results,
            "trend_summary": self._summarize_trends(results)
        }
```

---

## Best Practices

### Performance

```python
# Reuse advisor instance
advisor = SuiDeFiAdvisor()  # Initialize once

# Batch operations
addresses = ["0x123...", "0x456..."]
for addr in addresses:
    result = advisor.analyze_portfolio(addr)  # Reuse client
```

### Error Handling

```python
def safe_analysis(advisor, address):
    try:
        result = advisor.analyze_portfolio(address)
        if "error" in result:
            return {"status": "error", "message": result["error"]}
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "exception", "message": str(e)}
```

### Rate Limiting

```python
import time

def analyze_with_rate_limit(advisor, addresses, delay=1.0):
    results = {}
    for addr in addresses:
        results[addr] = advisor.analyze_portfolio(addr)
        time.sleep(delay)  # Avoid overwhelming the API
    return results
```

---

## Version Information

- **Current Version**: 1.0.0
- **PySui Compatibility**: >=0.65.0
- **Python Compatibility**: >=3.8

---

For more examples and advanced usage, see the main [README.md](README.md) and [SETUP.md](SETUP.md) files. 