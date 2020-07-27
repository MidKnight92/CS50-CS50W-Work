// async function sent_email(){
//     // Get the values
//     try {
//       const recipients =  document.querySelector('#compose-recipients').value;
//       const subject = document.querySelector('#compose-subject').value;
//       const body =  document.querySelector('#compose-body').value; 
//       const createEmailResponse = await fetch('/emails', {
//         method: 'POST',
//         body: JSON.stringify({
//           recipients: `${recipients}`,
//           subject: `${subject}`,
//           body: `${body}`
//         })
//       });
//       const parsedEmail = await createEmailResponse.json();
//       console.log(parsedEmail);
//     } catch (error) {
//       console.log(error);
//     }
// }
function sent_email() {
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: 'baz@example.com',
      subject: 'Meeting time',
      body: 'How about we meet tomorrow at 3pm?'
    })
  })
    .then(response => response.json())
    .then(result => {
      // Print result
      console.log(result);
    });
}
