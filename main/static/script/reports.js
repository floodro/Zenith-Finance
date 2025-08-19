// Parse Django JSON safely
const months = JSON.parse(document.getElementById('months').textContent);
const incomeData = JSON.parse(document.getElementById('incomeData').textContent);
const expenseData = JSON.parse(document.getElementById('expenseData').textContent);
const categoryLabels = JSON.parse(document.getElementById('categoryLabels').textContent);
const categoryTotals = JSON.parse(document.getElementById('categoryTotals').textContent);

// Debug check
console.log("Months:", months);
console.log("Income:", incomeData);
console.log("Expenses:", expenseData);

// Normalize data (ensure both arrays match months length)
function normalizeData(months, data) {
    const normalized = months.map((_, idx) => data[idx] ?? 0);
    return normalized;
}

const normalizedIncome = normalizeData(months, incomeData);
const normalizedExpense = normalizeData(months, expenseData);

// Chart 1: Income vs Expenses (Bar Chart)
const ctx1 = document.getElementById('incomeExpenseChart').getContext('2d');
new Chart(ctx1, {
    type: 'bar',
    data: {
        labels: months,
        datasets: [
            {
                label: 'Income',
                data: normalizedIncome,
                backgroundColor: '#38A169', // green
            },
            {
                label: 'Expenses',
                data: normalizedExpense,
                backgroundColor: '#E53E3E', // red
            }
        ]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
    }
});

// Chart 2: Expense Breakdown (Pie Chart)
const ctx2 = document.getElementById('expenseBreakdownChart').getContext('2d');
new Chart(ctx2, {
    type: 'pie',
    data: {
        labels: categoryLabels,
        datasets: [{
            data: categoryTotals,
            backgroundColor: [
                '#E53E3E', '#3182CE', '#DD6B20', '#38A169', '#805AD5',
                '#D53F8C', '#319795', '#718096', '#F6E05E', '#4FD1C5'
            ],
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
    }
});

// Chart 3: Line Chart (Trends Over Time)
const ctx3 = document.getElementById('incomeExpenseLineChart').getContext('2d');
new Chart(ctx3, {
    type: 'line',
    data: {
        labels: months,
        datasets: [
            {
                label: 'Income',
                data: normalizedIncome,
                borderColor: '#38A169',
                backgroundColor: 'rgba(56, 161, 105, 0.2)',
                fill: true,
                tension: 0.3
            },
            {
                label: 'Expenses',
                data: normalizedExpense,
                borderColor: '#E53E3E',
                backgroundColor: 'rgba(229, 62, 62, 0.2)',
                fill: true,
                tension: 0.3
            }
        ]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: { beginAtZero: true }
        }
    }
});

// Chart 4: Income Breakdown (Pie Chart)
const ctx4 = document.getElementById('incomeBreakdownChart').getContext('2d');
new Chart(ctx4, {
    type: 'pie',
    data: {
        labels: categoryLabels,
        datasets: [{
            data: categoryTotals,
            backgroundColor: [
                '#38A169', '#3182CE', '#DD6B20', '#E53E3E', '#805AD5',
                '#D53F8C', '#319795', '#718096', '#F6E05E', '#4FD1C5'
            ],
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
    }
});