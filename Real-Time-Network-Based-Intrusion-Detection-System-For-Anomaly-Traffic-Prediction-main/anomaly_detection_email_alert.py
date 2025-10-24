import pandas as pd
import plotly.express as px
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import logging
import configparser
import os


logging.basicConfig(filename='anomaly_detection.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')


config = configparser.ConfigParser()
config.read('config.ini')

def send_email_alert(anomalies_file, visualization_file, readme_file):
    try:

        from_email = config['EMAIL']['From']
        from_password = config['EMAIL']['Password']
        to_email = config['EMAIL']['To']
        subject = "Network Anomaly Alert"

        # TO create the email content
        body = """Hello Network Administrator,

Anomalies have been detected in the network traffic. Please find attached the following files for details:

1. Anomalies Data: A CSV file containing the details of the detected anomalies.
2. Visualization: An HTML file providing an interactive visual representation of the anomalies.
3. README: A text file explaining the anomalies and the visualization.

Kindly review the attached files and take the necessary actions.

Best regards,
Network Security Team
"""

        # Email setup
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Attach files
        attach_file_to_email(msg, anomalies_file)
        attach_file_to_email(msg, visualization_file)
        attach_file_to_email(msg, readme_file)

        # Send the email
        server = smtplib.SMTP_SSL(config['EMAIL']['SMTP_Server'], config['EMAIL']['SMTP_Port'])
        server.login(from_email, from_password)
        server.send_message(msg)
        server.quit()
        log_and_print("Email alert sent successfully.")
    except Exception as e:
        log_and_print(f"Failed to send email alert: {e}", level="error")

def attach_file_to_email(msg, filename):
    try:
        with open(filename, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(filename)}")
            msg.attach(part)
    except Exception as e:
        log_and_print(f"Failed to attach file {filename}: {e}", level="error")

def create_interactive_visualization(anomalies):
    try:
        fig = px.scatter(anomalies, x=anomalies.index, y='length', color='src_ip_bytes', size='dst_ip_bytes',
                         title='Anomalies in Network Traffic',
                         labels={'index': 'Index', 'length': 'Packet Length', 'src_ip_bytes': 'Source IP Bytes', 'dst_ip_bytes': 'Destination IP Bytes'})

        visualization_file = 'Data/anomaly_visualization.html'
        fig.write_html(visualization_file)
        log_and_print("Interactive visualization created successfully.")
        return visualization_file
    except Exception as e:
        log_and_print(f"Failed to create interactive visualization: {e}", level="error")

def create_readme(anomalies_file, visualization_file):
    try:
        readme_content = f"""
Network Anomaly Detection Report
================================

Anomalies have been detected in the network traffic. This report contains the following files:

1. {anomalies_file}: This CSV file contains the details of the detected anomalies. Each row represents an anomaly with various network packet features.

2. {visualization_file}: This HTML file provides an interactive visual representation of the anomalies. The scatter plot shows packet lengths, with colors representing source IP bytes and sizes representing destination IP bytes.

Explanation of the Visualization:
---------------------------------
- The x-axis represents the index of the data points.
- The y-axis represents the packet length.
- The color gradient represents the source IP bytes, with darker colors indicating higher values.
- The size of the points represents the destination IP bytes, with larger points indicating higher values.
- You can hover over the points to see more details about each anomaly.

Please review the attached files and take the necessary actions.

Best regards,
Network Security Team
"""
        readme_file = 'Data/README.txt'
        with open(readme_file, 'w') as file:
            file.write(readme_content)
        log_and_print("README file created successfully.")
        return readme_file
    except Exception as e:
        log_and_print(f"Failed to create README file: {e}", level="error")

def handle_anomalies():
    try:
       
        predicted_data = pd.read_csv('Data/predicted_data_with_anomalies.csv')

        # Filter the anomalies
        anomalies = predicted_data[predicted_data['predicted_anomaly'] == -1]

        if not anomalies.empty:
            anomalies_file = 'Data/detected_anomalies.csv'
            # Save the anomalies to a CSV file
            anomalies.to_csv(anomalies_file, index=False)

            # Create interactive visualization
            visualization_file = create_interactive_visualization(anomalies)

            # Create README file
            readme_file = create_readme(anomalies_file, visualization_file)

            # Send an email alert with the anomalies, visualization, and README
            send_email_alert(anomalies_file, visualization_file, readme_file)
        else:
            log_and_print("No anomalies detected.")
    except Exception as e:
        log_and_print(f"Failed to handle anomalies: {e}", level="error")

def log_and_print(message, level="info"):
    if level == "info":
        logging.info(message)
        print(message)
    elif level == "error":
        logging.error(message)
        print(message)

if __name__ == "__main__":
    handle_anomalies()
