;(function($){
    $(document).ready(function(){

        function fix_form_action(){
            var form = $("#content-main form");
            if(form.length > 0){
                var action = form.attr("action");
                var href = window.location.href;
                if(href.indexOf("_edit_flag=1") >= 0){
                    if(action.indexOf("?") < 0){
                        action += "?";
                    }
                    action += "&_edit_flag=1";
                }
                action = action.replace("?&", "?").replace("&&", "&");
                form.attr("action", action);
            }
        }
        window.setTimeout(fix_form_action, 1);

        $(".submit-row .cancellink").each(function(){
            var href = window.location.href;
            if(href.indexOf("_edit_flag=1") >= 0){
                href = href.replace("_edit_flag=1", "");
            }
            href = href.replace("?&", "?").replace("&&", "&");
            $(this).attr("href", href);
        });
        $(".submit-row .editlink").each(function(){
            var href = window.location.href;
            if(href.indexOf("?") < 0){
                href += "?";
            }
            href += "&_edit_flag=1";
            href = href.replace("?&", "?");
            $(this).attr("href", href);
        });
        
    });
})(jQuery);
