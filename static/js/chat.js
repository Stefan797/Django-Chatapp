async function sendMessage() {
    let fd = new FormData();
    // let token = '{{ csrf_token }}';
    // let date = '{% now "SHORT_DATETIME_FORMAT" %}'; //https://stackoverflow.com/questions/29637768/django-present-current-date-and-time-in-template new Date mouth day // djan
    fd.append('userfirstname', userfirstname);
    fd.append('textmessage', messageField.value);
    fd.append('csrfmiddlewaretoken', token);
    fd.append('Datum', date);
    try {
        // messageContainer.innerHTML += `
        // <div id="deleteMessage" class="message_line_right">
        // <div class="speech-bubble-right">
        //   <span>${date}</span> <span>${userfirstname}</span> <i>${messageField.value}</i>
        // </div>
        // </div>
        // `;
        await fetch('/chat/'+ chatuser, {
            method: 'POST',
            body: fd
        });

        // document.getElementById('deleteMessage').remove();
        messageContainer.innerHTML += `
        <div id="deleteMessage" class="message_line_right">
        <div class="speech-bubble-right">
          <span>${date}</span> <span>${userfirstname}</span> <i>${messageField.value}</i>
        </div>
        </div>
        `;
        document.getElementById('messageField').value = '';
        console.log('Success!!!');
      } catch (e) {
        console.error('An error occured', e);
      }
}
