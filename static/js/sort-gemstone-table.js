let currentSorting = { column: 'value', direction: 'asc' };

function sortTable(column, dataType) {
    const tbody = document.querySelector("#gemstoneTable tbody");
    const rows = Array.from(tbody.querySelectorAll("tr"));

    const columnMap = {
        "name": 1,
        "value": 2,
        "clarity": 3,
        "color": 4,
    };

    const index = columnMap[column];

    if (currentSorting.column === column) {
        currentSorting.direction = (currentSorting.direction === 'asc') ? 'desc' : 'asc';
    } else {
        currentSorting.column = column;
        currentSorting.direction = 'asc';
    }

    const sortedRows = rows.sort((a, b) => {
        const aValue = a.cells[index].innerText;
        const bValue = b.cells[index].innerText;

        let comparison;
        if (dataType === "number") {
            comparison = Number(aValue.replace(/[^\d]/g, "")) - Number(bValue.replace(/[^\d]/g, ""));
        } else {
            comparison = aValue.localeCompare(bValue);
        }

        return (currentSorting.direction === 'asc') ? comparison : -comparison;
    });

    while (tbody.firstChild) {
        tbody.firstChild.remove();
    }

    sortedRows.forEach(row => {
        tbody.appendChild(row);
    });
}

