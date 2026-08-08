# Pirate King's Scheduler

A terminal-based CPU Scheduling Simulator developed in **Go**.

The project simulates how an operating system schedules processes waiting for CPU execution. Each process is represented as a pirate crew arriving at different times and competing for CPU execution.

---

## Features

The simulator supports three CPU scheduling algorithms:

- **First Come First Serve (FCFS)**
- **Shortest Job First (SJF) - Non-Preemptive**
- **Round Robin (RR)**

It provides:

- Process ID input
- Arrival Time input
- Burst Time input
- Time Quantum input for Round Robin
- Gantt Chart / execution timeline
- Completion Time
- Waiting Time
- Turnaround Time
- Average Waiting Time
- Average Turnaround Time
- Input validation
- Interactive terminal interface

---

## Technologies Used

- **Go (Golang)**
- Go standard library
- Visual Studio Code
- Ubuntu/Linux Terminal

---

## Project Structure

```text
pirate-kings-scheduler/
│
├── main.go
├── process.go
├── scheduler.go
├── utils.go
├── go.mod
└── README.md
```

### File Description

| File | Description |
|------|-------------|
| `main.go` | Handles the main menu, user input, validation, algorithm selection, and Round Robin time quantum |
| `process.go` | Defines the `Process` structure and scheduling-related attributes |
| `scheduler.go` | Contains FCFS, SJF Non-Preemptive, and Round Robin implementations |
| `utils.go` | Contains result-table and Gantt-chart utility functions |
| `go.mod` | Defines the Go module |
| `README.md` | Project documentation |

---

# Scheduling Algorithms

## 1. First Come First Serve (FCFS)

FCFS executes processes in the order in which they arrive.

### Approach

1. Sort processes according to Arrival Time.
2. Execute the first available process completely.
3. Calculate Completion Time.
4. Calculate Waiting Time.
5. Calculate Turnaround Time.
6. Repeat until all processes are completed.

### Characteristics

- Non-preemptive
- Simple to implement
- Uses FIFO ordering
- Can cause the **convoy effect**

### Time Complexity

`O(n log n)` due to sorting.

---

## 2. Shortest Job First (SJF) - Non-Preemptive

SJF selects the process with the shortest Burst Time among the processes that have already arrived.

### Approach

1. Check which processes have arrived.
2. Select the process with the smallest Burst Time.
3. Execute it completely.
4. Mark the process as completed.
5. Repeat until all processes finish.

### Characteristics

- Non-preemptive
- Generally provides lower average waiting time
- May cause starvation for long processes

### Time Complexity

`O(n²)` in the current implementation.

---

## 3. Round Robin (RR)

Round Robin gives each process a fixed amount of CPU time called the **Time Quantum**.

If a process does not finish within the quantum, it is placed at the end of the ready queue.

### Approach

1. Add arrived processes to the ready queue.
2. Select the process at the front of the queue.
3. Execute it for at most one Time Quantum.
4. If the process finishes, calculate its Completion Time.
5. If it does not finish, place it at the end of the queue.
6. Add newly arrived processes to the queue.
7. Continue until all processes finish.

### Characteristics

- Preemptive
- Uses a FIFO ready queue
- Provides better response time for interactive systems
- Performance depends on the Time Quantum

### Time Complexity

Approximately `O(n × k)`, where `k` depends on the number of time slices required.

---

# Scheduling Formulas

### Completion Time

The time at which a process finishes execution.

```text
CT = Time at which process finishes
```

### Turnaround Time

```text
Turnaround Time = Completion Time - Arrival Time
```

### Waiting Time

```text
Waiting Time = Turnaround Time - Burst Time
```

### Average Waiting Time

```text
Average Waiting Time =
Sum of Waiting Times / Number of Processes
```

### Average Turnaround Time

```text
Average Turnaround Time =
Sum of Turnaround Times / Number of Processes
```

---

# Example

Consider the following processes:

| Process | Arrival Time | Burst Time |
|---------|-------------:|-----------:|
| P1 | 0 | 5 |
| P2 | 1 | 3 |
| P3 | 2 | 2 |
| P4 | 4 | 4 |

For **Round Robin** with **Time Quantum = 2**:

```text
P1 → P2 → P3 → P1 → P4 → P2 → P1 → P4
```

### Gantt Chart

```text
| P1 | P2 | P3 | P1 | P4 | P2 | P1 | P4 |
0    2    4    6    8    10   11   12   14
```

### Results

| Process | Completion | Waiting | Turnaround |
|---------|-----------:|--------:|-----------:|
| P1 | 12 | 7 | 12 |
| P2 | 11 | 7 | 10 |
| P3 | 6 | 2 | 4 |
| P4 | 14 | 6 | 10 |

```text
Average Waiting Time    = 5.50
Average Turnaround Time = 9.00
```

---

# How to Run

## 1. Install Go

On Ubuntu:

```bash
sudo apt update
sudo apt install golang-go
```

Verify the installation:

```bash
go version
```

---

## 2. Navigate to the Project

```bash
cd pirate-kings-scheduler
```

---

## 3. Initialize the Go Module

If `go.mod` does not already exist:

```bash
go mod init pirate-kings-scheduler
```

If `go.mod` already exists, this step can be skipped.

---

## 4. Run the Simulator

```bash
go run .
```

---

# Sample Terminal Interface

```text
+==========================================+
|        PIRATE KING'S SCHEDULER           |
+==========================================+
|                                          |
|   1. First Come First Serve (FCFS)       |
|   2. Shortest Job First (SJF)            |
|   3. Round Robin (RR)                    |
|   4. Exit                                |
|                                          |
+==========================================+

Choose Algorithm:
```

---

# Input Validation

The simulator validates:

- Number of processes must be greater than `0`
- Arrival Time cannot be negative
- Burst Time must be greater than `0`
- Time Quantum must be greater than `0`
- Algorithm selection must be between `1` and `4`

---

# New Concepts Learned

## Go Programming

- Go packages
- Structs
- Slices
- Functions
- Loops
- Conditional statements
- User input using `fmt.Scan`
- Sorting using the `sort` package

## Operating Systems

- CPU Scheduling
- Process execution
- Arrival Time
- Burst Time
- Completion Time
- Waiting Time
- Turnaround Time
- Preemptive vs Non-Preemptive scheduling
- Time Quantum
- Ready Queue
- Gantt Charts

## Data Structures

- Arrays / Slices
- FIFO Queue
- Process tracking
- Simulation using queues

## Problem Solving

- Simulating CPU execution
- Handling processes arriving at different times
- Managing remaining execution time
- Calculating scheduling metrics
- Handling CPU idle periods
- Designing modular code

---

# Resources Used

The following resources were used to understand the concepts and implementation:

- Go official documentation
- Go `fmt` package documentation
- Go `sort` package documentation
- Operating Systems course material
- CPU Scheduling algorithm references
- Class notes and examples

---

# Future Improvements

Possible future improvements include:

- Priority Scheduling
- Preemptive SJF / Shortest Remaining Time First
- Multilevel Queue Scheduling
- Multilevel Feedback Queue
- Response Time calculation
- CPU utilization calculation
- Throughput calculation
- Colored terminal output
- Export results to CSV
- Interactive execution animation

---


**Language:** Go  
**Interface:** Terminal / CLI  
**Platform:** Linux / Ubuntu
