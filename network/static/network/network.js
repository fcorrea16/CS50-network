document.addEventListener('DOMContentLoaded', function () {
    //  like and dislike function
    likeButtons = document.querySelectorAll('.like-post')

    likeButtons.forEach(btn => {
        btn.addEventListener('click', event => {
            element = event.target
            if (event.target.classList.contains('btn-primary')) {
                element.classList.remove('btn-primary')
                element.classList.add('btn-secondary')
                likes = element.nextElementSibling.innerHTML
                element.nextElementSibling.innerHTML = parseInt(likes) + 1
                console.log("hello1")
            } else {
                element = event.target
                element.classList.add('btn-primary')
                element.classList.remove('btn-secondary')
                likes = element.nextElementSibling.innerHTML
                element.nextElementSibling.innerHTML = parseInt(likes) - 1
                console.log("hello2")
            }
            fetch('/editlike', {
                method: 'POST',
                body: JSON.stringify({
                    liked_post: element.id
                })
            })

        });
    });

    // new post button disabled and character count
    const newPostButton = document.querySelector('#submit-post');
    if (newPostButton) {
        document.querySelector('#submit-post').disabled = true;

        newContent = document.querySelector('#new-content')

        newContent.onkeypress = function () {
            if (this.value.length > 0) {
                newPostButton.disabled = false;
                document.querySelector('#form-message').innerHTML = "Characters left " + (280 - this.value.length)
            }
        };
    }




    // edit post
    editButtons = document.querySelectorAll('.edit-post')
    editButtons.forEach(btn => {
        btn.addEventListener('click', event => {
            editButton = event.target
            post_id_string = editButton.parentNode.parentNode.id
            post_id_split = post_id_string.split("-", 2)
            post_id = post_id_split[1]
            post_content = editButton.parentNode.nextElementSibling
            document.querySelector('.post-content-' + post_id).classList.add('hide')
            document.querySelector('.form-content-' + post_id).classList.remove('hide')
            document.querySelector('.edit-content-' + post_id).innerHTML = document.querySelector('.post-content-' + post_id).innerHTML
            submit_button = document.querySelector('.edit-content-' + post_id).nextSibling.nextSibling
            console.log(submit_button)
            submit_button.addEventListener('click', event => {
                inputContent = document.querySelector('.edit-content-' + post_id).value
                fetch('post/' + post_id)
                    .then(response => response.json())
                    .then(post => {
                        console.log(post)
                        fetch('/post/' + post.id, {
                            method: 'PUT',
                            body: JSON.stringify({ content: inputContent })
                        })


                    })

            })

        })
    })
})
