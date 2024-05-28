#! /bin/bash
#$SPARK_HOME/sbin/start-all.sh &
export KAFKA_HEAP_OPTS="-Xmx250M -Xms250M"
$KAFKA_HOME/bin/zookeeper-server-start.sh $KAFKA_HOME/config/zookeeper.properties &
$KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/server.properties
