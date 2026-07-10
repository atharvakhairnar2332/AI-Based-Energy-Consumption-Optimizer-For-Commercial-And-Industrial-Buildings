const browseButton = document.getElementById("browse-btn");
const fileInput = document.getElementById("dataset-file");
const selectedFile = document.getElementById("selected-file");
const sampleDatasetPath =
    "sample_sheets/SampleDatasets_.zip";
const analyzeButton = document.getElementById("analyze-btn");

const resultsSection =
    document.getElementById("results-section");

    const statusCircle =
    document.getElementById("status-circle");


const indoorTemp =
    document.getElementById("indoor-temp");

    const uploadArea =
    document.querySelector(".upload-area");

const indoorHumidity =
    document.getElementById("indoor-humidity");

    const downloadDatasetButton =
    document.getElementById("download-dataset-btn");
    

const outdoorTemp =
    document.getElementById("outdoor-temp");

const outdoorHumidity =
    document.getElementById("outdoor-humidity");

const analysisList =
    document.getElementById("analysis-list");

const fanStatus =
    document.getElementById("fan-status");

const statusIndicator =
    document.getElementById("status-indicator");

    const analysisUI =
    document.getElementById("analysis-ui");

const processingSection =
    document.getElementById("processing-section");

const recommendation =
    document.getElementById("recommendation-text");

window.addEventListener("DOMContentLoaded", () => {

    document.getElementById("error-box").style.display = "none";

});

// Browse File

browseButton.addEventListener("click", () => {

    fileInput.click();

});

fileInput.addEventListener("change", () => {

    if (fileInput.files.length > 0) {

        selectedFile.textContent =
            "Selected File: " +
            fileInput.files[0].name;

    }

    else {

        selectedFile.textContent =
            "No file selected";

    }

});

// Drag & Drop Upload

uploadArea.addEventListener("dragover", (e) => {

    e.preventDefault();

    uploadArea.style.borderColor = "#2563EB";

    uploadArea.style.background = "#EFF6FF";

});


uploadArea.addEventListener("dragleave", () => {

    uploadArea.style.borderColor = "";

    uploadArea.style.background = "";

});


uploadArea.addEventListener("drop", (e) => {

    e.preventDefault();

    uploadArea.style.borderColor = "";

    uploadArea.style.background = "";

    if (e.dataTransfer.files.length > 0) {

        fileInput.files = e.dataTransfer.files;

        selectedFile.textContent =
            "Selected File: " +
            fileInput.files[0].name;

    }

});

// Analyze

analyzeButton.addEventListener("click", () => {

    if (
        analyzeButton.textContent ===
        "Analyze Another Dataset"
    ) {

        resultsSection.hidden = true;

        processingSection.hidden = true;

        resultsSection.style.opacity = "0";
        analysisUI.hidden = false;

        fileInput.value = "";

        selectedFile.textContent =
            "No file selected";

        document.getElementById("error-box").style.display =
            "none";

        analyzeButton.textContent =
            "Analyze Dataset";

        return;

    }

    predictDataset();

});

// Main Prediction Function

async function predictDataset() {

    document.getElementById("error-box").style.display = "none";
resultsSection.hidden = true;


if (fileInput.files.length === 0) {

    processingSection.hidden = true;

analysisUI.hidden = false;

    const errorBox =
        document.getElementById("error-box");

    const errorTitle =
        document.getElementById("error-title");

    const errorMessage =
        document.getElementById("error-message");

    errorTitle.textContent =
        "No Dataset Selected";

    errorMessage.textContent =
        "Please select a CSV or Excel dataset before running the analysis.";

   processingSection.hidden = true;

   analysisUI.hidden = false;

   errorBox.style.display = "flex";

   return;

 }
   analysisUI.hidden = true;

   processingSection.hidden = false;
   processingSection.scrollIntoView({

    behavior: "smooth",

    block: "center"

});
   analyzeButton.textContent = "Analyzing...";
   analyzeButton.disabled = true;
   analyzeButton.classList.add("analyzing");

   analyzeButton.style.opacity = "0.6";
   analyzeButton.style.cursor = "not-allowed";



    const formData = new FormData();

    formData.append(
        "file",
        fileInput.files[0]
    );

    const occupancy = document.querySelector(
        'input[name="occupancy"]:checked'
    ).value;

    formData.append(
        "occupancy",
        occupancy === "occupied" ? 1 : 0
    );

    try {

        const fetchPromise = fetch(

    "http://127.0.0.1:8000/predict",

    {

        method: "POST",

        body: formData

    }

);

const animationPromise =
    runPipelineAnimation();

const response =
    await fetchPromise;

const data =
    await response.json();

if (!response.ok) {

    throw new Error(
        data.detail
    );

}

await animationPromise;

displayResults(data);

    }

catch (error) {

    processingSection.hidden = true;

    analysisUI.hidden = false;

    resultsSection.hidden = true;

    analyzeButton.disabled = false;

    analyzeButton.textContent =
        "Analyze Dataset";
    analyzeButton.classList.remove("analyzing");
        analyzeButton.disabled = false;

    analyzeButton.style.opacity = "1";
    analyzeButton.style.cursor = "pointer";


    const errorBox =
        document.getElementById("error-box");

    const errorTitle =
        document.getElementById("error-title");

    const errorMessage =
        document.getElementById("error-message");

    errorTitle.textContent =
        "Dataset Validation Failed";

    errorMessage.textContent =
        error.message;

   errorBox.style.display = "flex";

    errorBox.scrollIntoView({

        behavior: "smooth",

        block: "center"

    });

    console.error(error);
}
}

// Display Results

function displayResults(data) {

    console.log("displayResults() called");

    document.getElementById("error-box").style.display = "none";

    indoorTemp.textContent =
        data.future_environment.indoor_temp_C.toFixed(2) + " °C";

    indoorHumidity.textContent =
        data.future_environment.indoor_humidity.toFixed(2) + " %";

    outdoorTemp.textContent =
        data.future_environment.outdoor_temp_C.toFixed(2) + " °C";

    outdoorHumidity.textContent =
        data.future_environment.outdoor_humidity.toFixed(2) + " %";



    analysisList.innerHTML = "";

    data.decision.analysis.forEach(item => {

        const li =
            document.createElement("li");

        li.textContent = item;

        analysisList.appendChild(li);

    });

   fanStatus.textContent =
    data.decision.fan_status;

statusIndicator.textContent = "";

console.log("Fan Status:", data.decision.fan_status);

if (data.decision.fan_status.trim().toUpperCase() === "ON") {

   statusCircle.style.backgroundColor = "#DCFCE7";
   statusCircle.style.borderColor = "#22C55E";
   statusCircle.style.boxShadow = "0 0 12px rgba(34,197,94,.18)";

   statusIndicator.style.color = "#15803D";
   statusIndicator.textContent = "ON";

} else {

    statusCircle.style.backgroundColor = "#FEE2E2";
    statusCircle.style.borderColor = "#EF4444";
    statusCircle.style.boxShadow = "0 0 12px rgba(239,68,68,.18)";

    statusIndicator.style.color = "#B91C1C";
    statusIndicator.textContent = "OFF";

}


    if (data.decision.fan_status === "ON") {

        recommendation.textContent =
            "The AI recommends turning the fan ON based on the predicted future environmental conditions.";

    }

    else {

        recommendation.textContent =
            "The AI recommends keeping the fan OFF because the predicted future environmental conditions remain comfortable.";

    }



    resultsSection.hidden = false;
    setTimeout(() => {

    resultsSection.scrollIntoView({

        behavior: "smooth",

        block: "start"

    });

    }, 300);
    setTimeout(() => {

    resultsSection.style.opacity = "1";

    }, 100);

    analyzeButton.disabled = false;

    analyzeButton.textContent =
    "Analyze Another Dataset";
    analyzeButton.classList.remove("analyzing");
    analyzeButton.disabled = false;
    analyzeButton.style.opacity = "1";
    analyzeButton.style.cursor = "pointer";

}

function sleep(ms) {

    return new Promise(resolve => setTimeout(resolve, ms));

}

async function runPipelineAnimation() {

    const message =
        document.getElementById("processing-message");

    const steps = [

        "Uploading dataset...",

        "Validating dataset structure...",

        "Preprocessing input features...",

        "Forecasting future environment using LSTM...",

        "Optimizing fan decision using PPO...",

        "Generating energy optimization report...",

        "Analysis complete"

    ];

    for (let i = 0; i < steps.length; i++) {

    if (i === steps.length - 1) {

        message.style.transition = "none";

        message.textContent = steps[i];
        message.style.fontSize = "22px";
        message.style.fontWeight = "500";
        message.style.color = "#040303";

        message.style.transform = "scale(.7)";

        message.style.opacity = "0";

        message.offsetHeight;

        message.style.transition =
            "transform .3s ease, opacity .3s ease";

        message.style.transform = "scale(1)";

        message.style.opacity = "1";

        await sleep(900);

        break;

    }

    message.style.opacity = "0";

    message.style.transform = "translateY(30px)";

    await sleep(250);

    message.style.transition = "none";

    message.textContent = steps[i];

    message.style.transform = "translateY(-30px)";

    message.style.opacity = "0";

    message.offsetHeight;

    message.style.transition =
        "transform .45s ease, opacity .45s ease";

    message.style.transform = "translateY(0)";

    message.style.opacity = "1";

    await sleep(700);

    }

}

downloadDatasetButton.addEventListener("click", () => {

    const link =
        document.createElement("a");

    link.href =
        sampleDatasetPath;

    link.download =
        sampleDatasetPath.split("/").pop();

    document.body.appendChild(link);

    link.click();

    document.body.removeChild(link);

});