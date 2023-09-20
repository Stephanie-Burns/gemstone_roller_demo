
const gemValues = {
    'gem-10-count': 10,
    'gem-50-count': 50,
    'gem-100-count': 100,
    'gem-500-count': 500,
    'gem-1000-count': 1000,
    'gem-5000-count': 5000,
};

const gemIds = Object.keys(gemValues);

function increment(id, event) {
    let elem = document.getElementById(id);
    let count = parseInt(elem.innerText);
    let incrementValue = event.shiftKey ? 10 : 1;  // Check if Shift is pressed
    count += incrementValue;
    elem.innerText = count;
    document.getElementById(id + '-input').value = count;
    calculate();
}

function decrement(id, event) {
    let elem = document.getElementById(id);
    let count = parseInt(elem.innerText);
    let decrementValue = event.shiftKey ? 10 : 1;  // Check if Shift is pressed
    count -= decrementValue;
    if (count < 0) count = 0;  // Ensure value doesn't go below zero
    elem.innerText = count;
    document.getElementById(id + '-input').value = count;
    calculate();
}

function clearCounts() {
    // Clear gem counts and input values
    gemIds.forEach(id => {
        document.getElementById(id).innerText = '0';
        document.getElementById(id + '-input').value = '0';
    });

    // Clear the gemstone-results div
    document.getElementById('gemstone-results').innerHTML = "";

    // Recalculate totals
    calculate();
}

function calculate() {
    let totalCount = 0;
    let totalValue = 0;

    for (const [gemId, gemValue] of Object.entries(gemValues)) {
        const count = parseInt(document.getElementById(gemId).innerText);
        totalCount += count;
        totalValue += count * gemValue;
    }

    document.getElementById('gemstone-count').innerText = totalCount;
    document.getElementById('gemstone-value').innerText = totalValue;
}
