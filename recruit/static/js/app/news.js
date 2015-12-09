/**
 * Created by junco on 15/11/13.
 */

$(function () {

    //招聘信息表格设置
    var table = $("#recruitnews").DataTable({
        "ajax": '/get_recruit_msg/',
        "columns": [
            {"data": "recruit_title"},
            {"data": "person_name"},
            {"data": "recruit_posttime"},
            {"data": "recruit_endtime"}
        ],
        // 关闭每页显示多少条数据的选择器
        "bLengthChange": false,
        // 关闭搜索过滤栏
        // 这个功能不能关掉，不然搜索
        //"bFilter": false,
        // 设置每页显示招聘动态数为10
        "iDisplayLength": 10,
        // 默认设置第3列降序排序，即按最新发布时间排序
        "aaSorting": [[2, "desc"]],
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

    // 发布新动态，激动模态框
    $("a[class='navbar-brand']").click(function () {
        $('#cerate_news').modal();
    });


    // 新招聘动态，发布验证
    $('#commitbtn').click(function () {
        // 获取各个表单的值
        var title = $('#title').val();
        var company = $('#company').val();
        var endtime = $('#endtime').val();
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
            toastr.error('请填写招聘企业', '提示');
            return false;
        }
        if (detail == '') {
            $('#detail').parent().addClass('has-error');
            toastr.error('请填写详细信息', '提示');
            return false;
        }

        $.post("/commit_recruit_news/", {
                title: title,
                company: company,
                endtime: endtime,
                detail: detail,
                csrfmiddlewaretoken: get_cookie('csrftoken')
            },
            function (data) {
                data = JSON.parse(data);
                result = data['result'];
                // 关闭modal
                if (result == false) {
                    toastr.error('动态发布失败，请联系网站管理员！' + data['message'], '出错啦！');
                }
                if (result == true) {
                    $('#closebtn').click();
                    toastr.success('动态发布成功', '提示');
                    // 重新加载datatables数据，使新增加的数据生效
                    table.ajax.reload();
                }
            }
        );
    });


    // 关闭modal的时候将表单进行清空
    $('#closebtn').click(function () {
        // 去掉所有的错误提示样式
        $('form div').removeClass('has-error');
        // 去掉所有input框的error样式
        $('#news_form')[0].reset();

    });

    // Datetimepicker
    var date = $('#endtime').datetimepicker({
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

    // datatables 点击某一行时，触发该行的行事件，通过该条消息的Id值来获取信息
    $('#recruitnews tbody').on('click', 'tr', function () {
        var object = table.row(this).data();
        var id = object.id;

        window.open('/recruit/' + id);

    });

});