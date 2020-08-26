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
    
})

const findPost = (button) => {
    document.querySelectorAll('p').forEach(p  => {
        if (button.id === p.id){
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
        }
    })
}