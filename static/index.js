function submitPost(event) {
    event.preventDefault();
    const titleInput = document.querySelector(["[name='title']"]);
    const contentInput = document.querySelector(["[name='content']"]);

    const postData = {title: titleInput.value, content: contentInput.value};

    if (!titleInput.value || !contentInput.value){
        return alert("Error: Please enter title and content to submit post")
    }

    fetch('http://localhost:5000/api/posts', {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(postData)
    }).then(res => {
        if (res.status === 200) {
        titleInput.value = ""
        contentInput.value = ""
        window.location.reload();
        }
    }).catch(error => {
        console.error(error);
        return alert("Something went wrong...")
    })
}

function handleDelete(post_id) {
       fetch("http://localhost:5000/api/posts/" + post_id, {
        method: "DELETE"
       })
       .then(res => {
        if (res.status === 200) {
            console.log(res);
            window.location.reload();
            return;
        }
       })
       .catch(error => {
        console.log(error);
        return alert("Something went wrong...")
       })
}