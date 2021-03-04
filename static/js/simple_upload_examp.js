<script>
    //form Submit action
    $("form").submit(function(event){
        //disable the default form submission
        event.preventDefault();
        //grab all form data
        var formData = new FormData($(this)[0]);
        function setProgress(e) {
            if (e.lengthComputable) {
                var complete = e.loaded / e.total;
                $("#pBar").text(Math.floor(complete*100)+"%");
            }
        }
        $.ajax({
            xhr: function() {
                var xhr = new window.XMLHttpRequest();
                xhr.upload.addEventListener("progress", setProgress, false);
                xhr.addEventListener("progress", setProgress, false);
                return xhr;
            },
            url: 'http://127.0.0.1:8080/simple_upload',
            type: 'POST',
            data: formData,
            async: true,
            cache: false,
            contentType: false,
            processData: false,
            enctype: 'multipart/form-data',
            success: function (returndata) {
                alert(returndata);
            }
        });
        return false;
    });
</script>