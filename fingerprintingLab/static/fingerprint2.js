
(function () {
  
  const target     = document.getElementById("target-sentence").textContent.trim();
  const input      = document.getElementById("typing-input");
  const restartBtn = document.getElementById("restart-button");
  const timeOut    = document.getElementById("result-time");
  const speedOut   = document.getElementById("result-speed");
  const corrOut    = document.getElementById("result-corrections");

  let startTime   = null;  
  let corrections = 0;      
  let finished    = false;  

  
  input.addEventListener("keydown", function (event) {
    if (finished) return;

   
    if (startTime === null && event.key.length === 1) {
      startTime = performance.now();
      console.log("Timer started");
    }

    if (startTime !== null && (event.key === "Backspace" || event.key === "Delete")) {
      corrections++;
      console.log("Correction #" + corrections);
    }
  });

  
  input.addEventListener("input", function () {
    if (finished || startTime === null) return;

    if (input.value === target) {
      finished = true;

     
      const seconds = (performance.now() - startTime) / 1000;
      const wpm     = (target.length / 5) / (seconds / 60);
      const cpm     = target.length / (seconds / 60);

      
      timeOut.textContent  = seconds.toFixed(2) + " s";
      speedOut.textContent = wpm.toFixed(2) + " WPM ";
      corrOut.textContent  = corrections;
      input.disabled = true;

      
      const behaviour = {
        type:        "typing",
        typingTime:  Number(seconds.toFixed(2)),
        typingSpeed: Number(wpm.toFixed(2)),
        corrections: corrections,
        sentenceLength: target.length,
      };
      console.log("Sending behaviour:", behaviour);

      fetch("/collect", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(behaviour),
      });
    }
  });


  restartBtn.addEventListener("click", function () {
    startTime = null;
    corrections = 0;
    finished = false;
    input.value = "";
    input.disabled = false;
    timeOut.textContent = speedOut.textContent = corrOut.textContent = "";
    input.focus();
  });
})();