document.getElementById("hamburguer").addEventListener("click", function() {
    var content = document.getElementById("meat");
    if (content.style.display === "none") {
        content.style.display = "block";
    } else {
        content.style.display = "none";
    }
});