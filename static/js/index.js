function like(post_id) {
    const likeCount = document.getElementById(`likes-count-${post_id}`);
    const likeButton = document.getElementById(`like-button-${post_id}`);

    fetch(`/like/${post_id}`, {method: "POST"})
        .then((res) => res.json())
            .then((data) => {
                likeCount.innerHTML = data['likes'];
                if (data['liked'] === true) {
                    likeButton.className = "btn btn-success";
                }
                else {
                    likeButton.className = "btn btn-outline-success";
                }
                
            })
    .catch((e) => alert("Для того чтобы оценивать записи вам нужно войти в аккаунт"));
}