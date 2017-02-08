(function () {

    'use strict';

    var configOptions = {
        endpoint : '/api/word'
    };

    jQuery(document).ready(run);

    function run() {
        jQuery('form').on('submit', submitForm);
    }

    function submitForm(e) {
        e.preventDefault();
        var data = jQuery(e.currentTarget).serialize();

        jQuery('button').prop('disabled', true);
        jQuery.ajax({
            url: configOptions.endpoint,
            method: 'POST',
            data: data,
            success: readQueueResults,
            error: showError
        });

        function readQueueResults(response) {
            console.log(response);
            var data = response;
            console.log(data);
            if (data.job) {
                console.log('we here');
                var interval = setInterval(function () {
                    jQuery.ajax({
                        url: configOptions.endpoint,
                        method: 'GET',
                        data: 'job_id=' + data.job,
                        success: showResults
                    });
                }, 500);
            }
            if (data.pronounceability) {
                showResults(response);
            }
            function showResults(response) {
                if (response) {
                    clearInterval(interval);

                    jQuery('button').prop('disabled', false);

                    var data = response;
                    renderMessage('alert-success', 'Your word is <b>' + data.pronounceability + '%</b> pronounceable');
                }
            }
        }

        function showError(error) {
            console.warn(error.status, error.statusText);

            jQuery('button').prop('disabled', false);

            renderMessage('alert-danger', '<b>' + error.status + '</b> - ' + error.statusText);
        }
    }

    function renderMessage(classes, message) {
        jQuery('.alert').remove();

        var div = jQuery('<div>', {class: 'alert clear text-center row ' + classes});
        div.append(message);
        div.appendTo('.col-md-6');
    }

}());