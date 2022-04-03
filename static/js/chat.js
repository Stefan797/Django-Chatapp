async function sendMessage() {
    let fd = new FormData();
    let token = '{{ csrf_token }}';
    let date = '{% now "SHORT_DATETIME_FORMAT" %}'; //https://stackoverflow.com/questions/29637768/django-present-current-date-and-time-in-template new Date mouth day // djan
    fd.append('textmessage', messageField.value);
    fd.append('csrfmiddlewaretoken', token);
    fd.append('Datum', date);
    try {
        messageContainer.innerHTML += `
      <div id="deleteMessage">
      <span class="color-gray">${date}</span> {{ request.user.first_name }}: <i class="color-gray">${messageField.value}</i> 
      </div>`;
        await fetch('/chat/', {
            method: 'POST',
            body: fd
        });

        document.getElementById('deleteMessage').remove();
        messageContainer.innerHTML += `
      <div>
      <span class="color-gray">${date}</span> {{ request.user.first_name }}: <i>${messageField.value}</i> 
      </div>`;
        console.log('Success!!!');
    } catch (e) {
        console.error('An error occured', e);
    }
}
