function BindEvents() {
    $(".select").chosen();

    $('.delete').on('click', function (e) {
        e.preventDefault();

        var href = $(this).attr('href');

        $.confirm({
            title: 'Are you sure?',
            content: 'Are you sure you want to remove this honoree?',
            icon: 'fa fa-question-circle',
            animation: 'scale',
            closeAnimation: 'scale',
            opacity: 0.5,
            buttons: {
                confirm: function () {
                    window.location.href = href;
                    return true;
                },
                cancel: function () {
                    return true;
                }
            }
        });
    });

    var config = {
        '.chosen-select': {},
        '.chosen-select-deselect': { allow_single_deselect: true },
        '.chosen-select-no-single': { disable_search_threshold: 10 },
        '.chosen-select-no-results': { no_results_text: 'Oops, nothing found!' },
        '.chosen-select-width': { width: "95%" }
    }
    for (var selector in config) {
        $(selector).chosen(config[selector]);
    }
}
