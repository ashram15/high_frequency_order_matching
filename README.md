# High-Frequency Order Matching Engine

A low-latency order matching engine built in C++ with Python tools for testing and visualization. This project implements a limit order book with price-time priority matching, designed to handle high-frequency trading scenarios.

![Demo](assets/HFOM_demo.gif)

## Features

- **Fast C++ Matching Engine** - Efficient order matching using STL data structures
- **Price-Time Priority** - Orders matched based on best price first, then FIFO
- **TCP Socket Server** - Real-time communication on port 8080
- **Dual Queue System** - Separate bid/ask queues with optimal sorting
- **Python Testing Clients** - Send orders and visualize order book depth
- **Real-time Visualization** - Live matplotlib charts showing market depth

## Architecture

### Core Components

- **Order.h** - Order structure with ID, price, quantity, type, and timestamp
- **OrderBook.h/cpp** - Limit order book with bid/ask queues and matching logic
- **main.cpp** - TCP socket server that processes incoming orders
- **client.py** - Simple Python client for sending test orders
- **client_vis.py** - Advanced client with real-time market depth visualization

### Matching Algorithm

The engine uses two sorted maps for optimal matching (best bid and best ask):
- **Bids (Buy Orders)**: Sorted high → low (most aggressive buyer first)
- **Asks (Sell Orders)**: Sorted low → high (cheapest seller first)

When a buyer's offer price ≥ seller's requested price, orders are matched and executed at the seller's price (standard market rules). 

## Prerequisites

- C++ compiler (g++, clang, or similar)
- Python 3.x
- Python packages (for visualization):
  ```bash
  pip install matplotlib
  ```

## Build & Run

### 1. Compile the C++ Server

```bash
# Compile the matching engine
g++ -std=c++11 main.cpp OrderBook.cpp -o matching-engine

# Or use the existing binary if available
./matching-server
```

### 2. Start the Server

```bash
./matching-engine
```

You should see:
```
>>> TRADING ENGINE LISTENING ON PORT 8080 <<<
```

### 3. Run a Test Client

In a separate terminal:

**For Simple Client (Basic Testing)**
```bash
python3 client.py
```

**For Visualization Client (Live Order Book)**
```bash
python3 client_vis.py
```

## Order Protocol

Orders are sent as plain text over TCP in the format:
```
<TYPE> <PRICE> <QUANTITY>
```

Examples:
- `B 100 5` - Buy 5 shares at $100
- `S 102 10` - Sell 10 shares at $102


## Usage Examples

### Example 1: Manual Order Submission

```python
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 8080))
client.send(b"B 100 5")  # Buy 5 @ $100
response = client.recv(1024)
client.close()
```

### Example 2: Order Matching Scenario

```bash
# Terminal 1: Start server
./matching-engine

# Terminal 2: Send orders
python3 client.py
```

Expected Output:
```
Sending: S 100 10
Server Replied: Order Processed
Sending: B 100 5
MATCH: 5 shares at $100
Server Replied: Order Processed
```

## Visualization

The `client_vis.py` client provides a live order book visualization:
- **Green bars**: Bid volume at each price level
- **Red bars**: Ask volume at each price level
- Updates every 200ms with real-time market depth

The visualization runs a market maker algorithm that continuously submits random orders to create realistic market activity.

## Key Design Decisions

1. **STL Maps for Order Book** - `std::map` provides O(log n) insertion and automatic sorting
2. **Greater Comparator for Bids** - Ensures highest bid is at `.begin()` for fast access
3. **Price-Time Priority** - FIFO queues at each price level ensure fairness
4. **One Connection Per Order** - Simplified protocol (can be extended to persistent connections)
5. **Socket Reuse Option** - `SO_REUSEADDR` prevents "Address already in use" errors during development

## Project Structure

```
high_frequency_order_matching/
├── Order.h              # Order data structure
├── OrderBook.h          # Order book interface
├── OrderBook.cpp        # Matching logic implementation
├── main.cpp             # TCP server and main loop
├── client.py            # Basic Python test client
├── client_vis.py        # Visualization client with live charts
├── matching-engine      # Compiled binary (after build)
└── README.md            # This file
```

## Testing

The `client.py` includes a test suite that:
1. Adds a sell order (S 100 10)
2. Adds a buy order that matches (B 100 5)
3. Sends 20 random orders to stress-test the system

Watch the server terminal for `MATCH:` messages indicating successful trades.

## Performance Considerations

- **Low Latency**: C++ implementation for microsecond-level order processing
- **Memory Management**: Proper cleanup of matched orders prevents memory leaks
- **Data Structures**: Sorted maps enable O(log n) order insertion and O(1) best price lookup

## License

This project is open source and available for educational purposes.

