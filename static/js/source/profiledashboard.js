function BindEvents() {
    var now = new Date();
    var hours = now.getHours();

    if (hours >= 0 && hours < 12)
        $('#greeting').text('Good morning');
    else if (hours >= 12 && hours <= 17)
        $('#greeting').text('Good afternoon');
    else
        $('#greeting').text('Good evening');
}
window.fbAsyncInit = function () {
    FB.init({
        appId: '2743452285889047',
        autoLogAppEvents: true,
        xfbml: true,
        version: 'v7.0'
    });
};
function fb_share(url) {
    FB.ui({
        method: 'share',
        href: url
    }, function (response) { }
    );
}