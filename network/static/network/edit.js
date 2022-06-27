function edit(id) {
    var edit_box = document.querySelector(`#edit-box-${id}`);
    var edit_btn = document.querySelector(`#edit-btn-${id}`);
    edit_box.style.display = 'block';
    edit_btn.style.display = 'block';

    edit_btn.addEventListener('click', () => {
        fetch('/edit/' + id, {
            method: 'POST',
            body: JSON.stringify({
                post: edit_box.value
            })
        });

        edit_box.style.display = 'none';
        edit_btn.style.display = 'none';

        document.querySelector(`#post-${id}`).innerHTML = edit_box.value;
    });

    edit_box.value = "";
}


