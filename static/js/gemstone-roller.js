
const gemValues = {
    'gem-10-count': 10,
    'gem-50-count': 50,
    'gem-100-count': 100,
    'gem-500-count': 500,
    'gem-1000-count': 1000,
    'gem-5000-count': 5000,
};

const gemIds = Object.keys(gemValues);

function increment(id) {
    let elem = document.getElementById(id);
    let count = parseInt(elem.innerText) + 1;
    elem.innerText = count;
    document.getElementById(id + '-input').value = count;
    calculate();
}

function decrement(id) {
    let elem = document.getElementById(id);
    let count = parseInt(elem.innerText);
    if (count > 0) {
        count--;
        elem.innerText = count;
        document.getElementById(id + '-input').value = count;
    }
    calculate();
}

function clearCounts() {
    gemIds.forEach(id => {
        document.getElementById(id).innerText = '0';
        document.getElementById(id + '-input').value = '0';
    });
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