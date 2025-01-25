// document.addEventListener('DOMContentLoaded', function () {
//     const form = document.getElementById('to-do-form');
//     const toDoList = document.getElementById('to-do-list');

//     form.addEventListener('submit', function (event) {
//         event.preventDefault(); // Запобігаємо перезавантаженню сторінки

//         const url = form.getAttribute('action');
//         const formData = new FormData(form);

//         fetch(url, {
//             method: 'POST',
//             body: formData,
//             headers: {
//                 'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value
//             }
//         })
//         .then(response => response.json())
//         .then(data => {
//             if (data.errors) {
//                 // Якщо є помилки, виводимо їх
//                 alert('Помилка: ' + JSON.stringify(data.errors));
//             } else {
//                 // Додаємо новий елемент до списку
//                 const newToDo = document.createElement('p');
//                 newToDo.textContent = data.name;
//                 toDoList.appendChild(newToDo);

//                 // Очищаємо форму
//                 form.reset();
//             }
//         })
//         .catch(error => {
//             console.error('Помилка:', error);
//         });
//     });
// });


document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('to-do-form');
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(form);
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        fetch('/home/to_do', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken,
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.id && data.name) {
                // Створюємо новий елемент у списку
                const newItem = document.createElement('div');
                newItem.style.display = 'flex';
                newItem.style.flexWrap = 'wrap';
                newItem.style.alignItems = 'baseline';
                newItem.style.justifyContent = 'space-between';
                newItem.innerHTML = `
                    <p>${data.name}</p>
                    <button class="btn btn-sm delete-todo" data-id="${data.id}">
                        <i class="fa fa-times"></i>
                    </button>
                    <hr/>
                `;

                // Додаємо новий елемент до списку
                document.getElementById('to-do-list').appendChild(newItem);

                // Оновлюємо слухачів подій для кнопок видалення
                addDeleteEventListeners();
            }
        })
        .catch(error => console.error('Error:', error));
    });

    function addDeleteEventListeners() {
        // Додаємо слухачів подій для всіх кнопок видалення
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
                        button.closest('div').remove();  // Видаляємо елемент зі списку
                    }
                })
                .catch(error => console.error('Error:', error));
            });
        });
    }

    // Ініціалізуємо слухачів подій для кнопок видалення при завантаженні сторінки
    addDeleteEventListeners();
});