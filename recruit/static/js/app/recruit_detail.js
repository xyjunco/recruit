/**
 * Created by junco on 15/12/9.
 */

$(function () {

    // 从url中解析出当前招聘页面的ID
    var recruit_id = window.location.pathname.split('/')[2];

    $('#comments-container').comments({
        profilePictureURL: 'https://app.viima.com/static/media/user_profiles/user-icon.png',
        roundProfilePictures: true,
        textareaPlaceholderText: '增加一条评论内容...',
        popularText: '热门评论',
        newestText: '最新评论',
        oldestText: '旧时评论',
        sendText: '评论',
        replyText: '回复',
        editText: '编辑',
        saveText: '保存',
        deleteText: '删除',
        editedText: '修改于 ',
        youText: '我',
        viewAllRepliesText: '查看全部 __replyCount__ 条评论',
        hideRepliesText: '隐藏',
        noCommentsText: '暂无评论',
        highlightColor: '#4cb6cb',

        // 获取所有评论内容
        getComments: function (success, error) {
            $.ajax({
                type: 'get',
                url: '/api/recruit/comments/' + recruit_id,
                success: function (commentsArray) {
                    success(commentsArray)
                },
                error: error
            });
        },

        // 新增一条评论内容
        postComment: function (commentJSON, success, error) {
            $.ajax({
                type: 'post',
                url: '/api/recruit/post_comment/' + recruit_id + '/',
                data: {
                    data: commentJSON,
                    objid: recruit_id,
                    csrfmiddlewaretoken: get_cookie('csrftoken')
                },
                success: function () {
                    success(commentJSON)
                },
                error: error
            });
            return commentJSON;
        },

        // update一条已经存在的评论内容
        putComment: function (commentJSON, success, error) {
            $.ajax({
                type: 'post',
                url: '/api/recruit/update_comment/' + recruit_id + '/',
                data: {
                    data: commentJSON,
                    csrfmiddlewaretoken: get_cookie('csrftoken')
                },
                success: function (data) {
                    success(commentJSON)
                },
                error: error
            });
        },

        // 删除一条评论
        deleteComment: function (commentJSON, success, error) {
            $.ajax({
                type: 'post',
                url: '/api/recruit/delete_comment/' + recruit_id + '/',
                data: {
                    data: commentJSON,
                    csrfmiddlewaretoken: get_cookie('csrftoken')
                },
                success: function (data) {
                    success(commentJSON)
                },
                error: error
            });
        },

        // 点赞 或 取消赞
        upvoteComment: function (commentJSON, success, error) {
            $.ajax({
                type: 'post',
                url: '/api/recruit/upvote/' + recruit_id + '/',
                data: {
                    data: commentJSON,
                    csrfmiddlewaretoken: get_cookie('csrftoken')
                },
                success: function () {
                    success(commentJSON)
                },
                error: error
            });

        }
    });
});