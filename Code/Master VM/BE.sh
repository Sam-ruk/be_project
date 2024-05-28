#! /bin/bash
# BE Project Installer
# Samruddhi Khairnar

read -p "Enter your username (eg: admin, without slashes) :" X

sudo apt update
sudo apt install openjdk-11-jdk -y

# Spark, Kafka Installation 
gdown 14Wa_oblOmqBmdOyBmPD-nQE88KXH_2Su 
gdown 1QiavogIvI4_I-_9y_yY4tCfmjNjwB70x

# Start Processes :
gdown 1BZqMM63giHL7_Su2u9ll02an2Atw3XC5
# Stop Processes : 
gdown 1ZOq5tkUe6eHhQ_d4JDCLNS2Q2StcGKMH

sudo apt install tar -y
tar -xzvf spark.tar.gz
tar -xzvf kafka.tar.gz
   
sudo mkdir /app
sudo mkdir /app/zookeeper
sudo chmod 777 /app/zookeeper
sudo mkdir /app/kafka-logs
sudo mkdir /app/kafka-logs/logs
sudo chmod 777 /app/kafka-logs/logs

sudo echo "export JAVA_HOME="/usr/lib/jvm/java-11-openjdk-amd64/"
export SPARK_HOME=/home/"$X"/spark-3.4.0-bin-hadoop3/
export KAFKA_HOME=/home/"$X"/kafka_2.13-3.4.0/" >> .bashrc
source .bashrc

# Libraries
pip3 install pyspark confluent_kafka dash dash_bootstrap_components

# SSH setup
sudo apt install openssh-client openssh-server -y

echo "PubkeyAuthentication yes
PasswordAuthentication no
ChallengeResponseAuthentication no" | sudo tee --append /etc/ssh/sshd_config

sudo service ssh restart
ssh-keygen -t rsa
cp ~/.ssh/id_rsa.pub ~/.ssh/authorized_keys
chmod 700 ~/.ssh | chmod 644 ~/.ssh/id_rsa.pub | chmod 600 ~/.ssh/authorized_keys | chmod 600 ~/.ssh/id_rsa | chmod 755 ~
ssh localhost
