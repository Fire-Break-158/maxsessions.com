function BindEvents() {
    $(".select").chosen();

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

    $('#ctl00_primaryContent_tbPassword').on('click', function () {
        $(this).select();
        $(this).attr('type', 'password');
    });
    $('#ctl00_primaryContent_tbConfirm').on('click', function () {
        $(this).select();
        $(this).attr('type', 'password');
    });
}
