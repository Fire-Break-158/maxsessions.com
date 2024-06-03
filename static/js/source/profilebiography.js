function BindEvents() {
    $('#ctl00_primaryContent_tbBio').hide();
    CKEDITOR.replace('ctl00_primaryContent_tbBio', {
        height: '365px'
    });
    $('#ctl00_primaryContent_tbBio').show();
}

function getEditorData() {
    CKEDITOR.instances["ctl00_primaryContent_tbBio"].updateElement();
}
