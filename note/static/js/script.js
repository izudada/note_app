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