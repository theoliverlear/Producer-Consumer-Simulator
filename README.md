# Producer Consumer Simulator 📟
Welcome to Producer Consumer Simulator! This repository serves as a tool to explore and learn critical operating systems concepts like producer-consumer balancing, buffer utilization, and concurrency. Designed with Python, this simulator is both intuitive and powerful, offering features to manipulate configurations, analyze performance, and refine your understanding of system behavior. 🌟

## CIDS 429 - Operating Systems
### Final Project
#### By Oliver Sigwarth, Anthany Toum, Kollin Weikel, and Milton Massaquoi

---

## 📖 Overview 
The Producer Consumer Simulator is an educational tool crafted to provide hands-on experience with essential operating systems concepts. From efficiency metrics to real-time execution tracing and intelligent configuration suggestions, this Python-based project has everything you need to learn and experiment with producer-consumer dynamics in a controlled environment.

## 🛠️ Key Features
- Command-Line Configuration: Easily set up your simulation with arguments like buffer size, number of producers/consumers, and processing speeds.
Example: python pc-simulator.py -b 100 -p 2 -c 3 -ps 1:5 -cs 2:4 -v
- Efficiency Calculator: Measure and rank your configuration's throughput to identify bottlenecks and optimize performance.
- Execution Tracing: Trace producer and consumer activities with detailed logs showing idle times, buffer utilization, and bottlenecks.
- Verbose Mode: Enable detailed output for an in-depth look at your simulation's behavior.
- Smart Suggestions: Receive configuration suggestions to balance producer and consumer workloads and enhance performance.
- Unit Testing: Ensures accuracy and reliability of the simulator’s operations.
  
## ⚙️ Installation
1. Clone Repository:
   git clone https://github.com/theoliverlear/Producer-Consumer-Simulator.git
2. Change Directory:
   cd producer-consumer-simulator 

## 📋 Usage
### Running the Simulator 
1. Configure the simulation via command line. For example:
   python pc-simulator.py -b 100 -p 2 -c 3 -ps 1:5 -cs 2:4 -v
2. View real-rime logging, effiency metrics, and suggestions directly in terminal.

## 🔍 Features in Detail
### Efficiency Calculator 
- Provides throughput metrics: Throughput = Total Items/Total Time Taken
- Ranks your configuration's performance using percentiles.

### Execution Tracing 
- Tracks thread activity: idle states, buffer utilization, and bottlenecks.
- Provides insights into thread scheduling and queue saturation.

### Configuration Suggestions
- Suggests improvements based on the buffer size, thread count, and speed mismatches.

### Unit Testing 
- Guarantees program reliability through comprehensive test cases.

## 🧰 Development
### Dependencies 
- Python
- Logging for detailed execution tracing
- Unit testing framework (ex: unittest)

## 🌟 Contributions
We welcome contributions! Follow these steps:
1. Fork the repository.
2. Create a new branch.
3. Make your changes and commit them.
4. Push to your fork.
5. Submit a pull request.

## 🙌 Acknowledgments
Thank you for using the Producer Consumer Simulator! We hope it enhances your learning experience and provides valuable insights into operating systems concepts. 🚀✨

