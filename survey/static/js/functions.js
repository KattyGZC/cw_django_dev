document.addEventListener("DOMContentLoaded", function () {
    const likeIcon = document.querySelector('.vote-like');
    const dislikeIcon = document.querySelector('.vote-dislike');

    likeIcon.addEventListener('click', function () {
        toggleVoteAndSendRequest(this, dislikeIcon);
    });

    dislikeIcon.addEventListener('click', function () {
        toggleVoteAndSendRequest(this, likeIcon);
    });

    function toggleVoteAndSendRequest(selectedIcon, otherIcon) {
        let voteValue = selectedIcon.dataset.value;
        const questionId = selectedIcon.dataset.question;

        if (selectedIcon.classList.contains('fal')) {
            selectedIcon.classList.remove('fal');
            selectedIcon.classList.add('fas');
            otherIcon.classList.remove('fas');
            otherIcon.classList.add('fal');
        } else {
            selectedIcon.classList.remove('fas');
            selectedIcon.classList.add('fal');
            voteValue = 'none';
        }

        sendVoteRequest(questionId, voteValue);
    }

    function sendVoteRequest(questionId, voteValue) {
        const url = `/question/${questionId}/vote/${voteValue}/`;

        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => {
            if (!response.ok) {
                throw response;
            }
            return response.json();
        })
        .then(data => {
            alert("Respuesta: " + data.message);
        })
        .catch(response => {
            response.json().then(data => {
                alert("Error: " + data.Error); 
                likeIcon.classList.add('fal');
                likeIcon.classList.remove('fas');
                dislikeIcon.classList.add('fal');
                dislikeIcon.classList.remove('fas');
            }).catch(error => {
                console.error('Error al procesar la respuesta:', error);

            });
        });
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});

