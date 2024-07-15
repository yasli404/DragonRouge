from scapy.all import sniff, IP

def packet_callback(packet):
    if IP in packet:
        ip_src = packet[IP].src
        ip_dst = packet[IP].dst
        print(f"Packet: {ip_src} -> {ip_dst}")

def start_sniffing(interface):
    print(f"Starting packet sniffing on interface {interface}")
    sniff(iface=interface, prn=packet_callback, store=0)

if __name__ == "__main__":
    interface = "eth0"  # Remplacez par l'interface réseau à surveiller
    start_sniffing(interface)