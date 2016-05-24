/**
 * Created by junco on 15/12/3.
 */

$(function () {

    $.get('/get_tags_with_id/', {}, function (data) {
        $("#tags").select2({
            data: JSON.parse(data),
            tags: true
        });
    });

    var themeColor = ['Red', 'Pink', 'Purple', 'Deep-Purple', 'Indigo', 'Blue', 'Light-Blue',
        'Cyan', 'Teal', 'Green', 'Light-Green', 'Lime', 'Yellow', 'Amber',
        'Orange', 'Deep-Orange', 'Brown', 'Grey', 'Blue-Grey'];

    $("#filter_btn").click(function () {
        $('.resume-group').empty();
        var tags = $("#tags").val();
        $.post('/filter_resume/',
            {
                tags: JSON.stringify(tags),
                csrfmiddlewaretoken: get_cookie('csrftoken')
            },
            function (data) {
                $('.resume-group').html(data);
                
                // 初始化简历样式
                $('.material-card').materialCard({
                    icon_close: 'fa-arrow-left',
                    icon_open: 'fa-bars',
                    icon_spin: 'fa-spin-fast',
                    card_activator: 'click'       //string: click or hover
                }).each(function () {
                    $(this).addClass(themeColor[Math.floor(Math.random() * themeColor.length)]);
                });

            });

    })
});