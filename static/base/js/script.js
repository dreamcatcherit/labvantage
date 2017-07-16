/**
 * Created by prism on 10/22/16.
 */
(function() {
    /*
    validate password in create user form
     */


    $(function () {
        $("#create_user").click(function () {
            var password = $("#password").val();
            var confirmPassword = $("#confirm_password").val();
            if (password != confirmPassword) {
                $('#user_create_error_message').append("<div id='password_not_matching'>Password is not matching</div>");
                return false;
            }
            return true;
        });
    });
   $('#password').on('input', function () {
        if(!($('#password_not_matching').length == 0))
            $('#password_not_matching').remove();
    });
    $('#confirm_password').on('input', function () {
        if(!($('#password_not_matching').length == 0))
            $('#user_create_error_message').remove();
    });

    // $("#req-form").submit(function (e) {
    //     e.preventDefault();
    //     if($('#password').val() === $('#confirm_password').val()) {
    //         $('#req-form').submit();
    //     } else {
    //         if($('#password_not_matching').length == 0)
    //             $('#user_create_error_message').append("<div id='password_not_matching'>Password is not matching</div>");
    //     }
    //
    // })
    /*
     * date time picker method
     *
     */
     $(function(){
                                                $("#datetimepicker1").datetimepicker();
                                                $("#datetimepicker2").datetimepicker();
                                                $("#datetimepicker3").datetimepicker();
                                                $("#datetimepicker4").datetimepicker();
                                                $("#datetimepicker5").datetimepicker();
                                                $(".dtpick").datetimepicker();
                                            });
    $('#ati_mins').change(function(){
        $("#ati_typical").attr({
   "min" : $('#ati_mins').val(),
   "max" : $('#ati_maxs').val()
});
    });
    $('#ati_maxs').change(function(){
                $("#ati_typical").attr({
                    "max" : $('#ati_maxs').val(),
                    "min" : $('#ati_mins').val()
});

    });


//    eims/view_calibration_test/id/<id>

    $('#add_field').click(function(){
       
        $('#attachments').append(
            "<div class='control-group'><label class='control-label' for='upload_file'>Upload File</label> <div class='controls'>							  <input class='input-xlarge focused' name='upload_file' type='file' ></div></div>"

        );
    });

})();