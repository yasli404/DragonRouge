import argparse
import psutil
import time
from collections import defaultdict
from scapy.all import sniff, IP

class NetworkMonitor:
    def __init__(self):
        self.packet_counts = defaultdict(int)
        self.start_time = time.time()

    def packet_callback(self, packet):
        if IP in packet:
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            self.packet_counts[(src_ip, dst_ip)] += 1

    def monitor_network(self, interface, duration):
        print(f"Monitoring network on {interface} for {duration} seconds...")
        sniff(iface=interface, prn=self.packet_callback, timeout=duration)

    def print_stats(self):
        print("\nNetwork Statistics:")
        total_packets = sum(self.packet_counts.values())
        elapsed_time = time.time() - self.start_time
        print(f"Total packets: {total_packets}")
        print(f"Packets per second: {total_packets / elapsed_time:.2f}")
        print("\nTop 5 connections:")
        for (src, dst), count in sorted(self.packet_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"{src} -> {dst}: {count} packets")

        io = psutil.net_io_counters()
        print(f"\nBytes sent: {io.bytes_sent}")
        print(f"Bytes received: {io.bytes_recv}")

def list_interfaces():
    interfaces = psutil.net_if_addrs()
    print("Available network interfaces:")
    for interface in interfaces:
        print(f" - {interface}")

def main():
    parser = argparse.ArgumentParser(description="Network Monitoring Tool")
    parser.add_argument('-i', '--interface', type=str, help='Network interface to monitor', required=True)
    parser.add_argument('-d', '--duration', type=int, help='Monitoring duration in seconds', default=60)
    args = parser.parse_args()

    if args.interface not in psutil.net_if_addrs():
        print(f"Error: Interface {args.interface} not found.")
        list_interfaces()
        return

    monitor = NetworkMonitor()
    monitor.monitor_network(args.interface, args.duration)
    monitor.print_stats()

if __name__ == "__main__":
    main()
