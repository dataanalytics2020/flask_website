$(function () { 
    $('#accordion li span').click(function() { 
        $(this).next('ul').slideToggle(); 
    }); 
});


$(function(){
    //地域を選択
    $('.area_btn').click(function(){
        $('.area_overlay').show();
        $('.pref_area').show();
        var area = $(this).data('area');
        $('[data-list]').hide();
        $('[data-list="' + area + '"]').show();
    });
    
    //レイヤーをタップ
    $('.area_overlay').click(function(){
        prefReset();
    });
    
    //都道府県をクリック
    $('.pref_list [data-id]').click(function(){
        if($(this).data('id')){
            var id = $(this).data('id');
            //都道府県IDに応じて別ページに飛ばす
            console.log('window.location.href')
            console.log(window.location.href)
            let domain_url = window.location.href.replace('/top','')
            window.location.href =  domain_url  + '/recommend/' + id;
            prefReset();
        }
    });
    
    //表示リセット
    function prefReset(){
        $('[data-list]').hide();
        $('.pref_area').hide();
        $('.area_overlay').hide();
    }
});

