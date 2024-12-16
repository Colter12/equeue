document.addEventListener("DOMContentLoaded", function() {
    function updateQueue() {
        fetch('/user/')
            .then(response => response.text())
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                const newQueue = doc.querySelector('.queue-list');
                document.querySelector('.queue-list').innerHTML = newQueue.innerHTML;
            })
            .catch(error => console.error('Error updating queue:', error));
    }

    document.querySelector('.get-ticket').addEventListener('click', function(e) {
        e.preventDefault();
        fetch('/user/create/')
            .then(() => updateQueue())
            .catch(error => console.error('Error getting ticket:', error));
    });

    setInterval(updateQueue, 5000);
});
