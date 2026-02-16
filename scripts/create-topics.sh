#!/bin/bash
# Create Kafka topics in Redpanda
# Usage: ./scripts/create-topics.sh [broker_address]

BROKER=${1:-"localhost:19092"}

echo "Creating Kafka topics on broker: $BROKER"

rpk topic create task-events \
  --brokers "$BROKER" \
  --partitions 3 \
  --replicas 1

rpk topic create reminders \
  --brokers "$BROKER" \
  --partitions 3 \
  --replicas 1

rpk topic create task-updates \
  --brokers "$BROKER" \
  --partitions 3 \
  --replicas 1

echo ""
echo "Listing topics:"
rpk topic list --brokers "$BROKER"
