package main

import "fmt"

func main() {

	for {

		fmt.Println()
		fmt.Println("+==========================================+")
		fmt.Println("|        PIRATE KING'S SCHEDULER           |")
		fmt.Println("+==========================================+")
		fmt.Println("|                                          |")
		fmt.Println("|   1. First Come First Serve (FCFS)       |")
		fmt.Println("|   2. Shortest Job First (SJF)            |")
		fmt.Println("|   3. Round Robin (RR)                    |")
		fmt.Println("|   4. Exit                                |")
		fmt.Println("|                                          |")
		fmt.Println("+==========================================+")

		var choice int

		fmt.Print("\nChoose Algorithm: ")
		fmt.Scan(&choice)

		if choice == 4 {
			fmt.Println("\nThe Pirate King's Scheduler has sailed away!")
			break
		}

		if choice < 1 || choice > 4 {
			fmt.Println("\nInvalid choice. Please select 1-4.")
			continue
		}

		var n int

		fmt.Print("Enter Number of Processes: ")
		fmt.Scan(&n)

		if n <= 0 {
			fmt.Println("Number of processes must be greater than 0.")
			continue
		}

		processes := make([]Process, n)

		for i := 0; i < n; i++ {

			fmt.Printf("\nProcess %d\n", i+1)

			fmt.Print("Process ID: ")
			fmt.Scan(&processes[i].PID)

			for {
				fmt.Print("Arrival Time: ")
				fmt.Scan(&processes[i].ArrivalTime)

				if processes[i].ArrivalTime >= 0 {
					break
				}

				fmt.Println("Arrival Time cannot be negative.")
			}

			for {
				fmt.Print("Burst Time: ")
				fmt.Scan(&processes[i].BurstTime)

				if processes[i].BurstTime > 0 {
					break
				}

				fmt.Println("Burst Time must be greater than 0.")
			}

			processes[i].RemainingTime = processes[i].BurstTime
		}

		switch choice {

		case 1:
			fcfs(processes)

		case 2:
			sjf(processes)

		case 3:

			var quantum int

			for {
				fmt.Print("Time Quantum: ")
				fmt.Scan(&quantum)

				if quantum > 0 {
					break
				}

				fmt.Println("Time Quantum must be greater than 0.")
			}

			roundRobin(processes, quantum)
		}

		fmt.Println("\n------------------------------------------")
		fmt.Println("Press Enter to return to the main menu...")
		fmt.Scanln()
		fmt.Scanln()
	}
}
