var main = function() {
    $('#post_btn').click(function(){
        var post = $('#post_box').val();
        $('<li>').text(post).prependTo('#posts');
        $('#post_box').val('');
        $('.counter').text('500');
        $('#post_btn').addClass('disabled');
    });

    $('#post_box').keyup(function(){
        var postLength = $(this).val().length;
        var charactersLeft = 500 - postLength;

        $('.counter').text(charactersLeft);

        if(charactersLeft < 0) {
            $('.counter').text('0');
            $('#post_btn').addClass('disabled');
        } else if(charactersLeft == 500) {
            $('#post_btn').addClass('disabled');
        } else {
            $('#post_btn').removeClass('disabled');
        }
    });

    $('#post_btn').addClass('disabled');
}

$(document).ready(main);