document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('prediction-form');
    const resultsSection = document.getElementById('results-section');
    const resLikelihood = document.getElementById('res-likelihood');
    const resProbability = document.getElementById('res-probability');
    const refreshHistoryBtn = document.getElementById('refresh-history');
    
    // Load history on mount
    loadHistory();

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Disable button during loading
        const btn = form.querySelector('button[type="submit"]');
        const originalText = btn.textContent;
        btn.textContent = 'Analyzing...';
        btn.disabled = true;

        const payload = {
            price: parseFloat(document.getElementById('price').value),
            income: parseFloat(document.getElementById('income').value),
            location: document.getElementById('location').value,
            size: parseFloat(document.getElementById('size').value),
            amenities: document.getElementById('amenities').value || ""
        };

        try {
            const response = await fetch('/api/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                const data = await response.json();
                showResult(data.likelihood, data.probability);
                loadHistory(); // refresh table
            } else {
                alert('Error making prediction.');
            }
        } catch (err) {
            console.error(err);
            alert('Failed to connect to the server.');
        } finally {
            btn.textContent = originalText;
            btn.disabled = false;
        }
    });

    refreshHistoryBtn.addEventListener('click', loadHistory);

    function showResult(likelihood, probability) {
        resultsSection.classList.remove('hidden');
        resLikelihood.textContent = likelihood;
        resProbability.textContent = `${probability}%`;
        
        // Styling based on result
        resLikelihood.className = 'value ' + (likelihood === 'Yes' ? 'val-yes' : 'val-no');
        
        // Add a slight pop animation
        resultsSection.style.animation = 'none';
        setTimeout(() => {
            resultsSection.style.animation = 'pulse 0.5s ease';
        }, 10);
    }

    async function loadHistory() {
        try {
            const response = await fetch('/api/history');
            if (response.ok) {
                const history = await response.json();
                renderTable(history);
            }
        } catch (err) {
            console.error('Failed to load history:', err);
        }
    }

    function renderTable(data) {
        const tbody = document.querySelector('#history-table tbody');
        tbody.innerHTML = '';

        data.forEach(item => {
            const tr = document.createElement('tr');
            
            const badgeClass = item.likelihood === 'Yes' ? 'badge-yes' : 'badge-no';

            tr.innerHTML = `
                <td>$${item.price.toLocaleString()}</td>
                <td>$${item.income.toLocaleString()}</td>
                <td style="text-transform: capitalize;">${item.location}</td>
                <td><span class="badge ${badgeClass}">${item.likelihood}</span></td>
                <td>${item.probability}%</td>
            `;
            tbody.appendChild(tr);
        });
        
        if (data.length === 0) {
            const tr = document.createElement('tr');
            tr.innerHTML = `<td colspan="5" style="text-align:center; color: var(--text-secondary);">No predictions yet.</td>`;
            tbody.appendChild(tr);
        }
    }
});
