document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('#submit').disabled = true;
    document.querySelector('#mytext').onkeyup = () => {
        if(document.querySelector('#mytext').value.length > 0){
            document.querySelector('#submit').disabled = false;
        }
        else {
            document.querySelector('#submit').disabled = true;
        }
    }
    const x = document.getElementsByTagName('i');
    const y = document.getElementsByClassName("Comment");
    console.log(y[0].id)
    for (let index = 0; index < x.length; index++) {
        document.querySelector('#'+x[index].id).addEventListener('click', (e) => increase(e, x[index].id));
        document.querySelector('#'+y[index].id).addEventListener('click', (e) => showComment(e, y[index].parentNode, x[index].id));
    }
});
function showComment(event, tag, post_id) {
    const commentBox = tag.parentNode.querySelector('div')
    commentBox.style.display = 'block';
    commentBox.querySelector('input').addEventListener('click', () => postComment(commentBox,post_id));
}
function postComment(commentBox, post_id){
    const username = JSON.parse(document.getElementById('user_name').textContent)
    const content = commentBox.querySelector('textarea').value;
    const element = document.createElement('div');
    element.className = "comment-box";
    element.innerHTML = `<div class="user-comment">${username}</div><div class="new-comment">${content}</div>`;
    commentBox.insertBefore(element, commentBox.lastChild)
    commentBox.querySelector('textarea').value = '';
    const id = post_id.split('-')[1];
    console.log(post_id);
    fetch('/comment/'+id, {
        method: "POST",
        body: JSON.stringify({
            "content": content
        })
    })
}
function increase(event, post_id) {
    document.querySelector('#'+post_id).classList.toggle("fa-thumbs-down");
    const id = post_id.split('-')[1];
    fetch('/like/'+id,{
        method: "PUT",
        body: JSON.stringify({
            like: true
        })
    });
    const l = document.querySelector('#'+post_id).innerHTML;
    const cl = document.getElementById(post_id);
    if(cl.className === "fa fa-thumbs-up"){
        document.querySelector('#'+post_id).innerHTML = parseInt(l) + 1;
    }
    else {
        document.querySelector('#'+post_id).innerHTML = parseInt(l) - 1;
    }
}