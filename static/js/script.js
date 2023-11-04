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
            $('[name="pref_id"]').val(id);
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


$(function() {
    var topBtn = $('.page-top');    
    topBtn.hide();
    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            topBtn.fadeIn();
        } else {
            topBtn.fadeOut();
        }
    });
    topBtn.click(function () {
        $('body,html').animate({
            scrollTop: 0
        }, 50);
        return false;
    });
});


$(document).ready(function(){
    $("#syuzai_table").DataTable({
        "language":{url:"https://cdn.datatables.net/plug-ins/1.11.5/i18n/ja.json",},
            // 件数切替機能 無効
        lengthChange: true,
        // 検索機能 無効
        searching: true,
        // ソート機能 無効
        ordering: true,
        // 情報表示 無効
        info: true,
        // ページング機能 無効
        paging: true,
        // ページングの件数切替機能 無効
        pagingType: "full_numbers",
        // ページングの件数切替機能 無効
        lengthMenu: [ 5, 10, 30, 100 ],
        // ページングの件数切替機能 無効
        pageLength: 6,

        //列の幅を調整する
        autoWidth: true,
        
        // 初期表示の並び替えなし
        order: [],
    });
});

$(document).ready(function(){
    $("#media_table").DataTable({
        "language":{url:"https://cdn.datatables.net/plug-ins/1.11.5/i18n/ja.json",},
        // 件数切替機能 無効
        lengthChange: true,
        // 検索機能 無効
        searching: true,
        // ソート機能 無効
        ordering: true,
        // 情報表示 無効
        info: true,
        // ページング機能 無効
        paging: true,
        // ページングの件数切替機能 無効
        pagingType: "full_numbers",
        // ページングの件数切替機能 無効
        lengthMenu: [ 5, 10, 30, 100 ],
        // ページングの件数切替機能 無効
        pageLength: 6,

        //列の幅を調整する
        autoWidth: true,
        
        // 初期表示の並び替えなし
        order: []
    });
    $("#hall_table").DataTable({
        "language":{url:"https://cdn.datatables.net/plug-ins/1.11.5/i18n/ja.json",},
            // 件数切替機能 無効
        lengthChange: true,
        // 検索機能 無効
        searching: true,
        // ソート機能 無効
        ordering: true,
        // 情報表示 無効
        info: true,
        // ページング機能 無効
        paging: true,
        // ページングの件数切替機能 無効
        pagingType: "full_numbers",
        // ページングの件数切替機能 無効
        lengthMenu: [ 5, 10, 30, 100 ],
        // ページングの件数切替機能 無効
        pageLength: 6,

        //列の幅を調整する
        autoWidth: true,
        
        // 初期表示の並び替えなし
        order: []
    });
});

$(function() {
    $("#date_pick").datepicker({
        locale: 'ja',
        dateFormat: 'yy年MMdd日 (DD)',
        yearSuffix: '年',
        showMonthAfterYear: true,
        monthNames: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
        dayNames: ['日', '月', '火', '水', '木', '金', '土'],
        dayNamesMin: ['日', '月', '火', '水', '木', '金', '土'],
        ignoreReadonly: true,
        minDate: new Date(),
        maxDate: '+6d'
    }).css({
        'margin': 'auto',
        'padding': 'auto',
        });
});
