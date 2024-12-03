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
            clearSchedule();
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

function clearSchedule() {
    const rows = document.querySelectorAll("#greedy-table tr, #dp-table tr");

    rows.forEach(row => {
        const cells = row.querySelectorAll('td');
        
        for (let i = 1; i < cells.length; i++) {
            cells[i].textContent = '';
        }
    });

    console.log("Table cleared")
}

function populateSchedule(algoType, schedule) {

    for (const [day, classes] of Object.entries(schedule)) {
        classes.forEach(cls => {
            cellId = `${algoType}-${day}-period-${cls.start_period}`;
            cell = document.getElementById(cellId);
            if (cell) {
                cell.textContent = cls.class_name; // Populate the cell with the class name
            }
            if (cls.start_period != cls.end_period) {
                cellId = `${algoType}-${day}-period-${cls.end_period}`;
                cell = document.getElementById(cellId);
                if (cell) {
                    cell.textContent = cls.class_name; // Populate the cell with the class name
                }
            }
        });
    }
}
