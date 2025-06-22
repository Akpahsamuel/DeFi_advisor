# 🚀 Quick Setup Guide

Get your Sui DeFi Advisor running in under 5 minutes!

## Step 1: Prerequisites ✅

### Python Installation
Make sure you have Python 3.8 or higher:
```bash
python --version
# Should show Python 3.8.x or higher
```

If you don't have Python installed:
- **Windows**: Download from [python.org](https://python.org)
- **macOS**: `brew install python` or download from python.org
- **Linux**: `sudo apt install python3 python3-pip` (Ubuntu/Debian)

## Step 2: Install Dependencies 📦

### Option A: Simple Installation (Recommended)
```bash
pip install pysui
```

### Option B: Full Installation with Requirements File
```bash
# Clone or download the project files
# Then install from requirements.txt
pip install -r requirements.txt
```

### Option C: Virtual Environment (Best Practice)
```bash
# Create virtual environment
python -m venv defi-advisor-env

# Activate it
# On Windows:
defi-advisor-env\Scripts\activate
# On macOS/Linux:
source defi-advisor-env/bin/activate

# Install dependencies
pip install pysui
```

## Step 3: Test Installation 🧪

### Quick Test
```bash
python -c "import pysui; print('✅ PySui installed successfully')"
```

### Full Test with Demo
```bash
python defi_advisor.py
```

You should see output like:
```
✅ DeFi Advisor initialized successfully
🚀 Starting Sui DeFi Advisor Demo
==================================================
🔍 Analyzing portfolio for address: 0x00878369f475a454939af7b84cdd981515b1329f159a1aeb9bf0f8899e00083a
```

## Step 4: First Analysis 📊

### Analyze Any Sui Address
```python
from defi_advisor import SuiDeFiAdvisor

# Initialize
advisor = SuiDeFiAdvisor()

# Replace with any Sui address you want to analyze
address = "0x00878369f475a454939af7b84cdd981515b1329f159a1aeb9bf0f8899e00083a"

# Get full report
report = advisor.generate_report(address)
print(report)
```

### Get Specific Analysis
```python
# Just portfolio analysis
portfolio = advisor.analyze_portfolio(address)
print(f"Risk Level: {portfolio['portfolio_summary']['risk_level']}")

# Just staking opportunities
staking = advisor.get_staking_opportunities()
for tip in staking['recommendations']:
    print(f"💡 {tip}")
```

## 🎯 What Each Function Does

| Function | What It Does | Example Output |
|----------|-------------|----------------|
| `generate_report(address)` | Full DeFi analysis report | Complete portfolio + staking analysis |
| `analyze_portfolio(address)` | Portfolio composition & risk | `{"risk_level": "Medium", "insights": [...]}` |
| `get_staking_opportunities()` | Staking recommendations | `{"recommendations": ["Stake SUI tokens"]}` |

## 🔧 Troubleshooting

### Common Issues & Solutions

**❌ "ModuleNotFoundError: No module named 'pysui'"**
```bash
# Solution: Install pysui
pip install pysui
```

**❌ "Client not initialized" error**
```bash
# Solution: Check internet connection
# The advisor needs to connect to Sui blockchain
ping google.com
```

**❌ "Permission denied" on installation**
```bash
# Solution: Use --user flag or virtual environment
pip install --user pysui
# OR create virtual environment (recommended)
```

**❌ Analysis returns empty results**
```bash
# Solution: Check if the address has any assets
# Some addresses might be empty or invalid
```

### Network Issues

If you get connection errors:
1. **Check internet connection**
2. **Try again in a few minutes** (Sui GraphQL might be busy)
3. **Use a different network** if on restricted WiFi

## 🚀 Next Steps

### 1. Analyze Your Own Portfolio
Replace the example address with your own Sui wallet address:
```python
my_address = "0xYOUR_SUI_ADDRESS_HERE"
advisor = SuiDeFiAdvisor()
my_report = advisor.generate_report(my_address)
print(my_report)
```

### 2. Monitor Multiple Addresses
```python
addresses = [
    "0xaddress1...",
    "0xaddress2...",
    "0xaddress3..."
]

for addr in addresses:
    print(f"\n=== Analysis for {addr} ===")
    report = advisor.generate_report(addr)
    print(report)
```

### 3. Build Custom Features
```python
class MyCustomAdvisor(SuiDeFiAdvisor):
    def my_custom_analysis(self, address):
        portfolio = self.analyze_portfolio(address)
        # Add your custom logic here
        return {"custom_insight": "Your custom analysis"}

# Use your custom advisor
my_advisor = MyCustomAdvisor()
custom_result = my_advisor.my_custom_analysis("0x123...")
```

## 🎉 You're Ready!

Your Sui DeFi Advisor is now set up and ready to analyze portfolios!

### Quick Commands Reference
```bash
# Run demo
python defi_advisor.py

# Test installation
python -c "from defi_advisor import SuiDeFiAdvisor; print('✅ Ready!')"

# Analyze specific address
python -c "
from defi_advisor import SuiDeFiAdvisor
advisor = SuiDeFiAdvisor()
print(advisor.generate_report('0x00878369f475a454939af7b84cdd981515b1329f159a1aeb9bf0f8899e00083a'))
"
```

Need help? Check the main [README.md](README.md) for detailed documentation!

---

**🎯 Pro Tip**: Bookmark addresses you analyze frequently and create a script to generate daily reports for your favorite wallets! 