function BindEvents() {
    $(".select").chosen();

    $(".servicedate").datepicker({
        changeMonth: true,
        changeYear: true,
        yearRange: "-100:+0"
    });
}

function bindSearchTable() {
    $("#results").dataTable({});
}
