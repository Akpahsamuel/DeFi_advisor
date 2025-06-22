#!/usr/bin/env python3
"""
Simple DeFi Advisor for Sui Blockchain
No smart contracts required - uses existing blockchain data
"""

from pysui import PysuiConfiguration, SyncGqlClient
import pysui.sui.sui_pgql.pgql_query as qn
import json
from typing import Dict, List, Optional
import os

class SuiDeFiAdvisor:
    """DeFi advisor that analyzes Sui blockchain data without smart contracts"""
    
    def __init__(self):
        """Initialize the advisor with Sui GraphQL client"""
        try:
            # Use the properly configured PysuiConfiguration
            cfg = PysuiConfiguration(group_name=PysuiConfiguration.SUI_GQL_RPC_GROUP)
            self.client = SyncGqlClient(pysui_config=cfg, write_schema=False)
            print("✅ DeFi Advisor initialized successfully on MAINNET")
            print(f"📡 Connected to: {cfg.url}")
        except Exception as e:
            print(f"❌ Failed to initialize: {e}")
            self.client = None
    
    def analyze_portfolio(self, address: str) -> Dict:
        """
        Analyze a wallet's portfolio for DeFi opportunities
        NO SMART CONTRACTS NEEDED - reads existing blockchain data
        """
        if not self.client:
            return {"error": "Client not initialized"}
        
        try:
            print(f"🔍 Analyzing portfolio for address: {address}")
            
            # Get all coin balances
            balances_result = self.client.execute_query_node(
                with_node=qn.GetAllCoinBalances(owner=address)
            )
            
            # Get all owned objects
            objects_result = self.client.execute_query_node(
                with_node=qn.GetObjectsOwnedByAddress(owner=address)
            )
            
            # Basic portfolio analysis
            analysis = self._analyze_portfolio_data(balances_result, objects_result)
            
            return analysis
            
        except Exception as e:
            return {"error": f"Analysis failed: {e}"}
    
    def get_staking_opportunities(self) -> Dict:
        """
        Find best staking opportunities using existing validators
        NO SMART CONTRACTS NEEDED - uses Sui's built-in staking
        """
        if not self.client:
            return {"error": "Client not initialized"}
        
        try:
            print("🎯 Finding staking opportunities...")
            
            # Get validator APY information
            validators_result = self.client.execute_query_node(
                with_node=qn.GetValidatorsApy()
            )
            
            # Get current gas price for cost analysis
            gas_result = self.client.execute_query_node(
                with_node=qn.GetReferenceGasPrice()
            )
            
            opportunities = self._analyze_staking_data(validators_result, gas_result)
            
            return opportunities
            
        except Exception as e:
            return {"error": f"Staking analysis failed: {e}"}
    
    def _analyze_portfolio_data(self, balances_result, objects_result) -> Dict:
        """Analyze portfolio data and provide insights"""
        try:
            balances_data = balances_result.result_data
            objects_data = objects_result.result_data
            
            # Count different assets - fix the data parsing
            coin_types = []
            total_balance_count = 0
            total_balance_value = 0
            
            # Parse coin balances correctly
            if hasattr(balances_data, 'data') and balances_data.data:
                for balance in balances_data.data:
                    if hasattr(balance, 'coin_type'):
                        coin_types.append(balance.coin_type)
                        total_balance_count += 1
                        # Extract balance value
                        if hasattr(balance, 'total_balance'):
                            try:
                                balance_val = int(balance.total_balance)
                                total_balance_value += balance_val
                            except (ValueError, TypeError):
                                pass
            
            # Count objects (NFTs, DeFi positions, etc.)
            object_count = 0
            special_objects = []
            if hasattr(objects_data, 'data') and objects_data.data:
                object_count = len(objects_data.data)
                # Identify special objects
                for obj in objects_data.data:
                    if hasattr(obj, 'object_type'):
                        obj_type = obj.object_type
                        if 'suins_registration' in obj_type.lower():
                            special_objects.append("SuiNS Domain")
                        elif 'vote' in obj_type.lower():
                            special_objects.append("Voting NFT")
                        elif 'upgradecap' in obj_type.lower():
                            special_objects.append("Package Upgrade Cap")
                        elif 'coin::coin' in obj_type.lower():
                            # Skip coin objects as they're counted separately
                            continue
                        else:
                            special_objects.append("DeFi Position")
            
            # Generate insights based on actual data
            insights = []
            risk_level = "Low"
            
            if total_balance_count == 0:
                insights.append("⚠️  Empty portfolio - consider acquiring some SUI tokens")
                risk_level = "High"
            elif total_balance_count == 1:
                insights.append("⚠️  Single asset portfolio - consider diversification")
                risk_level = "High"
            elif total_balance_count <= 3:
                insights.append("📊 Limited diversification - consider adding more asset types")
                risk_level = "Medium"
            else:
                insights.append("✅ Good diversification across multiple assets")
                risk_level = "Low"
            
            if object_count > 0:
                insights.append(f"🎨 You own {object_count} objects including: {', '.join(special_objects[:3])}")
            
            # Check for SUI tokens specifically
            has_sui = any('sui::SUI' in ct for ct in coin_types)
            if has_sui:
                insights.append("💰 You have SUI tokens - great for staking!")
            
            # Check for stablecoins
            has_stablecoins = any('usdc' in ct.lower() or 'usdt' in ct.lower() for ct in coin_types)
            if has_stablecoins:
                insights.append("🛡️  You have stablecoins - good for portfolio stability")
            
            return {
                "portfolio_summary": {
                    "total_coin_types": total_balance_count,
                    "unique_coin_types": len(set(coin_types)),
                    "objects_owned": object_count,
                    "risk_level": risk_level,
                    "special_objects": special_objects
                },
                "insights": insights,
                "coin_types": [ct.split('::')[-1] if '::' in ct else ct for ct in coin_types[:5]],  # Show readable names
                "recommendations": self._generate_recommendations(total_balance_count, coin_types, has_sui, has_stablecoins)
            }
            
        except Exception as e:
            return {"error": f"Portfolio analysis failed: {e}"}
    
    def _analyze_staking_data(self, validators_result, gas_result) -> Dict:
        """Analyze staking opportunities"""
        try:
            opportunities = {
                "top_validators": [],
                "gas_cost_analysis": {},
                "recommendations": []
            }
            
            # Basic gas analysis
            if hasattr(gas_result.result_data, 'reference_gas_price'):
                gas_price = gas_result.result_data.reference_gas_price
                # Convert gas price to int if it's a string
                try:
                    gas_price_int = int(gas_price) if isinstance(gas_price, str) else gas_price
                    opportunities["gas_cost_analysis"] = {
                        "current_gas_price": str(gas_price),
                        "recommendation": "Low gas costs - good time for transactions" if gas_price_int < 1000 else "High gas costs - consider waiting"
                    }
                except (ValueError, TypeError):
                    opportunities["gas_cost_analysis"] = {
                        "current_gas_price": str(gas_price),
                        "recommendation": "Gas price information available"
                    }
            
            # Validator analysis would go here
            # For now, provide general staking advice
            opportunities["recommendations"] = [
                "💡 Staking SUI tokens can provide passive income",
                "🎯 Look for validators with high APY and good performance",
                "⚖️  Consider validator commission rates and uptime",
                "🔄 Diversify across multiple validators to reduce risk"
            ]
            
            return opportunities
            
        except Exception as e:
            return {"error": f"Staking analysis failed: {e}"}
    
    def _generate_recommendations(self, coin_count: int, coin_types: List[str], has_sui: bool, has_stablecoins: bool) -> List[str]:
        """Generate personalized DeFi recommendations"""
        recommendations = []
        
        if coin_count == 0:
            recommendations.extend([
                "🚀 Start by acquiring some SUI tokens",
                "📚 Learn about Sui ecosystem and available DeFi protocols",
                "💼 Consider dollar-cost averaging into your first positions"
            ])
        elif coin_count <= 2:
            recommendations.extend([
                "🌈 Diversify into stablecoins for stability",
                "💰 Start staking SUI tokens for passive income",
                "🔍 Explore Sui DeFi protocols for yield opportunities"
            ])
        else:
            recommendations.extend([
                "⚖️  Review portfolio balance regularly",
                "📈 Consider yield farming opportunities",
                "🛡️  Keep some stablecoins for stability",
                "🔄 Rebalance portfolio quarterly"
            ])
        
        if has_sui:
            recommendations.append("💰 Consider staking your SUI tokens for passive income")
        
        if has_stablecoins:
            recommendations.append("🛡️  Consider holding stablecoins for portfolio stability")
        
        return recommendations
    
    def generate_report(self, address: str) -> str:
        """Generate a comprehensive DeFi report"""
        print("📊 Generating comprehensive DeFi report...")
        
        portfolio = self.analyze_portfolio(address)
        staking = self.get_staking_opportunities()
        
        report = f"""
🏦 SUI DEFI ADVISOR REPORT
{'='*50}

📍 Address: {address}

📊 PORTFOLIO ANALYSIS:
{'-'*30}
"""
        
        if "error" not in portfolio:
            summary = portfolio.get("portfolio_summary", {})
            report += f"""
• Total Coin Types: {summary.get('total_coin_types', 0)}
• Unique Assets: {summary.get('unique_coin_types', 0)}
• Objects Owned: {summary.get('objects_owned', 0)}
• Risk Level: {summary.get('risk_level', 'Unknown')}

💡 KEY INSIGHTS:
"""
            for insight in portfolio.get("insights", []):
                report += f"  {insight}\n"
            
            report += f"\n🎯 RECOMMENDATIONS:\n"
            for rec in portfolio.get("recommendations", []):
                report += f"  {rec}\n"
        else:
            report += f"  ❌ {portfolio['error']}\n"
        
        report += f"""
💰 STAKING OPPORTUNITIES:
{'-'*30}
"""
        
        if "error" not in staking:
            for rec in staking.get("recommendations", []):
                report += f"  {rec}\n"
            
            gas_info = staking.get("gas_cost_analysis", {})
            if gas_info:
                report += f"\n⛽ Gas Price: {gas_info.get('current_gas_price', 'Unknown')}\n"
                report += f"  {gas_info.get('recommendation', '')}\n"
        else:
            report += f"  ❌ {staking['error']}\n"
        
        report += f"""
{'='*50}
🤖 Report generated by Sui DeFi Advisor
📅 Timestamp: {json.dumps({"generated": "now"}, indent=2)}
"""
        
        return report

# End of SuiDeFiAdvisor class
# Use main.py to run the advisor 