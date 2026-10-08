\# AI Prompt Log



\## 1. AI Tool Used



AI tool: ChatGPT  

Model: GPT-5.6 Luna



ChatGPT was used as a programming assistant during the development of the

Operating Systems synchronization assignment.



The student tested the generated and modified code locally and made manual

changes based on testing and understanding of the synchronization logic.



\---



\## 2. Initial Prompt



I need to implement an Operating Systems programming assignment on classical

process synchronization using semaphores and monitors.



The assignment requires four separate implementations:



1\. Readers-Writers using semaphores

2\. Readers-Writers using a monitor

3\. Dining Philosophers using semaphores with exactly 4 philosophers

4\. Dining Philosophers using a monitor with exactly 4 philosophers



The programs must use actual concurrent threads and generate HTML simulations

from the execution events and state transitions.



Help me build the implementations step by step so that I can understand,

test, and explain the code myself.



\---



\## 3. Important Follow-up Prompts



\### Readers-Writers - Semaphore



I want to build the Readers-Writers semaphore implementation first.

Explain the code step by step and help me test whether multiple readers can

read concurrently while the writer gets exclusive access.



\### Readers-Writers - Monitor



Now help me create the monitor-based Readers-Writers implementation using

Python locks and condition variables.



\### Dining Philosophers - Semaphore



Now let's implement Dining Philosophers using semaphores with exactly four

philosophers. The implementation should handle the deadlock problem.



\### Dining Philosophers - Monitor



Now implement the Dining Philosophers problem using a monitor equivalent with

a lock and condition variable.



\### Execution Tracking



The assignment requires the HTML simulation to be generated from actual

execution data. Help me record state transitions from the running program.



\### Fork Tracking



Add fork ownership tracking so that the HTML simulation can show which

philosopher owns each of the four forks.



\### HTML Generation



Generate an HTML simulation from the actual execution events, including

philosopher states, fork ownership, event timeline, and replay controls.



\---



\## 4. Manual Changes Made by the Student



The following activities were manually performed and tested by the student:



\- Created the required project folders and Python files.

\- Ran each synchronization implementation from the command line.

\- Checked the execution output and state transitions.

\- Tested the Readers-Writers semaphore implementation.

\- Tested the Readers-Writers monitor implementation.

\- Tested the Dining Philosophers semaphore implementation.

\- Tested the Dining Philosophers monitor implementation.

\- Added and verified execution-event tracking.

\- Added fork ownership tracking for the Dining Philosophers simulations.

\- Ran the programs repeatedly to observe different concurrent execution orders.

\- Generated and opened the HTML simulations in a browser.

\- Organized the generated HTML files into the `generated\_html` directory.

\- Created the screenshots and AI prompt-log directories as required by the

&#x20; assignment.



The student reviewed the synchronization logic rather than submitting the

AI-generated code without testing.



\---



\## 5. AI Error / Limitation Identified



During the Dining Philosophers semaphore implementation, an initial approach

used one semaphore for each fork and had philosophers acquire their left fork

followed by their right fork.



This approach can lead to deadlock if all four philosophers acquire one fork

and then wait for the other fork.



Testing and analysis identified this limitation. The implementation was

modified to use an additional room semaphore allowing at most three

philosophers to attempt fork acquisition simultaneously. This breaks the

circular-wait condition and prevents the demonstrated deadlock scenario.



This was an important example where the generated implementation needed to be

tested and understood rather than accepted without verification.



\---



\## 6. HTML Simulation Development



The HTML simulations were generated from execution events recorded by the

Python programs.



For Dining Philosophers, each event contains:



\- Execution time

\- Philosopher ID

\- Philosopher state

\- Fork ownership information



The generated HTML reads this execution data and replays the recorded

state transitions.



The simulations include philosopher states, fork availability/ownership,

event timelines, and playback controls.



\---



\## 7. Reflection



Using AI helped with code structure, debugging, event logging, and HTML

generation. However, testing the programs was necessary to identify

synchronization problems and verify that the generated simulations actually

represented the program execution.



The final implementations were tested locally and the student should be able

to explain the use of semaphores, locks, condition variables, critical

sections, shared resources, deadlock prevention, and the execution-to-HTML

workflow during the viva.

