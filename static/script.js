document
  .getElementById("evaluateBtn")
  .addEventListener("click", async function () {
    const course = document.getElementById("course").value;
    const clo = document.getElementById("clo").value;
    const objectives = document.getElementById("objectives").value;
    const targets = document.getElementById("targets").value;
    const paper = document.getElementById("paper").value;

    if (course === "" || clo === "" || targets === "" || paper === "") {
      alert("Please fill in all required fields!");
      return;
    }

    const data = {
      course: course,
      clo: clo,
      objectives: objectives,
      targets: targets,
      paper: paper,
    };

    try {
      const response = await fetch("/evaluate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      const result = await response.json();

      alert(result.message);

      console.log("Backend Response:", result);
    } catch (error) {
      alert("Something went wrong!");
      console.log(error);
    }
  });
