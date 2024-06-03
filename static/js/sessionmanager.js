$(function () { // Wrap it all in jQuery documentReady because we use jQuery UI Dialog
    // HtmlHelpers Module
    // Call by using HtmlHelpers.getQueryStringValue("myname");
    var HtmlHelpers = function() {
        return {
            getQueryStringValue: function(name) {
                var match = RegExp('[?&]' + name + '=([^&]*)').exec(window.location.search);
                return match && decodeURIComponent(match[1].replace(/\+/g, ' '));
            }
        };
    }();

    // StringHelpers Module
    // Call by using StringHelpers.padLeft("1", "000");
    var StringHelpers = function() {
        return {
            // Pad string using padMask.  string '1' with padMask '000' will produce '001'.
            padLeft: function(string, padMask) {
                string = '' + string;
                return (padMask.substr(0, (padMask.length - string.length)) + string);
            }
        };
    }();

    // SessionManager Module
    var SessionManager = function() {
        // NOTE:  I use @Session.Timeout here, which is Razor syntax, and I am pulling that value
        //        right from the ASP.NET MVC Session variable.  Dangerous!  Reckless!  Awesome-sauce!
        //        You can just hard-code your timeout here if you feel like it.  But I might cry.
        var sessionTimeoutSeconds = HtmlHelpers.getQueryStringValue('smt') || (txrylyx * 60),
            countdownSeconds = HtmlHelpers.getQueryStringValue('smc') || 300,
            secondsBeforePrompt = sessionTimeoutSeconds - countdownSeconds,
            $dlg,
            displayCountdownIntervalId,
            promptToExtendSessionTimeoutId,
            originalTitle = document.title,
            count = countdownSeconds,
            extendSessionUrl = '/Handlers/Session.ashx?t=Extend',
            expireSessionUrl = '/Handlers/Session.ashx?t=Expire';

        var endSession = function() {
            $dlg.dialog('close');
            window.location.href = '/Logout.aspx?type=' + usertype;
        };

        var displayCountdown = function() {
            var countdown = function() {
                var cd = new Date(count * 1000),
                    minutes = cd.getUTCMinutes(),
                    seconds = cd.getUTCSeconds(),
                    minutesDisplay = minutes === 1 ? '1 minute ' : minutes === 0 ? '' : minutes + ' minutes ',
                    secondsDisplay = seconds === 1 ? '1 second' : seconds + ' seconds',
                    cdDisplay = minutesDisplay + secondsDisplay;

                document.title = 'Expire in ' +
                    StringHelpers.padLeft(minutes, '00') + ':' +
                        StringHelpers.padLeft(seconds, '00');
                $('#sm-countdown').html(cdDisplay);
                if (count === 0) {
                    document.title = 'Session Expired';
                    endSession();
                }
                count--;
            };
            countdown();
            displayCountdownIntervalId = window.setInterval(countdown, 1000);
        };

        var promptToExtendSession = function() {
            $dlg = $('#sm-countdown-dialog')
                .dialog({
                    title: 'Session Timeout Warning',
                    height: 250,
                    width: 450,
                    bgiframe: true,
                    modal: true,
                    buttons: {
                        'Continue': function() {
                            $(this).dialog('close');
                            refreshSession();
                            document.title = originalTitle;
                        },
                        'Log Out': function() {
                            endSession(false);
                        }
                    }
                });
            count = countdownSeconds;
            displayCountdown();
        };

        var refreshSession = function() {
            window.clearInterval(displayCountdownIntervalId);
            var img = new Image(1, 1);
            img.src = extendSessionUrl;
            window.clearTimeout(promptToExtendSessionTimeoutId);
            startSessionManager();
        };

        var startSessionManager = function() {
            promptToExtendSessionTimeoutId =
                window.setTimeout(promptToExtendSession, secondsBeforePrompt * 1000);
        };

        // Public Functions
        return {
            start: function() {
                startSessionManager();
            },

            extend: function() {
                refreshSession();
            }
        };
    }();

    SessionManager.start();

    // Whenever an input changes, extend the session,
    // since we know the user is interacting with the site.
    $(':input').change(function() {
        SessionManager.extend();
    });
});
