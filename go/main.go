package main

import (
	"fmt"
	"log"
	"net/http"
	"strconv"
	"time"
)

func main() {
	s := http.NewServeMux()

	// v1 - no timeout
	s.Handle(
		"GET /v1/sleep/{n}/echo/{message}",
		handleSleepEcho,
	)

	// v2 - timeout using http.TimeoutHandler, still executes
	s.Handle(
		"GET /v2/sleep/{n}/echo/{message}",
		http.TimeoutHandler(handleSleepEcho, 2*time.Second, "Server Timeout"),
	)

	// v3 - timeout using http.TimeoutHandler and context.Deadline(), doesn't execute
	s.Handle(
		"GET /v3/sleep/{n}/echo/{message}",
		http.TimeoutHandler(handleSleepEcho3, 2*time.Second, "Server Timeout"),
	)

	// v4 - timeout using context.Done(), doesn't execute
	s.Handle(
		"GET /v4/sleep/{n}/echo/{message}",
		http.TimeoutHandler(handleSleepEcho4, 2*time.Second, "Server Timeout"),
	)

	log.Default().Printf("Starting server on port 8080")
	log.Fatal(http.ListenAndServe(":8080", s))
}

// handleSleepEcho synchronously sleeps for "n" seconds and then writes the "message" to the response.
var handleSleepEcho = http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
	n, message, err := extractPathValues(r)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
	}

	log.Printf("Sleeping for %d seconds", n)

	time.Sleep(time.Duration(n) * time.Second)

	log.Printf("Echoing message: %s", message)

	w.Write([]byte(message))
})

// handleSleepEcho3 sleeps for "n" seconds and then writes the "message" to the response.
//
// It will check if the request has been cancelled every 100 milliseconds.
var handleSleepEcho3 = http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
	n, message, err := extractPathValues(r)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
	}

	log.Printf("Sleeping for %d seconds", n)

	start := time.Now()
	deadline, ok := r.Context().Deadline()
	for time.Since(start) < time.Duration(n)*time.Second {
		if ok && time.Now().After(deadline) {
			log.Printf("Request cancelled")
			return
		}

		time.Sleep(100 * time.Millisecond)
	}

	log.Printf("Echoing message: %s", message)

	w.Write([]byte(message))
})

// handleSleepEcho4 sleeps for "n" seconds and then writes the "message" to the response.
//
// It will take the first of two possible events: the sleep duration elapses or the request is cancelled.
var handleSleepEcho4 = http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
	n, message, err := extractPathValues(r)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
	}

	log.Printf("Sleeping for %d seconds", n)

	select {
	case <-time.After(time.Duration(n) * time.Second):
		log.Printf("Echoing message: %s", message)
		w.Write([]byte(message))
	case <-r.Context().Done():
		log.Printf("Request cancelled")
	}
})

// extractPathValues extracts the "n" and "message" values from the url path.
func extractPathValues(r *http.Request) (int, string, error) {
	// extract positive integer "n" from url path
	n, err := strconv.Atoi(r.PathValue("n"))
	if err != nil {
		return 0, "", fmt.Errorf("invalid sleep value: %v", err)
	} else if n < 0 {
		return 0, "", fmt.Errorf("sleep value (%d) must be positive", n)
	}

	// extract non-empty string "message" from url path
	message := r.PathValue("message")
	if message == "" {
		return 0, "", fmt.Errorf("message is required")
	}

	return n, message, nil
}
