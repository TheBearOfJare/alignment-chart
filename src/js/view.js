function setHeightFromWidth(element) {
    const width = element.offsetWidth;
    element.style.height = `${width}px`;
}

const q1 = document.getElementById('q1');
const q2 = document.getElementById('q2');
const q3 = document.getElementById('q3');
const q4 = document.getElementById('q4');
if (window.location.pathname.includes("/view")) {
    const chartTitle = window.location.pathname.split('/view')[1].split('/')[0];

    document.getElementById('displayTitle').addEventListener('click', () => {
    window.location.href = '/charts' + chartTitle;
})
}
else {
    const chartTitle = window.location.pathname.split('/charts')[1].split('/')[0];
}


setHeightFromWidth(q1);
setHeightFromWidth(q2);
setHeightFromWidth(q3);
setHeightFromWidth(q4);
placeElements();

window.addEventListener('resize', () => {
    setHeightFromWidth(q1);
    setHeightFromWidth(q2);
    setHeightFromWidth(q3);
    setHeightFromWidth(q4);
    placeElements();
});

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


function placeElements() {
    const elements = document.querySelectorAll('.element');
    Array.from(elements).forEach(element => {
        // console.log(element.getAttribute('name'));
        const name = element.getAttribute('name');
        if (name == "unranked") {
            // make it a child of the unranked container
            element.parentNode.removeChild(element);
            document.getElementById('unranked').appendChild(element);
        }
        else {
            const [right, top] = name.split(';');
            // console.log(right, top);
            element.style.right = 100 - right + "%";
            element.style.top = 100 - top + "%";
            element.style.height = Math.max(60 / (Math.max(elements.length, 1)), 5) + "%";
            // console.log(element.style.height,element.style.right,element.style.top);
        }

    });
}