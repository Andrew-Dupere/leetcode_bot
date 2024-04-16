// Select all elements with class "view-line"
var elements = document.querySelectorAll(".view-line");

// Iterate over the selected elements
elements.forEach(function(element) {
    // Set the text content of each element
    element.textContent = "Your text here";
});


// Select all elements with class "view-line"
var elements = document.querySelector(".view-line");

elements.focus();
