document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  

  // By default, load the inbox
  load_mailbox('inbox');
});



async function get_emails(mailbox){
  try {
    await fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(result => {
      // Show fetched messages
      if (result.length !== 0){
          result.forEach(email => {
          const element = document.createElement('div');
          element.innerHTML = `<b>Sender:</b> ${email['sender']} <br/><b>Subject:</b>${email['subject']} <br/> <b>Message:</b> ${email['body']} <br/><b>Time:</b> ${email['timestamp']}`;
          element.style = "border: solid 2px dodgerBlue; background-color: GhostWhite; padding: 1%; margin-bottom: 4%;";
          document.querySelector('#emails-view').append(element)
        });
      // No messages to fetch relay that to user  
      } else {
        const div = document.createElement('div');
        div.innerHTML = `<p>No messages</p>`
        document.querySelector('#emails-view').append(div)
      }
    });

  } catch (error) {
    // Create an error message and append it to the emails-view
    const div = document.createElement('div');
    div.innerHTML = `<p>Sorry there was an error</p>`
    document.querySelector('#emails-view').append(div)
    console.log(error);
  }
}

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Add history to the browser
  window.history.pushState({}, "",`/`);
  get_emails(mailbox);
}


