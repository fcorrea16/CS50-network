document.addEventListener('DOMContentLoaded', function () {

    likeButtons = document.querySelectorAll('.like-post')

    likeButtons.forEach(btn => {
        btn.addEventListener('click', event => {
            console.log(event.target.id);
            // add to database
        })
    })
});

function like(id) {
    fetch('post/' + id)
        .then(response => response.json())
        .then(post => {
            fetch('/post/' + post.id, {
                method: 'PUT',
                body: JSON.stringify({})
            })
            location.reload()
                .then();
        })
}
