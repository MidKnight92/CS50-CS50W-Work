console.log("Running");

function walkingDog(){
    let element = document.getElementById("dog");
    let position = 0;
    let id = setInterval(frame, 5);

    function frame() {
        if (position === 180){
            clearInterval(id);
        } else {
            position++;
            element.style.top = `${position}px`;
            element.style.left = `${position}px`;
        }
    }
}

const getGeolocation = () => {
    let x = document.getElementById("location");

    if (navigator.geolocation){
        navigator.geolocation.getCurrentPosition(showPosition);
    } else {
        x.innerHTML = "You're lucky! I can not detect where you are."
    }
}

const showPosition = (position)=> {
    let x = document.getElementById("location");

    x.innerHTML = "<br>Latitude: " + position.coords.latitude + "<br>Longitude: " + position.coords.longitude;
}

