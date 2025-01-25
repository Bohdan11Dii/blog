document.addEventListener('DOMContentLoaded', function() {
    const likeButton = document.querySelector('.like-button');

    if (likeButton) {
        likeButton.addEventListener('click', function(event) {
            event.preventDefault(); // Запобігаємо дефолтній поведінці форми (оновленню сторінки)
            const form = likeButton.closest('form');
            const url = form.getAttribute('data-url');

            // Надсилаємо запит на сервер
            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value,
                },
                body: new FormData(form)
            })
            .then(response => response.json())
            .then(data => {
                // Оновлення DOM на основі відповіді від сервера
                if (data.liked) {
                    likeButton.querySelector('i').classList.remove('fa-regular');
                    likeButton.querySelector('i').classList.add('fa-solid');
                    likeButton.querySelector('span').textContent = ' Ви вже вподобали';
                } else {
                    likeButton.querySelector('i').classList.remove('fa-solid');
                    likeButton.querySelector('i').classList.add('fa-regular');
                    likeButton.querySelector('span').textContent = ' Лайк';
                }

                // Оновлення лічильника лайків
                const likeCount = document.querySelector('.like-count');
                if (likeCount) {
                    likeCount.textContent = data.like_count;
                }
            })
            .catch(error => {
                console.error('Error:', error); // Лог помилки у разі проблеми із запитом
            });
        });
    }
});
