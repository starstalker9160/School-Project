document.addEventListener("DOMContentLoaded", function () {
    const colors = ["#EE6352", "#746afe", "#59CD90", "#3FA7D6", "#FAC05E"];
    document.body.style.backgroundColor =  colors[Math.floor(Math.random() * colors.length)];
});
