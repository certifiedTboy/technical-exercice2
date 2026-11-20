const textInput = document.getElementById("textInput");
const summarizeButton = document.getElementById("summarizeButton");
const summaryOutput = document.getElementById("summaryOutput");
const statusBox = document.getElementById("status");

async function summarizeText() {
  statusBox.textContent = "";
  const text = textInput.value.trim();

  if (!text) {
    summaryOutput.textContent = "Please enter some text first.";
    return;
  }

  summarizeButton.disabled = true;
  statusBox.textContent = "Generating summary...";
  statusBox.classList.remove("error");

  try {
    // TODO 4:
    // Send the user's text to the backend API.
    const response = await fetch("http://127.0.0.1:8000/api/summarize", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error("something went wrong");
    }
    const data = await response.json();

    // TODO 5:
    // Process the API response and display the generated summary.

    if (data && data?.result && data?.result?.content) {
      summaryOutput.textContent = data?.result?.content;
    } else {
      throw new Error("something went wrong");
    }
  } catch (error) {
    console.error(error.message);
    statusBox.textContent = "Something went wrong. Please try again.";
    statusBox.classList.add("error");
  } finally {
    summarizeButton.disabled = false;
  }
}

summarizeButton.addEventListener("click", summarizeText);
