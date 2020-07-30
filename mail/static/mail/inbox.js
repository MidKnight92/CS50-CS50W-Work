document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  
  // Get data
  document.querySelector("#compose-form").onsubmit = () => {
    sent_email()
  };

  // By default, load the inbox
  load_mailbox('inbox');
});



async function get_emails(mailbox){
  console.log(mailbox);
  try {
    await fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(result => {
      console.log(result);
      // Show fetched messages
      if (result.length !== 0){
          result.forEach(email => {
          // Create div element
          const element = document.createElement('div');

          element.innerHTML = `<b>Sender:</b> ${email['sender']} <br/><b>Subject:</b>${email['subject']} <br/> <b>Message:</b> ${email['body']} <br/><b>Time:</b> ${email['timestamp']}`;

          // Display unread emails with white background and read emails with a gray background
          if (email["read"]){
            element.style = "border: solid 2px dodgerBlue; background-color: gray; padding: 1%; margin-bottom: 4%;";
          } else {
            element.style = "border: solid 2px dodgerBlue; background-color: white; padding: 1%; margin-bottom: 4%;";
          }
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

    // Add history to the browser
    window.history.pushState({}, "",`/`);
    return;
  }
}


async function sent_email(){
  try {
    await fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
      })
    })
    .then (response => response.json())
    .then(result => {

      // Error send user back to the compose email section
      if (result["message"] ){
        
        console.log("message sent,now loading mailbox")

        // Update url
        window.history.pushState({}, '', '/');

        // Load user's sent mailbox
        load_mailbox('sent');

        // Stop the form from submitting
        return false;
      } else {

        console.log("in the else")
        // Create an error message and append it to the emails-view
        const div = document.createElement('div');
        div.innerHTML = `<p>Error: ${result["error"]}</p>`
        document.querySelector('#emails-view').append(div)

        // Show emails view with message and hide other views
        document.querySelector('#emails-view').style.display = 'block';
        document.querySelector('#compose-view').style.display = 'none';
        window.history.pushState({}, '', '/')
        return false;
          }
    });

  } catch (error) {
    console.log("in the catch of sent_email")
    console.log(error)
    // Create an error message and append it to the emails-view
    const div = document.createElement('div');
    div.innerHTML = `<p>Error: ${result["error"]}</p>`
    document.querySelector('#emails-view').append(div)

    // Show emails view with message and hide other views
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';
    console.log(error);
    return false;
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

  // Add history to the browser
  window.history.pushState({}, "",`/`);
}

function load_mailbox(mailbox) {
  console.log("in load mailbox",mailbox)
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  get_emails(mailbox);

  // Add history to the browser
  window.history.pushState({}, "",`/`);
}

console.log("end of js");