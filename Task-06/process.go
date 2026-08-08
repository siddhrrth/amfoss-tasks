package main

type Process struct {
	PID string

	ArrivalTime int
	BurstTime   int

	RemainingTime int

	CompletionTime int
	WaitingTime    int
	TurnaroundTime int
}
