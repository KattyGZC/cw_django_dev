document.addEventListener("DOMContentLoaded", function () {

    function sendVoteRequest(url, element) {
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
                    element.classList.add('fal');
                    element.classList.remove('fas');
                }).catch(error => {
                    console.error('Error al procesar la respuesta:', error);

                });
            });
    }

    document.querySelectorAll('.vote').forEach(function (vote) {
        vote.querySelectorAll('a').forEach(a => {
            a.addEventListener('click', function (e) {
                e.preventDefault();
                let voteValue = this.getAttribute('data-value');
                const questionId = this.getAttribute('data-question');

                const otherIcon = Array.from(vote.querySelectorAll('a')).find(el => el !== this);
                this.classList.toggle('fas');
                this.classList.toggle('fal');
                otherIcon.classList.add('fal');
                otherIcon.classList.remove('fas');

                if (this.classList.contains('fal') && otherIcon.classList.contains('fal')) {
                    voteValue = 'none'
                }
                const url = `/question/${questionId}/vote/${voteValue}/`;

                sendVoteRequest(url, this);
            })

        })

    })

    document.querySelectorAll('.answers').forEach(function (answer) {
        answer.addEventListener('click', function (e) {

            if (e.target.tagName === 'A') {
                e.preventDefault();
                const questionId = e.target.getAttribute('data-question');
                let answerValue = e.target.getAttribute('data-value');
                answer.querySelectorAll('a').forEach(a => {
                    if (answerValue == a.getAttribute('data-value') && a.classList.contains('fas')){
                        answerValue = '0'
                    }
                    a.classList.remove('fas');
                    a.classList.add('fal');
                });
                if (answerValue != '0'){
                    e.target.classList.add('fas')
                    e.target.classList.remove('fal')
                }

                const url = `/question/${questionId}/answer/${answerValue}/`;
                sendVoteRequest(url, e.target);
            }
        });
    });


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

