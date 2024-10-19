document.addEventListener("DOMContentLoaded", (event) => {

  alert("Hello World")
    let portfolio = [];
  // Fetch the JSON data
  fetch("static/combined_data.json")
    .then((response) => response.json())
    .then((data) => {
      const datalist = document.getElementById("datalistOptions");
      // Generate HTML dynamically
      data.forEacompany) => {
        const dataoption = document.createElement("option");
        dataoption.setAttribute("value", `${company.symbol}`);
        datalist.appendChild(dataoption);
      });
    })
    .catch((error) => console.error("Error fetching data:", error));
  let myESG = -1;
  let button = document.querySelector(".stock");
  button.addEventListener("click", () => {
    let symbol = document.querySelector("#symbol").value;
    let amount = document.querySelector("#amount").value;
    let url = `https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=${symbol}&interval=5min&apikey=7KXZE5DT8SYQ4UCT`;
    fetch(url)
      .then((response) => response.json())
      .then((data) => {
        const table = document.getElementById("table");
        const row = document.createElement("tr");
        const cell1 = document.createElement("td");
        const cell2 = document.createElement("td");
        const cell3 = document.createElement("td");
        const cell4 = document.createElement("td");
        const cell5 = document.createElement("td");
        let name = data["Meta Data"]["8. Name"];
        let time = data["Meta Data"]["3. Last Refreshed"];
        let price = data["Time Series (5min)"][time]["4. close"];

        portfolio.push(symbol);

        fetch("static/combined_data.json")
          .then((response) => response.json())
          .then((data) => {
            data.forEach((company) => {
              if (company.symbol === symbol) {
                let esg = company.esg;
                myESG += esg;
              }
            });
          });
        
        cell1.innerHTML = input;
        cell2.innerHTML = name;
        cell3.innerHTML = price;
        cell4.innerHTML = amount;
        cell5.innerHTML = esg;

        cell3.setAttribute("id", `${symbol}price`);

        row.appendChild(cell1);
        row.appendChild(cell2);
        row.appendChild(cell3);
        row.appendChild(cell4);
        row.appendChild(cell5);
        table.appendChild(row);
      })
      .catch((error) => console.error("Error fetching data:", error));
  });
  let ESGdisplay = document.querySelector(".myESG");
  if(myESG > 0 && myESG < 10){
    ESGdisplay.setAttribute("style", "color: green");
    ESGdisplay.innerHTML = myESG;
  } else if(myESG > 10 && myESG < 25){
    ESGdisplay.setAttribute("style", "color: yellow");
    ESGdisplay.innerHTML = myESG;
  } else if(myESG > 25){
    ESGdisplay.setAttribute("style", "color: red");
    ESGdisplay.innerHTML = myESG;
  }
  
  else{
    ESGdisplay.innerHTML = "No ESG data available";
  }

  setInterval(()=>{
    for(let i = 0; i < portfolio.length; i++){
      let url = `https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=${portfolio[i]}&interval=5min&apikey=7KXZE5DT8SYQ4UCT`;
      fetch(url)
        .then((response) => response.json())
        .then((data) => {
          let time = data["Meta Data"]["3. Last Refreshed"];
          let price = data["Time Series (5min)"][time]["4. close"];
          let cell3 = document.querySelector(`#${portfolio[i]}price`);
          cell3.innerHTML = price;
        })
        .catch((error) => console.error("Error fetching data:", error));
    }

  }, 1000);

  



});

//7KXZE5DT8SYQ4UCT
