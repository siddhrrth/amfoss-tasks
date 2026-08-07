# Pirate King's Scheduler

## Overview

Pirate King's Scheduler is a terminal-based CPU Scheduling Simulator written in Go.

Every pirate crew represents a CPU process. The simulator executes them using different CPU Scheduling Algorithms while displaying execution order, waiting time, turnaround time, and averages.

---

## Algorithms Implemented

- First Come First Serve (FCFS)
- Shortest Job First (Non-Preemptive)
- Round Robin

---

## Features

- Interactive terminal interface
- User-defined process details
- Gantt Chart visualization
- Waiting Time calculation
- Turnaround Time calculation
- Average Waiting Time
- Average Turnaround Time

---

## Process Input

Each process requires:

- Process ID
- Arrival Time
- Burst Time

Round Robin additionally requires:

- Time Quantum

---

## Example

Menu

1. FCFS
2. SJF
3. Round Robin

Example Output

| P1 | P2 | P3 |

0    5    8    10

---

## Project Structure

```
main.go
scheduler.go
process.go
utils.go
README.md
```

---

## Scheduling Formulas

Turnaround Time

```
TAT = Completion Time - Arrival Time
```

Waiting Time

```
WT = Turnaround Time - Burst Time
```

Average Waiting Time

```
Sum(WT) / Number of Processes
```

Average Turnaround Time

```
Sum(TAT) / Number of Processes
```

---

## Concepts Learned

- CPU Scheduling Algorithms
- Process Simulation
- Queue implementation
- Sorting in Go
- Structs
- Slices
- Terminal-based visualization
- Time complexity analysis

---

## Resources Used

- Go Documentation
- Operating Systems CPU Scheduling Concepts
- Go slices and sort package
- Queue implementation using slices

---

## Future Improvements

- Priority Scheduling
- Preemptive SJF
- Multi-Level Queue Scheduling
- Colored terminal output
- CSV export
- Live animation of Gantt Chart
