document.addEventListener("mousemove", (e) => {
    const cursor = document.querySelector(".cursor");
    const circle = document.querySelector(".cursor-circle");

    cursor.style.left = `${e.clientX}px`;
    cursor.style.top = `${e.clientY}px`;

    circle.style.left = `${e.clientX}px`;
    circle.style.top = `${e.clientY}px`;
});
