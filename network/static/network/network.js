document.addEventListener('DOMContentLoaded', function () {

    likeButtons = document.querySelectorAll('.like-post')

    likeButtons.forEach(btn => {
        btn.addEventListener('click', event => {
            console.log("clicked button")
            console.log(event.target.id)
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





