/**
 * Created by junco on 15/12/9.
 */

$(function () {
    $('#comments-container').comments({
        profilePictureURL: 'https://app.viima.com/static/media/user_profiles/user-icon.png',
        roundProfilePictures: true,
        textareaRows: 1,
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