document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function(event) {
        event.preventDefault();

        // Capture form data
        const formData = new FormData(event.target);
        const data = {};

        formData.forEach((value, key) => {
            data[key] = value;
        });

        // Improved sanitization using DOMPurify
        for (const key in data) {
            if (data.hasOwnProperty(key)) {
                data[key] = DOMPurify.sanitize(data[key]);
            }
        }

        // Get the form action attribute
        const formAction = event.target.action;

        // Post data
        fetch(formAction, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(result => {
            console.log('Success:', result);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});