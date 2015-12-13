$(document).ready(function(){
    $('.faq_question').mouseenter(function(){
         $(this).addClass('current');
     });
    $('.faq_question').mouseleave(function(){
         $(this).removeClass('current');
     });
    $('.faq_question').click(function () {
        $(this).next('.ans').toggleClass('hidden');
    });
});