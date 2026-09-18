(function () {
    function integerValue(input) {
        const value = Number.parseInt(input.value, 10);
        return Number.isFinite(value) ? value : 0;
    }

    function updateBudget() {
        const page = document.getElementById('purchase-page');
        if (!page) return;

        const budget = Number.parseInt(page.dataset.budget, 10);
        let total = 0;
        document.querySelectorAll('.candy-row').forEach(function (row) {
            const input = row.querySelector('input[type="number"]');
            const price = Number.parseInt(row.dataset.price, 10);
            total += integerValue(input) * price;
        });

        const remaining = budget - total;
        document.getElementById('total-spent').textContent = total;
        document.getElementById('amount-remaining').textContent = remaining;

        const status = document.getElementById('budget-status');
        if (remaining === 0) {
            status.textContent = '✅ Your 30¢ budget is allocated exactly.';
            status.className = 'mt-2 text-success fw-bold';
        } else if (remaining > 0) {
            status.textContent = 'You still need to allocate ' + remaining + '¢.';
            status.className = 'mt-2 text-warning fw-bold';
        } else {
            status.textContent = 'You are ' + Math.abs(remaining) + '¢ over budget.';
            status.className = 'mt-2 text-danger fw-bold';
        }
    }

    document.addEventListener('DOMContentLoaded', function () {
        document.querySelectorAll('.candy-row input[type="number"]').forEach(function (input) {
            input.addEventListener('input', updateBudget);
            input.addEventListener('change', updateBudget);
        });
        updateBudget();
    });
})();
