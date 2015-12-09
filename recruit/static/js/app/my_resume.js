/**
 * Created by junco on 15/11/24.
 */

$(function () {

    var themeColor = ['Red', 'Pink', 'Purple', 'Deep-Purple', 'Indigo', 'Blue', 'Light-Blue',
        'Cyan', 'Teal', 'Green', 'Light-Green', 'Lime', 'Yellow', 'Amber',
        'Orange', 'Deep-Orange', 'Brown', 'Grey', 'Blue-Grey'];

    $('#commitbtn').click(function () {
        // 如果之前有错误，先去掉之前的错误提示
        $('form div').removeClass('has-error');

        var resume_desc = $('#resume_desc').val();
        var tags = $("#tags").tagsinput('items');
        var filelist = document.getElementById('upload_file').files;

        if (!filelist.length) {
            toastr.warning('您还没有选择任何文件', '提示');
            return false;
        }

        if (tags.length == 0) {
            $('#tags').parent().addClass('has-error');
            toastr.warning('请至少为您的简历增加一个标签', '提示');
            return false;
        }

        // 检查是否支持FormData
        if (window.FormData) {
            file = filelist[0];
            var formData = new FormData();
            // 建立一个upload表单项，值为上传的文件
            formData.append('file', file);
            formData.append('tags', JSON.stringify(tags));
            formData.append('resume_desc', resume_desc);
            formData.append('csrfmiddlewaretoken', get_cookie('csrftoken'));

            var xhr = new XMLHttpRequest();
            xhr.open('POST', '/upload_resume/');

            // 定义上传完成后的回调函数
            xhr.onload = function () {
                data = JSON.parse(xhr.response);
                var result = data['result'];
                if (result) {
                    // 操纵DOM树，增加一份简历
                    addResumeToDom(data['message']);
                    $('#closebtn').click();
                    toastr.success('成功上传简历：' + file.name, '提示');
                    // 善后工作，清空文件上传框
                    $('.dropify-clear').click();
                    $('#resume_desc').val('');
                }
                else {
                    $('#closebtn').click();
                    toastr.error('上传简历失败:' + data['message'], '出错了');
                }
            };
            xhr.send(formData);
            xhr.upload.onprogress = function (event) {
                if (event.lengthComputable) {
                    var complete = (event.loaded / event.total * 100 | 0);
                    var progress = document.getElementById('uploadprogress');
                    progress.value = progress.innerHTML = complete;
                }
            };
        }
        else {
            toastr.error('该浏览器不支持文件上传，请使用Firefox，Chrome等浏览器！', '出错了');
        }
    });

    // 操纵DOM树，增加一份简历
    function addResumeToDom(message) {
        // count为当前页面已有简历数，也是当前最后一份简历的button按钮的value值，前端渲染时下标是从1开始计算的
        var count = $('.resume-item').length;

        var html = '<div class="col-md-4 col-sm-6 col-xs-12 resume-item">' +
            '<article class="material-card">' +
            '<h2>' +
            '<span><h5>' + message['resume_name'] + '</h5></span>' +
            '<strong><h5>上传于' + message['upload_time'] + '</h5></strong>' +
            '</h2>' +
            '<div class="mc-content">' +
            '<div class="img-container">' +
            '<img class="img-responsive" src="' + message['resume_thumb'] + '"></div>' +
            '<div class="mc-description">' + message['resume_desc'] + '</div>' +
            '</div>' +
            '<a class="mc-btn-action"><i class="fa fa-bars"></i></a>' +
            '<div class="mc-footer">' +
            '<div class="col-md-12 col-sm-12 col-xs-12">';
        if (message['is_gathered']) {
            html = html + '<input type="checkbox" class="gather" value="' + message['resume_id'] + '" checked>可被收集';
        }
        else {
            html = html + '<input type="checkbox" class="gather" value="' + message['resume_id'] + '">可被收集';
        }
        html = html + '</div>' +
            '<div class="btn-group btn-group-sm" role="group" aria-labelledby>' +
            '<button type="button" class="btn btn-success" value="' + count + 1 + '"' +
            'onclick="window.open("/resume/' + message['resume_id'] + '")">' +
            '<i class="fa fa-search"></i>&nbsp;查看' +
            '</button>' +
            '<button type="button" class="btn btn-info"' +
            'onclick="window.open("' + message['resume_url'] + '")">' +
            '<i class="fa fa-cloud-download"></i>&nbsp;下载' +
            '</button>' +
            '<button type="button" class="btn btn-danger deletebtn" value="' + message['resume_id'] + '">' +
            '<i class="fa fa-times"></i>&nbsp;删除' +
            '</button>' +
            '</div>' +
            '</div>' +
            '</article>' +
            '</div>';

        // 找出最后一个简历对象，在它后面append新上传的简历
        $('.resume-group').append(html);

        // 初始化简历样式
        $('.material-card').materialCard({
            icon_close: 'fa-arrow-left',
            icon_open: 'fa-bars',
            icon_spin: 'fa-spin-fast',
            card_activator: 'click'       //string: click or hover
        }).each(function () {
            $(this).addClass(themeColor[Math.floor(Math.random() * themeColor.length)]);
        });

    }


    // 初始化简历样式
    $('.material-card').materialCard({
        icon_close: 'fa-arrow-left',
        icon_open: 'fa-bars',
        icon_spin: 'fa-spin-fast',
        card_activator: 'click'       //string: click or hover
    }).each(function () {
        $(this).addClass(themeColor[Math.floor(Math.random() * themeColor.length)]);
    });


    $('.gather').mousedown(function () {
        var checkobj = $(this);
        var resume_id = $(this).val();
        var checked = $(this)[0].checked;

        var content = '';
        if (checked) {
            content = '确定要将该简历标记为【不可被收集】吗？取消标记后，该简历将不会被收集';
        }
        else {
            content = '确定要将该简历标记为【可收集】吗？标记成功后，该简历将会出现在筛选列表中';
        }

        $.confirm({
            title: '确认',
            content: content,
            confirmButtonClass: 'btn-danger',
            confirmButton: '确定',
            cancelButtonClass: 'btn-primary',
            cancelButton: '取消',
            animation: 'rotate',
            // 6秒后自动点击cancel按钮，以 | 作为分隔，时间单位为毫秒
            autoClose: 'cancel|6000',
            icon: 'fa fa-warning',
            // 禁止在框外触发单击事件
            backgroundDismiss: false,
            confirm: function () {
                $.post("/change_resume_gathered/", {
                        id: resume_id,
                        csrfmiddlewaretoken: get_cookie('csrftoken')
                    },
                    function (data) {
                        data = JSON.parse(data);
                        result = data['result'];
                        if (result == false) {
                            toastr.error('简历状态修改失败，请联系网站管理员！' + data['message'], '出错啦！');
                        }
                        if (result == true) {
                            checkobj.click();
                            toastr.success('修改简历状态成功！', '提示');
                        }
                    }
                );
            },
            cancel: function () {
                return false;
            }
        });
    });

    // 简历删除按钮点击事件
    $('.deletebtn').click(function () {
        resume_id = $(this).val();
        resume_obj = $(this).parents('.resume-item');
        $.confirm({
            title: '确认',
            content: '确认要删除此简历吗？',
            confirmButtonClass: 'btn-danger',
            confirmButton: '确定',
            cancelButtonClass: 'btn-primary',
            cancelButton: '取消',
            animation: 'rotate',
            // 6秒后自动点击cancel按钮，以 | 作为分隔，时间单位为毫秒
            autoClose: 'cancel|6000',
            icon: 'fa fa-warning',
            // 禁止在框外触发单击事件
            backgroundDismiss: false,
            confirm: function () {
                $.post("/delete_resume/", {
                        id: resume_id,
                        csrfmiddlewaretoken: get_cookie('csrftoken')
                    },
                    function (data) {
                        data = JSON.parse(data);
                        result = data['result'];
                        if (result == false) {
                            toastr.error('简历删除失败，请联系网站管理员！' + data['message'], '出错啦！');
                        }
                        if (result == true) {
                            resume_obj.remove();
                            toastr.success('删除成功！', '提示');
                        }
                    }
                );
            },
            cancel: function () {
                return false;
            }
        });
    });


    // 初始化文件上传框
    $('.dropify').dropify({
        messages: {
            'default': '点击选择文件 或拖拽文件到这里</br>仅支持PDF格式',
            'replace': '点击或拖拽文件到这里来替换文件',
            'remove': '移除文件',
            'error': '对不起，您的简历太大了</br>最大允许文件大小：500K'
        },
        // 设置可上传简历的最大大小
        maxFileSize: '1M'
    });


    // Twitter Typehead.js 这个太麻烦了，文档看不明白。总之是用来提示标签补全的
    var tag = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.whitespace,
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        // 所有标签全部存在LocolStorage中，可能获取到的不是数据库中最新的标签
        prefetch: '/get_tags/'
    });

    $('#tags').tagsinput({
        typeaheadjs: {
            name: 'tags',
            autoSelect: true,
            source: tag
        }
    });


});