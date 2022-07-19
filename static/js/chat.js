async function sendMessage() {
   
    let fd = new FormData();
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
        let response = await fetch('/chat/'+ chatuser, {
            method: 'POST',
            body: fd
        });

        let responseAsJson = await response.text();
        console.log(responseAsJson);

        const DjangoFormatDate = getdjangoFormatDate(date);

        // document.getElementById('deleteMessage').remove();
        messageContainer.innerHTML += `
        <div id="deleteMessage" class="message_line_right">
        <div class="speech-bubble-right">
          <span>[${date}]</span> <span>${userfirstname}</span> <i>${messageField.value}</i>
        </div>
        </div>
        `;
        document.getElementById('messageField').value = '';
        console.log('Success!!!');
      } catch (e) {
        console.error('An error occured', e);
      }
}

function getdjangoFormatDate(date) {
  console.log(date);
 
}
