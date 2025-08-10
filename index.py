#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
import os
import time
import random
import concurrent.futures
from typing import Optional, Dict, Any, List
from datetime import datetime
import sys

try:
    from tabulate import tabulate
except ImportError:
    print("Installing tabulate for beautiful table output...")
    os.system("pip install tabulate")
    from tabulate import tabulate


class ProxyManager:
    
    def __init__(self, proxy_file: str = "proxies.txt"):
        self.proxy_file = proxy_file
        self.proxies = self._load_proxies()
        self._validate_proxies()
    
    def _load_proxies(self) -> List[str]:
        proxies = []
        
        if not os.path.exists(self.proxy_file):
            print(f"File {self.proxy_file} not found. Creating example file...")
            self._create_example_proxy_file()
            return []
        
        try:
            with open(self.proxy_file, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if line.startswith('http://'):
                            proxies.append(line)
                        else:
                            parts = line.split(':')
                            if len(parts) >= 4:
                                host, port, username = parts[0], parts[1], parts[2]
                                password = ':'.join(parts[3:])
                                
                                if self._validate_proxy_format(host, port, username, password):
                                    proxy_url = f"http://{username}:{password}@{host}:{port}"
                                    proxies.append(proxy_url)
                                else:
                                    print(f"Invalid proxy format in line {line_num}: {line}")
            
            return proxies
        except Exception as e:
            print(f"Error loading proxies: {e}")
            return []
    
    def _create_example_proxy_file(self):
        example_content = """# Proxy format: host:port:username:password
"""
        try:
            with open(self.proxy_file, 'w', encoding='utf-8') as f:
                f.write(example_content)
            print(f"Created file {self.proxy_file}. Add your proxies to it.")
        except Exception as e:
            print(f"Error creating proxy file: {e}")
    
    def _validate_proxy_format(self, host: str, port: str, username: str, password: str) -> bool:
        try:
            if not host or not port or not username:
                return False
            
            port_int = int(port)
            if not (1 <= port_int <= 65535):
                return False
            
            return True
        except:
            return False
    
    def _validate_proxies(self) -> None:
        valid_count = len(self.proxies)
        if valid_count > 0:
            print(f"Loaded {valid_count} valid proxies")
        else:
            print("No proxies loaded - direct connections will be used")
    
    def get_random_proxy(self) -> Optional[Dict[str, str]]:
        if not self.proxies:
            return None
        
        proxy_url = random.choice(self.proxies)
        return {
            'http': proxy_url,
            'https': proxy_url
        }


class WalletManager:
    
    def __init__(self, wallet_file: str = "wallets.txt"):
        self.wallet_file = wallet_file
        self.wallets = self._load_wallets()
    
    def _load_wallets(self) -> List[str]:
        wallets = []
        
        if not os.path.exists(self.wallet_file):
            print(f"File {self.wallet_file} not found. Creating example file...")
            self._create_example_wallet_file()
            return []
        
        try:
            with open(self.wallet_file, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if self._is_valid_address(line):
                            wallets.append(line)
                        else:
                            print(f"Invalid wallet address in line {line_num}: {line}")
            
            return wallets
        except Exception as e:
            print(f"Error loading wallets: {e}")
            return []
    
    def _create_example_wallet_file(self):
        example_content = """# Ethereum wallet addresses (one per line)
# Example:
# 0x1234567890123456789012345678901234567890
# 0xabcdefabcdefabcdefabcdefabcdefabcdefabcd

# Add your wallet addresses below:
"""
        try:
            with open(self.wallet_file, 'w', encoding='utf-8') as f:
                f.write(example_content)
            print(f"Created file {self.wallet_file}. Add wallet addresses to it.")
        except Exception as e:
            print(f"Error creating wallet file: {e}")
    
    def _is_valid_address(self, address: str) -> bool:
        return (
            isinstance(address, str) and
            len(address) == 42 and
            address.startswith('0x') and
            all(c in '0123456789abcdefABCDEF' for c in address[2:])
        )


class PharosAPIClient:
    
    API_BASE = "https://api.pharosnetwork.xyz"
    BEARER_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3ODA5MTQ3NjEsImlhdCI6MTc0OTM3ODc2MSwic3ViIjoiMHgyNkIxMzVBQjFkNjg3Mjk2N0I1YjJjNTcwOWNhMkI1RERiREUxMDZGIn0.k1JtNw2w67q7lw1kFHmSXxapUS4GpBwXdZH3ByVMFfg"
    
    def __init__(self, proxy_manager: ProxyManager):
        self.proxy_manager = proxy_manager
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Authorization': f'Bearer {self.BEARER_TOKEN}',
            'Origin': 'https://testnet.pharosnetwork.xyz',
            'Referer': 'https://testnet.pharosnetwork.xyz/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_user_data(self, wallet_address: str) -> Dict[str, Any]:
        try:
            profile_url = f"{self.API_BASE}/user/profile"
            profile_params = {'address': wallet_address}
            
            tasks_url = f"{self.API_BASE}/user/tasks"
            tasks_params = {'address': wallet_address}
            
            proxies = self.proxy_manager.get_random_proxy()
            
            profile_response = self._make_request(profile_url, profile_params, proxies, timeout=10)
            tasks_response = self._make_request(tasks_url, tasks_params, proxies, timeout=10)
            
            if not profile_response or not tasks_response:
                return {
                    'success': False,
                    'error': 'Failed to get data from API',
                    'address': wallet_address
                }
            
            return self._process_api_response(profile_response, tasks_response, wallet_address)
            
        except Exception as e:
            return {
                'success': False,
                'error': f'API Error: {str(e)}',
                'address': wallet_address
            }
    
    def _make_request(self, url: str, params: Dict[str, str], 
                     proxies: Optional[Dict[str, str]], timeout: int) -> Optional[Dict[str, Any]]:
        try:
            response = self.session.get(
                url, 
                params=params, 
                proxies=proxies, 
                timeout=timeout
            )
            
            if response.status_code == 200:
                try:
                    return response.json()
                except ValueError as e:
                    print(f"JSON parsing error: {e}")
                    return None
            else:
                print(f"HTTP {response.status_code} for {url}")
                return None
                
        except requests.exceptions.Timeout:
            print(f"Request timeout to {url}")
            return None
        except requests.exceptions.ProxyError:
            print(f"Proxy error for {url}")
            return None
        except Exception as e:
            print(f"Request error to {url}: {e}")
            return None
    
    def _process_api_response(self, profile_data: Dict[str, Any], 
                            tasks_data: Dict[str, Any], 
                            wallet_address: str) -> Dict[str, Any]:
        try:
            if profile_data.get('code') != 0:
                error_msg = profile_data.get('msg', 'Unknown error')
                if 'get user info failed' in error_msg:
                    error_msg = 'Wallet not registered in Pharos Network'
                return {
                    'success': False,
                    'error': error_msg,
                    'address': wallet_address
                }
            
            profile = profile_data.get('data', {}).get('user_info', {})
            total_points = profile.get('TotalPoints', 0)
            current_level = self._calculate_level(total_points)
            
            if tasks_data.get('code') != 0:
                task_counts = {'send_count': 0, 'swap_count': 0, 'lp_count': 0, 'social_tasks': 0, 
                             'mint_domain': 0, 'mint_nft': 0, 'faroswap_lp': 0, 'faroswap_swaps': 0,
                             'primuslabs_send': 0, 'rwafi': 0, 'stake': 0, 'fiamma_bridge': 0, 'brokex': 0}
            else:
                user_tasks = tasks_data.get('data', {}).get('user_tasks', [])
                task_counts = self._parse_task_data(user_tasks)
            
            return {
                'success': True,
                'address': wallet_address,
                'total_points': total_points,
                'current_level': current_level,
                'send_count': task_counts['send_count'],
                'swap_count': task_counts['swap_count'],
                'lp_count': task_counts['lp_count'],
                'social_tasks': task_counts['social_tasks'],
                'mint_domain': task_counts['mint_domain'],
                'mint_nft': task_counts['mint_nft'],
                'faroswap_lp': task_counts['faroswap_lp'],
                'faroswap_swaps': task_counts['faroswap_swaps'],
                'primuslabs_send': task_counts['primuslabs_send'],
                'rwafi': task_counts['rwafi'],
                'stake': task_counts['stake'],
                'fiamma_bridge': task_counts['fiamma_bridge'],
                'brokex': task_counts['brokex'],
                'member_since': profile.get('CreateTime'),
                'rank': None
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Data processing error: {str(e)}',
                'address': wallet_address
            }
    
    def _parse_task_data(self, user_tasks: List[Dict[str, Any]]) -> Dict[str, int]:
        task_counts = {
            'send_count': 0, 'swap_count': 0, 'lp_count': 0, 'social_tasks': 0,
            'mint_domain': 0, 'mint_nft': 0, 'faroswap_lp': 0, 'faroswap_swaps': 0,
            'primuslabs_send': 0, 'rwafi': 0, 'stake': 0,
            'fiamma_bridge': 0, 'brokex': 0
        }
        
        task_id_mapping = {
            103: 'send_count',
            101: 'swap_count',
            102: 'lp_count',
            107: 'faroswap_swaps',
            106: 'faroswap_lp',
            105: 'mint_nft',
            104: 'mint_domain',
            108: 'primuslabs_send',
            112: 'rwafi',
            110: 'stake',
            111: 'brokex',
            113: 'fiamma_bridge',
            201: 'social_tasks',
            202: 'swap_count',
            203: 'lp_count',
            109: 'rwafi',
            114: 'rwafi'
        }
        
        for task in user_tasks:
            task_id = task.get('TaskId', 0)
            complete_times = task.get('CompleteTimes', 0)
            
            task_type = task_id_mapping.get(task_id)
            if task_type:
                task_counts[task_type] += complete_times
        
        return task_counts
    
    def _calculate_level(self, total_points: int) -> int:
        if total_points >= 10000:
            return 5
        elif total_points >= 5000:
            return 4
        elif total_points >= 2000:
            return 3
        elif total_points >= 500:
            return 2
        else:
            return 1


class PharosChecker:
    
    def __init__(self):
        self.proxy_manager = ProxyManager()
        self.wallet_manager = WalletManager()
        self.api_client = PharosAPIClient(self.proxy_manager)
    
    def check_wallets(self, max_workers: int = 5):
        wallets = self.wallet_manager.wallets
        
        if not wallets:
            print("No wallets to check. Add addresses to wallets.txt")
            return
        
        print(f"Starting check of {len(wallets)} wallets...")
        print("=" * 80)
        
        results = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_wallet = {
                executor.submit(self.api_client.get_user_data, wallet): wallet 
                for wallet in wallets
            }
            
            for i, future in enumerate(concurrent.futures.as_completed(future_to_wallet), 1):
                wallet = future_to_wallet[future]
                try:
                    result = future.result()
                    results.append(result)
                    
                    print(f"Processed wallet {i}/{len(wallets)}: {wallet[:10]}...")
                    
                    time.sleep(random.uniform(0.5, 1.5))
                    
                except Exception as e:
                    print(f"Error for {wallet}: {e}")
                    results.append({
                        'success': False,
                        'error': str(e),
                        'address': wallet
                    })
        
        print("\n" + "=" * 80)
        self._display_results(results)
    
    def check_single_wallet(self, wallet_address: str):
        if not self.wallet_manager._is_valid_address(wallet_address):
            print(f"Invalid wallet address format: {wallet_address}")
            return
        
        print(f"Checking wallet: {wallet_address}")
        print("=" * 80)
        
        try:
            result = self.api_client.get_user_data(wallet_address)
            self._display_results([result])
        except Exception as e:
            print(f"Error checking wallet: {e}")
            result = {
                'success': False,
                'error': str(e),
                'address': wallet_address
            }
            self._display_results([result])
    
    def _display_results(self, results: List[Dict[str, Any]]):
        
        for result in results:
            if result.get('success'):
                print("\n\033[92mWALLET CHECK RESULTS\033[0m")
                print("=" * 80)
                
                main_table = [[
                    result['address'][:10] + '...',
                    result['total_points'],
                    result['current_level'],
                    result.get('member_since', 'N/A')[:10] if result.get('member_since') else 'N/A'
                ]]
                
                headers = ['Wallet Address', 'Points', 'Level', 'Member Since']
                print(tabulate(main_table, headers=headers, tablefmt='grid'))
                
                print("\nDETAILED TRANSACTION INFORMATION")
                print("=" * 80)
                
                task_table = [
                    ['Send Transactions', result['send_count'], 'Zenith Swap Transactions', result['swap_count']],
                    ['Zenith LP Transactions', result['lp_count'], 'Mint Domain', result['mint_domain']],
                    ['Mint NFT', result['mint_nft'], 'FaroSwap LP', result['faroswap_lp']],
                    ['FaroSwap Swaps', result['faroswap_swaps'], 'PrimusLabs Send', result['primuslabs_send']],
                    ['RWAfi', result['rwafi'], 'Stake', result['stake']],
                    ['Fiamma Bridge', result['fiamma_bridge'], 'BrokeX', result['brokex']]
                ]
                
                print(tabulate(task_table, tablefmt='grid'))
                
            else:
                print(f"\nERROR for {result['address'][:10]}...: {result['error']}")
                print("=" * 80)


def show_menu():
    print("\nPharos Network Stats Checker v4.0.0")
    print("=" * 50)
    print("1. Load wallets from wallets.txt file")
    print("2. Enter wallet address manually")
    print("0. Exit")
    print("=" * 50)


def get_user_choice():
    while True:
        try:
            choice = input("\nSelect option (0-2): ").strip()
            if choice in ['0', '1', '2']:
                return choice
            else:
                print("Invalid choice. Please enter 0, 1, or 2.")
        except KeyboardInterrupt:
            print("\nExiting...")
            return '0'
        except Exception as e:
            print(f"Input error: {e}")


def get_wallet_address():
    while True:
        try:
            address = input("\nEnter wallet address (0x...): ").strip()
            if address.lower() == 'exit' or address == '0':
                return None
            if len(address) == 42 and address.startswith('0x'):
                return address
            else:
                print("Invalid address format. Please enter a valid Ethereum address.")
        except KeyboardInterrupt:
            print("\nReturning to menu...")
            return None
        except Exception as e:
            print(f"Input error: {e}")


def main():
    checker = PharosChecker()
    
    while True:
        show_menu()
        choice = get_user_choice()
        
        if choice == '0':
            print("Goodbye!")
            break
        elif choice == '1':
            checker.check_wallets()
            input("\nPress Enter to return to menu...")
        elif choice == '2':
            wallet_address = get_wallet_address()
            if wallet_address:
                checker.check_single_wallet(wallet_address)
            input("\nPress Enter to return to menu...")


if __name__ == "__main__":
    main()
