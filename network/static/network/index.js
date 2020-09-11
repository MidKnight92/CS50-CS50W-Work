console.log("running")

document.addEventListener('DOMContentLoaded', function() {
    
    // Listen for which Button was clicked
    document.querySelectorAll('button').forEach(button => {
        button.onclick = () => {
            if (button.dataset.action === "edit"){
                button.innerText = "Save";
                button.className = "btn btn-outline-primary btn-sm";
                findPost(button);
            } else {
                button.dataset.action = "edit"
                button.innerText = "Edit";
                button.className = "btn btn-outline-secondary btn-sm";
                const text = document.querySelector('textarea').value
                savePost(button, text)
            }       
        }
    })
    
    // Listen for which thumbsup was clicked
    document.querySelectorAll('svg').forEach(thumbsup => {
        thumbsup.addEventListener('click', () => {
            if (thumbsup.dataset.action == "like") {
                thumbsup.dataset.action = "unlike"
                const span = thumbsup.parentElement.childNodes[1].firstChild;
                let num = parseInt(span.innerText)
                num = num + 1
                span.innerText = String(num)
                span.dataset.likes = num                
                like(thumbsup.dataset.post_id, thumbsup.dataset.post_user_id)
            } else {
                thumbsup.dataset.action = "like"
                const span = thumbsup.parentElement.childNodes[1].firstChild;
                console.log(span)
                let num = parseInt(span.innerText)
                console.log(num)
                if (num > 0){
                    num = num - 1
                    span.innerText = String(num)
                    span.dataset.likes = num 
                }
                unlike(thumbsup.dataset.post_id, thumbsup.dataset.post_user_id)
            }
        })
    })
})

const findPost = (button) => {
    document.querySelectorAll('p').forEach(p  => {
        if (button.id === p.id){
            console.log(p);
            p.innerHTML = `<textarea>${p.dataset.textcontent}</textarea>`;
            button.dataset.action = "save";
        }
    })
}

const savePost = (button, text) => {
    document.querySelectorAll('p').forEach(p  => {
        if (button.id === p.id){
            p.dataset.textcontent = text;
            p.innerHTML = `${text}`;
            url = window.location.href
            try {
                fetch(url, {
                    method: 'POST',
                    body: JSON.stringify({
                        post_id: p.id,
                        post: text
                    })
                }).then(response => {
                    console.log(response)
                })
            } catch (error) {
                console.log(error);
            }
        }
    })
}

const like = (postId, userId) => {
    console.log("like")
    try {
        // post, user
        url = window.location.href
        fetch(url, {
            method: 'PUT',
            body: JSON.stringify({
                post_id: postId,
                user_id: userId,
                action: 'like'
            })
        }).then(response  => {
            console.log(response)
        })
    } catch (error) {
        console.log(error)
    }
}

const unlike = (postId, userId) => {
    console.log('unlike')
    try {
        url = window.location.href
        fetch(url, {
            method: 'PUT',
            body: JSON.stringify({
                post_id: postId,
                user_id: userId,
                action: 'unlike'
            })
        }).then(response  => {
            console.log(response)
        })
    } catch (error) {
        console.log(error)
    }
}