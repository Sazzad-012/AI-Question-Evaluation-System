const evaluateBtn = document.getElementById("evaluateBtn");

evaluateBtn.addEventListener("click", function () {
  const course = document.getElementById("course").value;
  const clo = document.getElementById("clo").value;
  const objectives = document.getElementById("objectives").value;
  const targets = document.getElementById("targets").value;
  const paper = document.getElementById("paper").value;

  if (
    course.trim() === "" ||
    clo.trim() === "" ||
    targets.trim() === "" ||
    paper.trim() === ""
  ) {
    alert("Please fill in all required fields!");
    return;
  }

  alert("Question paper information collected successfully!");

  console.log("Course:", course);
  console.log("Course Learning Outcomes:", clo);
  console.log("Programming Objectives:", objectives);
  console.log("Target Distribution:", targets);
  console.log("Question Paper:", paper);
});
