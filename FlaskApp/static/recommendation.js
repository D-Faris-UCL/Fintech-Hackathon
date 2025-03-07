document.addEventListener("DOMContentLoaded", (event) => {
    let slider_sustainability = document.getElementById("sustainability");
    let p_sustainability = document.getElementById("p_sustainability");
    p_sustainability.innerHTML = `Sustainability: ${slider_sustainability.value}`;
    // Update the current slider value (each time you drag the slider handle)
    slider_sustainability.oninput = function(){
        p_sustainability.innerHTML = `Sustainability: ${this.value}`;
    }

    let slider_returns = document.getElementById("returns");
    let p_returns = document.getElementById("p_returns");
    p_returns.innerHTML = `Returns: ${slider_returns.value}`;
    // Update the current slider value (each time you drag the slider handle)
    slider_returns.oninput = function(){
        p_returns.innerHTML = `Returns: ${this.value}`;
    }
    let slider_risk = document.getElementById("risk");
    let p_risk = document.getElementById("p_risk");
    p_risk.innerHTML = `Risk: ${slider_risk.value}`;
    // Update the current slider value (each time you drag the slider handle)
    slider_risk.oninput = function(){
        p_risk.innerHTML = `Risk: ${this.value}`;
    }

    const recommendations = document.querySelectorAll(".recommendation");
    recommendations.forEach((recommendation) => {
        recommendation.addEventListener("click", (event) => {
            value = event.target.value;
            console.log(value);
            description = document.querySelector(`#${value}`);
            console.log(description);
            if (description.classList.contains("hidden")) {
                description.classList.remove("hidden");
            } else {
                description.classList.add("hidden");
            }
        });
    });
    fetch("static/combined_data.json")
    .then((response) => response.json())
    .then((data) => {
      const datalist = document.getElementById("datalistOptions");
      // Generate HTML dynamically
      for (const company in data) {
        const dataoption = document.createElement("option");
        dataoption.setAttribute("value", `${company}`);
        datalist.appendChild(dataoption);
      }
    })
    .catch((error) => console.error("Error fetching data:", error));



});