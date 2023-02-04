const searchField = document.querySelector("#searchField");
const tableOutput = document.querySelector(".table-output");
const appTable = document.querySelector(".app-table");
tableOutput.style.display = "none";



searchField.addEventListener("keyup", (e) => {
    const searchValue = e.target.value;

    if(searchValue.trim().length > 0) {
      // console.log("searchValue", searchValue);
      fetch("/search-expenses", {
        body: JSON.stringify({ searchText: searchValue }),
        method: "POST",
      })
        .then((res) => res.json())
        .then((data) => {
          console.log("data", data);
          appTable.style.display = "none";

          tableOutput.style.display = "block";


          if(data.length === 0){
              tableOutput.innerHTML = "No results found"
          }
      });
    }
});