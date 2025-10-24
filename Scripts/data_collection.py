from scapy.all import sniff, wrpcap
import logging
import os
import datetime

def capture_traffic(interface, duration=30, output_folder="Data", filename_format="{timestamp}_captured_traffic.pcap", log_level=logging.INFO):
    logging.basicConfig(level=log_level, filename="packet_capture.log", format='%(asctime)s - %(levelname)s: %(message)s')

    try:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
    except OSError as e:
        logging.error(f"Error creating output folder: {e}")
        print(f"Error creating output folder: {e}")
        return

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_path = os.path.join(output_folder, filename_format.format(timestamp=timestamp))

    start_time = datetime.datetime.now()

    logging.info(f"Capturing traffic on interface: {interface} and saving to {output_path}")
    print(f"Capturing traffic on interface: {interface} and saving to {output_path}")

    try:
        captured_packets = sniff(iface=interface, timeout=duration)
        wrpcap(output_path, captured_packets)

        captured_duration = (datetime.datetime.now() - start_time).total_seconds()

        logging.info("Capture completed successfully.")
        print("Capture completed successfully.")
    except KeyboardInterrupt:
        logging.info("Capture interrupted by user.")
        print("Capture interrupted by user.")
        return
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")
        return
    finally:
        captured_duration = (datetime.datetime.now() - start_time).total_seconds()
        logging.info(f"Total capture duration: {captured_duration:.2f} seconds")
        print(f"Total capture duration: {captured_duration:.2f} seconds")

interface = "wlan0"
duration = 30
output_folder = "Data"
filename_format = "{timestamp}_captured_traffic.pcap"
log_level = logging.DEBUG

capture_traffic(interface, duration, output_folder, filename_format, log_level)