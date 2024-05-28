# Hybrid DC Micro-grid using Machine Learning for Load Demand Forecasting

## Introduction
This project is aimed at building a Hybrid DC Micro-grid using Machine Learning for load demand forecasting. The micro-grid system combines renewable energy sources (such as solar panels) with battery storage and traditional grid power. Machine learning models are used to predict load demand, optimize energy usage, and enhance overall efficiency. 🌞🔋💡

## Technology Stack
- **Python3**: A versatile programming language. 🐍
- **JupyterLab** and **Colab**: For data exploration, analysis, and model development. 📊
- **Dash**: A Python framework for building interactive web applications. 🚀
- **Tensorflow**: Used for deep learning-based model training. 🧠
- **Apache Kafka**: Simulated pub-sub producer-consumer communication for real-time data points. 🔄

## Installation Instructions
1. **Master Node Setup (VM 1):**
   - Set up an Ubuntu-based virtual machine on AWS EC2, having 1 GB RAM.
   - Download the Kafka installer.
   - Run the installer script `BE.sh`.
   - Configure Kafka properties in `server.properties` with the public IP of the VM.
   - Start Kafka processes using `kafka_start_1G.sh`.
   - Install necessary Python libraries:
     ```bash
     pip3 install confluent_kafka dash plotly dash_bootstrap_components
     ```
   - Copy the contents of the Master VM folder (containing code for the Dashboard and Kafka Consumer) to the VM.
   - Run the Dashboard and Kafka Consumer code in separate terminals.

2. **Inference Node Setup (VM 2):**
   - Set up another Ubuntu-based VM on AWS EC2, having 2 GB RAM.
   - Copy the contents of the Inference VM folder (containing code for prediction models) to this VM.
   - Install necessary libraries:
     ```bash
     pip3 install flask h5py numpy tensorflow
     ```
   - Run the Flask server code.

3. **Raspberry Pi Setup:**
   - Setup a Raspberry Pi 3 B with Wi-Fi connection.
   - Copy the contents of the Rpi folder (including Kafka Producer, Switching Algorithm, and Fan Speed Control code) to the Pi.
   - Adjust IP addresses in the Kafka Producer and Switching Algorithm code.
   - Install required libraries:
     ```bash
     pip3 install RPi.GPIO numpy requests confluent_kafka adafruit-circuitpython-ads1x15 Adafruit_DHT
     sudo apt-get install -y python3-smbus
     ```
   - Run the Kafka Producer, Switching Algorithm, and Fan Speed Control code.

## Viewing the Dashboard
Access the Dashboard via a browser using the public IP of the Master Node and port 8050. 🖥️

## Project Report
For detailed information about the hybrid micro-grid, machine learning techniques, and implementation steps, refer to the project report submitted to the university.

---

**Project Team:**
- Sakshi Jadhav
- Samruddhi Khairnar
- Kunika Narnaware
- Pranjal Shewale
