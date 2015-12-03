/**
 * Created by junco on 15/11/13.
 */

$(function () {

    // 面试交流  整个大表格设置
    var table = $("#communication").DataTable({
        "ajax": '/get_communications_msg/',
        "columns": [
            {"data": "interview_title"},
            {"data": "person_name"},
            {"data": "interview_company"},
            {"data": "interview_time"}
        ],
        // 关闭每页显示多少条数据的选择器
        "bLengthChange": false,
        // 关闭搜索过滤栏
        // 这个功能不能关掉，不然搜索
        //"bFilter": false,
        // 设置每页显示招聘动态数为10
        "iDisplayLength": 10,
        // 默认设置第4列降序排序，即按最新发布时间排序
        "aaSorting": [[3, "desc"]],
        "oLanguage": {
            //国际化配置
            "sProcessing": "正在获取数据，请稍后...",
            "sLengthMenu": "每页 _MENU_ 条",
            "sZeroRecords": "没有您要搜索的内容",
            "sInfo": " _START_ - _END_ ，共 _TOTAL_ 条",
            "sInfoEmpty": "记录数为0",
            "sInfoFiltered": "(共 _MAX_ 条)",
            "sSearch": "搜索",
            "oPaginate": {
                "sFirst": "第一页",
                "sPrevious": "上一页",
                "sNext": "下一页",
                "sLast": "最后一页"
            }
        }
    });

    // 在CSS中将select的默认"placeholder"字体颜色改为统一样式，其它标题颜色都是#94aab0
    // 但是这会导致其它选项的颜色也变为#94aab0，所以通过监听change事件来让其变回黑色
    $("#interview_class").on("change", function () {
        $(this).css({
            'color': 'black'
        });
    });

    // datatables 点击某一行时，触发该行的行事件，通过该条消息的Id值来获取信息
    $('#recruitnews tbody').on('click', 'tr', function () {
        var object = table.row(this).data();
        var id = object.id;
        // 通过向后台post已获得的id值，来获取该id值对应的信息
        $.post("/get_communication/",
            {
                id: id,
                csrfmiddlewaretoken: get_cookie('csrftoken')
            },
            function (data) {
                show_detail(JSON.parse(data));
            });
    });

    function show_detail(data) {
        console.log(data);
    }

    // DataTables自定义搜索框，原来的搜索框位置太恶心了，单独占一个row还是在右上方
    // 不能将bFilter设置为false，否则会关闭过滤功能，只能通过CSS将.datatables_filter设置为display: none
    // 然后再在自定义的input框上使用datatables的search方法来进行过滤
    $("#searchbox").bind("keyup search input paste cut", function () {
        table.search(this.value).draw();
    });

    // 重置搜索条件，使表格恢复到初始状态
    $("#resetbtn").click(function () {
        table.search('').draw();
    });


    // 新招聘动态，发布验证
    $('#commitbtn').click(function () {
        // 获取各个表单的值
        var title = $('#title').val();
        var company = $('#company').val();
        var interview_time = $('#interview_time').val();
        var interview_way = $("input[name='btn']:checked").val();
        var interview_class = $('#interview_class').val();
        var detail = $('#detail').val();

        // 如果之前有错误，先去掉之前的错误提示
        $('form div').removeClass('has-error');

        if (title == '') {
            $('#title').parent().addClass('has-error');
            toastr.error('请填写动态标题', '提示');
            return false;
        }
        if (company == '') {
            $('#company').parent().addClass('has-error');
            toastr.error('请填写面试企业', '提示');
            return false;
        }
        if (interview_time == '') {
            $('#interview_time').parent().addClass('has-error');
            toastr.error('请选择面试时间', '提示');
            return false;
        }

        // 如果没有按钮被checked
        if (!interview_way) {
            interview_way = 0;
        }
        if (interview_way == 0) {
            $('input[name="btn"]').parents('.form-group').addClass('has-error');
            toastr.error('请选择面试形式', '提示');
            return false;
        }
        if (interview_class == null) {
            $('#interview_class').parent().addClass('has-error');
            toastr.error('请选择面试类别', '提示');
            return false;
        }
        if (detail == '') {
            $('#detail').parent().addClass('has-error');
            toastr.error('请填写面试内容整理', '提示');
            return false;
        }

        $.post("/commit_communication/", {
                title: title,
                company: company,
                interview_time: interview_time,
                interview_way: interview_way,
                interview_class: interview_class,
                detail: detail,
                csrfmiddlewaretoken: get_cookie('csrftoken')
            },
            function (data) {
                data = JSON.parse(data);
                result = data['result'];
                // 关闭modal
                if (result == false) {
                    toastr.error('发布失败，请联系网站管理员！' + data['message'], '出错啦！');
                }
                if (result == true) {
                    $('#closebtn').click();
                    toastr.success('面试经历分享成功', '提示');
                    table.ajax.reload();
                }
            }
        );
    });


    // 关闭modal的时候将表单进行清空
    $('#closebtn').click(function () {
        // 去掉所有的错误提示样式
        $('.error-message').remove();
        // 去掉所有input框的error样式
        $('input').removeClass('error');
        $('textarea').removeClass('error');
        $('#news_form')[0].reset();

    });

    // Datetimepicker
    var date = $('#interview_time').datetimepicker({
        format: 'yyyy-mm-dd',
        minView: "month",
        autoclose: true,
        todayHighlight: true,
        language: 'zh-CN'
    });

    // 初始化Markdown
    $('#detail').markdown({
        autofocus: true,
        savable: false,
        resize: 'vertical',
        iconlibrary: 'fa',
        language: 'zh'
    });

});