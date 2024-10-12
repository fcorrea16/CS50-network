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
            if (document.querySelector('.form-content-' + post_id).classList.contains('hide')) {
                post_content = editButton.parentNode.nextElementSibling
                document.querySelector('.post-content-' + post_id).classList.add('hide')
                document.querySelector('.form-content-' + post_id).classList.remove('hide')
                document.querySelector('.edit-content-' + post_id).innerHTML = document.querySelector('.post-content-' + post_id).innerHTML
                submit_button = document.querySelector('.edit-content-' + post_id).nextSibling.nextSibling
                console.log(submit_button)
                submit_button.addEventListener('click', event => {
                    inputContent = document.querySelector('.edit-content-' + post_id).value
                    document.querySelector('.post-content-' + post_id).innerHTML = inputContent
                    fetch('../post/' + post_id)
                        .then(response => response.json())
                        .then(post => {
                            fetch('/post/' + post.id, {
                                method: 'PUT',
                                body: JSON.stringify({ content: inputContent })
                            })
                            document.querySelector('.form-content-' + post_id).classList.add('hide')
                            document.querySelector('.post-content-' + post_id).classList.remove('hide')
                        })

                })
            } else {
                document.querySelector('.form-content-' + post_id).classList.add('hide')
                document.querySelector('.post-content-' + post_id).classList.remove('hide')
            }

        })
    })


    // follow and unfollow function
    // FIX HERE
    const request_user_follows = JSON.parse(document.getElementById('request_user_follows_id').textContent);
    var unfollowButton = document.querySelector('.unfollow')

    if (typeof (unfollowButton) != 'undefined' && unfollowButton != null) {
        unfollowButton.addEventListener('click', event => {
            element = event.target
            fetch('../follower/' + request_user_follows)
                .then(response => response.json())
                .then(post => {
                    console.log(post)
                    console.log("hi")
                    fetch('/follower/' + request_user_follows, {
                        method: 'DELETE',
                        body: JSON.stringify({ follower_id: request_user_follows })
                    })
                    element.classList.remove('unfollow', 'btn-outline-primary')
                    element.classList.add('btn-primary')
                    element.innerHTML = "Follow"
                    this.location.reload()
                })
        })
    }

})


