#!/usr/bin/env python3
"""
Main entry point for the Sui DeFi Advisor
"""

from defi_advisor import SuiDeFiAdvisor
from defi_platforms import SuiDeFiPlatforms
import sys

def main():
    """Main function to run the DeFi advisor"""
    print("🚀 Welcome to Sui DeFi Advisor!")
    print("="*50)
    
    # Initialize both the advisor and platforms detector
    advisor = SuiDeFiAdvisor()
    platforms_detector = SuiDeFiPlatforms()
    
    if not advisor.client or not platforms_detector.client:
        print("❌ Failed to initialize. Please check your connection.")
        return
    
    # Get address from command line or prompt user
    if len(sys.argv) > 1:
        address = sys.argv[1]
        print(f"📍 Using provided address: {address}")
    else:
        # Always prompt user for address
        print("📍 Please enter a Sui wallet address to analyze:")
        print("   (Example: 0x1a2b3c4d5e6f7890abcdef1234567890abcdef1234567890abcdef1234567890)")
        
        try:
            address = input("🔗 Wallet Address: ").strip()
            
            if not address:
                print("❌ No address provided. Exiting.")
                return
            
            # Basic validation
            if not address.startswith('0x') or len(address) != 66:
                print("⚠️  Warning: Address format may be incorrect")
                print("   Expected: 0x followed by 64 hex characters")
                
                confirm = input("Continue anyway? (y/N): ").strip().lower()
                if confirm != 'y':
                    print("👋 Goodbye!")
                    return
        
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            return
        except Exception as e:
            print(f"❌ Error getting address: {e}")
            return
    
    print(f"\n🎯 Analyzing wallet: {address}")
    print("="*50)
    
    try:
        # Ask user what type of analysis they want
        print("\n📊 Choose analysis type:")
        print("1. 📈 Portfolio Analysis (Default)")
        print("2. 🏗️  DeFi Platforms Detection") 
        print("3. 🔍 Complete Analysis (Both)")
        
        try:
            choice = input("\nEnter choice (1-3) or press Enter for default: ").strip()
            if not choice:
                choice = "1"
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            return
        
        if choice == "1":
            # Portfolio analysis only
            print("\n" + "="*50)
            report = advisor.generate_report(address)
            print(report)
            
        elif choice == "2":
            # DeFi platforms detection only
            print("\n" + "="*50)
            platforms_report = platforms_detector.generate_platforms_report(address)
            print(platforms_report)
            
        elif choice == "3":
            # Complete analysis
            print("\n" + "="*50)
            print("📈 PORTFOLIO ANALYSIS:")
            print("="*50)
            report = advisor.generate_report(address)
            print(report)
            
            print("\n" + "="*50)
            print("🏗️ DEFI PLATFORMS ANALYSIS:")
            print("="*50)
            platforms_report = platforms_detector.generate_platforms_report(address)
            print(platforms_report)
            
        else:
            print("❌ Invalid choice. Running default portfolio analysis.")
            report = advisor.generate_report(address)
            print(report)
        
        # Ask if user wants detailed analysis
        try:
            detailed = input("\n🔬 Want detailed JSON analysis? (y/N): ").strip().lower()
            if detailed == 'y':
                print("\n" + "="*50)
                print("📊 DETAILED PORTFOLIO DATA:")
                print("="*50)
                portfolio_analysis = advisor.analyze_portfolio(address)
                import json
                print(json.dumps(portfolio_analysis, indent=2, default=str))
                
                if choice in ["2", "3"]:
                    print("\n" + "="*50)
                    print("🏗️ DETAILED PLATFORMS DATA:")
                    print("="*50)
                    platforms_data = platforms_detector.detect_platform_interactions(address)
                    print(json.dumps(platforms_data, indent=2, default=str))
                
        except KeyboardInterrupt:
            print("\n👋 Analysis complete!")
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        print("Please try again or check your internet connection.")

if __name__ == "__main__":
    main() 