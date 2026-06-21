document.addEventListener("DOMContentLoaded", () => {
  const backendBaseUrlInput = document.getElementById("backendBaseUrl");
  const accessTokenInput = document.getElementById("accessToken");
  const saveButton = document.getElementById("saveButton");
  const statusMessage = document.getElementById("statusMessage");

  chrome.storage.local.get(["backendBaseUrl", "accessToken"], (result) => {
    backendBaseUrlInput.value = result.backendBaseUrl || "http://localhost:8080";
    accessTokenInput.value = result.accessToken || "";
  });

  saveButton.addEventListener("click", () => {
    const backendBaseUrl = backendBaseUrlInput.value.trim();
    const accessToken = accessTokenInput.value.trim();

    if (!backendBaseUrl) {
      statusMessage.textContent = "\uBC31\uC5D4\uB4DC \uC8FC\uC18C\uB97C \uC785\uB825\uD574\uC8FC\uC138\uC694.";
      statusMessage.style.color = "#dc2626";
      return;
    }

    if (!accessToken) {
      statusMessage.textContent = "Access Token\uC744 \uC785\uB825\uD574\uC8FC\uC138\uC694.";
      statusMessage.style.color = "#dc2626";
      return;
    }

    chrome.storage.local.set(
      {
        backendBaseUrl,
        accessToken
      },
      () => {
        statusMessage.textContent = "\uC124\uC815\uC774 \uC800\uC7A5\uB418\uC5C8\uC2B5\uB2C8\uB2E4.";
        statusMessage.style.color = "#16a34a";
      }
    );
  });
});
