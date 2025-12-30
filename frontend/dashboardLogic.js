// Camel face functions
const API_URL = "http://localhost:8080/";

async function loadTickerData() {
    const ticker = document.getElementById('tickerInput').value.toUpperCase();
    const statusLabel = document.getElementById('statusMsg');
    
    statusLabel.innerText = `FETCHING ${ticker}...`;
    statusLabel.style.color = "orange";

    try {
        // 1. Fetch from C Server
        const response = await fetch(`${API_URL}${ticker}`);
        
        if (!response.ok) throw new Error("Server returned 404");
        
        const jsonData = await response.json();
        
        // 2. Process Data for Charting
        renderDashboard(jsonData);
        statusLabel.innerText = "DATA RECEIVED OK";
        statusLabel.style.color = "#238636"; // Green

    } catch (error) {
        console.error(error);
        statusLabel.innerText = `ERROR: ${error.message}`;
        statusLabel.style.color = "red";
    }
}

function renderDashboard(data) {
    // Extract arrays for Plotly
    const years = data.fiscalHistory.map(item => item.year);
    const revenues = data.fiscalHistory.map(item => item.revenue);
    const incomes = data.fiscalHistory.map(item => item.netIncome);

    // 3. Create the Chart
    const trace1 = {
        x: years,
        y: revenues,
        name: 'Revenue',
        type: 'bar',
        marker: { color: '#1f6feb' }
    };

    const trace2 = {
        x: years,
        y: incomes,
        name: 'Net Income',
        type: 'scatter',
        mode: 'lines+markers',
        line: { color: '#2ea043', width: 3 }
    };

    const layout = {
        title: {
            text: `${data.companyName} (${data.ticker}) - Fiscal Performance`,
            font: { color: '#fff' }
        },
        paper_bgcolor: '#161b22',
        plot_bgcolor: '#161b22',
        xaxis: { 
            color: '#8b949e', 
            tickmode: 'linear' // Show every year
        },
        yaxis: { 
            color: '#8b949e',
            gridcolor: '#30363d'
        },
        legend: { font: { color: '#fff' } }
    };

    Plotly.newPlot('financialChart', [trace1, trace2], layout);

    // 4. Update Stats Panel (Most recent year)
    const latest = data.fiscalHistory[data.fiscalHistory.length - 1];
    
    document.getElementById('latestRevenue').innerText = formatMoney(latest.revenue);
    document.getElementById('latestIncome').innerText = formatMoney(latest.netIncome);
    document.getElementById('dataYears').innerText = data.fiscalHistory.length;
    
    // Calculate Margin
    const margin = ((latest.netIncome / latest.revenue) * 100).toFixed(2);
    const marginElem = document.getElementById('netMargin');
    marginElem.innerText = `${margin}%`;
    marginElem.style.color = margin > 0 ? '#2ea043' : 'red';
}

function formatMoney(amount) {
    // Converts 1000000000 to $1.0B
    return "$" + (amount / 1000000000).toFixed(2) + "B";
}

// Load default on start
loadTickerData();