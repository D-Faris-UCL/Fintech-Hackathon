document.addEventListener("DOMContentLoaded", (event) => {
  alert("Hello World");
  let portfolio = [];

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

  let myESG = -1;
  let button = document.querySelector(".stock");

  // Button click event to fetch stock data
  button.addEventListener("click", () => {
    let symbol = document.querySelector("#symbol").value;
    let amount = parseFloat(document.querySelector("#amount").value);

    const url = `https://yahoo-finance15.p.rapidapi.com/api/yahoo/qu/quote/${symbol}`;
    const options = {
      method: "GET",
      headers: {
        "X-RapidAPI-Key": "fedc9dcd3msh5943cc43b56134fp14ce94jsn5d0d45ca8d6c",
        "X-RapidAPI-Host": "yahoo-finance15.p.rapidapi.com",
      },
    };

    fetch(url, options)
      .then((response) => response.json())
      .then((data) => {
        if (!data.quoteResponse.result.length) {
          alert("No data found for the entered stock symbol.");
          return;
        }

        const stockData = data.quoteResponse.result[0]; // Correct data access
        const price = stockData.regularMarketPrice || 0;
        const name = stockData.longName || "Unknown Stock";

        // Update table with stock data
        let table = document.querySelector(".table");
        let row = document.createElement("tr");
        let cell1 = document.createElement("td");
        let cell2 = document.createElement("td");
        let cell3 = document.createElement("td");
        let cell4 = document.createElement("td");
        let cell5 = document.createElement("td");
        let cell6 = document.createElement("td");

        cell1.innerHTML = symbol;
        cell2.innerHTML = name;
        cell3.innerHTML = price;
        cell4.innerHTML = amount;
        cell5.innerHTML = amount * price;
        cell6.innerHTML = "Fetching ESG..."; // Placeholder for ESG

        row.appendChild(cell1);
        row.appendChild(cell2);
        row.appendChild(cell3);
        row.appendChild(cell4);
        row.appendChild(cell5);
        row.appendChild(cell6);
        table.appendChild(row);

        // Fetch ESG data
        fetch("static/combined_data.json")
          .then((response) => response.json())
          .then((esgData) => {
            for (const company in esgData) {
              if (company === symbol) {
                let esg = esgData[company].esg || "No ESG data";
                cell6.innerHTML = esg;
                myESG += esgData[company].esg || 0; // Add ESG to total score
              }
            }
            updateESGDisplay(myESG);
          });

        cell3.setAttribute("id", `${symbol}price`); // Use backticks for string interpolation

        portfolio.push(symbol);
      })
      .catch((error) => console.error("Error fetching stock data:", error));
  });

  // Function to update the ESG display
  const updateESGDisplay = (myESG) => {
    let ESGdisplay = document.querySelector(".myESG");
    if (myESG > 0 && myESG < 10) {
      ESGdisplay.setAttribute("style", "color: green");
      ESGdisplay.innerHTML = myESG;
    } else if (myESG > 10 && myESG < 25) {
      ESGdisplay.setAttribute("style", "color: yellow");
      ESGdisplay.innerHTML = myESG;
    } else if (myESG > 25) {
      ESGdisplay.setAttribute("style", "color: red");
      ESGdisplay.innerHTML = myESG;
    } else {
      ESGdisplay.innerHTML = "No ESG data available";
    }
  };

  // Update stock prices at intervals
  setInterval(() => {
    for (let i = 0; i < portfolio.length; i++) {
      let url = `https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=${portfolio[i]}&interval=5min&apikey=7KXZE5DT8SYQ4UCT`;
      fetch(url)
        .then((response) => response.json())
        .then((data) => {
          let time = data["Meta Data"]["3. Last Refreshed"];
          let price = data["Time Series (5min)"][time]["4. close"];
          let cell3 = document.querySelector(`#${portfolio[i]}price`);
          cell3.innerHTML = price;
        })
        .catch((error) => console.error("Error fetching price data:", error));
    }
  }, 5000); // Updated interval to 5 seconds to avoid overloading
});
