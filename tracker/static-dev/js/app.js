
(function($) {
$.fn.extend({
    postlink: function() {
        return this.each(function() {
            $(this).click(function(e) {
                var frm = $(this).closest("form");
                frm.append("<input type='hidden' name='transition' value='" + $(this).data('transition') + "'>");
                frm.submit();
                e.preventDefault();
            });
        });
    }
});
})(jQuery);


$(document).foundation({
    equalizer : {
        equalize_on_stack: true,
    }
});


$(document).ready(function(){
    $(".postlink").postlink();
})

