function selected (){
    for(l in menulist){
        if(menulist[l]['url'] === window.location.pathname)
        {
            $('#baritem-'+l).css({'font-weight': '900', 'color':'#C1E800',});
        }
    }
}

function adduserinfo(text){
    $('#userinfo').html(function(){
        return '<img src="/static/img/user.png"> '+text;
    });
}

$(document).ready(function(){
    $('.baritem').live('mouseover', function(){
        $(this).css({'background-color': '#636363'});
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
                  'height': '30px',
                  'background-color': '#242424',
                  'color': 'white',
                  'padding-top': '10px',
                  'margin': '0',
    });
    $(divbar).prepend(
        $('<span>', {id: 'userinfo'})
        .css({ 'height':'30px', 'padding': '12px', 'margin': '0', 'right': '20px', 'top':'0px', 'position':'absolute'})

    );
    menulist = {1: {'url': '/add', 'name': 'Добавить'},
                2: {'url': '/', 'name': 'список'},
                }

    for (m = Object.keys(menulist).length; m>0; m--){
        $(divbar).prepend(
            $('<span>', {id: 'baritem-'+m, class: 'baritem'})
            .css({ 'height':'30px', 'padding': '12px', 'cursor': 'pointer', 'margin': '0', 'border-radius': '6px'})
            .text(menulist[m]['name'])
        );
    }
    
       
    $('body').prepend(divbar);
    selected();
});
