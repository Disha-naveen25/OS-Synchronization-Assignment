```markdown
# AI-Assisted Synchronization Algorithms with Program-Generated HTML Simulation

## Student Information

- **Name:** Disha Naveen
- **USN:** NNM24IS075
- **Course:** Operating Systems
- **Programming Language:** Python
- **Python Version:** 3.13.6

---

# 1. Project Overview

This project demonstrates classical process synchronization problems using
semaphores and monitors.

The project implements two standard synchronization problems:

1. Readers-Writers Problem
2. Dining Philosophers Problem

Each problem is implemented using both:

- Semaphore-based synchronization
- Monitor-based synchronization

Therefore, the project contains four independent implementations:

1. Readers-Writers using Semaphore
2. Readers-Writers using Monitor
3. Dining Philosophers using Semaphore
4. Dining Philosophers using Monitor

The programs use actual concurrent threads and synchronization primitives.
During execution, the programs record state changes and execution events.

The recorded execution events are then used by the same program to generate
HTML simulations.

The overall workflow is:

```text
Execute Python Program
        ↓
Perform Synchronization
        ↓
Capture Execution Events
        ↓
Generate HTML Simulation
        ↓
Open HTML in Browser
```

The HTML simulation is generated from the actual execution trace rather than
being a pre-scripted animation.

---

# 2. Objectives

The main objectives of this project are:

- To understand process/thread synchronization.
- To implement the Readers-Writers problem using semaphores.
- To implement the Readers-Writers problem using a monitor.
- To implement the Dining Philosophers problem using semaphores.
- To implement the Dining Philosophers problem using a monitor.
- To understand mutual exclusion and critical sections.
- To observe waiting and execution states of concurrent threads.
- To understand deadlock and methods used to prevent it.
- To observe possible starvation and fairness limitations.
- To record synchronization events during execution.
- To generate a visual HTML simulation from the recorded execution.
- To understand the difference between semaphore-based and monitor-based
  synchronization.

---

# 3. Implementations

## 3.1 Readers-Writers Using Semaphore

File:

```text
readers_writers/semaphore/readers_writers_semaphore.py
```

This implementation uses Python's `threading.Semaphore`.

Two semaphores are used:

- `rw_mutex` - controls access to the shared resource.
- `mutex` - protects the shared `read_count` variable.

Multiple readers are allowed to read the shared resource simultaneously.

A writer requires exclusive access to the shared resource.

The first reader acquires the resource lock and the last reader releases it.
This allows multiple readers to execute the reading section concurrently
while preventing a writer from accessing the resource at the same time.

The implementation follows a reader-preference approach.

### Main synchronization concepts

- Mutual exclusion for writers
- Concurrent access for readers
- Protection of the reader count
- Shared resource synchronization
- Reader/writer waiting

---

## 3.2 Readers-Writers Using Monitor

File:

```text
readers_writers/monitor/readers_writers_monitor.py
```

This implementation uses:

- `threading.Lock`
- `threading.Condition`

The monitor class manages access to the shared resource.

The monitor maintains:

- Number of active readers
- Whether a writer is active
- Number of waiting writers

Condition variables are used to make readers and writers wait until the
required synchronization condition becomes true.

The implementation gives preference to waiting writers by preventing new
readers from entering when a writer is already waiting.

### Main synchronization concepts

- Mutual exclusion through a monitor lock
- Condition variables
- Reader/writer coordination
- Waiting and notification
- Shared state protection

---

# 4. Dining Philosophers Using Semaphore

File:

```text
dining_philosophers/semaphore/dining_philosophers_semaphore.py
```

This implementation simulates exactly four philosophers and four forks.

Each fork is represented using a semaphore.

An additional semaphore called `room` is used to limit the number of
philosophers attempting to acquire forks simultaneously.

The room semaphore is initialized as:

```python
threading.Semaphore(NUM_PHILOSOPHERS - 1)
```

For four philosophers, this allows at most three philosophers to enter the
fork-acquisition stage at the same time.

Each philosopher follows states such as:

```text
THINKING
HUNGRY
WAITING
ACQUIRING
EATING
RELEASING
FINISHED
```

The room semaphore prevents the circular-wait condition that can cause
deadlock when all philosophers hold one fork and wait for the other.

### Main synchronization concepts

- Fork resource management
- Semaphore acquisition and release
- Mutual exclusion
- Deadlock prevention
- Concurrent execution
- Waiting states

---

# 5. Dining Philosophers Using Monitor

File:

```text
dining_philosophers/monitor/dining_philosophers_monitor.py
```

This implementation uses a monitor consisting of:

- `threading.Lock`
- `threading.Condition`

The monitor maintains the availability of all four forks.

Fork ownership is also tracked during execution.

A philosopher can acquire both required forks only when both are available.

The check and acquisition of both forks are performed while holding the
monitor lock.

When a philosopher finishes eating, both forks are released and waiting
philosophers are notified.

The philosopher states include:

```text
THINKING
HUNGRY
WAITING
ACQUIRING
EATING
RELEASING
FINISHED
```

### Main synchronization concepts

- Monitor-based mutual exclusion
- Condition variables
- Fork availability
- Fork ownership
- Waiting and notification
- Deadlock prevention

---

# 6. HTML Simulation

A major requirement of this project is that each implementation must produce
an HTML simulation from its actual execution.

The Python programs record execution events while the threads are running.

Examples of recorded events include:

```text
Reader 1: WAITING
Reader 1: READING
Writer 1: WAITING
Writer 1: WRITING
Writer 1: FINISHED
```

For Dining Philosophers, events include:

```text
Philosopher 0: THINKING
Philosopher 0: HUNGRY
Philosopher 0: WAITING
Philosopher 0: ACQUIRING
Philosopher 0: EATING
Philosopher 0: RELEASING
Philosopher 0: FINISHED
```

The program converts these recorded events into execution snapshots and
embeds the recorded data into the generated HTML file.

Therefore, the HTML simulation represents the execution trace produced by
the Python program.

---

# 7. Readers-Writers HTML Simulation

The Readers-Writers simulation displays information such as:

- Reader IDs
- Reader states
- Writer state
- Active readers
- Waiting processes
- Shared resource status
- Critical-section activity
- Execution event timeline

The generated files are:

```text
generated_html/readers_writers_semaphore.html
generated_html/readers_writers_monitor.html
```

The HTML simulation provides controls such as:

- Start
- Pause
- Reset
- Simulation speed

The execution timeline can be observed step-by-step in the browser.

---

# 8. Dining Philosophers HTML Simulation

The Dining Philosophers simulation displays:

- All four philosophers
- Four forks
- Philosopher states
- Fork availability
- Fork ownership
- Execution timeline
- Current synchronization state

The generated files are:

```text
generated_html/dining_philosophers_semaphore.html
generated_html/dining_philosophers_monitor.html
```

The simulation represents the circular arrangement of philosophers and forks.

The fork ownership information allows the user to observe which philosopher
currently owns a fork.

---

# 9. Project Structure

```text
OS-Synchronization-Assignment/
│
├── README.md
│
├── ai_prompts/
│   └── prompts.md
│
├── dining_philosophers/
│   │
│   ├── monitor/
│   │   └── dining_philosophers_monitor.py
│   │
│   └── semaphore/
│       └── dining_philosophers_semaphore.py
│
├── generated_html/
│   ├── dining_philosophers_monitor.html
│   ├── dining_philosophers_semaphore.html
│   ├── readers_writers_monitor.html
│   └── readers_writers_semaphore.html
│
├── readers_writers/
│   │
│   ├── monitor/
│   │   └── readers_writers_monitor.py
│   │
│   └── semaphore/
│       └── readers_writers_semaphore.py
│
├── references/
│   └── references.md
│
└── screenshots/
    ├── rw_semaphore.png
    ├── rw_monitor.png
    ├── dp_semaphore.png
    └── dp_monitor.png
```

---

# 10. Requirements

The project requires:

- Python 3.13 or compatible Python version
- A modern web browser

The project uses Python standard-library modules such as:

```python
threading
time
random
json
os
```

No external Python package is required for the synchronization
implementations.

---

# 11. How to Run the Project

First, open a terminal in the project root:

```text
OS-Synchronization-Assignment
```

---

## 11.1 Run Readers-Writers Semaphore

Move to:

```text
readers_writers/semaphore
```

Run:

```bash
python readers_writers_semaphore.py
```

The program performs the synchronization and generates:

```text
generated_html/readers_writers_semaphore.html
```

---

## 11.2 Run Readers-Writers Monitor

Move to:

```text
readers_writers/monitor
```

Run:

```bash
python readers_writers_monitor.py
```

The generated HTML file is:

```text
generated_html/readers_writers_monitor.html
```

---

## 11.3 Run Dining Philosophers Semaphore

Move to:

```text
dining_philosophers/semaphore
```

Run:

```bash
python dining_philosophers_semaphore.py
```

The generated HTML file is:

```text
generated_html/dining_philosophers_semaphore.html
```

---

## 11.4 Run Dining Philosophers Monitor

Move to:

```text
dining_philosophers/monitor
```

Run:

```bash
python dining_philosophers_monitor.py
```

The generated HTML file is:

```text
generated_html/dining_philosophers_monitor.html
```

---

# 12. Viewing the HTML Simulations

After running an implementation, open the corresponding HTML file from the
`generated_html` folder in a web browser.

For example:

```text
generated_html/readers_writers_semaphore.html
```

or:

```text
generated_html/dining_philosophers_monitor.html
```

The HTML files can be opened directly in browsers such as:

- Google Chrome
- Microsoft Edge
- Mozilla Firefox

The simulation controls can then be used to replay the recorded execution
trace.

---

# 13. Execution Behavior

Because the implementations use concurrent threads, the exact execution
order may vary between different runs.

For example, a Readers-Writers execution may produce:

```text
Reader 1: WAITING
Reader 1: READING
Reader 2: WAITING
Reader 2: READING
Reader 3: WAITING
Reader 3: READING
Writer 1: WAITING
Reader 3: FINISHED
Reader 2: FINISHED
Reader 1: FINISHED
Writer 1: WRITING
Writer 1: FINISHED
```

A Dining Philosophers execution may produce:

```text
Philosopher 0: HUNGRY
Philosopher 0: WAITING
Philosopher 0: ACQUIRING
Philosopher 0: EATING
Philosopher 3: HUNGRY
Philosopher 3: WAITING
...
```

The ordering is not hard-coded. It depends on thread scheduling and the
execution timing.

---

# 14. Synchronization Concepts Demonstrated

## 14.1 Race Condition

A race condition occurs when multiple concurrent threads access shared data
and the final result depends on the timing or ordering of their execution.

In the Readers-Writers implementation, the shared reader count is protected
so that multiple threads do not incorrectly modify it at the same time.

---

## 14.2 Mutual Exclusion

Mutual exclusion ensures that only the permitted thread or group of threads
can access a critical section at a particular time.

Examples in this project include:

- Writer-exclusive access in Readers-Writers.
- Protection of `read_count`.
- Exclusive ownership of forks in Dining Philosophers.
- Monitor lock protection of shared state.

---

## 14.3 Critical Section

A critical section is a portion of code where shared data or shared
resources are accessed.

Examples include:

- Updating the Readers-Writers reader count.
- Entering and leaving the shared resource.
- Acquiring and releasing Dining Philosophers forks.
- Updating fork ownership information.

---

## 14.4 Deadlock

Deadlock occurs when processes or threads wait indefinitely for resources
held by each other.

The Dining Philosophers problem is a classical example where deadlock can
occur if every philosopher picks up one fork and waits for the other fork.

The semaphore implementation prevents this using a room semaphore that
allows at most three philosophers to attempt fork acquisition simultaneously.

The monitor implementation checks that both required forks are available
before assigning them to a philosopher.

---

## 14.5 Starvation

Starvation occurs when a thread waits for a resource for an indefinitely
long time because other threads continue to receive access.

The synchronization mechanisms used in this project prevent the demonstrated
deadlock situations, but they do not provide a universal guarantee of
fairness for every possible thread scheduling order.

The Readers-Writers semaphore implementation uses reader preference, so
continuous arrival of readers could delay a writer.

---

# 15. Semaphore vs Monitor

| Feature | Semaphore | Monitor |
|---|---|---|
| Basic mechanism | Semaphore counter with acquire/release | Lock with condition variables |
| Mutual exclusion | Explicitly managed | Encapsulated by monitor |
| Waiting | Threads block on semaphore/condition | Threads wait using condition variables |
| Shared state | Usually managed separately | Encapsulated inside monitor |
| Programming style | More explicit synchronization | Higher-level synchronization abstraction |
| Example in project | Fork semaphores and `rw_mutex` | Lock + Condition |
| Main operations | `acquire()` / `release()` | Lock + `wait()` / `notify()` |
| State management | Programmer manages synchronization state | Monitor class manages synchronization state |

The semaphore implementations make resource acquisition and release explicit.

The monitor implementations group the shared state and synchronization
operations into a synchronization object.

---

# 16. Deadlock Handling

## Readers-Writers

The shared resource is protected so that:

- Multiple readers can access the resource concurrently.
- A writer receives exclusive access.
- Readers cannot enter while a writer is actively using the resource.

---

## Dining Philosophers - Semaphore

The semaphore implementation uses:

```python
room = threading.Semaphore(NUM_PHILOSOPHERS - 1)
```

For four philosophers:

```text
room = Semaphore(3)
```

This prevents all four philosophers from simultaneously holding one fork
and waiting for another fork.

Therefore, the circular-wait condition required for the classical deadlock
scenario is prevented.

---

## Dining Philosophers - Monitor

The monitor checks the availability of both required forks while holding the
monitor lock.

A philosopher acquires both forks only when both are available.

This avoids a state where a philosopher permanently holds one fork while
waiting for the second fork.

---

# 17. Testing and Verification

Each of the four implementations was executed independently.

The execution was checked for:

- Correct program termination.
- Correct synchronization behavior.
- Correct reader/writer states.
- Correct philosopher states.
- Correct fork ownership.
- Correct semaphore acquisition and release.
- Correct monitor waiting and notification.
- Successful HTML generation.
- Correct display of execution events in the HTML simulation.

The generated HTML files were opened in a web browser to verify the
simulation.

---

# 18. Screenshots

Screenshots of the four generated simulations are stored in:

```text
screenshots/
```

The screenshots correspond to:

```text
rw_semaphore.png
rw_monitor.png
dp_semaphore.png
dp_monitor.png
```

These screenshots provide visual evidence of the generated simulations and
the execution states.

---

# 19. AI Usage

AI assistance was used as a programming support tool during the development
of this project.

AI assistance was used for:

- Understanding semaphore-based synchronization.
- Understanding monitor-based synchronization.
- Designing synchronization logic.
- Structuring concurrent thread execution.
- Designing execution-event logging.
- Developing the event-to-HTML simulation approach.
- Debugging implementation issues.
- Reviewing synchronization behavior.
- Improving the generated HTML visualization.
- Understanding deadlock prevention and synchronization concepts.

The implementations were executed and tested locally after development.

The student reviewed the generated code, modified the implementation where
required, tested the programs, and verified the generated HTML simulations.

A detailed record of the AI interaction is provided in:

```text
ai_prompts/prompts.md
```

The prompt log contains the important development prompts, follow-up
requests, testing/debugging interactions, manual changes, and identified
limitations.

---

# 20. AI Error / Limitation Identified During Development

During the development of the Dining Philosophers semaphore implementation,
an initial approach using individual fork semaphores with left-then-right
fork acquisition could lead to a circular-wait situation.

The implementation was therefore modified to include a room semaphore that
limits the number of philosophers attempting to acquire forks
simultaneously.

For four philosophers, at most three philosophers can enter the
fork-acquisition stage at the same time.

This modification prevents the classical circular-wait deadlock scenario.

The corrected implementation was executed and tested before being included
in the final project.

---

# 21. Limitations

The project has the following limitations:

1. The exact execution order can vary between runs because the programs use
   concurrent threads.

2. Timing delays and thread scheduling can affect the order in which events
   occur.

3. Rerunning a program may therefore produce a different but valid
   synchronization trace.

4. The generated HTML simulation represents the actual execution trace
   recorded during the run that generated that HTML file.

5. The project demonstrates synchronization concepts and is not intended as
   a performance benchmark.

6. Fairness is not guaranteed for every synchronization scenario.

7. The Readers-Writers semaphore implementation uses reader preference,
   which can allow writer starvation if readers continuously arrive.

8. The Dining Philosophers solutions prevent the demonstrated deadlock
   condition, but prevention of deadlock does not automatically guarantee
   starvation-free scheduling.

---

# 22. References

The main references used during development are documented in:

```text
references/references.md
```

The references include:

- The Operating Systems assignment specification.
- Python documentation related to threading and synchronization.
- Synchronization concepts related to semaphores, monitors, mutual
  exclusion, deadlock, and condition variables.
- AI assistance used during development.

---

# 23. Academic Integrity and AI Disclosure

AI was used only as a programming and learning assistant.

The student is responsible for:

- Understanding the synchronization algorithms.
- Understanding the submitted source code.
- Testing the implementations.
- Verifying the generated HTML simulations.
- Explaining the synchronization mechanisms during evaluation.
- Documenting AI assistance.
- Identifying and correcting implementation limitations.

The final implementation was tested locally and reviewed before submission.

---

# 24. Integrity Declaration

I declare that I have reviewed and tested the submitted implementation and
understand the synchronization mechanisms used in the project.

AI tools were used as programming and learning assistance, and their use is
documented in the project under:

```text
ai_prompts/prompts.md
```

I take responsibility for understanding, testing, and explaining the
submitted work.

---

# 25. Final Deliverables Checklist

The project contains the following required components:

- [x] Readers-Writers using Semaphore
- [x] Readers-Writers using Monitor
- [x] Dining Philosophers using Semaphore
- [x] Dining Philosophers using Monitor
- [x] Exactly 4 philosophers in Dining Philosophers implementations
- [x] Actual concurrent threads
- [x] Synchronization using semaphores
- [x] Synchronization using monitor/lock/condition variables
- [x] Execution event recording
- [x] Program-generated HTML simulations
- [x] Four generated HTML files
- [x] Four screenshots
- [x] AI prompt documentation
- [x] References
- [x] README documentation
- [x] Testing and verification of implementations

---

# 26. Conclusion

This project demonstrates four implementations of classical process
synchronization problems using semaphores and monitors.

The Readers-Writers implementations demonstrate controlled concurrent access
to a shared resource, while the Dining Philosophers implementations
demonstrate resource allocation, mutual exclusion, waiting, and deadlock
prevention.

The project also connects synchronization logic with visualization by
recording actual execution events and converting those events into
program-generated HTML simulations.

This makes it possible to observe how concurrent threads change states,
wait for resources, enter critical sections, acquire resources, and release
them during execution.
```
