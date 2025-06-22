#!/usr/bin/env python3
"""
Main entry point for the Sui DeFi Advisor
"""

from defi_advisor import SuiDeFiAdvisor
import sys

def main():
    """Main function to run the DeFi advisor"""
    print("🚀 Welcome to Sui DeFi Advisor!")
    print("="*50)
    
    # Initialize the advisor
    advisor = SuiDeFiAdvisor()
    
    if not advisor.client:
        print("❌ Failed to initialize advisor. Please check your connection.")
        return
    
    # Get address from command line or prompt user
    if len(sys.argv) > 1:
        address = sys.argv[1]
        print(f"📍 Using provided address: {address}")
    else:
        # Always prompt user for address
        print("📍 Please enter a Sui wallet address to analyze:")
        print("   (Example: 0x42c7235d44467c971772636f4426970ad1475de79ee3cd6ebd63c65eca5ebd48)")
        
        try:
            address = input("🔗 Wallet Address: ").strip()
            
            # Validate address format
            if not address:
                print("❌ No address provided. Exiting.")
                return
            
            if not address.startswith('0x'):
                print("❌ Invalid address format. Address should start with '0x'")
                return
            
            if len(address) != 66:  # 0x + 64 hex characters
                print("❌ Invalid address length. Sui addresses should be 66 characters long (0x + 64 hex)")
                return
                
            print(f"✅ Using address: {address}")
            
        except KeyboardInterrupt:
            print("\n\n👋 Thanks for using Sui DeFi Advisor!")
            return
        except Exception as e:
            print(f"❌ Error getting address: {e}")
            return
    
    print("\n🔍 Analyzing wallet...")
    
    # Generate comprehensive report
    report = advisor.generate_report(address)
    print(report)
    
    # Offer detailed analysis
    print("\n" + "="*50)
    print("📊 Would you like detailed analysis? (y/n): ", end="")
    
    try:
        choice = input().lower().strip()
        if choice in ['y', 'yes']:
            print("\n📊 Detailed Portfolio Analysis:")
            portfolio_analysis = advisor.analyze_portfolio(address)
            
            if "error" not in portfolio_analysis:
                summary = portfolio_analysis.get("portfolio_summary", {})
                print(f"• Risk Level: {summary.get('risk_level', 'Unknown')}")
                print(f"• Total Assets: {summary.get('total_coin_types', 0)} coin types")
                print(f"• Objects Owned: {summary.get('objects_owned', 0)}")
                
                special_objects = summary.get('special_objects', [])
                if special_objects:
                    print(f"• Special Objects: {', '.join(special_objects)}")
                
                print(f"\n💡 Key Insights:")
                for insight in portfolio_analysis.get("insights", []):
                    print(f"  {insight}")
                
                print(f"\n🎯 Recommendations:")
                for rec in portfolio_analysis.get("recommendations", []):
                    print(f"  {rec}")
            else:
                print(f"❌ {portfolio_analysis['error']}")
            
            print("\n💰 Staking Analysis:")
            staking_analysis = advisor.get_staking_opportunities()
            
            if "error" not in staking_analysis:
                gas_info = staking_analysis.get("gas_cost_analysis", {})
                if gas_info:
                    print(f"⛽ Current Gas: {gas_info.get('current_gas_price', 'Unknown')}")
                    print(f"  {gas_info.get('recommendation', '')}")
                
                print(f"\n💡 Staking Recommendations:")
                for rec in staking_analysis.get("recommendations", []):
                    print(f"  {rec}")
            else:
                print(f"❌ {staking_analysis['error']}")
    
    except KeyboardInterrupt:
        print("\n\n👋 Thanks for using Sui DeFi Advisor!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    print("\n" + "="*50)
    print("🤖 Analysis complete! Thank you for using Sui DeFi Advisor.")

if __name__ == "__main__":
    main() 