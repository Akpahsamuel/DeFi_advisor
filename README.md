# Sui DeFi Advisor 🏦

An AI-powered DeFi advisor for the Sui blockchain that analyzes portfolios and provides investment insights **without requiring custom smart contracts**.

## 🌟 Features

### Portfolio Analysis
- **Real-time portfolio scanning** - Analyze any Sui wallet address
- **Asset diversification scoring** - Evaluate portfolio risk and balance
- **Risk assessment** - Categorize portfolio risk levels (Low/Medium/High)
- **Object tracking** - Monitor NFTs and DeFi positions

### Staking Opportunities
- **Validator analysis** - Find best staking opportunities
- **APY tracking** - Monitor validator performance and returns
- **Gas optimization** - Analyze transaction costs and timing

### AI-Powered Insights
- **Personalized recommendations** - Tailored advice based on portfolio composition
- **Market analysis** - Real-time blockchain data interpretation
- **Yield optimization** - Suggestions for maximizing returns

## 🚀 Quick Start

### Prerequisites

1. **Install Python 3.8+**
2. **Install PySui**:
   ```bash
   pip install pysui
   ```

### Basic Usage

```python
from defi_advisor import SuiDeFiAdvisor

# Initialize the advisor
advisor = SuiDeFiAdvisor()

# Analyze any Sui address
address = "0x00878369f475a454939af7b84cdd981515b1329f159a1aeb9bf0f8899e00083a"
report = advisor.generate_report(address)
print(report)
```

### Run the Demo

```bash
python defi_advisor.py
```

## 📊 What You Get

### Portfolio Analysis Report
```
🏦 SUI DEFI ADVISOR REPORT
==================================================

📍 Address: 0x00878369f475a454939af7b84cdd981515b1329f159a1aeb9bf0f8899e00083a

📊 PORTFOLIO ANALYSIS:
------------------------------
• Total Coin Types: 3
• Unique Assets: 2
• Objects Owned: 5
• Risk Level: Medium

💡 KEY INSIGHTS:
  📊 Limited diversification - consider adding more asset types
  🎨 You own 5 objects (NFTs/DeFi positions)
  💰 Consider staking your SUI tokens for passive income

🎯 RECOMMENDATIONS:
  🌈 Diversify into stablecoins for stability
  💰 Start staking SUI tokens for passive income
  🔍 Explore Sui DeFi protocols for yield opportunities
```

### Individual Analysis Functions

```python
# Portfolio analysis
portfolio = advisor.analyze_portfolio(address)
print(f"Risk Level: {portfolio['portfolio_summary']['risk_level']}")

# Staking opportunities
staking = advisor.get_staking_opportunities()
for recommendation in staking['recommendations']:
    print(recommendation)
```

## 🔧 Technical Architecture

### No Smart Contracts Required! ✅

This advisor works by:

1. **Reading existing blockchain data** using PySui GraphQL queries
2. **Analyzing portfolio composition** with built-in algorithms
3. **Providing insights** based on DeFi best practices
4. **Suggesting optimizations** using existing Sui protocols

### Key Components

```python
class SuiDeFiAdvisor:
    def __init__(self):
        # Initialize PySui GraphQL client
        cfg = PysuiConfiguration(group_name=PysuiConfiguration.SUI_GQL_RPC_GROUP)
        self.client = SyncGqlClient(pysui_config=cfg, write_schema=False)
    
    def analyze_portfolio(self, address: str):
        # Get coin balances
        balances = self.client.execute_query_node(
            with_node=qn.GetAllCoinBalances(owner=address)
        )
        
        # Get owned objects
        objects = self.client.execute_query_node(
            with_node=qn.GetObjectsOwnedByAddress(owner=address)
        )
        
        # Analyze and return insights
        return self._analyze_portfolio_data(balances, objects)
```

## 🎯 Use Cases

### 1. Personal Portfolio Management
```python
# Check your own portfolio
my_address = "0x123..."
advisor = SuiDeFiAdvisor()
insights = advisor.analyze_portfolio(my_address)
```

### 2. Multi-Address Monitoring
```python
# Monitor multiple wallets
addresses = ["0x123...", "0x456...", "0x789..."]
for addr in addresses:
    report = advisor.generate_report(addr)
    print(f"Report for {addr}:\n{report}\n")
```

### 3. Staking Strategy
```python
# Find best staking opportunities
staking_ops = advisor.get_staking_opportunities()
print("Best staking strategies:")
for rec in staking_ops['recommendations']:
    print(f"  • {rec}")
```

## 📈 Advanced Features

### Risk Assessment Algorithm

The advisor categorizes portfolios based on:

- **Asset Count**: More assets = lower risk
- **Diversification**: Different coin types reduce concentration risk
- **Object Holdings**: NFTs and DeFi positions add complexity

```python
def _calculate_risk_level(self, coin_count: int, unique_assets: int) -> str:
    if coin_count == 0:
        return "High"  # Empty portfolio
    elif coin_count <= 1:
        return "High"  # Single asset
    elif coin_count <= 3:
        return "Medium"  # Limited diversification
    else:
        return "Low"  # Well diversified
```

### Recommendation Engine

Personalized advice based on portfolio composition:

```python
def _generate_recommendations(self, coin_count: int, coin_types: List[str]) -> List[str]:
    if coin_count == 0:
        return ["🚀 Start by acquiring some SUI tokens"]
    elif coin_count <= 2:
        return ["🌈 Diversify into stablecoins", "💰 Start staking SUI tokens"]
    else:
        return ["⚖️ Review portfolio balance", "📈 Consider yield farming"]
```

## 🛠️ Development Setup

### Full Development Environment

1. **Clone and setup**:
   ```bash
   git clone <your-repo>
   cd sui-defi-advisor
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install pysui
   ```

3. **Optional: Install Sui binaries** (for advanced features):
   ```bash
   # Install Rust first
   curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
   
   # Install Sui binaries (optional)
   # Follow: https://docs.sui.io/guides/developer/getting-started/sui-install
   ```

### Testing

```bash
# Test with example address
python defi_advisor.py

# Test individual functions
python -c "
from defi_advisor import SuiDeFiAdvisor
advisor = SuiDeFiAdvisor()
print('✅ Advisor initialized successfully')
"
```

## 🔍 Available Query Types

The advisor uses these PySui GraphQL queries:

| Query | Purpose | Smart Contract Required |
|-------|---------|------------------------|
| `GetAllCoinBalances` | Get all coin balances | ❌ No |
| `GetObjectsOwnedByAddress` | Get NFTs and objects | ❌ No |
| `GetValidatorsApy` | Get staking opportunities | ❌ No |
| `GetReferenceGasPrice` | Get current gas costs | ❌ No |
| `GetDelegatedStakes` | Get staking positions | ❌ No |

## 🚧 Roadmap

### Phase 1: Analysis (Current) ✅
- [x] Portfolio composition analysis
- [x] Risk assessment
- [x] Basic recommendations
- [x] Staking opportunities

### Phase 2: Enhanced Analysis (Next)
- [ ] Historical performance tracking
- [ ] Yield farming opportunity detection
- [ ] Gas optimization suggestions
- [ ] Multi-timeframe analysis

### Phase 3: AI Integration
- [ ] OpenAI integration for advanced insights
- [ ] Market sentiment analysis
- [ ] Predictive recommendations
- [ ] Natural language reports

### Phase 4: Automation
- [ ] Automated rebalancing suggestions
- [ ] Alert system for opportunities
- [ ] Portfolio optimization
- [ ] Risk monitoring

## 🤝 Contributing

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Test thoroughly**
5. **Submit a pull request**

### Areas for Contribution

- **New analysis algorithms**
- **Additional DeFi protocols integration**
- **UI/Web interface**
- **Performance optimizations**
- **Documentation improvements**

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

### Common Issues

**Q: "Client not initialized" error**
```
A: Make sure you have internet connection. The advisor needs to connect to Sui GraphQL endpoint.
```

**Q: Address analysis returns empty results**
```
A: Verify the address format is correct (starts with 0x). Some addresses might have no assets.
```

**Q: Staking analysis fails**
```
A: This might be due to network issues or Sui GraphQL endpoint being unavailable.
```

### Getting Help

- **GitHub Issues**: Report bugs and request features
- **Documentation**: Check this README for examples
- **PySui Docs**: https://pysui.readthedocs.io/

## 🎉 Examples

### Complete Analysis Example

```python
#!/usr/bin/env python3
from defi_advisor import SuiDeFiAdvisor
import json

def main():
    # Initialize advisor
    advisor = SuiDeFiAdvisor()
    
    # Test addresses (replace with real addresses)
    addresses = [
        "0x00878369f475a454939af7b84cdd981515b1329f159a1aeb9bf0f8899e00083a",
        # Add more addresses here
    ]
    
    for address in addresses:
        print(f"\n{'='*60}")
        print(f"Analyzing: {address}")
        print('='*60)
        
        # Full report
        report = advisor.generate_report(address)
        print(report)
        
        # Detailed JSON data
        portfolio = advisor.analyze_portfolio(address)
        print("\nDetailed Data:")
        print(json.dumps(portfolio, indent=2, default=str))

if __name__ == "__main__":
    main()
```

### Custom Analysis Example

```python
from defi_advisor import SuiDeFiAdvisor

class CustomDeFiAnalyzer(SuiDeFiAdvisor):
    def analyze_yield_opportunities(self, address: str):
        """Custom yield analysis"""
        portfolio = self.analyze_portfolio(address)
        staking = self.get_staking_opportunities()
        
        # Custom logic here
        yield_score = self._calculate_yield_score(portfolio, staking)
        
        return {
            "yield_score": yield_score,
            "recommendations": self._custom_yield_recommendations(portfolio)
        }
    
    def _calculate_yield_score(self, portfolio, staking):
        # Your custom yield scoring algorithm
        return 0.75  # Example score
    
    def _custom_yield_recommendations(self, portfolio):
        # Your custom recommendation logic
        return ["Custom recommendation 1", "Custom recommendation 2"]

# Usage
analyzer = CustomDeFiAnalyzer()
yield_analysis = analyzer.analyze_yield_opportunities("0x123...")
print(f"Yield Score: {yield_analysis['yield_score']}")
```

---

**Built with ❤️ for the Sui ecosystem**

*This advisor helps you make informed DeFi decisions without the complexity of writing smart contracts. Just analyze, learn, and optimize your Sui portfolio!* 