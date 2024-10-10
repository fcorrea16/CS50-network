$(document).ready(function () {
    //  like and dislike function

    $('.like-post').click(function (evt) {
        console.log($(this)[0])
        if ($(this[0]).hasClass("btn-primary")) {
            console.log("true for class")
            $(this).removeClass('btn-primary')
            $(this).addClass('btn-secondary')
            console.log($(this))
        } else {
            $(this).addClass('btn-primary')
            $(this).removeClass('btn-secondary')
            console.log("false for class")
            console.log($(this))
        }
    });
})
// likeButtons = $('.like-post')
// console.log(likeButtons)

// likeButtons.each(btn => {
//     btn.on("click", function () {
//         element = this.target
//         console.log(element)
//         if (this.target.classList.contains('btn-primary')) {
//             element.classList.remove('btn-primary')
//             element.classList.add('btn-secondary')
//             likes = element.nextElementSibling.innerHTML
//             element.nextElementSibling.innerHTML = parseInt(likes) + 1
//             console.log("hello1")
//         } else {
//             element = this.target
//             element.classList.add('btn-primary')
//             element.classList.remove('btn-secondary')
//             likes = element.nextElementSibling.innerHTML
//             element.nextElementSibling.innerHTML = parseInt(likes) - 1
//             console.log("hello2")
//         }
//         fetch('/editlike', {
//             method: 'POST',
//             body: JSON.stringify({
//                 liked_post: element.id



// new post button disabled and character count
// newPostButton = document.querySelector('#submit-post').disabled = true;
// newContent = document.querySelector('#new-content')

// newContent.onkeyup = function () {
//     console.log(this.value.length);
//     if (this.value.length > 0) {
//         newPostButton = document.querySelector('#submit-post').disabled = false;
//         document.querySelector('#form-message').innerHTML = "Characters left " + (280 - this.value.length)
//     }

// };


// edit post
// editButtons = $('.edit-post')
// editButtons.each(btn => {
//     btn.addEventListener('click', event => {
//         editButton = event.target
//         post_id_string = editButton.parentNode.parentNode.id
//         post_id = post_id_string.split("-", 2)
//         console.log(post_id[1])
//         console.log(editButton.next('.post-content'))
//     })
//     fetch('/post' + post_id[1], {
//         method: 'PUT',
//         body: JSON.stringify({

//         })
//     })
// })




