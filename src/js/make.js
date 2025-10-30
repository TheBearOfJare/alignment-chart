function setHeightFromWidth(element) {
    const width = element.offsetWidth;
    element.style.height = `${width}px`;
}

const q1 = document.getElementById('q1');
const q2 = document.getElementById('q2');
const q3 = document.getElementById('q3');
const q4 = document.getElementById('q4');

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


var isDragging = false;
var startX, startY, activeElement;

document.addEventListener("DOMContentLoaded", function() {

    const chartDiv = document.getElementById('chart');
    // const elements = document.querySelectorAll('.element');

    chartDiv.addEventListener('click', (e) => {
        if (!e.target.classList.contains('element')) {
            if (isDragging) {
                isDragging = false;
                activeElement.name = `${Math.max(0,Math.min(100 - Math.floor(activeElement.style.right.toString().replace('px', '')/chartDiv.offsetWidth*100), 100))};${Math.min(100, Math.max(0, 100 - Math.floor(activeElement.style.top.toString().replace('px', '')/chartDiv.offsetHeight*100)))}`;
                console.log(activeElement.name);
                
                placeElements();
                return;
            }
            else {
                return;
            }
        }

        
        if (!isDragging) {
            activeElement = e.target;
            isDragging = true;
        }
        else {
            isDragging = false;
            activeElement.name = `${Math.max(0,Math.min(100 - Math.floor(activeElement.style.right.toString().replace('px', '')/chartDiv.offsetWidth*100), 100))};${Math.min(100, Math.max(0, 100 - Math.floor(activeElement.style.top.toString().replace('px', '')/chartDiv.offsetHeight*100)))}`;
            placeElements();
        }
    });

    chartDiv.addEventListener('mousemove', (e) => {
        if (!isDragging) return;

        const x = e.pageX - chartDiv.offsetLeft + (activeElement.offsetWidth / 2);
        const y = e.pageY - chartDiv.offsetTop - (activeElement.offsetHeight / 2);

        activeElement.style.right = `${chartDiv.offsetWidth - x}px`;
        activeElement.style.top = `${y}px`;
    });


    // submit all the elements and the author name to go in the database
    this.getElementById('submit').addEventListener('click', () => {
        
        elements = [];
        for (var i = 0; i < document.querySelectorAll('.element').length; i++) {
            elements.push(document.querySelectorAll('.element')[i].getAttribute('name'));
        }

        chartTitle = window.location.pathname.split('/make')[1];
        // console.log(chartTitle);
        // post to /make
        fetch('/make' + chartTitle, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "author": document.getElementById('author').value,
                "data": elements
            })
        }).then(response => {
            if (response.ok) {
                window.location.href = '/view' + chartTitle + '/' + document.getElementById('author').value;
            }
            
        })
            
    })


});


function moveToUnranked(element) {
    element.parentNode.removeChild(element);
    document.getElementById('unranked').appendChild(element);
}

function moveToChart(element) {
    element.parentNode.removeChild(element);
    document.getElementById('chart').appendChild(element);
}

