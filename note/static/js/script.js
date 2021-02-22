$(document).ready(function(){
    var adjustSideBar = function(){
        $(".sidebar").slimScroll({
            height:document.documentElement.clientHeight - $(".navbar").outerHeight()
        });
    };

    adjustSideBar();

    $(window).resize(function(){
        adjustSideBar();
    });

    $(".sideMenuToggler").on("click", function() {
        $(".wrapper").toggleClass("active");
    });
});

function deleteCategory(catID){
    fetch('/delete_category', {
        method: 'POST',
        body: JSON.stringify({catID: catID})
    }).then((_res) => {
        window.location.href = "/home" 
    })
}

function deleteNote(noteID, catID){
    fetch('/delete_note', {
        method: 'POST',
        body: JSON.stringify({noteID: noteID})
    })
    .then((_res) => {
        window.location.href = "/categories/" + catID + "/notes" 
    })
}