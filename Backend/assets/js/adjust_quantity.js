 $(document).ready(function(){
            $('button').click(function(){
                //$('#test').html("here");
                var $button = $(this);
                var oldValue = $button.parent().find("input").val();
                var name = $button.parent().parent().parent().find("td:eq(1)");
                var restaurant = $button.parent().parent().parent().find("td:eq(0)");
                var id = $button.parent().parent().parent().find("td:eq(5)");

                if ($button.text() == "+") {
                    var newVal = parseInt(oldValue) + 1;
                    //var n1 = $button.parent().parent().parent().find("td:eq(1)");
                    name.css({"color":"red"});
                    $.ajax({
                        type: 'POST',
                        dataType: 'json',
                        url: '/increment',
                        data: {
                                'dish_name': name.text(),
                                'restaurant_name': restaurant.text(),
                                'id': id.text()
                              },
                        async: true,
                        success: function(data){
                            $('#test').html(data.name + ' ' + data.other + ' ' + data.id);
                        },
                        error:function(exception){alert('Exeption:'+exception);}
                    });
                } else if ($button.text() == "-") {
                    if (oldValue > 0) {
                        var newVal = parseInt(oldValue) - 1;
                        //var n2 = $button.parent().parent().parent().find("td:eq(1)");
                        name.css({"color":"green"});
                        $.ajax({
                            type: 'POST',
                            dataType: 'json',
                            url: '/decrement',
                            data: {
                                    'dish_name': name.text(),
                                    'restaurant_name': restaurant.text(),
                                    'id': id.text()
                                  },
                            async: true,
                            success: function(data){
                                $('#test').html(data.name + ' ' + data.other + ' ' + data.id);
                            },
                            error:function(exception){alert('Exeption:'+exception);}
                        });
                    } else {
                        newVal = 0;
                    }
                }

                $button.parent().find("input").val(newVal);
            });
            $('#paybutton')
        });