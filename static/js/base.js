// Base functionality for NornNet application

// Determine base path so app works at site root and under /nornnet
function getBasePath() {
  const path = window.location.pathname || '';
  return path.startsWith('/nornnet') ? '/nornnet' : '';
}

// Load available AI models into header dropdown
async function loadModels() {
  try {
    const response = await fetch(`${getBasePath()}/models`);
    const data = await response.json();
    const modelSelect = document.getElementById("model_select");

    if (modelSelect && data.models && data.models.length > 0) {
      modelSelect.innerHTML = "";

      // Sort models: default model first, then alphabetically
      const defaultModel = data.default || "llama3.1:8b-instruct-q4_K_M";
      const sortedModels = data.models.sort((a, b) => {
        if (a === defaultModel) return -1;
        if (b === defaultModel) return 1;
        return a.localeCompare(b);
      });

      sortedModels.forEach(model => {
        const option = document.createElement("option");
        option.value = model;
        option.textContent = model;
        if (model === defaultModel) {
          option.selected = true;
        }
        modelSelect.appendChild(option);
      });
    }
  } catch (error) {
    console.error("Error loading models:", error);
  }
}

// ---------------- Dark Mode Toggle ----------------
function initDarkMode() {
  const darkModeToggle = document.getElementById("darkModeToggle");
  if (darkModeToggle) {
    darkModeToggle.addEventListener("click", () => {
      document.body.classList.toggle("dark-mode");
      if (document.body.classList.contains("dark-mode")) {
        darkModeToggle.textContent = "☀️ Light Mode";
      } else {
        darkModeToggle.textContent = "🌙 Dark Mode";
      }
    });
  }
}

// Initialize on page load
document.addEventListener("DOMContentLoaded", () => {
  loadModels();
  initDarkMode();
});
