document.addEventListener('DOMContentLoaded', function() {

  // Get data
  document.querySelector("#compose-form").onsubmit = () => {
    sent_email()
  };
});

async function sent_email(){
  // try {
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
        
        console.log("loading mailbox")

        // Update url
        window.history.pushState({}, '', 'emails/sent')
        // Load user's sent mailbox
        load_mailbox('sent');

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
        console.log(error);
          }
    });

  // } catch (error) {
  //   console.log("in the catch")
  //   // Create an error message and append it to the emails-view
  //   const div = document.createElement('div');
  //   div.innerHTML = `<p>Error: ${result["error"]}</p>`
  //   document.querySelector('#emails-view').append(div)

  //   // Show emails view with message and hide other views
  //   document.querySelector('#emails-view').style.display = 'block';
  //   document.querySelector('#compose-view').style.display = 'none';
  //   console.log(error);
  //   return false;
  // }
  // console.log("end")
  return false;
}