import socket
import time
import threading
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --- GLOBAL STATE ---
# We use lists to track the volume at each price level
# Format: {price: quantity}
bids = {}
asks = {}

# --- NETWORKING THREAD ---


def market_maker():
    """ This function runs in the background, spamming orders to the C++ engine. """
    print("✅ Trader Algorithm Started...")

    while True:
        try:
            # 1. Generate a Random Order
            side = random.choice(["B", "S"])

            # Tighter spread to force more matches
            if side == "B":
                price = random.randint(95, 102)
            else:
                price = random.randint(98, 105)

            qty = random.randint(1, 10)

            # 2. Update Local View (Graph)
            if side == "B":
                bids[price] = bids.get(price, 0) + qty
            else:
                asks[price] = asks.get(price, 0) + qty

            # 3. Send to C++ Engine (New Connection Every Time)
            # We open a NEW socket for every order because the C++ server closes it after 1 msg.
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(('127.0.0.1', 8080))

            msg = f"{side} {price} {qty}"
            client.send(msg.encode('utf-8'))

            # Optional: Read response if you want to be sure it arrived
            # response = client.recv(1024)

            client.close()  # Clean up connection

        except Exception as e:
            print(f"⚠️ Error sending order: {e}")
            time.sleep(1)  # Wait a bit before retrying if server is down
            continue

        time.sleep(0.1)  # Fast trading speed
# --- VISUALIZATION ---


def update_graph(frame):
    """ This runs every 100ms to redraw the graph """
    plt.cla()  # Clear axis

    # Plot Bids (Green)
    if bids:
        sorted_bids = sorted(bids.items())  # Sort by price
        prices = [p for p, q in sorted_bids]
        qtys = [q for p, q in sorted_bids]
        plt.bar(prices, qtys, color='green', alpha=0.6, label='Bids (Buyers)')

    # Plot Asks (Red)
    if asks:
        sorted_asks = sorted(asks.items())
        prices = [p for p, q in sorted_asks]
        qtys = [q for p, q in sorted_asks]
        plt.bar(prices, qtys, color='red', alpha=0.6, label='Asks (Sellers)')

    plt.title('Live Limit Order Book Depth')
    plt.xlabel('Price ($)')
    plt.ylabel('Volume (Qty)')
    plt.legend(loc='upper right')
    plt.grid(True, linestyle='--', alpha=0.3)


if __name__ == "__main__":
    # 1. Start the Trader in a background thread
    t = threading.Thread(target=market_maker)
    t.daemon = True  # Kills thread when main program exits
    t.start()

    # 2. Start the Live Graph (Main Thread)
    fig = plt.figure(figsize=(10, 6))
    ani = FuncAnimation(fig, update_graph, interval=200)  # Update every 200ms
    plt.show()


# ### 🚀 How to Run the Visualization

# 1.  **Start your C++ Server** (Terminal 1):
#     ```bash
#     ./matching_server
#     ```
# 2.  **Start the Visualizer** (Terminal 2):
#     ```bash
#     python3 client_viz.py
