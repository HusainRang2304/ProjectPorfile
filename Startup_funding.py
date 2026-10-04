# @title 📊 Startup Funding Dashboard {display-mode: "form"}
# This version run on google colab.
import json
import pandas as pd
import numpy as np
from IPython.display import display, HTML
from google.colab import output

# Register error logger callback
def _report_js_error(message):
    print(f"JavaScript Error: {message}")

output.register_callback('report_js_error', _report_js_error)

# Ensure the dataset is accessible and clean it minimally if needed
# Reference the existing 'startup' DataFrame from previous steps
try:
    df = startup.copy()
except NameError:
    df = pd.read_csv("startup_funding.csv")
    df.drop('Remarks', inplace=True, axis=1, errors='ignore')
    column_name = ["SrNo","Date","Startup_name","Industry","Vertical","Location","Investor_Name","InvestmentType", "Amount"]
    df.columns = column_name[:len(df.columns)]
    df['Amount'] = df['Amount'].fillna(0)
    df['Amount'] = df['Amount'].astype(str).str.replace(',', '')
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce').fillna(0)

# Basic cleanups for JS mapping compatibility
df['Industry'] = df['Industry'].fillna('Unknown').astype(str).str.strip()
df['Location'] = df['Location'].fillna('Unknown').astype(str).str.strip()
df['Startup_name'] = df['Startup_name'].fillna('Unknown').astype(str).str.strip()
df['InvestmentType'] = df['InvestmentType'].fillna('Unknown').astype(str).str.strip()

# Clean location names a bit (e.g., Bengaluru/Bangalore)
def clean_loc(loc):
    l = loc.lower()
    if 'bangalore' in l or 'bengaluru' in l: return 'Bengaluru'
    if 'delhi' in l: return 'New Delhi'
    if 'mumbai' in l: return 'Mumbai'
    if 'gurgaon' in l or 'gurugram' in l: return 'Gurgaon'
    if 'noida' in l: return 'Noida'
    if 'pune' in l: return 'Pune'
    if 'hyderabad' in l: return 'Hyderabad'
    return loc

df['Cleaned_Location'] = df['Location'].apply(clean_loc)

# Keep top records to keep payload lightweight and responsive
dashboard_df = df[['Startup_name', 'Industry', 'Cleaned_Location', 'InvestmentType', 'Amount']].copy()
dashboard_df = dashboard_df.dropna(subset=['Startup_name'])
data_records = dashboard_df.to_dict(orient='records')
data_json = json.dumps(data_records)

html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Startup Funding Dashboard</title>
    <!-- Tailwind CSS CDN for elegant UI -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Chart.js CDN -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {
            background-color: #f4f6f8;
            font-family: ui-sans-serif, system-ui, sans-serif;
        }
        .canvas-wrapper {
            position: relative;
            flex-grow: 1;
            min-height: 250px;
            height: 100%;
        }
    </style>
</head>
<body class="p-6">

    <!-- Header & Dashboard Controls -->
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
        <div>
            <h1 class="text-3xl font-bold text-gray-800">📊 Startup Funding Dashboard</h1>
            <p class="text-gray-500 mt-1">Interactive analysis of investments, industries, and locations</p>
        </div>
        <div class="flex flex-wrap gap-4">
            <div>
                <label class="block text-xs font-semibold text-gray-600 uppercase mb-1">Industry Filter</label>
                <select id="industry-filter" class="bg-white border border-gray-300 text-gray-700 py-2 px-4 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500" onchange="filterData()">
                    <option value="All">All Industries</option>
                </select>
            </div>
            <div>
                <label class="block text-xs font-semibold text-gray-600 uppercase mb-1">Location Filter</label>
                <select id="location-filter" class="bg-white border border-gray-300 text-gray-700 py-2 px-4 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500" onchange="filterData()">
                    <option value="All">All Locations</option>
                </select>
            </div>
        </div>
    </div>

    <!-- KPI Summary Cards -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
            <p class="text-xs font-semibold text-gray-400 uppercase tracking-wider">Total Funding Raised</p>
            <h3 class="text-2xl font-bold text-gray-800 mt-2" id="kpi-total-funding">$0</h3>
            <p class="text-xs text-green-500 font-medium mt-1">▲ In USD</p>
        </div>
        <div class="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
            <p class="text-xs font-semibold text-gray-400 uppercase tracking-wider">Average Deal Size</p>
            <h3 class="text-2xl font-bold text-gray-800 mt-2" id="kpi-avg-funding">$0</h3>
            <p class="text-xs text-blue-500 font-medium mt-1">Mean value per deal</p>
        </div>
        <div class="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
            <p class="text-xs font-semibold text-gray-400 uppercase tracking-wider">Total Funded Startups</p>
            <h3 class="text-2xl font-bold text-gray-800 mt-2" id="kpi-startup-count">0</h3>
            <p class="text-xs text-indigo-500 font-medium mt-1">Unique brands</p>
        </div>
        <div class="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
            <p class="text-xs font-semibold text-gray-400 uppercase tracking-wider">Max Single Investment</p>
            <h3 class="text-2xl font-bold text-gray-800 mt-2" id="kpi-max-funding">$0</h3>
            <p class="text-xs text-purple-500 font-medium mt-1" id="kpi-max-startup">Name</p>
        </div>
    </div>

    <!-- Charts Row -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
        <!-- Industry Distribution -->
        <div class="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 flex flex-col lg:col-span-2">
            <h3 class="text-lg font-bold text-gray-800 mb-4">Funding Volume by Industry (Top 10)</h3>
            <div class="canvas-wrapper">
                <canvas id="industryChart"></canvas>
            </div>
        </div>
        <!-- Location Distribution -->
        <div class="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 flex flex-col">
            <h3 class="text-lg font-bold text-gray-800 mb-4">Top Funding Hubs (Location Share)</h3>
            <div class="canvas-wrapper">
                <canvas id="locationChart"></canvas>
            </div>
        </div>
    </div>

    <!-- Bottom Section: Detailed Deals Table -->
    <div class="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
        <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 gap-4">
            <div>
                <h3 class="text-lg font-bold text-gray-800">Detailed Funding Records</h3>
                <p class="text-gray-400 text-sm">Scroll and search individual transactions matching your filters</p>
            </div>
            <input type="text" id="table-search" placeholder="Search startups..." class="bg-gray-50 border border-gray-200 text-gray-700 py-2 px-4 rounded-lg w-full md:w-64 focus:outline-none focus:ring-2 focus:ring-blue-500" onkeyup="filterTable()">
        </div>
        <div class="overflow-x-auto">
            <table class="min-w-full text-sm text-left text-gray-500">
                <thead class="text-xs text-gray-700 uppercase bg-gray-50">
                    <tr>
                        <th class="py-3 px-6">Startup Name</th>
                        <th class="py-3 px-6">Industry</th>
                        <th class="py-3 px-6">Location</th>
                        <th class="py-3 px-6">Investment Type</th>
                        <th class="py-3 px-6 text-right">Amount (USD)</th>
                    </tr>
                </thead>
                <tbody id="table-body">
                    <!-- JS dynamic loading -->
                </tbody>
            </table>
        </div>
        <div class="flex justify-between items-center mt-4">
            <button id="prev-btn" onclick="prevPage()" class="px-4 py-2 bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-lg text-xs font-semibold disabled:opacity-50">Previous</button>
            <span id="page-num" class="text-xs text-gray-500 font-medium">Page 1</span>
            <button id="next-btn" onclick="nextPage()" class="px-4 py-2 bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-lg text-xs font-semibold disabled:opacity-50">Next</button>
        </div>
    </div>

    <script>
        window.onerror = function(message) {
            google.colab.kernel.invokeFunction('report_js_error', [message], {});
        };

        // Inject raw database values directly into JS
        const dataset = STARTUP_DATA_REPLACE;

        let filteredData = [...dataset];
        let currentTablePage = 1;
        const itemsPerPage = 10;
        let industryChart = null;
        let locationChart = null;

        // Initialize Filters
        function initFilters() {
            const industries = [...new Set(dataset.map(item => item.Industry).filter(Boolean))].sort();
            const locations = [...new Set(dataset.map(item => item.Cleaned_Location).filter(Boolean))].sort();

            const indSelect = document.getElementById('industry-filter');
            industries.forEach(ind => {
                const opt = document.createElement('option');
                opt.value = ind;
                opt.textContent = ind;
                indSelect.appendChild(opt);
            });

            const locSelect = document.getElementById('location-filter');
            locations.forEach(loc => {
                const opt = document.createElement('option');
                opt.value = loc;
                opt.textContent = loc;
                locSelect.appendChild(opt);
            });
        }

        // Primary filtering pipeline
        function filterData() {
            const selectedInd = document.getElementById('industry-filter').value;
            const selectedLoc = document.getElementById('location-filter').value;

            filteredData = dataset.filter(item => {
                const matchInd = (selectedInd === 'All' || item.Industry === selectedInd);
                const matchLoc = (selectedLoc === 'All' || item.Cleaned_Location === selectedLoc);
                return matchInd && matchLoc;
            });

            currentTablePage = 1;
            updateKPIs();
            updateCharts();
            renderTable();
        }

        // KPI Calculation
        function updateKPIs() {
            let totalFunding = 0;
            let maxFunding = 0;
            let maxStartup = "N/A";
            const uniqueStartups = new Set();

            filteredData.forEach(item => {
                const amt = Number(item.Amount) || 0;
                totalFunding += amt;
                if (amt > maxFunding) {
                    maxFunding = amt;
                    maxStartup = item.Startup_name;
                }
                if (item.Startup_name) uniqueStartups.add(item.Startup_name);
            });

            const avgFunding = filteredData.length > 0 ? (totalFunding / filteredData.length) : 0;

            document.getElementById('kpi-total-funding').textContent = formatCurrency(totalFunding);
            document.getElementById('kpi-avg-funding').textContent = formatCurrency(avgFunding);
            document.getElementById('kpi-startup-count').textContent = uniqueStartups.size.toLocaleString();
            document.getElementById('kpi-max-funding').textContent = formatCurrency(maxFunding);
            document.getElementById('kpi-max-startup').textContent = "Target: " + maxStartup;
        }

        function formatCurrency(num) {
            if (num >= 1.0e+9) return "$" + (num / 1.0e+9).toFixed(2) + " B";
            if (num >= 1.0e+6) return "$" + (num / 1.0e+6).toFixed(2) + " M";
            return "$" + num.toLocaleString(undefined, {minimumFractionDigits: 0, maximumFractionDigits: 0});
        }

        // Dynamic Charts Drawing
        function updateCharts() {
            // 1. Industry distribution summary
            const indMap = {};
            filteredData.forEach(item => {
                const ind = item.Industry || 'Unknown';
                const amt = Number(item.Amount) || 0;
                indMap[ind] = (indMap[ind] || 0) + amt;
            });
            const sortedInds = Object.entries(indMap).sort((a,b) => b[1] - a[1]).slice(0, 10);

            const indLabels = sortedInds.map(x => x[0]);
            const indValues = sortedInds.map(x => x[1]);

            if (industryChart) industryChart.destroy();
            const ctx1 = document.getElementById('industryChart').getContext('2d');
            industryChart = new Chart(ctx1, {
                type: 'bar',
                data: {
                    labels: indLabels,
                    datasets: [{
                        label: 'Total Funding (USD)',
                        data: indValues,
                        backgroundColor: 'rgba(59, 130, 246, 0.85)',
                        borderRadius: 6,
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false }
                    },
                    scales: {
                        y: { beginAtZero: true }
                    }
                }
            });

            // 2. Location Share representation
            const locMap = {};
            filteredData.forEach(item => {
                const loc = item.Cleaned_Location || 'Unknown';
                const amt = Number(item.Amount) || 0;
                locMap[loc] = (locMap[loc] || 0) + amt;
            });
            const sortedLocs = Object.entries(locMap).sort((a,b) => b[1] - a[1]).slice(0, 5);
            const locLabels = sortedLocs.map(x => x[0]);
            const locValues = sortedLocs.map(x => x[1]);

            if (locationChart) locationChart.destroy();
            const ctx2 = document.getElementById('locationChart').getContext('2d');
            locationChart = new Chart(ctx2, {
                type: 'doughnut',
                data: {
                    labels: locLabels,
                    datasets: [{
                        data: locValues,
                        backgroundColor: [
                            '#4F46E5', '#3B82F6', '#10B981', '#F59E0B', '#EF4444'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { position: 'bottom' }
                    }
                }
            });
        }

        // Paginated Deals Table rendering
        let currentTableData = [];
        function renderTable() {
            const tableBody = document.getElementById('table-body');
            tableBody.innerHTML = '';

            const searchValue = document.getElementById('table-search').value.toLowerCase();
            currentTableData = filteredData.filter(item => 
                (item.Startup_name || '').toLowerCase().includes(searchValue)
            );

            const totalPages = Math.ceil(currentTableData.length / itemsPerPage) || 1;
            if (currentTablePage > totalPages) currentTablePage = totalPages;

            const start = (currentTablePage - 1) * itemsPerPage;
            const end = start + itemsPerPage;
            const pageItems = currentTableData.slice(start, end);

            pageItems.forEach(item => {
                const tr = document.createElement('tr');
                tr.className = 'border-b hover:bg-gray-50';
                tr.innerHTML = `
                    <td class="py-4 px-6 font-semibold text-gray-800">${item.Startup_name || 'N/A'}</td>
                    <td class="py-4 px-6">${item.Industry || 'N/A'}</td>
                    <td class="py-4 px-6">${item.Cleaned_Location || 'N/A'}</td>
                    <td class="py-4 px-6">${item.InvestmentType || 'N/A'}</td>
                    <td class="py-4 px-6 text-right font-medium text-gray-900">${(item.Amount || 0).toLocaleString()}</td>
                `;
                tableBody.appendChild(tr);
            });

            document.getElementById('page-num').textContent = `Page ${currentTablePage} of ${totalPages}`;
            document.getElementById('prev-btn').disabled = (currentTablePage === 1);
            document.getElementById('next-btn').disabled = (currentTablePage === totalPages);
        }

        function filterTable() {
            currentTablePage = 1;
            renderTable();
        }

        function prevPage() {
            if (currentTablePage > 1) {
                currentTablePage--;
                renderTable();
            }
        }

        function nextPage() {
            const totalPages = Math.ceil(currentTableData.length / itemsPerPage) || 1;
            if (currentTablePage < totalPages) {
                currentTablePage++;
                renderTable();
            }
        }

        // Execution Entry Point
        initFilters();
        filterData();
    </script>
</body>
</html>
""".replace('STARTUP_DATA_REPLACE', data_json)

display(HTML(html_content))
