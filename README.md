# Interrupting

Two big takeaway(s):

- Interrupting is useful, but can also be rude and unsafe.
- Cooperative multitasking is a cleaner approach.

## Concepts

1. Client-side timeouts
  - axios timeout
  - requests timeout
  - http/net timeout
2. Server timeouts
  - flask with multi-thread
3. Server interrupts
  - flask with unsafe exception raise
  - flask with early return
  - go deadlines
  - go done channel and pipelines

## Example

Client requests (I/O) expensive (long-running) data from a server.

Fibonacci O(2^n)
