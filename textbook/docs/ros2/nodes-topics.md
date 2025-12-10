---
sidebar_label: ROS 2 Nodes and Topics
---

# ROS 2 Nodes and Topics

This chapter delves deeper into the fundamental communication mechanisms in ROS 2: nodes and topics, which form the backbone of the publish/subscribe communication pattern.

## Nodes in Depth

### Node Lifecycle
ROS 2 nodes follow a specific lifecycle that provides better control over their state:

#### States
- **Unconfigured**: Initial state after creation
- **Inactive**: Configured but not active
- **Active**: Running and processing callbacks
- **Finalized**: Node is being destroyed

#### Transition Callbacks
You can define callbacks for state transitions:
- `on_configure()`: Called when moving from unconfigured to inactive
- `on_activate()`: Called when moving from inactive to active
- `on_deactivate()`: Called when moving from active to inactive
- `on_cleanup()`: Called when moving from inactive to unconfigured
- `on_shutdown()`: Called when shutting down the node
- `on_error()`: Called when an error occurs

### Node Parameters
Nodes can be configured with parameters:

```python
# Declare a parameter with default value
self.declare_parameter('param_name', 'default_value')

# Get parameter value
param_value = self.get_parameter('param_name').value
```

### Quality of Service (QoS)
QoS settings control how messages are delivered:

#### Reliability
- `Reliable`: All messages are delivered (if possible)
- `BestEffort`: Messages may be dropped

#### Durability
- `Volatile`: Only new messages are received
- `TransientLocal`: Past messages are available to new subscribers

#### History
- `KeepLast`: Store a specific number of messages
- `KeepAll`: Store all messages (use with caution)

## Topics and Publishers/Subscribers

### Advanced Topic Usage

#### Creating Publishers
```python
# With default QoS
publisher = self.create_publisher(String, 'topic_name', 10)

# With custom QoS
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
qos_profile = QoSProfile(
    reliability=ReliabilityPolicy.RELIABLE,
    history=HistoryPolicy.KEEP_LAST,
    depth=10
)
publisher = self.create_publisher(String, 'topic_name', qos_profile)
```

#### Creating Subscribers
```python
# With default QoS
subscription = self.create_subscription(
    String,
    'topic_name',
    self.listener_callback,
    10
)

# With custom QoS
subscription = self.create_subscription(
    String,
    'topic_name',
    self.listener_callback,
    qos_profile
)
```

### Message Types
ROS 2 supports various built-in message types:
- **std_msgs**: Basic data types (String, Int32, Float64, etc.)
- **geometry_msgs**: Geometric primitives (Point, Pose, Twist, etc.)
- **sensor_msgs**: Sensor data (LaserScan, Image, JointState, etc.)
- **nav_msgs**: Navigation messages (Odometry, Path, OccupancyGrid, etc.)

### Custom Messages
You can create custom message types:
1. Define the message in a `.msg` file
2. Add message dependencies to `package.xml`
3. Update `CMakeLists.txt` to build the messages
4. Use the generated message type in your code

## Topic Management

### Topic Information
Use command-line tools to inspect topics:
```bash
# List all topics
ros2 topic list

# Get information about a specific topic
ros2 topic info /topic_name

# Echo messages on a topic
ros2 topic echo /topic_name std_msgs/msg/String

# Publish a message to a topic
ros2 topic pub /topic_name std_msgs/msg/String "data: 'Hello'"
```

### Topic Monitoring
Monitor topic performance:
```bash
# Monitor topic rate
ros2 topic hz /topic_name

# Monitor topic delay
ros2 topic delay /topic_name
```

## Advanced Communication Patterns

### Publisher-Subscriber Best Practices

#### Publisher Guidelines
- Choose appropriate queue size based on message rate
- Use appropriate QoS settings for your use case
- Consider message size and frequency for bandwidth usage
- Implement proper error handling

#### Subscriber Guidelines
- Process messages efficiently to avoid queue overflow
- Use appropriate QoS settings that match publishers
- Consider using callback groups for complex nodes
- Handle message timestamps appropriately

### Threading and Callbacks
ROS 2 provides different executors for handling callbacks:

#### Single-threaded Executor
```python
executor = SingleThreadedExecutor()
executor.add_node(node)
executor.spin()
```

#### Multi-threaded Executor
```python
executor = MultiThreadedExecutor(num_threads=4)
executor.add_node(node)
executor.spin()
```

### Callback Groups
Organize callbacks into groups for better control:
```python
# Create a callback group
callback_group = MutuallyExclusiveCallbackGroup()

# Assign subscriptions to groups
subscription = self.create_subscription(
    String,
    'topic_name',
    self.callback1,
    10,
    callback_group=callback_group
)
```

## Performance Considerations

### Message Optimization
- Use appropriate data types (avoid unnecessary precision)
- Consider message compression for large data
- Use efficient serialization methods
- Minimize message copying

### Topic Design
- Use descriptive topic names
- Follow naming conventions
- Consider message frequency vs. necessity
- Design for loose coupling between nodes

### Memory Management
- Monitor queue sizes to prevent memory issues
- Use appropriate QoS settings for memory usage
- Consider message lifecycle and cleanup
- Profile memory usage in long-running systems

## Troubleshooting Common Issues

### Topic Connection Problems
- Verify topic names match exactly
- Check that nodes are on the same ROS domain
- Ensure QoS profiles are compatible
- Confirm nodes are running and properly initialized

### Message Loss
- Increase queue size for high-frequency topics
- Use appropriate reliability settings
- Check network performance for distributed systems
- Consider message priority and timing requirements

### Performance Issues
- Profile message rates and processing times
- Optimize callback execution time
- Use appropriate threading models
- Consider using intra-process communication for same-process nodes