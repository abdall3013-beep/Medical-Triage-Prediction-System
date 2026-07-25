// ===============================
// Medical Triage Dashboard
// ===============================

const API_URL = "http://127.0.0.1:5000/predict";

// ===============================
// Elements
// ===============================

const predictBtn = document.getElementById("predictBtn");
const resetBtn = document.getElementById("resetBtn");
const spinner = document.getElementById("spinner");

const prediction = document.getElementById("prediction");
const priority = document.getElementById("priority");
const recommendation = document.getElementById("recommendation");
const predictionTime = document.getElementById("predictionTime");

const totalCases = document.getElementById("totalCases");
const highCases = document.getElementById("highCases");
const mediumCases = document.getElementById("mediumCases");
const lowCases = document.getElementById("lowCases");

const themeBtn = document.getElementById("themeBtn");

// ===============================
// History
// ===============================
let history = [];

const API = "http://127.0.0.1:5000";


// ===============================
// Statistics
// ===============================

function updateStatistics() {

    totalCases.textContent = history.length;

    highCases.textContent =
        history.filter(x => x.priority === "HIGH").length;

    mediumCases.textContent =
        history.filter(x => x.priority === "MEDIUM").length;

    lowCases.textContent =
        history.filter(x => x.priority === "LOW").length;

}

updateStatistics();
async function loadDashboardStats() {

    try {

        const response = await fetch(`${API}/history`);

        history = await response.json();

        updateStatistics();


        updateChart();
        updateRecentPatients();

    }

    catch (err) {

        console.log(err);

    }

}

// ===============================
// Chart
// ===============================

const ctx = document
.getElementById("triageChart")
.getContext("2d");

const triageChart = new Chart(ctx, {

    type: "doughnut",

    data: {

        labels: [

            "High",

            "Medium",

            "Low"

        ],

        datasets: [

            {

                data: [

                    0,

                    0,

                    0

                ],

                backgroundColor: [

                    "#ef4444",

                    "#f59e0b",

                    "#22c55e"

                ],

                borderWidth:0

            }

        ]

    },

    options:{

        responsive:true,

        plugins:{

            legend:{

                labels:{

                    color:"white"

                }

            }

        }

    }

});

function updateChart(){

    triageChart.data.datasets[0].data=[

        history.filter(x=>x.priority==="HIGH").length,

        history.filter(x=>x.priority==="MEDIUM").length,

        history.filter(x=>x.priority==="LOW").length

    ];

    triageChart.update();

}

updateChart();
function updateRecentPatients() {

    const tbody = document.getElementById("recentPatients");

    if (!tbody) return;

    tbody.innerHTML = "";

    history.slice(0,5).forEach(patient => {

        tbody.innerHTML += `

        <tr>

            <td>${patient.id}</td>

            <td>${patient.age}</td>

            <td>${patient.priority}</td>

            <td>${patient.created_at}</td>

        </tr>

        `;

    });

}

// ===============================
// Dark Mode
// ===============================

themeBtn.onclick=()=>{

    document.body.classList.toggle("dark");

};

// ===============================
// Reset
// ===============================

resetBtn.onclick=()=>{

    document
    .querySelectorAll("input")
    .forEach(input=>input.value="");

    document
    .querySelector("select")
    .selectedIndex=0;

    prediction.innerHTML="Waiting...";

    priority.innerHTML="--";

    recommendation.innerHTML="Fill patient information then press Predict.";

    predictionTime.innerHTML="";

};
// ===============================
// Predict
// ===============================

predictBtn.onclick = async () => {

    if (!validateInputs()) return;

    spinner.style.display = "block";

    predictBtn.disabled = true;

    

    spinner.style.display = "block";

    predictBtn.disabled = true;

    try {

        const patient = {

            age: Number(document.getElementById("age").value),

            heart_rate: Number(document.getElementById("heart_rate").value),

            systolic_blood_pressure: Number(document.getElementById("systolic_blood_pressure").value),

            oxygen_saturation: Number(document.getElementById("oxygen_saturation").value),

            body_temperature: Number(document.getElementById("body_temperature").value),

            pain_level: Number(document.getElementById("pain_level").value),

            chronic_disease_count: Number(document.getElementById("chronic_disease_count").value),

            previous_er_visits: Number(document.getElementById("previous_er_visits").value),

            arrival_mode: Number(document.getElementById("arrival_mode").value)

        };

        const response = await fetch(API_URL, {

    method: "POST",

    headers: {

        "Content-Type": "application/json"

    },

    body: JSON.stringify(patient)

});

if (!response.ok) {

    throw new Error(`HTTP Error: ${response.status}`);

}

const result = await response.json();

        spinner.style.display = "none";

        predictBtn.disabled = false;

        prediction.innerHTML = result.prediction;

        priority.innerHTML = result.priority;

        recommendation.innerHTML = result.recommendation;

        predictionTime.innerHTML =
            "Prediction Time : " + result.time;

        const circle = document.querySelector(".prediction-circle");

        if(result.priority==="HIGH"){

            circle.style.background="linear-gradient(135deg,#ef4444,#dc2626)";

            priority.style.color="#ef4444";

        }

        else if(result.priority==="MEDIUM"){

            circle.style.background="linear-gradient(135deg,#f59e0b,#d97706)";

            priority.style.color="#f59e0b";

        }

        else{

            circle.style.background="linear-gradient(135deg,#22c55e,#16a34a)";

            priority.style.color="#22c55e";

        }

      await loadDashboardStats();

    }

    catch(error){

    spinner.style.display = "none";

    predictBtn.disabled = false;

    console.error(error);

    showToast(
        "Error: " + error.message,
        "error"
    );

}

};
// ===============================
// Toast Notification
// ===============================

function showToast(message, type = "success") {

    const toast = document.createElement("div");

    toast.className = "toast";

    if (type === "error") {

        toast.style.background = "#ef4444";

    } else {

        toast.style.background = "#22c55e";

    }

    toast.innerHTML = `
        <i class="fa-solid fa-circle-check"></i>
        ${message}
    `;

    document.body.appendChild(toast);

    setTimeout(() => {

        toast.classList.add("show");

    }, 100);

    setTimeout(() => {

        toast.classList.remove("show");

        setTimeout(() => {

            toast.remove();

        }, 500);

    }, 3000);

}

// ===============================
// Validation
// ===============================

function validateInputs() {

    const inputs = document.querySelectorAll("input");

    for (let input of inputs) {

        if (input.value === "") {

            showToast("Please fill all fields.", "error");

            input.focus();

            return false;

        }

    }

    return true;

}

// ===============================
// Button Animation
// ===============================

predictBtn.addEventListener("mouseenter", () => {

    predictBtn.style.transform = "scale(1.05)";

});

predictBtn.addEventListener("mouseleave", () => {

    predictBtn.style.transform = "scale(1)";

});

// ===============================
// Fade In Cards
// ===============================

const cards = document.querySelectorAll(".card");

const observer = new IntersectionObserver((entries) => {

    entries.forEach(entry => {

        if (entry.isIntersecting) {

            entry.target.style.opacity = "1";

            entry.target.style.transform = "translateY(0)";

        }

    });

});

cards.forEach(card => {

    card.style.opacity = "0";

    card.style.transform = "translateY(40px)";

    card.style.transition = ".7s";

    observer.observe(card);

});

// ===============================
// Welcome Toast
// ===============================

window.onload = () => {

    loadDashboardStats();

    showToast("Medical Triage Dashboard Loaded");

};