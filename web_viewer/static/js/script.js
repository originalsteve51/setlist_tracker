const rowContainer = document.getElementById('row-container');
function createRow(text, index) {
    const rowDiv = document.createElement('div');
    rowDiv.className = 'row';
    rowDiv.innerText = text;
    rowDiv.onclick = () => {
        rowDiv.classList.toggle('active');
    };
    rowDiv.setAttribute('data-index', index);
    return rowDiv;
}
async function fetchRows() {
    try {
        const response = await fetch('/get_rows'); // Adjust this URL to your Flask endpoint
        const data = await response.json();
        populateRows(data);
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}
function populateRows(data) {
    rowContainer.innerHTML = ''; // Clear existing rows
    data.forEach((text, index) => {
        const row = createRow(text, index);
        rowContainer.appendChild(row);
    });
}

// setInterval(fetchRows, 10000); // Fetch data every second

document.addEventListener("DOMContentLoaded", 
    function()
    {
        console.log("The page was either loaded or refreshed");

        // Need to clear rows before getting them again, otherwise
        // the list keeps repeating itself
        rowContainer.innerHTML = ''; // Clear existing rows
        fetchRows();
    });

