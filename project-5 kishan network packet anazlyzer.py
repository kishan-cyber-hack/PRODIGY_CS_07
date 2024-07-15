import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext
from scapy.all import sniff, wrpcap, IP, TCP, UDP, ARP, ICMP

class PacketSnifferApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Network Packet Analyzer")

        self.is_sniffing = False
        self.packets = []

        self.start_button = tk.Button(root, text="Start Capture", command=self.start_sniffing)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop Capture", command=self.stop_sniffing, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        self.save_button = tk.Button(root, text="Save Packets", command=self.save_packets, state=tk.DISABLED)
        self.save_button.pack(pady=10)

        self.filter_button = tk.Button(root, text="Set Filter", command=self.set_filter)
        self.filter_button.pack(pady=10)

        self.text_area = scrolledtext.ScrolledText(root, height=20, width=100)
        self.text_area.pack(pady=10)

        self.filter_expression = ""

    def set_filter(self):
        self.filter_expression = simpledialog.askstring("Input", "Enter filter expression (e.g., 'tcp', 'udp', 'port 80'):")
        if self.filter_expression:
            self.text_area.insert(tk.END, f"Filter set to: {self.filter_expression}\n")

    def packet_callback(self, packet):
        packet_info = self.get_packet_info(packet)
        self.text_area.insert(tk.END, packet_info)
        self.text_area.see(tk.END)
        self.packets.append(packet)

    def get_packet_info(self, packet):
        info = []
        if IP in packet:
            info.append(f"Source IP: {packet[IP].src}")
            info.append(f"Destination IP: {packet[IP].dst}")
            info.append(f"Protocol: {packet[IP].proto}")
        if TCP in packet:
            info.append(f"Source Port: {packet[TCP].sport}")
            info.append(f"Destination Port: {packet[TCP].dport}")
            info.append(f"Flags: {packet[TCP].flags}")
        if UDP in packet:
            info.append(f"Source Port: {packet[UDP].sport}")
            info.append(f"Destination Port: {packet[UDP].dport}")
        if ARP in packet:
            info.append(f"ARP Source MAC: {packet[ARP].hwsrc}")
            info.append(f"ARP Destination MAC: {packet[ARP].hwdst}")
        if ICMP in packet:
            info.append(f"ICMP Type: {packet[ICMP].type}")
            info.append(f"ICMP Code: {packet[ICMP].code}")
        info.append("\n")
        return " | ".join(info) + "\n"

    def start_sniffing(self):
        self.is_sniffing = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.text_area.insert(tk.END, "Starting packet capture...\n")
        self.root.after(100, self.sniff_packets)

    def sniff_packets(self):
        if self.is_sniffing:
            sniff(filter=self.filter_expression, prn=self.packet_callback, count=10, timeout=1)
            self.root.after(100, self.sniff_packets)

    def stop_sniffing(self):
        self.is_sniffing = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.NORMAL)
        self.text_area.insert(tk.END, "Packet capture stopped.\n")

    def save_packets(self):
        file_path = 'captured_packets.pcap'
        wrpcap(file_path, self.packets)
        messagebox.showinfo("Save Packets", f"Packets saved to {file_path}")
        self.text_area.insert(tk.END, f"Packets saved to {file_path}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = PacketSnifferApp(root)
    root.mainloop()
