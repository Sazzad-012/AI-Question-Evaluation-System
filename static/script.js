let isProcessing = false;
let cooldownActive = false;

document
  .getElementById("evaluationForm")
  .addEventListener("submit", async function (event) {
    event.preventDefault();

    if (isProcessing || cooldownActive) {
      return;
    }

    const form = document.getElementById("evaluationForm");
    const button = document.getElementById("evaluateBtn");
    const formData = new FormData(form);

    isProcessing = true;
    button.disabled = true;
    button.textContent = "Evaluating... Please wait";

    try {
      const response = await fetch("/evaluate", {
        method: "POST",
        body: formData,
      });

      const result = await response.json();

      if (!response.ok) {
        alert(result.error || "Evaluation failed!");
        return;
      }

      const resultDiv = document.getElementById("result");

      resultDiv.innerHTML = DOMPurify.sanitize(
        marked.parse(result.evaluation_report),
      );

      resultDiv.style.display = "block";
      alert("Evaluation completed successfully!");
    } catch (error) {
      alert("Unable to connect to the server. Please try again.");
      console.log(error);
    } finally {
      isProcessing = false;
      cooldownActive = true;

      let remainingTime = 60;

      button.textContent = `Please wait ${remainingTime}s`;

      const countdown = setInterval(function () {
        remainingTime--;

        if (remainingTime > 0) {
          button.textContent = `Please wait ${remainingTime}s`;
        } else {
          clearInterval(countdown);
          cooldownActive = false;
          button.disabled = false;
          button.textContent = "Evaluate Question Paper";
        }
      }, 1000);
    }
  });
