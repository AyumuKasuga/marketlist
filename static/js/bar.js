$(document).ready(function(){
    $('.baritem').live('mouseover', function(){
        $(this).css({'background-color': 'red'});
    });
    $('.baritem').live('mouseout', function(){
        $(this).css({'background-color': ''});
    });
    $('.baritem').live('click', function(){
        id = $(this).attr('id').replace('baritem-','');
        window.location =  menulist[id]['url'];
    });
    
    var divbar = $('<div>', {id: 'bar'});
    $(divbar).css({'width': '100%',
                  'height': '25px',
                  'background-color': 'black',
                  'color': 'white',
                  'padding': '5px',
                  });

    menulist = {1: {'url': '/add', 'name': 'Добавить'},
                2: {'url': '/test1', 'name': 'тест1'},
                }
    for (var m in menulist){
        $(divbar).prepend(
            $('<span>', {id: 'baritem-'+m, class: 'baritem'})
            .text(menulist[m]['name'])
            .css({ 'height':'100%', 'padding': '5px', 'cursor': 'pointer', 'margin': '2px',})
        );
    }

    $('body').prepend(divbar);
});