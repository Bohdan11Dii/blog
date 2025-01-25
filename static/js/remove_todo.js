document.addEventListener('DOMContentLoaded', function() {
    const deleteButtons = document.querySelectorAll('.delete-todo');
    
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const toDoId = button.getAttribute('data-id');
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            fetch(`/home/delete-todo/${toDoId}/`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    alert(data.message);
                    button.closest('div').remove();  // Remove the to-do item from the list
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
});