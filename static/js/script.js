
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
gtag('config', 'G-F9XKYM3YYV');


// ローディング画面をフェードインさせてページ遷移
$(function(){
    // リンクをクリックしたときの処理。外部リンクやページ内移動のスクロールリンクなどではフェードアウトさせたくないので少し条件を加えてる。
    $(`a[href ^= "${location.href}"]` + 'a[target != "_blank"]').click(function(){
        var url = $(this).attr('href'); // クリックされたリンクのURLを取得
        $('#js-loader').fadeIn(600);    // ローディング画面をフェードイン
        setTimeout(function(){ location.href = url; }, 800); // URLにリンクする
        return false;
    });
});

// ページのロードが終わった後の処理
$(window).on('load', function(){
  $('#js-loader').delay(300).fadeOut(400); //ローディング画面をフェードアウトさせることでメインコンテンツを表示
});

// ページのロードが終わらなくても20秒たったら強制的に処理を実行
$(function(){ setTimeout('stopload()', 20000); });
function stopload(){
  $('#js-loader').delay(300).fadeOut(400); //ローディング画面をフェードアウトさせることでメインコンテンツを表示
}

// 画像が読み込めなかった場合に表示しない
document.addEventListener('DOMContentLoaded', () => {
    const images = [].slice.call(document.querySelectorAll('img'));
    images.forEach(el => {
      el.addEventListener('error', () => {
        el.remove();
      });
    });
  });


// ハンバーガーメニュー
$(function () { 
    $('#accordion li span').click(function() { 
        $(this).next('ul').slideToggle(); 
    }); 
});

// 日本地図の表示
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
        console.log(location.href)
        if($(this).data('id')){
            var id = $(this).data('id');
            if (  location.href.match(/recommend/) ) {
            console.log('recommend');
            $('[name="prefecture_name_en"]').val(id);
            prefReset();
            }
            else {
                console.log('else');
                window.location.href = location.href + 'prefecture/' + id;
                prefReset();
            }
        }
    });
    
    //表示リセット
    function prefReset(){
        $('[data-list]').hide();
        $('.pref_area').hide();
        $('.area_overlay').hide();
    }
});

//トップへ戻るボタン
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

// #syuzai_tableのデータテーブルの設定
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
        pageLength: 30,

        //列の幅を調整する
        autoWidth: true,
        
        // 初期表示の並び替えなし
        order: [],
    });
});

// #media_tableのデータテーブルの設定
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
        lengthMenu: [ 5, 10, 30, 50,100 ],
        // ページングの件数切替機能 無効
        pageLength: 30,

        //列の幅を調整する
        autoWidth: true,
        
        // 初期表示の並び替えなし
        order: []
    });

    $("#past_media_table").DataTable({
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
        lengthMenu: [ 5, 10, 30, 50,100 ],
        // ページングの件数切替機能 無効
        pageLength: 100,

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
        lengthMenu: [ 5, 10, 30, 50,100 ],
        // ページングの件数切替機能 無効
        pageLength: 30,

        //列の幅を調整する
        autoWidth: true,
        
        // 初期表示の並び替えなし
        order: []
    });
    $("#past_hall_table").DataTable({
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
        lengthMenu: [ 5, 10, 30, 50,100 ],
        // ページングの件数切替機能 無効
        pageLength: 100,

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

