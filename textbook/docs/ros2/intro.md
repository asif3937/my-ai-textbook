---
sidebar_label: Introduction to ROS 2
---

# Introduction to ROS 2

Robot Operating System 2 (ROS 2) is the next-generation robotics middleware that provides libraries and tools to help software developers create robot applications. Unlike the original ROS, ROS 2 is designed for production environments and addresses many of the limitations of the original system.

## What is ROS 2?

ROS 2 is not an actual operating system but rather a middleware framework that provides:
- Message passing between processes
- Hardware abstraction
- Device drivers
- Libraries for implementing common robot functionality
- Tools for testing, building, and managing code

## Key Improvements Over ROS 1

### Real-time Support
- Deterministic behavior for time-critical applications
- Real-time scheduling capabilities
- Predictable performance characteristics

### Security
- Built-in authentication and encryption
- Secure communication channels
- Role-based access control

### Scalability
- Support for multi-robot systems
- Distributed computing capabilities
- Cloud robotics integration

### Production Readiness
- Lifecycle management
- Deterministic build system
- Quality of service policies

## Architecture

### DDS (Data Distribution Service)
ROS 2 uses DDS as its underlying communication middleware:
- Provides publish/subscribe communication
- Supports real-time systems
- Offers multiple implementations (Fast DDS, Cyclone DDS, RTI Connext)

### Nodes and Processes
- Each node runs as a separate process
- Nodes can run on different machines
- Process isolation for fault tolerance

### Packages and Workspaces
- Modular code organization
- Dependency management
- Build system integration

## Core Concepts

### Nodes
- Processes that perform computation
- Communicate with other nodes through topics, services, and actions
- Can be written in multiple languages (C++, Python, etc.)

### Topics
- Publish/subscribe communication pattern
- Asynchronous message passing
- Multiple publishers and subscribers possible

### Services
- Request/response communication pattern
- Synchronous interaction
- Request and response message types

### Actions
- Goal-oriented communication
- Long-running tasks with feedback
- Cancel and status capabilities

## Installation and Setup

ROS 2 supports multiple platforms:
- Ubuntu Linux (primary platform)
- Windows
- macOS
- Real-time systems

The latest distribution is Rolling Ridley, with LTS versions like Humble Hawksbill providing long-term support.