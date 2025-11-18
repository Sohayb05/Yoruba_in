const form = document.getElementById("dream-form");
const resultEl = document.getElementById("result");
const button = document.getElementById("interpret-btn");

const setLoading = (isLoading) => {
  button.disabled = isLoading;
  button.textContent = isLoading ? "Interpreting..." : "Interpret dream";
  if (isLoading) {
    resultEl.innerHTML = `
      <div class="loader" role="status" aria-live="polite">
        <span></span><span></span><span></span>
      </div>`;
  }
};

const renderResult = (content) => {
  resultEl.innerHTML = `<p>${content}</p>`;
};

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const dream = new FormData(form).get("dream").trim();

  if (!dream) {
    renderResult("Please share your dream.");
    return;
  }

  setLoading(true);

  try {
    const response = await fetch("/api/interpret", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ dream }),
    });

    if (!response.ok) {
      throw new Error("Failed to interpret dream");
    }

    const data = await response.json();
    renderResult(data.interpretation || "No interpretation available.");
  } catch (error) {
    console.error(error);
    renderResult(
      "We could not reach the interpreter. Please try again in a moment."
    );
  } finally {
    setLoading(false);
  }
});
