// ==============================
// Admin Dashboard JS (Chart + Toggle + Dynamic Updates)
// ==============================

let chartType = "bar";
let chartInstance = null;

// Initialize chart when page loads
document.addEventListener("DOMContentLoaded", () => {
    const ctx = document.getElementById("teacherRatingsChart");
    if (!ctx) return;

    // Get data injected from Jinja (global variables)
    const teacherNames = window.teacherData?.names || [];
    const avgRatings = window.teacherData?.ratings || [];

    // Render chart
    renderChart(ctx, chartType, teacherNames, avgRatings);

    // Hook up toggle button
    const toggleBtn = document.getElementById("toggleChartBtn");
    if (toggleBtn) {
        toggleBtn.addEventListener("click", () => toggleChartType(ctx, teacherNames, avgRatings));
    }
});

// ----------------------------
// Render Chart Function
// ----------------------------
function renderChart(ctx, type, teacherNames, avgRatings) {
    if (chartInstance) {
        chartInstance.destroy();
    }

    const backgroundColors =
        type === "bar"
            ? ["rgba(79, 70, 229, 0.6)"]
            : [
                  "#4f46e5",
                  "#6366f1",
                  "#818cf8",
                  "#a5b4fc",
                  "#c7d2fe",
                  "#e0e7ff",
              ];

    chartInstance = new Chart(ctx, {
        type: type,
        data: {
            labels: teacherNames,
            datasets: [
                {
                    label: "Average Rating",
                    data: avgRatings,
                    backgroundColor: backgroundColors,
                    borderColor: type === "bar" ? "rgba(79, 70, 229, 1)" : "transparent",
                    borderWidth: 1,
                },
            ],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: {
                duration: 800,
                easing: "easeOutQuart",
            },
            scales: type === "bar"
                ? {
                      y: {
                          beginAtZero: true,
                          max: 5,
                          ticks: { color: "#555" },
                          grid: { color: "#eee" },
                      },
                      x: {
                          ticks: { color: "#555" },
                          grid: { color: "transparent" },
                      },
                  }
                : {},
            plugins: {
                legend: {
                    display: type === "pie",
                    labels: { color: "#444" },
                },
                tooltip: {
                    backgroundColor: "#4f46e5",
                    titleColor: "#fff",
                    bodyColor: "#fff",
                },
            },
        },
    });
}

// ----------------------------
// Toggle Chart Type
// ----------------------------
function toggleChartType(ctx, teacherNames, avgRatings) {
    chartType = chartType === "bar" ? "pie" : "bar";
    renderChart(ctx, chartType, teacherNames, avgRatings);
}

// ----------------------------
// AJAX Loader (Optional Future Upgrade)
// ----------------------------
// If you ever want class dropdown to load data dynamically
// without full page reload, this section can be activated.
/*
document.querySelector("#classSelect")?.addEventListener("change", async (e) => {
    const classId = e.target.value;
    const res = await fetch(`/admin/get-insights/${classId}`);
    const data = await res.json();

    // Update chart data dynamically
    renderChart(
        document.getElementById("teacherRatingsChart"),
        chartType,
        data.teacherNames,
        data.avgRatings
    );

    // Update summary stats
    document.getElementById("totalTeachers").textContent = data.summary.total_teachers;
    document.getElementById("totalStudents").textContent = data.summary.total_students;
    document.getElementById("totalFeedbacks").textContent = data.summary.total_feedbacks;
});
*/

// ======================
// Sidebar Toggle Logic
// ======================
document.addEventListener("DOMContentLoaded", () => {
    const sidebar = document.querySelector(".sidebar");
    const overlay = document.querySelector(".sidebar-overlay");
    const toggleButton = document.querySelector(".menu-toggle");

    if (!sidebar || !overlay || !toggleButton) return;

    toggleButton.addEventListener("click", () => {
        sidebar.classList.toggle("active");
        overlay.classList.toggle("active");
        document.body.classList.toggle("sidebar-open");
    });

    overlay.addEventListener("click", () => {
        sidebar.classList.remove("active");
        overlay.classList.remove("active");
        document.body.classList.remove("sidebar-open");
    });
});