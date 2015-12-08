function newComment(time, user_name, comment){
    img_emelemt = '<img src="http://www.gnosko.com/dist/img/unknown.gif" class="avatar"/>';
    comment_element = '<div class="post-comments"><P class="meta">' + time + ' <b>' + user_name + '</b> says:</p>' +
            '<p>'+ comment + '</p></div>';

    return img_emelemt + comment_element;
}

function getUserName(time, comment){
    var username = "Default";
    $.ajax({
        type: 'GET',
        dataType: 'json',
        url: '/getuserinfo',
        data: {'time': time, 'comment': comment},
        async: false,
        success: function(data){
            username = data.name;
        }
    });

    return username;
}

var main = function() {
    $('#post_btn').click(function(){
        var post = $('#post_box').val();
        var current_time = new Date();

        post = newComment(current_time.toUTCString(), getUserName(current_time, post), post);
        $('<li class="clearfix">').append(post).prependTo('#posts');
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