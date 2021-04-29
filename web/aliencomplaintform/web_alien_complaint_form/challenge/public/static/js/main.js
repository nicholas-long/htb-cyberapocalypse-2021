const form      = document.getElementById('form');
const complaint = document.getElementById('complaint');
const alerts    = document.getElementById('alerts');

const flash = (message, level) => {
    alerts.innerHTML += `
        <div class="alert alert-${level}" role="alert">
            <button type="button" id="closeAlert" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>
            <strong>${message}</strong>
        </div>
    `;
};

form.addEventListener('submit', e => {
    e.preventDefault();

    alerts.innerHTML = '';
    fetch('/api/submit', {
        method: 'POST',
        body: JSON.stringify({
            complaint: complaint.value,
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(resp => resp.json())
    .then(data => {
        if (data.error) {
            flash(data.message, 'danger');

            setTimeout(() => {
                document.getElementById('closeAlert').click();
            }, 3000);

            return 0;
        } 

        flash(data.message, 'success');

        setTimeout(() => {
            document.getElementById('closeAlert').click();
        }, 3000);
    });
});