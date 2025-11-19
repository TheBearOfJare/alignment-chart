if (window.location.pathname.includes("/view")) {
    const chartTitle = window.location.pathname.split('/view')[1].split('/')[0];

    document.getElementById('displayTitle').addEventListener('click', () => {
        window.location.href = '/charts' + chartTitle;
    })
}
else {
    const chartTitle = window.location.pathname.split('/charts')[1].split('/')[0];
    document.getElementById('displayTitle').addEventListener('click', () => {
        window.location.href = '/make' + chartTitle;
    })
}

// get all the temperatures
const temperatures = document.querySelectorAll('#temperature');

for (let i = 0; i < temperatures.length; i++) {
    degrees = parseInt(temperatures[i].innerHTML);
    temperatures[i].style.color = getGradient(degrees);
    flame = temperatures[i].children[0];
    if (degrees > 50) {
        flame.style.opacity = degrees / 100;
    }
    else {
        flame.style.opacity = 0;
    }
}

function getGradient(value) {
    if (value > 50) {
        red = 255 * value / 100;
        green = 255* value/200;
        blue = 255 * (100 - value) / 200;
    }
    else {
        red = 255* value/200;
        green = 0;
        blue = 255 * (100 - value) / 100;
    }
    
    
    return `rgb(${red}, ${green}, ${blue})`;

}