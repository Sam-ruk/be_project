# Hybrid DC Micro-grid using Machine Learning for Load Demand Forecasting

## Introduction
This project aims to build a Hybrid DC Micro-grid using machine learning techniques for load demand forecasting. The micro-grid system combines renewable energy sources (such as solar panels) with battery storage and traditional grid power. Machine learning models are used to predict load demand, optimize energy usage, and enhance overall efficiency. 🌞🔋💡

## Technology Stack
- **Python3**: A versatile programming language. 🐍
- **JupyterLab** and **Colab**: For data exploration, analysis, and model development. 📊
- **Dash**: A Python framework for building interactive web applications. 🚀
- **Tensorflow**: Used for deep learning-based model training. 🧠
- **Apache Kafka**: Simulated pub-sub producer-consumer communication for real-time data points. 🔄

## Installation (VM 1: Master Node)
1. Set up an Ubuntu-based virtual machine on AWS EC2 with 1 GB RAM.
2. Download the Kafka installer.
3. Install necessary Python libraries:
4. Configure Kafka properties (IP addresses) in `server.properties`.
5. Start Kafka processes using `kafka_start_1G.sh`.

## Dashboard and Kafka Consumer
1. Copy the contents of the Master VM folder (containing code for the Dashboard and Kafka Consumer) to the VM.
2. Run the Dashboard and Kafka Consumer code in separate terminals.

## Installation (VM 2: Inference Node)
1. Set up another Ubuntu-based VM on AWS EC2 with 2 GB RAM.
2. Copy the contents of the Inference VM folder (containing code for prediction models) to this VM.
3. Install necessary libraries:
4. Run the Flask server code.

## Installation (Raspberry Pi)
1. Set up a Raspberry Pi 3 B with Wi-Fi connectivity.
2. Copy the contents of the Rpi folder (including Kafka Producer, Switching Algorithm, and Fan Speed Control code) to the Pi.
3. Adjust IP addresses in the Kafka Producer and Switching Algorithm code.
4. Install required libraries:
5. Run the Kafka Producer, Switching Algorithm, and Fan Speed Control code.

## View the Dashboard
Access the Dashboard via a browser using the public IP of the Master Node and port 8050. 🖥️

## Project Report
- Includes details about the hybrid micro-grid, machine learning techniques, and implementation steps.
- Acknowledges the contributions of team members. 👏

---

**Project Team:**
- Sakshi Jadhav
- Samruddhi Khairnar
- Kunika Narnaware
- Pranjal Shewale