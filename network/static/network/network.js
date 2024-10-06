document.addEventListener('DOMContentLoaded', function () {

    likeButtons = document.querySelectorAll('.like-post')

    likeButtons.forEach(btn => {
        btn.addEventListener('click', event => {
            element = event.target
            if (event.target.classList.contains('btn-primary')) {
                element.classList.remove('btn-primary')
                element.classList.add('btn-secondary')
                likes = element.nextElementSibling.innerHTML
                element.nextElementSibling.innerHTML = likes + 1
                console.log("hello1")
            } else {
                element = event.target
                element.classList.add('btn-primary')
                element.classList.remove('btn-secondary')
                likes = element.nextElementSibling.innerHTML
                element.nextElementSibling.innerHTML = likes - 1
                console.log("hello2")
            }
            fetch('/editlike', {
                method: 'POST',
                body: JSON.stringify({
                    liked_post: element.id
                })
            })

        });
    })
});





