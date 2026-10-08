import threading
import time
import random
import json


# -----------------------------
# Shared data
# -----------------------------

read_count = 0

# Semaphore for protecting the shared resource
rw_mutex = threading.Semaphore(1)

# Semaphore for protecting read_count
mutex = threading.Semaphore(1)


# -----------------------------
# Event logging
# -----------------------------

events = []


def log_event(actor, state):
    """Record a synchronization state change."""
    events.append({
        "time": time.time(),
        "actor": actor,
        "state": state
    })

    print(f"{actor}: {state}")


# -----------------------------
# Reader thread
# -----------------------------

def reader(reader_id):
    global read_count

    actor = f"Reader {reader_id}"

    log_event(actor, "WAITING")

    # Protect read_count
    mutex.acquire()

    read_count += 1

    # The first reader blocks writers
    if read_count == 1:
        rw_mutex.acquire()

    mutex.release()

    log_event(actor, "READING")

    # Simulate reading
    time.sleep(random.uniform(0.5, 1.5))

    # Reader is finished
    mutex.acquire()

    read_count -= 1

    # The last reader allows writers
    if read_count == 0:
        rw_mutex.release()

    mutex.release()

    log_event(actor, "FINISHED")


# -----------------------------
# Writer thread
# -----------------------------

def writer(writer_id):
    actor = f"Writer {writer_id}"

    log_event(actor, "WAITING")

    # Writer needs exclusive access to the shared resource
    rw_mutex.acquire()

    log_event(actor, "WRITING")

    # Simulate writing
    time.sleep(random.uniform(0.5, 1.5))

    # Release the shared resource
    rw_mutex.release()

    log_event(actor, "FINISHED")

#-----------------------------

def generate_html():
    # -----------------------------------------
    # Reconstruct actual execution snapshots
    # -----------------------------------------

    reader_states = {}
    writer_states = {}

    snapshots = []

    first_time = events[0]["time"] if events else time.time()

    for index, event in enumerate(events, start=1):

        actor = event["actor"]
        state = event["state"]

        # Update actual actor state
        if "Reader" in actor:
            reader_states[actor] = state
        else:
            writer_states[actor] = state

        # Count readers currently reading
        active_readers = sum(
            1
            for value in reader_states.values()
            if value == "READING"
        )

        # Determine writer state
        active_writer = any(
            value == "WRITING"
            for value in writer_states.values()
        )

        waiting_writer = any(
            value == "WAITING"
            for value in writer_states.values()
        )

        # Determine shared resource status
        if active_writer:
            resource_status = "WRITING (exclusive)"
        elif active_readers > 0:
            resource_status = f"READING ({active_readers} active)"
        else:
            resource_status = "AVAILABLE"

        # Store a complete snapshot
        snapshots.append({
            "event_number": index,
            "time": round(event["time"] - first_time, 3),
            "actor": actor,
            "state": state,
            "readers": dict(reader_states),
            "writers": dict(writer_states),
            "active_readers": active_readers,
            "resource": resource_status,
            "writer_active": active_writer,
            "writer_waiting": waiting_writer
        })

    # Convert Python snapshots to JavaScript data
    snapshots_json = json.dumps(snapshots)

    html = f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<title>
Readers-Writers (Semaphore)
</title>

<style>

* {{
    box-sizing: border-box;
}}

body {{
    margin: 0;
    padding: 30px;
    font-family: Arial, sans-serif;
    background: #eef1f5;
    color: #222;
}}

.container {{
    max-width: 1200px;
    margin: auto;
}}

h1 {{
    text-align: center;
    margin-bottom: 25px;
}}

.controls {{
    background: white;
    padding: 18px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
    box-shadow: 0 2px 8px rgba(0,0,0,0.12);
    margin-bottom: 20px;
}}

button {{
    border: none;
    padding: 10px 18px;
    border-radius: 7px;
    cursor: pointer;
    font-size: 14px;
}}

.start {{
    background: #2e7d32;
    color: white;
}}

.pause {{
    background: #ef6c00;
    color: white;
}}

.reset {{
    background: #616161;
    color: white;
}}

button:hover {{
    opacity: 0.85;
}}

select {{
    padding: 9px;
    border-radius: 6px;
}}

.progress {{
    margin-left: auto;
    font-weight: bold;
}}

.resource {{
    background: white;
    padding: 18px;
    border-radius: 12px;
    text-align: center;
    margin-bottom: 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.12);
}}

.resource-title {{
    font-size: 14px;
    color: #666;
}}

.resource-status {{
    font-size: 22px;
    font-weight: bold;
    margin-top: 8px;
}}

.process-container {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 15px;
    margin-bottom: 25px;
}}

.process {{
    background: white;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    min-height: 130px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.12);
    border-top: 6px solid #999;
}}

.process.reader {{
    border-top-color: #2196F3;
}}

.process.writer {{
    border-top-color: #e53935;
}}

.process-name {{
    font-size: 20px;
    font-weight: bold;
}}

.process-type {{
    color: #666;
    margin: 6px;
}}

.process-state {{
    font-weight: bold;
    font-size: 18px;
    margin-top: 10px;
}}

.event-section {{
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.12);
}}

.event-section h2 {{
    margin-top: 0;
}}

.event-log {{
    max-height: 400px;
    overflow-y: auto;
}}

.event {{
    padding: 12px;
    margin: 7px 0;
    border-radius: 7px;
    background: #f5f6f8;
    border-left: 5px solid #999;
}}

.event.reader-event {{
    border-left-color: #2196F3;
}}

.event.writer-event {{
    border-left-color: #e53935;
}}

.event.current {{
    outline: 2px solid #333;
    background: #fff3cd;
}}

.event-top {{
    display: flex;
    justify-content: space-between;
    gap: 10px;
}}

.event-state {{
    font-weight: bold;
}}

.event-details {{
    margin-top: 8px;
    font-size: 13px;
    color: #555;
}}

@media (max-width: 800px) {{

    .process-container {{
        grid-template-columns: repeat(2, 1fr);
    }}

    .progress {{
        margin-left: 0;
    }}

}}

</style>

</head>


<body>

<div class="container">

<h1>
Readers-Writers (Semaphore)
</h1>


<!-- Controls -->

<div class="controls">

<button class="start" onclick="startSimulation()">
▶ Start
</button>

<button class="pause" onclick="pauseSimulation()">
⏸ Pause
</button>

<button class="reset" onclick="resetSimulation()">
↻ Reset
</button>

<label>
Speed:
<select id="speed">
    <option value="2000">0.5x</option>
    <option value="1000" selected>1x</option>
    <option value="500">2x</option>
    <option value="250">4x</option>
</select>
</label>

<div class="progress">
Progress:
<span id="progress">0 / {len(snapshots)}</span>
</div>

</div>


<!-- Shared Resource -->

<div class="resource">

<div class="resource-title">
Shared Resource
</div>

<div
    id="resource-status"
    class="resource-status"
>
AVAILABLE
</div>

</div>


<!-- Process Cards -->

<div
    id="process-container"
    class="process-container"
>
</div>


<!-- Event Log -->

<div class="event-section">

<h2>
Event Log (from program trace)
</h2>

<div
    id="event-log"
    class="event-log"
>
</div>

</div>

</div>


<script>

/*
    These snapshots were generated by the Python
    synchronization program from its actual events.
*/

const snapshots = {snapshots_json};

let currentIndex = 0;
let timer = null;
let running = false;


// -----------------------------------------
// Create initial process cards
// -----------------------------------------

const actors = [];

snapshots.forEach(snapshot => {{

    Object.keys(snapshot.readers).forEach(actor => {{

        if (!actors.includes(actor)) {{
            actors.push(actor);
        }}

    }});

    Object.keys(snapshot.writers).forEach(actor => {{

        if (!actors.includes(actor)) {{
            actors.push(actor);
        }}

    }});

}});


// -----------------------------------------
// Render process cards
// -----------------------------------------

function renderProcesses(snapshot) {{

    const container =
        document.getElementById("process-container");

    container.innerHTML = "";

    actors.forEach(actor => {{

        let state = "IDLE";

        if (snapshot.readers[actor]) {{
            state = snapshot.readers[actor];
        }}

        if (snapshot.writers[actor]) {{
            state = snapshot.writers[actor];
        }}

        const type =
            actor.includes("Reader")
            ? "Reader"
            : "Writer";

        const card =
            document.createElement("div");

        card.className =
            "process " +
            (type === "Reader"
                ? "reader"
                : "writer");

        card.innerHTML = `
            <div class="process-name">
                ${{actor}}
            </div>

            <div class="process-type">
                ${{type}}
            </div>

            <div class="process-state">
                ${{state}}
            </div>
        `;

        container.appendChild(card);

    }});

}}


// -----------------------------------------
// Render resource status
// -----------------------------------------

function renderResource(snapshot) {{

    document.getElementById(
        "resource-status"
    ).textContent = snapshot.resource;

}}


// -----------------------------------------
// Render event log
// -----------------------------------------

function renderEventLog() {{

    const log =
        document.getElementById("event-log");

    log.innerHTML = "";

    snapshots.forEach((snapshot, index) => {{

        const event =
            document.createElement("div");

        const isReader =
            snapshot.actor.includes("Reader");

        event.className =
            "event " +
            (isReader
                ? "reader-event"
                : "writer-event");

        if (index === currentIndex - 1) {{
            event.classList.add("current");
        }}

        event.innerHTML = `

            <div class="event-top">

                <strong>
                    Event ${{snapshot.event_number}}
                </strong>

                <strong>
                    ${{snapshot.actor}}
                </strong>

                <span class="event-state">
                    ${{snapshot.state}}
                </span>

            </div>

            <div class="event-details">

                Time: ${{snapshot.time}} s
                &nbsp; | &nbsp;

                Active Readers:
                ${{snapshot.active_readers}}

                &nbsp; | &nbsp;

                Resource:
                ${{snapshot.resource}}

            </div>

        `;

        log.appendChild(event);

    }});

    const currentEvent =
        log.querySelector(".current");

    if (currentEvent) {{
        currentEvent.scrollIntoView({{
            behavior: "smooth",
            block: "nearest"
        }});
    }}

}}


// -----------------------------------------
// Display current snapshot
// -----------------------------------------

function displaySnapshot(index) {{

    if (index >= snapshots.length) {{
        return;
    }}

    const snapshot =
        snapshots[index];

    renderProcesses(snapshot);

    renderResource(snapshot);

    currentIndex = index + 1;

    document.getElementById(
        "progress"
    ).textContent =
        currentIndex +
        " / " +
        snapshots.length;

    renderEventLog();

}}


// -----------------------------------------
// Start simulation
// -----------------------------------------

function startSimulation() {{

    if (running) {{
        return;
    }}

    if (currentIndex >= snapshots.length) {{
        resetSimulation();
    }}

    running = true;

    const delay =
        Number(
            document.getElementById("speed").value
        );

    function nextEvent() {{

        if (!running) {{
            return;
        }}

        if (currentIndex >= snapshots.length) {{
            running = false;
            return;
        }}

        displaySnapshot(currentIndex);

        timer = setTimeout(
            nextEvent,
            delay
        );

    }}

    nextEvent();

}}


// -----------------------------------------
// Pause simulation
// -----------------------------------------

function pauseSimulation() {{

    running = false;

    if (timer) {{
        clearTimeout(timer);
    }}

}}


// -----------------------------------------
// Reset simulation
// -----------------------------------------

function resetSimulation() {{

    pauseSimulation();

    currentIndex = 0;

    document.getElementById(
        "progress"
    ).textContent =
        "0 / " +
        snapshots.length;

    document.getElementById(
        "resource-status"
    ).textContent =
        "AVAILABLE";

    const container =
        document.getElementById(
            "process-container"
        );

    container.innerHTML = "";

    actors.forEach(actor => {{

        const type =
            actor.includes("Reader")
            ? "Reader"
            : "Writer";

        const card =
            document.createElement("div");

        card.className =
            "process " +
            (type === "Reader"
                ? "reader"
                : "writer");

        card.innerHTML = `

            <div class="process-name">
                ${{actor}}
            </div>

            <div class="process-type">
                ${{type}}
            </div>

            <div class="process-state">
                IDLE
            </div>

        `;

        container.appendChild(card);

    }});

    renderEventLog();

}}


// -----------------------------------------
// Initial page
// -----------------------------------------

resetSimulation();

</script>

</body>

</html>
"""

    # -----------------------------------------
    # Write HTML file
    # -----------------------------------------

    with open(
        "readers_writers_semaphore.html",
        "w",
        encoding="utf-8"
    ) as file:

        file.write(html)

    print(
        "HTML simulation generated: "
        "readers_writers_semaphore.html"
    )
# -----------------------------
# Main program
# -----------------------------

def main():

    readers = [
        threading.Thread(target=reader, args=(1,)),
        threading.Thread(target=reader, args=(2,)),
        threading.Thread(target=reader, args=(3,))
    ]

    writers = [
        threading.Thread(target=writer, args=(1,))
    ]

    threads = readers + writers

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print("\nExecution completed.")
    print(f"Total events recorded: {len(events)}")
    
    generate_html()

if __name__ == "__main__":
    main()