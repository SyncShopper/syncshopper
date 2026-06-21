console.log("[SyncShopper] background service worker loaded");

chrome.runtime.onInstalled.addListener(() => {
  console.log("[SyncShopper] extension installed");
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (!message) {
    return false;
  }

  if (message.type === "SYNC_SHOPPER_ANALYZE_DETECTION") {
    sendDetectionAnalyzeRequest(message, sendResponse);
    return true;
  }

  if (message.type !== "SYNC_SHOPPER_CAPTURE_VISIBLE_TAB") {
    return false;
  }

  if (!sender.tab || typeof sender.tab.windowId !== "number") {
    sendResponse({
      success: false,
      errorMessage: "No sender tab available for captureVisibleTab"
    });

    return false;
  }

  chrome.tabs.captureVisibleTab(
    sender.tab.windowId,
    { format: "png" },
    (dataUrl) => {
      if (chrome.runtime.lastError) {
        console.error("[SyncShopper] capture failed", chrome.runtime.lastError.message);

        sendResponse({
          success: false,
          errorMessage: chrome.runtime.lastError.message
        });

        return;
      }

      if (!dataUrl) {
        sendResponse({
          success: false,
          errorMessage: "No dataUrl returned from captureVisibleTab"
        });

        return;
      }

      sendResponse({
        success: true,
        dataUrl
      });
    }
  );

  return true;
});

async function sendDetectionAnalyzeRequest(message, sendResponse) {
  const { requestUrl, accessToken, requestBody } = message;

  if (!requestUrl || !accessToken || !requestBody) {
    sendResponse({
      success: false,
      errorMessage: "Missing detection request data"
    });
    return;
  }

  try {
    const response = await fetch(requestUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${accessToken}`
      },
      body: JSON.stringify(requestBody)
    });

    let result = null;
    const responseText = await response.text();

    if (responseText) {
      try {
        result = JSON.parse(responseText);
      } catch (error) {
        result = responseText;
      }
    }

    sendResponse({
      success: response.ok,
      status: response.status,
      result,
      errorMessage: response.ok ? null : `Request failed: ${response.status}`
    });
  } catch (error) {
    console.error("[SyncShopper] detection request failed", error);

    sendResponse({
      success: false,
      errorCode: "NETWORK_ERROR",
      errorMessage: error.message
    });
  }
}
