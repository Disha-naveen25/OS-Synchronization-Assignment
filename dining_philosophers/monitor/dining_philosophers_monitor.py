import threading
import time
import random
import json


NUM_PHILOSOPHERS = 4


# ============================================================
# Dining Philosophers Monitor
# ============================================================

class DiningPhilosophersMonitor:

    def __init__(self):
        self.lock = threading.Lock()

        self.forks_available = threading.Condition(self.lock)

        # True means the fork is available.
        self.forks = [True] * NUM_PHILOSOPHERS

        # Stores which philosopher owns each fork.
        # None means the fork is available.
        self.fork_owners = [None] * NUM_PHILOSOPHERS


    def acquire_forks(self, philosopher_id):

        left_fork = philosopher_id
        right_fork = (philosopher_id + 1) % NUM_PHILOSOPHERS

        with self.lock:

            # Wait until both required forks are available.
            while not (
                self.forks[left_fork]
                and self.forks[right_fork]
            ):
                self.forks_available.wait()

            # Acquire both forks atomically.
            self.forks[left_fork] = False
            self.forks[right_fork] = False

            self.fork_owners[left_fork] = philosopher_id
            self.fork_owners[right_fork] = philosopher_id


    def release_forks(self, philosopher_id):

        left_fork = philosopher_id
        right_fork = (philosopher_id + 1) % NUM_PHILOSOPHERS

        with self.lock:

            # Release both forks.
            self.forks[left_fork] = True
            self.forks[right_fork] = True

            self.fork_owners[left_fork] = None
            self.fork_owners[right_fork] = None

            # Wake philosophers waiting for forks.
            self.forks_available.notify_all()


    def get_fork_owners(self):

        with self.lock:
            return self.fork_owners.copy()


# ============================================================
# Global objects
# ============================================================

monitor = DiningPhilosophersMonitor()

events = []

event_lock = threading.Lock()


# ============================================================
# Event logging
# ============================================================

def log_event(philosopher_id, state):

    actor = f"Philosopher {philosopher_id}"

    # Get the current fork ownership.
    fork_snapshot = monitor.get_fork_owners()

    with event_lock:

        events.append({
            "time": time.time(),
            "actor": actor,
            "state": state,
            "forks": fork_snapshot
        })

        print(f"{actor}: {state}")


# ============================================================
# Philosopher thread
# ============================================================

def philosopher(philosopher_id):

    log_event(philosopher_id, "THINKING")

    time.sleep(random.uniform(0.5, 1.0))


    log_event(philosopher_id, "HUNGRY")


    log_event(philosopher_id, "WAITING")


    log_event(philosopher_id, "ACQUIRING")


    # Monitor waits until both forks are available.
    monitor.acquire_forks(philosopher_id)


    # Both forks have now been acquired.
    log_event(philosopher_id, "EATING")

    time.sleep(random.uniform(0.5, 1.0))


    log_event(philosopher_id, "RELEASING")


    # Release both forks.
    monitor.release_forks(philosopher_id)


    time.sleep(random.uniform(0.2, 0.5))


    log_event(philosopher_id, "FINISHED")


# ============================================================
# HTML generation
# ============================================================

def generate_html():

    html_file = "dining_philosophers_monitor.html"

    # Convert the actual Python execution events into JSON.
    events_json = json.dumps(events)


    html = f"""
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<title>
Dining Philosophers - Monitor Simulation
</title>


<style>

body {{

    font-family: Arial, sans-serif;

    background: #f4f4f4;

    margin: 0;

    padding: 20px;

    text-align: center;
}}


h1 {{

    margin-bottom: 5px;
}}


.subtitle {{

    color: #555;

    margin-bottom: 20px;
}}


.controls {{

    margin: 20px;
}}


button,
select {{

    padding: 8px 14px;

    margin: 4px;

    cursor: pointer;
}}


/* Dining table */

.table {{

    position: relative;

    width: 600px;

    height: 600px;

    margin: 20px auto;

    background: #ddd;

    border-radius: 50%;

    border: 4px solid #444;
}}


/* Center of table */

.center {{

    position: absolute;

    width: 180px;

    height: 180px;

    background: white;

    border: 3px solid #555;

    border-radius: 50%;

    top: 210px;

    left: 210px;

    display: flex;

    align-items: center;

    justify-content: center;

    font-weight: bold;
}}


/* Philosophers */

.philosopher {{

    position: absolute;

    width: 120px;

    padding: 12px;

    background: white;

    border: 3px solid #555;

    border-radius: 12px;

    transform: translate(-50%, -50%);
}}


.p0 {{

    top: 8%;

    left: 50%;
}}


.p1 {{

    top: 50%;

    left: 92%;
}}


.p2 {{

    top: 92%;

    left: 50%;
}}


.p3 {{

    top: 50%;

    left: 8%;
}}


/* State styles */

.thinking {{

    background: #d9eaff;
}}


.hungry {{

    background: #fff3b0;
}}


.waiting {{

    background: #ffd6a5;
}}


.acquiring {{

    background: #e5d4ff;
}}


.eating {{

    background: #b8f2b8;

    border-color: #228b22;
}}


.releasing {{

    background: #f5c6c6;
}}


.finished {{

    background: #ddd;
}}


/* Fork labels */

.fork {{

    position: absolute;

    font-weight: bold;

    font-size: 18px;
}}


.fork0 {{

    top: 25%;

    left: 72%;
}}


.fork1 {{

    top: 72%;

    left: 72%;
}}


.fork2 {{

    top: 72%;

    left: 25%;
}}


.fork3 {{

    top: 25%;

    left: 25%;
}}


/* Information section */

.info {{

    max-width: 850px;

    margin: 20px auto;

    background: white;

    padding: 20px;

    border-radius: 10px;

    text-align: left;
}}


.current-event {{

    font-size: 20px;

    font-weight: bold;

    margin-bottom: 15px;
}}


.fork-status {{

    display: grid;

    grid-template-columns: 1fr 1fr;

    gap: 10px;

    margin-bottom: 20px;
}}


.fork-box {{

    padding: 10px;

    border: 1px solid #aaa;

    border-radius: 6px;

    background: #f8f8f8;
}}


.timeline {{

    max-height: 250px;

    overflow-y: auto;

    font-family: monospace;

    background: #111;

    color: #eee;

    padding: 15px;

    border-radius: 8px;

    line-height: 1.7;
}}


.progress-container {{

    width: 100%;

    background: #ddd;

    height: 12px;

    border-radius: 6px;

    margin-top: 15px;
}}


.progress-bar {{

    height: 12px;

    width: 0%;

    border-radius: 6px;

    background: #555;
}}

</style>

</head>


<body>


<h1>
Dining Philosophers — Monitor
</h1>


<div class="subtitle">

Simulation generated from actual Python execution events

</div>


<div class="controls">

<button onclick="startSimulation()">
Start
</button>


<button onclick="pauseSimulation()">
Pause
</button>


<button onclick="resetSimulation()">
Reset
</button>


<label>

Speed:

<select id="speed">

<option value="0.5">
0.5x
</option>

<option value="1" selected>
1x
</option>

<option value="2">
2x
</option>

<option value="4">
4x
</option>

</select>

</label>

</div>


<div class="table">


<div class="center">

Monitor<br>

Shared Table

</div>


<div id="p0" class="philosopher p0">

Philosopher 0

<br>

<span>
THINKING
</span>

</div>


<div id="p1" class="philosopher p1">

Philosopher 1

<br>

<span>
THINKING
</span>

</div>


<div id="p2" class="philosopher p2">

Philosopher 2

<br>

<span>
THINKING
</span>

</div>


<div id="p3" class="philosopher p3">

Philosopher 3

<br>

<span>
THINKING
</span>

</div>


<div id="f0" class="fork fork0">

Fork 0

</div>


<div id="f1" class="fork fork1">

Fork 1

</div>


<div id="f2" class="fork fork2">

Fork 2

</div>


<div id="f3" class="fork fork3">

Fork 3

</div>


</div>


<div class="info">


<h3>
Current Event
</h3>


<div id="currentEvent" class="current-event">

Waiting to start...

</div>


<h3>
Fork Ownership
</h3>


<div class="fork-status">


<div id="fork0" class="fork-box">

Fork 0: Available

</div>


<div id="fork1" class="fork-box">

Fork 1: Available

</div>


<div id="fork2" class="fork-box">

Fork 2: Available

</div>


<div id="fork3" class="fork-box">

Fork 3: Available

</div>


</div>


<h3>
Progress
</h3>


<div class="progress-container">

<div id="progressBar" class="progress-bar">

</div>

</div>


<h3>
Event Timeline
</h3>


<div id="timeline" class="timeline">

</div>


</div>


<script>


// ============================================================
// Actual execution data generated by Python
// ============================================================

const events = {events_json};


let currentIndex = 0;

let timer = null;

let running = false;


// ============================================================
// Update philosopher state
// ============================================================

function updatePhilosopher(event) {{

    const match =
        event.actor.match(/\\d+/);

    if (!match) {{

        return;

    }}


    const philosopherNumber =
        parseInt(match[0]);


    const philosopher =
        document.getElementById(
            "p" + philosopherNumber
        );


    const stateText =
        philosopher.querySelector("span");


    stateText.textContent =
        event.state;


    philosopher.className =
        "philosopher p" + philosopherNumber;


    const state =
        event.state.toLowerCase();


    if (state === "thinking") {{

        philosopher.classList.add("thinking");

    }}

    else if (state === "hungry") {{

        philosopher.classList.add("hungry");

    }}

    else if (state === "waiting") {{

        philosopher.classList.add("waiting");

    }}

    else if (state === "acquiring") {{

        philosopher.classList.add("acquiring");

    }}

    else if (state === "eating") {{

        philosopher.classList.add("eating");

    }}

    else if (state === "releasing") {{

        philosopher.classList.add("releasing");

    }}

    else if (state === "finished") {{

        philosopher.classList.add("finished");

    }}

}}


// ============================================================
// Update fork ownership
// ============================================================

function updateForks(forks) {{

    for (let i = 0; i < 4; i++) {{

        const forkElement =
            document.getElementById(
                "fork" + i
            );


        if (forks[i] === null) {{

            forkElement.textContent =
                "Fork " + i + ": Available";

        }}

        else {{

            forkElement.textContent =
                "Fork " +
                i +
                ": Philosopher " +
                forks[i];

        }}

    }}

}}


// ============================================================
// Process one execution event
// ============================================================

function processEvent(event) {{

    updatePhilosopher(event);

    updateForks(event.forks);


    document.getElementById(
        "currentEvent"
    ).textContent =
        event.actor +
        " → " +
        event.state;


    const timeline =
        document.getElementById(
            "timeline"
        );


    timeline.innerHTML +=
        "[" +
        (currentIndex + 1) +
        "] " +
        event.actor +
        " → " +
        event.state +
        "<br>";


    timeline.scrollTop =
        timeline.scrollHeight;


    const progress =
        ((currentIndex + 1) / events.length) * 100;


    document.getElementById(
        "progressBar"
    ).style.width =
        progress + "%";

}}


// ============================================================
// Replay events
// ============================================================

function playNext() {{

    if (!running) {{

        return;

    }}


    if (currentIndex >= events.length) {{

        running = false;

        return;

    }}


    processEvent(
        events[currentIndex]
    );


    currentIndex++;


    const speed =
        parseFloat(
            document.getElementById(
                "speed"
            ).value
        );


    timer = setTimeout(

        playNext,

        1000 / speed

    );

}}


// ============================================================
// Start
// ============================================================

function startSimulation() {{

    if (running) {{

        return;

    }}


    if (currentIndex >= events.length) {{

        resetSimulation();

    }}


    running = true;

    playNext();

}}


// ============================================================
// Pause
// ============================================================

function pauseSimulation() {{

    running = false;


    if (timer !== null) {{

        clearTimeout(timer);

        timer = null;

    }}

}}


// ============================================================
// Reset
// ============================================================

function resetSimulation() {{

    pauseSimulation();


    currentIndex = 0;


    document.getElementById(
        "currentEvent"
    ).textContent =
        "Waiting to start...";


    document.getElementById(
        "timeline"
    ).innerHTML = "";


    document.getElementById(
        "progressBar"
    ).style.width =
        "0%";


    for (let i = 0; i < 4; i++) {{

        const philosopher =
            document.getElementById(
                "p" + i
            );


        philosopher.className =
            "philosopher p" + i;


        philosopher.querySelector(
            "span"
        ).textContent =
            "THINKING";

    }}


    updateForks([
        null,
        null,
        null,
        null
    ]);

}}


</script>


</body>

</html>
"""


    # Write the generated HTML file.
    with open(
        html_file,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(html)


    print(
        f"HTML simulation generated: {html_file}"
    )


# ============================================================
# Main
# ============================================================

def main():

    philosophers = [

        threading.Thread(
            target=philosopher,
            args=(i,)
        )

        for i in range(NUM_PHILOSOPHERS)

    ]


    # Start all philosopher threads.
    for philosopher_thread in philosophers:

        philosopher_thread.start()


    # Wait for all philosophers to finish.
    for philosopher_thread in philosophers:

        philosopher_thread.join()


    print("\nExecution completed.")

    print(
        f"Total events recorded: {len(events)}"
    )


    # Show recorded fork tracking.
    print("\nFork tracking:")

    for event in events:

        print(
            event["actor"],
            event["state"],
            "Forks:",
            event["forks"]
        )


    # Generate HTML from the actual execution.
    generate_html()


# ============================================================
# Program entry point
# ============================================================

if __name__ == "__main__":

    main()