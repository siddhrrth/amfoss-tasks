package main

import (
	"fmt"
	"sort"
)

func fcfs(processes []Process) {

	// Sort processes by Arrival Time
	sort.Slice(processes, func(i, j int) bool {
		return processes[i].ArrivalTime < processes[j].ArrivalTime
	})

	currentTime := 0

	var order []string
	var timeline []int

	fmt.Println("\n========== FCFS SCHEDULING ==========")

	for i := range processes {

		// If CPU is idle, move time forward
		if currentTime < processes[i].ArrivalTime {
			currentTime = processes[i].ArrivalTime
		}

		// Calculate Waiting Time
		processes[i].WaitingTime =
			currentTime - processes[i].ArrivalTime

		// Record starting time BEFORE execution
		order = append(order, processes[i].PID)
		timeline = append(timeline, currentTime)

		// Execute process
		currentTime += processes[i].BurstTime

		// Completion Time
		processes[i].CompletionTime = currentTime

		// Turnaround Time
		processes[i].TurnaroundTime =
			processes[i].CompletionTime -
				processes[i].ArrivalTime
	}

	// Record final ending time
	timeline = append(timeline, currentTime)

	printGanttChart(order, timeline)

	printResults(processes)
}

func sjf(processes []Process) {

	n := len(processes)
	completed := 0
	currentTime := 0

	visited := make([]bool, n)

	var order []string
	var timeline []int

	fmt.Println("\n========== SJF NON-PREEMPTIVE ==========")

	for completed < n {

		selected := -1

		// Find the shortest available process
		for i := 0; i < n; i++ {

			if !visited[i] &&
				processes[i].ArrivalTime <= currentTime {

				if selected == -1 ||
					processes[i].BurstTime < processes[selected].BurstTime {

					selected = i
				}
			}
		}

		// If no process has arrived yet, move time forward
		if selected == -1 {

			nextArrival := -1

			for i := 0; i < n; i++ {

				if !visited[i] {

					if nextArrival == -1 ||
						processes[i].ArrivalTime < nextArrival {

						nextArrival = processes[i].ArrivalTime
					}
				}
			}

			currentTime = nextArrival
			continue
		}

		// Calculate Waiting Time
		processes[selected].WaitingTime =
			currentTime - processes[selected].ArrivalTime

		// Record starting time BEFORE execution
		order = append(order, processes[selected].PID)
		timeline = append(timeline, currentTime)

		// Execute process completely
		currentTime += processes[selected].BurstTime

		// Completion Time
		processes[selected].CompletionTime = currentTime

		// Turnaround Time
		processes[selected].TurnaroundTime =
			processes[selected].CompletionTime -
				processes[selected].ArrivalTime

		visited[selected] = true
		completed++
	}

	// Record final ending time
	timeline = append(timeline, currentTime)

	printGanttChart(order, timeline)

	printResults(processes)
}

func roundRobin(processes []Process, quantum int) {

	if quantum <= 0 {
		fmt.Println("Time Quantum must be greater than 0.")
		return
	}

	n := len(processes)

	// Reset remaining time
	for i := 0; i < n; i++ {
		processes[i].RemainingTime = processes[i].BurstTime
	}

	// Sort by Arrival Time
	sort.Slice(processes, func(i, j int) bool {
		return processes[i].ArrivalTime < processes[j].ArrivalTime
	})

	queue := []int{}

	currentTime := 0
	completed := 0
	nextProcess := 0

	var order []string
	var timeline []int

	fmt.Println("\n========== ROUND ROBIN ==========")
	fmt.Printf("Time Quantum: %d\n", quantum)

	for completed < n {

		// If queue is empty, move CPU to next arriving process
		if len(queue) == 0 {

			if nextProcess < n &&
				currentTime < processes[nextProcess].ArrivalTime {

				currentTime = processes[nextProcess].ArrivalTime
			}

			// Add all processes that have arrived
			for nextProcess < n &&
				processes[nextProcess].ArrivalTime <= currentTime {

				queue = append(queue, nextProcess)
				nextProcess++
			}
		}

		// Safety check
		if len(queue) == 0 {
			continue
		}

		// Take first process from queue
		index := queue[0]
		queue = queue[1:]

		// Record starting time
		order = append(order, processes[index].PID)
		timeline = append(timeline, currentTime)

		// Determine execution time
		executionTime := quantum

		if processes[index].RemainingTime < quantum {
			executionTime = processes[index].RemainingTime
		}

		// Execute
		currentTime += executionTime
		processes[index].RemainingTime -= executionTime

		// Add newly arrived processes
		for nextProcess < n &&
			processes[nextProcess].ArrivalTime <= currentTime {

			queue = append(queue, nextProcess)
			nextProcess++
		}

		// Check if process finished
		if processes[index].RemainingTime == 0 {

			processes[index].CompletionTime = currentTime

			processes[index].TurnaroundTime =
				processes[index].CompletionTime -
					processes[index].ArrivalTime

			processes[index].WaitingTime =
				processes[index].TurnaroundTime -
					processes[index].BurstTime

			completed++

		} else {

			// Process still needs CPU time
			queue = append(queue, index)
		}
	}

	// Record final ending time
	timeline = append(timeline, currentTime)

	printGanttChart(order, timeline)

	printResults(processes)
}
