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
        console.log(element.getAttribute('name'));
        const [right, top] = element.getAttribute('name').split(';');
        // console.log(right, top);
        element.style.right = 100 - right + "%";
        element.style.top = 100 - top + "%";
        element.style.height = (60 / (Math.max(elements.length, 1) ** 1.1)) + "%";
        console.log(element.style.height,element.style.left,element.style.top);

    });
}