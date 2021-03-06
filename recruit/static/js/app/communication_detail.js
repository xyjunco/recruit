/**
 * Created by junco on 15/12/9.
 */

$(function () {
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
        getComments: function (success, error) {
            setTimeout(function () {
                success(commentsArray);
            }, 500);
        },
        putComment: function (data, success, error) {
            setTimeout(function () {
                success(data);
            }, 200)
        },
        deleteComment: function (data, success, error) {
            setTimeout(function () {
                success();
            }, 200)
        },
        upvoteComment: function (data, success, error) {
            setTimeout(function () {
                success(data);
            }, 200)
        }
    });
});