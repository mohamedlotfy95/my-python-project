
## Understanding the Issue

You're experiencing a common scenario where:
- Kafka's **log retention** is set to 7 days (messages purged from topics)
- **PVC storage** isn't reclaimed because Kafka's log segments remain on disk
- Old log segments consume storage even after data expiration

## Kafka Retention Mechanics

Kafka doesn't immediately delete data when retention time passes. Instead:
1. Messages are written to log segments
2. When a segment is "closed," Kafka checks if it's older than retention period
3. Entire segments are deleted (not individual messages)
4. If a segment has even one message within retention, the whole segment stays

## Best Practices for Strimzi Kafka

### 1. **Configure Log Retention Policies**

Set these at the broker or topic level in your Kafka custom resource:

```yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: my-cluster
spec:
  kafka:
    config:
      # Time-based retention (7 days)
      log.retention.hours: 168
      
      # Size-based retention (per partition)
      log.retention.bytes: 1073741824  # 1GB per partition
      
      # Segment size (smaller = more frequent cleanup)
      log.segment.bytes: 536870912  # 512MB
      
      # Cleanup check interval
      log.retention.check.interval.ms: 300000  # 5 minutes
      
      # Cleanup policy
      log.cleanup.policy: delete
      
      # Minimum cleanable ratio for compacted topics
      min.cleanable.dirty.ratio: 0.5
```

### 2. **Topic-Level Configuration**

For specific topics with different retention needs:

```yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
  name: my-topic
  labels:
    strimzi.io/cluster: my-cluster
spec:
  partitions: 3
  replicas: 2
  config:
    retention.ms: 604800000  # 7 days in milliseconds
    retention.bytes: 2147483648  # 2GB per partition
    segment.bytes: 268435456  # 256MB
    segment.ms: 86400000  # Roll segment every 24 hours
    delete.retention.ms: 86400000  # 1 day for tombstones
```

### 3. **Storage Configuration**

Ensure proper PVC sizing and monitoring:

```yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: my-cluster
spec:
  kafka:
    replicas: 3
    storage:
      type: jbod
      volumes:
      - id: 0
        type: persistent-claim
        size: 100Gi
        class: fast-ssd
        deleteClaim: false  # Keep PVCs on cluster deletion
    # Resource limits
    resources:
      requests:
        memory: 4Gi
        cpu: 1000m
      limits:
        memory: 4Gi
        cpu: 2000m
```

### 4. **Log Compaction (Alternative Strategy)**

For event sourcing or changelog topics:

```yaml
spec:
  config:
    log.cleanup.policy: compact
    min.compaction.lag.ms: 60000
    max.compaction.lag.ms: 86400000
    segment.ms: 3600000
```

## Implementation Steps

### Step 1: Audit Current Configuration

```bash
# Check current broker config
kubectl exec my-cluster-kafka-0 -n kafka -- bin/kafka-configs.sh \
  --bootstrap-server localhost:9092 \
  --entity-type brokers \
  --entity-default \
  --describe

# Check topic configurations
kubectl exec my-cluster-kafka-0 -n kafka -- bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --describe
```

### Step 2: Update Kafka Resource

```bash
kubectl edit kafka my-cluster -n kafka
```

Add the retention configurations shown above.

### Step 3: Monitor Disk Usage

Create a monitoring setup:

```yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: my-cluster
spec:
  kafka:
    metricsConfig:
      type: jmxPrometheusExporter
      valueFrom:
        configMapKeyRef:
          name: kafka-metrics
          key: kafka-metrics-config.yml
```

### Step 4: Set Up Alerts

Monitor these metrics:
- `kafka_log_log_size` - Total log size per topic/partition
- `kafka_server_brokertopicmetrics_bytesout_total` - Outbound throughput
- Disk usage on PVCs

## Recommended Settings Matrix

| Use Case | Retention Time | Segment Size | Segment Time |
|----------|---------------|--------------|--------------|
| **High-throughput logs** | 7 days | 512MB | 1 hour |
| **Event sourcing** | 30+ days | 256MB | 6 hours |
| **Metrics/monitoring** | 3 days | 128MB | 30 minutes |
| **Transactional data** | Compaction | 256MB | 12 hours |

## Troubleshooting Commands

```bash
# Force log cleanup (careful in production)
kubectl exec my-cluster-kafka-0 -n kafka -- bin/kafka-configs.sh \
  --bootstrap-server localhost:9092 \
  --entity-type topics \
  --entity-name my-topic \
  --alter \
  --add-config segment.ms=60000

# Check log directories
kubectl exec my-cluster-kafka-0 -n kafka -- du -sh /var/lib/kafka/data/kafka-log*

# View segment details
kubectl exec my-cluster-kafka-0 -n kafka -- ls -lh /var/lib/kafka/data/kafka-log0/
```

## Key Takeaways

1. **Smaller segments** = more frequent cleanup opportunities
2. **Set both time AND size limits** for better control
3. **Monitor disk usage** proactively
4. **Use compaction** for stateful/changelog topics
5. **Plan PVC size** for 2-3x your retention needs (accounting for replication)

