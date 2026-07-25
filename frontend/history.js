const API = "http://127.0.0.1:5000";

const tableBody = document.getElementById("tableBody");
const searchInput = document.getElementById("searchInput");
const refreshBtn = document.getElementById("refreshBtn");
const clearBtn = document.getElementById("clearBtn");

let patients = [];

// ===============================
// Load Data
// ===============================

async function loadHistory() {

    try {

        const response = await fetch(`${API}/history`);

        patients = await response.json();

        renderTable(patients);

    }

    catch (error) {

        console.log(error);

        alert("Cannot connect to Backend.");

    }

}

// ===============================
// Render Table
// ===============================

function renderTable(data) {

    tableBody.innerHTML = "";

    data.forEach(patient => {

        let colorClass = "";

        if (patient.priority === "HIGH")
            colorClass = "high";

        else if (patient.priority === "MEDIUM")
            colorClass = "medium";

        else
            colorClass = "low";

        tableBody.innerHTML += `

        <tr>

            <td>${patient.id}</td>

            <td>${patient.age}</td>

            <td class="${colorClass}">
                ${patient.priority}
            </td>

            <td>${patient.prediction}</td>

            <td>${patient.heart_rate}</td>

            <td>${patient.systolic_blood_pressure}</td>

            <td>${patient.created_at}</td>

            <td>

                <button
                    class="delete-btn"
                    onclick="deletePatient(${patient.id})">

                    Delete

                </button>

            </td>

        </tr>

        `;

    });

}

// ===============================
// Delete Patient
// ===============================

async function deletePatient(id) {

    if (!confirm("Delete this patient?"))
        return;

    await fetch(`${API}/history/${id}`, {

        method: "DELETE"

    });

    loadHistory();

}

// ===============================
// Clear Database
// ===============================

clearBtn.onclick = async () => {

    if (!confirm("Delete ALL patients?"))
        return;

    await fetch(`${API}/history`, {

        method: "DELETE"

    });

    loadHistory();

};

// ===============================
// Refresh
// ===============================

refreshBtn.onclick = () => {

    loadHistory();

};

// ===============================
// Search
// ===============================

searchInput.onkeyup = () => {

    const keyword = searchInput.value.toLowerCase();

    const filtered = patients.filter(patient =>

        patient.priority.toLowerCase().includes(keyword)

    );

    renderTable(filtered);

};

// ===============================
// Start
// ===============================

loadHistory();