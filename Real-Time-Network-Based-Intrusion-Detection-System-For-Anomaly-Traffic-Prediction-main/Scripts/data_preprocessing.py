from scapy.all import rdpcap, IP, TCP
import pandas as pd
import logging

def extract_packet_info(packet):
    return {
        'timestamp': packet.time,
        'src_ip': packet[IP].src,
        'dst_ip': packet[IP].dst,
        'src_port': packet[TCP].sport,
        'dst_port': packet[TCP].dport,
        'length': packet[IP].len,
        'flags': packet[TCP].flags
    }

def clean_data(pcap_file):
    logging.basicConfig(filename='data_preprocessing.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
    try:
        packets = rdpcap(pcap_file)
        logging.info("Successfully read packets from PCAP file.")
    except Exception as e:
        logging.error(f"Error reading PCAP file: {e}")
        return None
    cleaned_packet_info = []
    for packet in packets:
        if not all([packet.haslayer(IP), packet.haslayer(TCP)]):
            continue
        if packet[IP].len > 1500:
            continue
        packet_info = extract_packet_info(packet)
        cleaned_packet_info.append(packet_info)
    try:
        cleaned_data = pd.DataFrame(cleaned_packet_info)
        logging.info("Successfully converted data to DataFrame.")
    except Exception as e:
        logging.error(f"Error converting data to DataFrame: {e}")
        return None
    return cleaned_data

def save_cleaned_data(cleaned_data, output_file):
    try:
        cleaned_data.to_csv(output_file, index=False)
        logging.info(f"Successfully saved cleaned data to {output_file}.")
        return True
    except Exception as e:
        logging.error(f"Error saving cleaned data: {e}")
        return False

pcap_file = "Data/2024-07-06_07-14-28_captured_traffic.pcap"
cleaned_data = clean_data(pcap_file)
if cleaned_data is not None:
    print(f"Data shape after cleaning: {cleaned_data.shape}")
    print(f"Data columns: {cleaned_data.columns.tolist()}")
    print("Data cleaning complete!")
    logging.info("Data cleaning complete.")
    output_file = "Data/cleaned_new_data.csv"
    if save_cleaned_data(cleaned_data, output_file):
        print(f"Cleaned data saved to {output_file}.")
    else:
        print("Failed to save cleaned data.")
else:
    print("Data cleaning failed.")
    logging.error("Data cleaning failed.")
