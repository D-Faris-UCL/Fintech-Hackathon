document.addEventListener("DOMContentLoaded", (event) => {
  // Fetch the JSON data
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

  setInterval(() => {
    fetch("http://127.0.0.1:5001/api/data")
      .then((response) => response.json())
      .then((data) => {
        for (const comapany in data) {
          const price = document.getElementById(`price${company}`);
          price.innerHTML = `${data[price]}`;
          const value = document.getElementById(`value${company}`);
          value.innerHTML = `${data[value]}`;
        }
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  }, 10000);

  // Update stock prices at intervals
});
