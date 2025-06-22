#!/usr/bin/env python3
"""
Sui DeFi Platforms Detection Module
Identifies and analyzes major DeFi protocols on Sui blockchain
"""

from pysui import PysuiConfiguration, SyncGqlClient
import pysui.sui.sui_pgql.pgql_query as qn
from typing import Dict, List, Optional
import json

class SuiDeFiPlatforms:
    """Detect and analyze DeFi platforms on Sui"""
    
    def __init__(self):
        """Initialize with Sui GraphQL client"""
        try:
            cfg = PysuiConfiguration(group_name=PysuiConfiguration.SUI_GQL_RPC_GROUP)
            self.client = SyncGqlClient(pysui_config=cfg, write_schema=False)
            print("✅ DeFi Platforms detector initialized")
        except Exception as e:
            print(f"❌ Failed to initialize platforms detector: {e}")
            self.client = None
        
        # Major DeFi platforms on Sui with their identifiers
        self.platforms = {
            "NAVI": {
                "name": "NAVI Protocol",
                "type": "Lending/Borrowing",
                "description": "Leading lending protocol on Sui",
                "package_ids": [
                    "0xa99b8952d4f7d947ea77fe0ecdcc9e5fc0bcab2841d6e2a5aa00c3044e5544b5",
                    "0x0e2a7e0b6b8b5b5b5b5b5b5b5b5b5b5b5b5b5b5b5b5b5b5b5b5b5b5b5b5b5b5b"
                ],
                "coin_types": ["navi", "navx"],
                "features": ["Lending", "Borrowing", "Yield Farming"]
            },
            "CETUS": {
                "name": "Cetus Protocol",
                "type": "DEX/AMM",
                "description": "Concentrated liquidity DEX on Sui",
                "package_ids": [
                    "0x1eabed72c53feb3805120a081dc15963c204dc8d091542592abaf7a35689b2fb",
                    "0x0868b71c0cba55bf0faf6c40df8c179c67a4d0ba0e79965b68b3d72d7dfbf666"
                ],
                "coin_types": ["cetus"],
                "features": ["DEX", "Liquidity Pools", "Concentrated Liquidity"]
            },
            "SUILEND": {
                "name": "Suilend",
                "type": "Lending",
                "description": "Decentralized lending protocol",
                "package_ids": [
                    "0xf95b06141ed4a174f239417323bde3f209b972f5930d8521ea38a52aff3a6ddf"
                ],
                "coin_types": ["slnd"],
                "features": ["Lending", "Borrowing"]
            },
            "SCALLOP": {
                "name": "Scallop",
                "type": "Lending/DeFi",
                "description": "Multi-feature DeFi protocol",
                "package_ids": [
                    "0xefe8b36d5b2e43728cc323298626b83177803521d195cfb11e15b910e892fddf"
                ],
                "coin_types": ["sca", "scallop"],
                "features": ["Lending", "Staking", "Yield Farming"]
            },
            "DEEPBOOK": {
                "name": "DeepBook",
                "type": "DEX/Orderbook",
                "description": "Central limit order book DEX",
                "package_ids": [
                    "0x000000000000000000000000000000000000000000000000000000000000dee9"
                ],
                "coin_types": ["deep"],
                "features": ["Order Book", "Trading", "Market Making"]
            },
            "BLUEMOVE": {
                "name": "BlueMove",
                "type": "NFT/DeFi",
                "description": "NFT marketplace with DeFi features",
                "package_ids": [
                    "0x5c8657a6009556804585cd667be3b43487062195422ff586333721de0f8baeae"
                ],
                "coin_types": ["move"],
                "features": ["NFT Trading", "Staking", "Launchpad"]
            },
            "TURBOS": {
                "name": "Turbos Finance",
                "type": "DEX/AMM",
                "description": "Concentrated liquidity AMM",
                "package_ids": [
                    "0x91bfbc386a41afcfd9b2533058d7e915a1d3829089cc268ff4333d54d6339ca1"
                ],
                "coin_types": ["turbos"],
                "features": ["AMM", "Concentrated Liquidity", "Yield Farming"]
            },
            "AFTERMATH": {
                "name": "Aftermath Finance",
                "type": "DEX/AMM",
                "description": "Multi-pool AMM with advanced features",
                "package_ids": [
                    "0xefe170ec0be4d762196bedecd7a065816576198a6527c99282a2551aaa7da38c",
                    "0x0625dc2cd40aee3998a1d6620de8892964c15066e0a285d8b573910ed4c75d50"
                ],
                "coin_types": ["af", "aftermath"],
                "features": ["DEX", "Multi-Pool AMM", "Yield Farming", "Liquidity Mining"]
            },
            "BLUEFIN": {
                "name": "Bluefin",
                "type": "Derivatives/Perps",
                "description": "Decentralized derivatives and perpetuals exchange",
                "package_ids": [
                    "0xe1b4d32bc4747a6f2d99d5b7a5b4b4b4b4b4b4b4b4b4b4b4b4b4b4b4b4b4b4b4",
                    "0xbluefin_package_id_placeholder"
                ],
                "coin_types": ["blue", "bluefin"],
                "features": ["Perpetuals", "Derivatives", "Margin Trading", "Order Book"]
            }
        }
    
    def detect_platform_interactions(self, address: str) -> Dict:
        """Detect which DeFi platforms a wallet has interacted with"""
        if not self.client:
            return {"error": "Client not initialized"}
        
        try:
            print(f"🔍 Detecting DeFi platform interactions for: {address}")
            
            # Get all objects owned by the address
            objects_result = self.client.execute_query_node(
                with_node=qn.GetObjectsOwnedByAddress(owner=address)
            )
            
            # Get coin balances to check for platform tokens
            balances_result = self.client.execute_query_node(
                with_node=qn.GetAllCoinBalances(owner=address)
            )
            
            detected_platforms = self._analyze_platform_interactions(
                objects_result, balances_result
            )
            
            return detected_platforms
            
        except Exception as e:
            return {"error": f"Platform detection failed: {e}"}
    
    def _analyze_platform_interactions(self, objects_result, balances_result) -> Dict:
        """Analyze objects and balances to detect platform interactions"""
        detected = {
            "active_platforms": [],
            "token_holdings": [],
            "defi_positions": [],
            "recommendations": []
        }
        
        try:
            # Analyze coin balances for platform tokens
            if hasattr(balances_result.result_data, 'data') and balances_result.result_data.data:
                for balance in balances_result.result_data.data:
                    if hasattr(balance, 'coin_type'):
                        coin_type = balance.coin_type.lower()
                        
                        # Check against known platform tokens
                        for platform_key, platform_info in self.platforms.items():
                            for token in platform_info["coin_types"]:
                                if token.lower() in coin_type:
                                    detected["active_platforms"].append({
                                        "platform": platform_info["name"],
                                        "type": platform_info["type"],
                                        "token": token.upper(),
                                        "balance": getattr(balance, 'total_balance', 'Unknown')
                                    })
                                    detected["token_holdings"].append({
                                        "token": token.upper(),
                                        "platform": platform_info["name"],
                                        "balance": getattr(balance, 'total_balance', 'Unknown')
                                    })
            
            # Analyze objects for DeFi positions
            if hasattr(objects_result.result_data, 'data') and objects_result.result_data.data:
                for obj in objects_result.result_data.data:
                    if hasattr(obj, 'object_type'):
                        obj_type = obj.object_type.lower()
                        
                        # Check for known DeFi position types
                        for platform_key, platform_info in self.platforms.items():
                            for package_id in platform_info["package_ids"]:
                                if package_id.lower() in obj_type:
                                    detected["defi_positions"].append({
                                        "platform": platform_info["name"],
                                        "type": platform_info["type"],
                                        "position_type": self._identify_position_type(obj_type),
                                        "object_id": getattr(obj, 'object_id', 'Unknown')
                                    })
            
            # Generate recommendations based on detected platforms
            detected["recommendations"] = self._generate_platform_recommendations(detected)
            
            return detected
            
        except Exception as e:
            return {"error": f"Platform analysis failed: {e}"}
    
    def _identify_position_type(self, object_type: str) -> str:
        """Identify the type of DeFi position based on object type"""
        obj_type_lower = object_type.lower()
        
        if "pool" in obj_type_lower or "lp" in obj_type_lower:
            return "Liquidity Position"
        elif "stake" in obj_type_lower or "staking" in obj_type_lower:
            return "Staking Position"
        elif "borrow" in obj_type_lower or "loan" in obj_type_lower:
            return "Lending Position"
        elif "vault" in obj_type_lower:
            return "Vault Position"
        elif "farm" in obj_type_lower:
            return "Farming Position"
        else:
            return "DeFi Position"
    
    def _generate_platform_recommendations(self, detected_data: Dict) -> List[str]:
        """Generate recommendations based on detected platform usage"""
        recommendations = []
        
        active_platforms = detected_data.get("active_platforms", [])
        token_holdings = detected_data.get("token_holdings", [])
        defi_positions = detected_data.get("defi_positions", [])
        
        if not active_platforms and not defi_positions:
            recommendations.extend([
                "🚀 You haven't started using DeFi on Sui yet!",
                "💡 Consider starting with NAVI Protocol for lending",
                "🔄 Try Cetus DEX for token swapping",
                "📚 Research Sui DeFi ecosystem before investing"
            ])
        elif len(active_platforms) == 1:
            recommendations.extend([
                "🌈 Diversify across multiple DeFi platforms",
                "⚖️ Don't put all funds in one protocol",
                "🔍 Explore other Sui DeFi opportunities"
            ])
        else:
            recommendations.extend([
                "✅ Good diversification across platforms!",
                "📊 Monitor your positions regularly",
                "🔄 Consider rebalancing periodically"
            ])
        
        # Platform-specific recommendations
        platform_types = [p.get("type", "") for p in active_platforms]
        
        if "Lending/Borrowing" in platform_types:
            recommendations.append("💰 Monitor lending rates and adjust positions")
        
        if "DEX/AMM" in platform_types:
            recommendations.append("🌊 Watch for impermanent loss in liquidity positions")
        
        if len(token_holdings) > 0:
            recommendations.append("🎯 Consider staking platform tokens for additional rewards")
        
        return recommendations
    
    def get_platform_info(self, platform_name: str = None) -> Dict:
        """Get information about specific platform or all platforms"""
        if platform_name:
            platform_key = platform_name.upper()
            if platform_key in self.platforms:
                return {platform_key: self.platforms[platform_key]}
            else:
                return {"error": f"Platform {platform_name} not found"}
        else:
            return {"all_platforms": self.platforms}
    
    def generate_platforms_report(self, address: str) -> str:
        """Generate a comprehensive DeFi platforms report"""
        print("🏗️ Generating DeFi platforms report...")
        
        detection_result = self.detect_platform_interactions(address)
        
        report = f"""
🏗️ SUI DEFI PLATFORMS REPORT
{'='*50}

📍 Address: {address}

🔍 PLATFORM INTERACTIONS:
{'-'*30}
"""
        
        if "error" not in detection_result:
            active_platforms = detection_result.get("active_platforms", [])
            token_holdings = detection_result.get("token_holdings", [])
            defi_positions = detection_result.get("defi_positions", [])
            
            if active_platforms:
                report += "\n🎯 ACTIVE PLATFORMS:\n"
                for platform in active_platforms:
                    report += f"  • {platform['platform']} ({platform['type']})\n"
                    report += f"    Token: {platform['token']} | Balance: {platform['balance']}\n"
            
            if defi_positions:
                report += "\n💼 DEFI POSITIONS:\n"
                for position in defi_positions:
                    report += f"  • {position['platform']}: {position['position_type']}\n"
            
            if token_holdings:
                report += "\n🪙 PLATFORM TOKENS:\n"
                for holding in token_holdings:
                    report += f"  • {holding['token']} ({holding['platform']}): {holding['balance']}\n"
            
            if not active_platforms and not defi_positions:
                report += "\n📋 No DeFi platform interactions detected\n"
                report += "💡 This could mean you're new to Sui DeFi or using different platforms\n"
            
            report += "\n🎯 RECOMMENDATIONS:\n"
            for rec in detection_result.get("recommendations", []):
                report += f"  {rec}\n"
            
        else:
            report += f"  ❌ {detection_result['error']}\n"
        
        report += f"""
📚 AVAILABLE PLATFORMS ON SUI:
{'-'*30}
"""
        
        for platform_key, platform_info in self.platforms.items():
            report += f"\n🏗️ {platform_info['name']} ({platform_info['type']})\n"
            report += f"   {platform_info['description']}\n"
            report += f"   Features: {', '.join(platform_info['features'])}\n"
        
        report += f"""
{'='*50}
🤖 Report generated by Sui DeFi Platforms Detector
📅 Analysis complete
"""
        
        return report 