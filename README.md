# Pharos Network Stats Checker

🌟 **A comprehensive tool for checking Pharos Network wallet statistics and transaction data**

## 📋 Features

- **Batch Wallet Processing**: Load and check multiple wallets from a text file
- **Single Wallet Check**: Manually enter and check individual wallet addresses
- **Proxy Support**: Built-in proxy rotation for enhanced privacy and rate limiting
- **Multi-threading**: Concurrent processing for faster bulk wallet checks
- **Detailed Statistics**: Comprehensive transaction data and user information
- **Interactive Menu**: User-friendly command-line interface
- **Error Handling**: Robust error handling with detailed error messages

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Internet connection
- Valid Ethereum wallet addresses

### Installation

1. Clone or download this repository
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the program:
   ```bash
   python index.py
   ```

## 📁 File Structure

```
phr_check/
├── index.py           # Main application file
├── requirements.txt   # Python dependencies
├── wallets.txt       # Wallet addresses 
├── proxies.txt       # Proxy list 
└── README.md         # This file
```

## 🔧 Configuration

### Wallet Setup

1. **Automatic Setup**: On first run, the program creates `wallets.txt` with examples
2. **Manual Setup**: Add Ethereum wallet addresses to `wallets.txt`, one per line:
   ```
   0x1234567890123456789012345678901234567890
   0x1234567890123456789012345678901234567891
   ```

### Proxy Setup (Optional)

1. **Automatic Setup**: On first run, the program creates `proxies.txt` with examples
2. **Manual Setup**: Add proxies to `proxies.txt` in supported formats:
   ```
   # Format 1: host:port:username:password
   192.168.1.1:8080:user:pass
   
   # Format 2: http://username:password@host:port
   http://user:pass@192.168.1.1:8080
   ```

## 🎮 Usage

### Interactive Menu

When you run the program, you'll see an interactive menu:

```
📋 Select operation mode:
1️⃣  Load wallets from wallets.txt file
2️⃣  Enter wallet address manually
0️⃣  Exit
```

### Option 1: Batch Processing

- Loads all wallet addresses from `wallets.txt`
- Processes wallets concurrently (3 threads by default)
- Shows progress for each processed wallet
- Displays comprehensive results for all wallets

### Option 2: Single Wallet Check

- Prompts for manual wallet address input
- Validates address format
- Displays detailed information for the specified wallet

## 📊 Output Information

For each wallet, the program displays:

### Main Information
- **Wallet Address**: Ethereum address
- **Points**: Total Pharos Network points
- **Level**: Current user level
- **Member Since**: Registration date

### Detailed Transaction Statistics
- **Send Transactions**: Number of send operations
- **Zenith Swap Transactions**: Zenith platform swaps
- **Zenith LP Transactions**: Zenith liquidity provider transactions
- **Mint Domain**: Domain minting operations
- **Mint NFT**: NFT minting transactions
- **FaroSwap LP**: FaroSwap liquidity operations
- **FaroSwap Swaps**: FaroSwap trading transactions
- **PrimusLabs Send**: PrimusLabs send operations
- **RWAfi**: RWAfi platform interactions
- **Stake**: Staking operations
- **Fiamma Bridge**: Bridge transactions
- **BrokeX**: BrokeX platform activities

## ⚙️ Technical Details

### API Integration

- **Base URL**: `https://api.pharosnetwork.xyz`
- **Authentication**: Bearer token authentication
- **Endpoints**: 
  - `/user/info` - User profile information
  - `/user/tasks` - User task completion data

### Proxy Management

- **Automatic Rotation**: Random proxy selection for each request
- **Format Support**: Multiple proxy format support
- **Validation**: Built-in proxy testing and validation
- **Fallback**: Direct connection if no working proxies

### Error Handling

- **Network Errors**: Timeout and connection error handling
- **API Errors**: Proper API response error processing
- **Validation**: Address format and input validation
- **Graceful Degradation**: Continues operation despite individual failures

## 🛠️ Dependencies

- **requests**: HTTP library for API calls
- **tabulate**: Beautiful table formatting
- **concurrent.futures**: Multi-threading support

## 📝 Example Output

```
📊 WALLET CHECK RESULTS
================================================================================
+----------------------+---------+-------+------------------------+
| Wallet Address       | Points  | Level | Member Since           |
+======================+=========+=======+========================+
| 0x123214...        | 10000       | 5     | 2025-08-09             |
+----------------------+---------+-------+------------------------+

📋 DETAILED TRANSACTION INFORMATION
================================================================================
+----------------------+---------+------------------------+---------+
| Task Type            | Count   | Task Type              | Count   |
+======================+=========+========================+=========+
| Send Transactions    | 65      | Zenith Swap Transactions| 1     |
| Zenith LP Transactions| 12     | Mint Domain            | 01     |
| Mint NFT             | 11      | FaroSwap LP            | 2      |
| FaroSwap Swaps       | 85      | PrimusLabs Send        | 74     |
| RWAfi                | 5       | Stake                  | 13     |
| Fiamma Bridge        | 0       | BrokeX                 | 122    |
+----------------------+---------+------------------------+---------+
```

## 🔒 Security

- **No Private Keys**: Only public wallet addresses are used
- **Proxy Support**: Enhanced privacy through proxy rotation
- **Rate Limiting**: Built-in delays to respect API limits
- **Error Isolation**: Individual wallet failures don't affect others

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## 📄 License

This project is open source and available under the MIT License.

## ⚠️ Disclaimer

This tool is for informational purposes only. Use responsibly and in accordance with Pharos Network's terms of service.

---

**Made with ❤️ for the Pharos Network community**
