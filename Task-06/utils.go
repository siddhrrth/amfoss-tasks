package main

import "fmt"

func printResults(processes []Process) {

	fmt.Println()
	fmt.Println("RESULTS")
	fmt.Println("==========================================================================")
	fmt.Printf("%-8s %-10s %-8s %-12s %-10s %-12s\n",
		"PID",
		"Arrival",
		"Burst",
		"Completion",
		"Waiting",
		"Turnaround",
	)
	fmt.Println("--------------------------------------------------------------------------")

	totalWaiting := 0
	totalTurnaround := 0

	for _, p := range processes {

		fmt.Printf("  %-8s %-10d %-8d %-12d %-10d %-12d\n",
			p.PID,
			p.ArrivalTime,
			p.BurstTime,
			p.CompletionTime,
			p.WaitingTime,
			p.TurnaroundTime,
		)

		totalWaiting += p.WaitingTime
		totalTurnaround += p.TurnaroundTime
	}

	fmt.Println("--------------------------------------------------------------------------")

	avgWaiting := float64(totalWaiting) / float64(len(processes))
	avgTurnaround := float64(totalTurnaround) / float64(len(processes))

	fmt.Printf("Average Waiting Time    : %.2f\n", avgWaiting)
	fmt.Printf("Average Turnaround Time : %.2f\n", avgTurnaround)
}

func printGanttChart(order []string, timeline []int) {

	fmt.Println()
	fmt.Println("Gantt Chart:")
	fmt.Println()

	// Top border
	fmt.Print(" ")
	for range order {
		fmt.Print("--------")
	}
	fmt.Println()

	// Process names
	for _, pid := range order {
		fmt.Printf("| %-6s", pid)
	}
	fmt.Println("|")

	// Bottom border
	fmt.Print(" ")
	for range order {
		fmt.Print("--------")
	}
	fmt.Println()

	// Timeline
	for _, time := range timeline {
		fmt.Printf("%-8d", time)
	}

	fmt.Println()
}
