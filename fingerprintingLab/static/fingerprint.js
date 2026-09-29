

const features = {
  
  language:            navigator.language,
  languages:           navigator.languages.join(", "),
  userAgent:           navigator.userAgent,
  platform:            navigator.platform,
  hardwareConcurrency: navigator.hardwareConcurrency,        
  deviceMemory:        navigator.deviceMemory ?? "unavailable", 


  screenResolution:    screen.width + "x" + screen.height,
  availableScreen:     screen.availWidth + "x" + screen.availHeight,
  colorDepth:          screen.colorDepth,


  windowSize:          window.innerWidth + "x" + window.innerHeight,
  devicePixelRatio:    window.devicePixelRatio,                 // zoom / Retina scaling


  timeZone:            Intl.DateTimeFormat().resolvedOptions().timeZone,
  locale:              Intl.DateTimeFormat().resolvedOptions().locale,


  referrer:            document.referrer || "(none)",
};


console.log("Active features:", features);

//  Display the values inside the webpage
const outputElement = document.getElementById("feature-output");
outputElement.innerHTML = Object.entries(features)
  .map(([key, value]) => `<tr><th>${key}</th><td>${value}</td></tr>`)
  .join("");

//  Send the collected features to the Flask server
fetch("/collect", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ type: "active", features: features }),
});