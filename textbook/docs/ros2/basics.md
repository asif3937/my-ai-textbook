---
sidebar_label: ROS 2 Basics
---

# ROS 2 Basics

This chapter covers the fundamental concepts and practical aspects of working with ROS 2.

## Setting Up Your Development Environment

### Installation
To install ROS 2, you typically need:
- A supported operating system (Ubuntu, Windows, etc.)
- Proper system dependencies
- The ROS 2 distribution for your platform

### Workspace Structure
ROS 2 follows a standard workspace structure:
```
workspace_folder/
├── src/
│   ├── package_1/
│   ├── package_2/
│   └── ...
├── build/
├── install/
└── log/
```

## Creating Your First Package

### Package Structure
A basic ROS 2 package includes:
- `package.xml`: Package metadata
- `CMakeLists.txt`: Build configuration (for C++)
- `setup.py`: Build configuration (for Python)
- Source code in appropriate directories

### Creating a Package
Use the `ros2 pkg create` command to create a new package with proper structure.

## Nodes and Lifecycle

### Creating Nodes
Nodes are the basic computational units in ROS 2:

**In Python:**
```python
import rclpy
from rclpy.node import Node

class MyNode(Node):
    def __init__(self):
        super().__init__('my_node')
        # Node initialization code
```

**In C++:**
```cpp
#include "rclcpp/rclcpp.hpp"

class MyNode : public rclcpp::Node
{
public:
    MyNode() : Node("my_node") {
        // Node initialization code
    }
};
```

### Node Execution
Nodes must be properly initialized and spun to process messages:
```python
def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
```

## Communication Patterns

### Topics (Publish/Subscribe)
Topics enable asynchronous communication:

**Publisher:**
```python
publisher = self.create_publisher(String, 'topic_name', 10)
msg = String()
msg.data = 'Hello World'
publisher.publish(msg)
```

**Subscriber:**
```python
subscription = self.create_subscription(
    String,
    'topic_name',
    self.listener_callback,
    10)
```

### Services (Request/Response)
Services enable synchronous communication:

**Service Server:**
```python
self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.add_two_ints_callback)
```

**Service Client:**
```python
client = self.create_client(AddTwoInts, 'add_two_ints')
```

### Actions (Goal-Oriented)
Actions handle long-running tasks with feedback:

**Action Server:**
```python
self._action_server = ActionServer(
    self,
    Fibonacci,
    'fibonacci',
    self.execute_callback)
```

## Building and Running

### Building Packages
Use `colcon build` to build packages in your workspace:
```bash
colcon build --packages-select my_package
```

### Sourcing the Environment
After building, source the setup files:
```bash
source install/setup.bash
```

### Running Nodes
Use `ros2 run` to execute nodes:
```bash
ros2 run my_package my_node
```

### Launch Files
Launch files allow you to start multiple nodes at once:
```xml
<launch>
    <node pkg="my_package" exec="my_node" name="my_node_instance" />
</launch>
```

## Debugging and Tools

### Command Line Tools
ROS 2 provides various command-line tools:
- `ros2 topic`: Topic inspection and publishing
- `ros2 service`: Service inspection and calling
- `ros2 node`: Node information
- `ros2 param`: Parameter management
- `ros2 action`: Action inspection and sending goals

### Visualization
- RViz2: 3D visualization tool
- rqt: Graphical user interface framework
- PlotJuggler: Data plotting tool

## Best Practices

### Package Design
- Keep packages focused on specific functionality
- Use descriptive names
- Follow naming conventions
- Document your packages properly

### Code Structure
- Separate concerns into different classes/nodes
- Use composition over inheritance when appropriate
- Follow ROS 2 style guides
- Write unit tests

### Performance
- Consider QoS settings appropriately
- Use appropriate message types
- Optimize for your specific use case
- Profile your applications