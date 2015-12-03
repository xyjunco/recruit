/**
 * Created by junco on 15/11/21.
 */

$(function () {

    var click_start_date = '';
    var click_end_date = '';
    var modify_start_date = '';
    var modify_end_date = '';
    var modify_id = 0;

    // 校招日历使用FullCalendar插件，详细配置参考 http://fullcalendar.io/docs/
    var calendar = $('#calendar').fullCalendar({
        // 国际化处理
        monthNames: ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"],
        monthNamesShort: ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"],
        dayNames: ["周日", "周一", "周二", "周三", "周四", "周五", "周六"],
        dayNamesShort: ["周日", "周一", "周二", "周三", "周四", "周五", "周六"],
        today: ["今天"],
        // 设置一周中显示的第一天是哪天，周日是0，周一是1
        firstDay: 1,
        // 设置标题格式
        titleFormat: 'YYYY年MMMM',
        // 设置按钮文字内容
        buttonText: {
            today: '今天',
            month: '月',
            week: '周',
            day: '日',
            prev: '前一月',
            next: '后一月'
        },
        // 设置标题样式，可自定义按钮位置
        header: {
            left: 'today',
            center: 'title',
            right: 'prev,next '
        },
        // 设置日历单元格宽度与高度的比例
        aspectRatio: 1.8,
        // 是否允许用户通过单击或拖动选择日历中的对象
        editable: true,
        // 是否允许单击进行选择
        selectable: true,
        // 当点击页面日历以外的位置时，是否自动取消当前的选中状态
        unselectAuto: true,
        events: '/get_calendar_events/',

        // 单击某一天，或选择多天时，在该时间范围上新建事件
        select: function (startDate, endDate) {
            click_start_date = startDate.format();
            click_end_date = endDate.format();
            $('#new_event_title').text(click_start_date + ' 至 ' + click_end_date + ' 新事件');
            $('#new_event_btn').click();
        },
        // 点击某一具体事件时
        eventClick: function (calEvent) {
            modify_id = calEvent.id;
            modify_start_date = calEvent.start.format();
            modify_end_date = (calEvent.end == null) ? modify_start_date : calEvent.end.format();

            // 如果事件跨度仅为一天，即calEvent.end为null：
            if (!calEvent.end) {
                $('#modify_title').text('编辑' + modify_start_date + '事件');
            }
            else {
                $('#modify_title').text('编辑' + modify_start_date + '-' + modify_end_date + '事件');
            }

            $('#modify_event_title').attr('value', calEvent.title);
            $('#modify_color').minicolors('value', calEvent.color);
            startpicker.val(modify_start_date);
            endpicker.val(modify_end_date);
            $('#modify_event_btn').click();
        },
        // 发生拖拽事件时
        eventDrop: function (event, delta, revertFunc) {
            var start = event.start.format();
            var end = (event.end == null) ? start : event.end.format();

            $.confirm({
                title: '确认',
                content: '确认要将事件“' + event.title + '”移动到' + start + '这天？',
                confirmButtonClass: 'btn-danger',
                confirmButton: '确定',
                cancelButtonClass: 'btn-primary',
                cancelButton: '撤消',
                animation: 'rotate',
                // 6秒后自动点击cancel按钮，以 | 作为分隔，时间单位为毫秒
                autoClose: 'cancel|6000',
                icon: 'fa fa-warning',
                // 禁止在框外触发单击事件
                backgroundDismiss: false,
                confirm: function () {
                    $.post("/update_calendar_event/", {
                            id: event.id,
                            event: event.title,
                            start: start,
                            end: end,
                            color: event.color,
                            csrfmiddlewaretoken: get_cookie('csrftoken')
                        },
                        function (data) {
                            data = JSON.parse(data);
                            result = data['result'];
                            // 关闭modal
                            if (result == false) {
                                revertFunc();
                                toastr.error('操作失败，请联系网站管理员！' + data['message'], '出错啦！');
                            }
                            if (result == true) {
                                $('#closebtn2').click();
                                toastr.success('成功将事件“' + event.title + '”移动到' + start, '提示');
                                //重新获取所有事件数据
                                $('#calendar').fullCalendar('refetchEvents');
                            }
                        }
                    );
                },
                cancel: function () {
                    revertFunc();
                }
            });
        },
        // 拉长或缩短事件
        eventResize: function (event, delta, revertFunc) {
            var start = event.start.format();
            var end = (event.end == null) ? start : event.end.format();

            $.confirm({
                title: '确认',
                content: '确认要将事件“' + event.title + '”的结束时间修改为' + end + '这天？',
                confirmButtonClass: 'btn-danger',
                confirmButton: '确定',
                cancelButtonClass: 'btn-primary',
                cancelButton: '撤消',
                animation: 'rotate',
                // 6秒后自动点击cancel按钮，以 | 作为分隔，时间单位为毫秒
                autoClose: 'cancel|6000',
                icon: 'fa fa-warning',
                // 禁止在框外触发单击事件
                backgroundDismiss: false,
                confirm: function () {
                    $.post("/update_calendar_event/", {
                            id: event.id,
                            event: event.title,
                            start: start,
                            end: end,
                            color: event.color,
                            csrfmiddlewaretoken: get_cookie('csrftoken')
                        },
                        function (data) {
                            data = JSON.parse(data);
                            result = data['result'];
                            // 关闭modal
                            if (result == false) {
                                revertFunc();
                                toastr.error('操作失败，请联系网站管理员！' + data['message'], '出错啦！');
                            }
                            if (result == true) {
                                $('#closebtn2').click();
                                toastr.success('成功将事件“' + event.title + '”的结束时间变更为' + end);
                                //重新获取所有事件数据
                                $('#calendar').fullCalendar('refetchEvents');
                            }
                        }
                    );
                },
                cancel: function () {
                    revertFunc();
                }
            });
        }
    });


    // 删除事件
    $('#deletebtn').click(function () {
        $.confirm({
            title: '确认',
            content: '确认要删除' + modify_start_date + '这天的事件？',
            confirmButtonClass: 'btn-danger',
            confirmButton: '删除',
            cancelButtonClass: 'btn-primary',
            cancelButton: '取消',
            animation: 'rotate',
            // 6秒后自动点击cancel按钮，以 | 作为分隔，时间单位为毫秒
            autoClose: 'cancel|6000',
            icon: 'fa fa-warning',
            // 禁止在框外触发单击事件
            backgroundDismiss: false,
            confirm: function () {
                $.post("/delete_calendar_event/", {
                        id: modify_id,
                        csrfmiddlewaretoken: get_cookie('csrftoken')
                    },
                    function (data) {
                        data = JSON.parse(data);
                        result = data['result'];
                        // 关闭modal
                        if (result == false) {
                            toastr.error('删除失败，请联系网站管理员！' + data['message'], '出错啦！');
                        }
                        if (result == true) {
                            $('#closebtn2').click();
                            toastr.success('成功删除' + modify_start_date + '的事件', '提示');
                            //重新获取所有事件数据
                            $('#calendar').fullCalendar('refetchEvents');
                        }
                    }
                );
            },
            cancel: function () {
                // nothing to do
            }
        });
    });


    // 修改事件，提交按钮点击时
    $('#modifybtn').click(function () {
        // 获取输入的事件、颜色、日期等信息
        var modify_event_title = $('#modify_event_title').val();
        var color = modify_colorpicker.val();
        var start = startpicker.val();
        var end = endpicker.val();

        // 如果之前有错误，先去掉之前的错误提示
        $('form div').removeClass('has-error');

        // 如果没有输入标题
        if (modify_event_title == '') {
            $('#modify_event_title').parent().addClass('has-error');
            toastr.error('请填写事件标题', '提示');
            return false;
        }
        if (start == '') {
            $('#start').parent().addClass('has-error');
            toastr.error('请填写事件开始时间', '提示');
            return false;
        }
        if (end == '') {
            $('#end').parent().addClass('has-error');
            toastr.error('请填写事件结束时间', '提示');
            return false;
        }

        // TODO：还应该把当前用户传一下，好多地方都应该有类似的需求。等统一登陆做好了需要专门处理一下
        $.post("/update_calendar_event/", {
                id: modify_id,
                event: modify_event_title,
                start: start,
                end: end,
                color: color,
                csrfmiddlewaretoken: get_cookie('csrftoken')
            },
            function (data) {
                data = JSON.parse(data);
                result = data['result'];
                // 关闭modal
                if (result == false) {
                    toastr.error('修改失败，请联系网站管理员！' + data['message'], '出错啦！');
                }
                if (result == true) {
                    $('#closebtn2').click();
                    toastr.success('成功修改' + modify_start_date + '的事件', '提示');
                    //重新获取所有事件数据
                    $('#calendar').fullCalendar('refetchEvents');
                }
            }
        );
    });


    // 发布新事件，点击提交按钮时进行验证
    $('#commitbtn').click(function () {
        // 获取输入的事件
        var event = $('#event').val();

        // 如果之前有错误，先去掉之前的错误提示
        $('form div').removeClass('has-error');

        // 如果没有输入标题
        if (event == '') {
            $('#event').parent().addClass('has-error');
            toastr.error('请填写事件标题', '提示');
            return false;
        }

        // TODO：还应该把当前用户传一下，好多地方都应该有类似的需求。等统一登陆做好了需要专门处理一下
        $.post("/commit_calendar_event/", {
                event: event,
                start: click_start_date,
                end: click_end_date,
                color: colorpicker.val(),
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
                    toastr.success('成功添加' + click_start_date + '当天的事件', '提示');
                    //重新获取所有事件数据
                    $('#calendar').fullCalendar('refetchEvents');
                }
            }
        );

    });


    // Color Picker
    $.minicolors = {
        defaults: {
            animationSpeed: 50,
            animationEasing: 'swing',
            changeDelay: 0,
            control: 'hue',
            defaultValue: '#4cb6cb',
            hideSpeed: 100,
            inline: false,
            letterCase: 'lowercase',
            opacity: false,
            position: 'bottom left',
            show: null,
            showSpeed: 100,
            theme: 'bootstrap'
        }
    };
    var colorpicker = $('#color').minicolors();
    var modify_colorpicker = $('#modify_color').minicolors();

    // Datetimepicker
    var startpicker = $('#start_time').datetimepicker({
        format: 'yyyy-mm-dd',
        minView: "month",
        autoclose: true,
        todayHighlight: true,
        language: 'zh-CN'
    });
    var endpicker = $('#end_time').datetimepicker({
        format: 'yyyy-mm-dd',
        minView: "month",
        autoclose: true,
        todayHighlight: true,
        language: 'zh-CN'
    });


});