document.addEventListener("DOMContentLoaded", function() {
    console.log("Page loaded and scripts.js is working!");
});


$(document).ready(function() {
    var startDate = new Date("{{ job.start_time }}"); // Parse the start time
    var endDate = new Date("{{ job.end_time }}"); // Parse the end time
    var currentDate = new Date(); // Get the current date

    // Calculate progress percentage
    var totalDuration = endDate - startDate;
    var elapsedDuration = currentDate - startDate;
    var progressPercentage = (elapsedDuration / totalDuration) * 100;

    // Set the width of the progress bar
    $('.timeline-progress').css('width', progressPercentage + '%');
});
