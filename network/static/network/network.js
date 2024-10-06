document.addEventListener('DOMContentLoaded', function () {

    likeButtons = document.querySelectorAll('.like-post')

    likeButtons.forEach(btn => {
        btn.addEventListener('click', event => {
            if (event.target.classList.contains('btn-primary')) {
                event.target.classList.remove('btn-primary')
                event.target.classList.add('btn-secondary')
            } else {
                event.target.classList.add('btn-primary')
                event.target.classList.remove('btn-secondary')
            }
            liked_post = event.target.id
            fetch('/editlike', {
                method: 'POST',
                body: JSON.stringify({
                    liked_post: liked_post
                })
            })

        });
    })
});





