document.getElementById("generate-schedules").addEventListener("click", async () => {
    const courseInput = document.getElementById("course-input").value;
    const courseList = courseInput.split(",").map(course => course.trim());

    try {
        const response = await fetch("http://127.0.0.1:5000/generate_schedules", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ courses: courseList })
        });

        const data = await response.json();
        if (data.status === "success") {
            populateSchedule("dp", data.dp_schedule);
            populateSchedule("greedy", data.greedy_schedule);

            // Update credit counters
            document.getElementById("dp-credits").textContent = data.dp_credits;
            document.getElementById("greedy-credits").textContent = data.greedy_credits;
        } else {
            alert("Error: " + data.message);
        }
    } catch (error) {
        console.error("Error generating schedules:", error);
    }
});

function populateSchedule(algoType, schedule) {
    for (const [day, classes] of Object.entries(schedule)) {
        classes.forEach(cls => {
            const cellId = `${algoType}-${day}-period-${cls.start_period}`;
            const cell = document.getElementById(cellId);
            if (cell) {
                cell.textContent = cls.class_name; // Populate the cell with the class name
            }
        });
    }
}
