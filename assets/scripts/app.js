(function () {

    'use strict';

    var configOptions = {
        endpoint : '/pronounceable_percent'
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
            var data = jQuery.parseJSON(response);

            var interval = setInterval(function () {
                jQuery.ajax({
                    url: configOptions.endpoint,
                    method: 'GET',
                    data: 'id=' + data.id,
                    success: showResults
                });
            }, 500);

            function showResults(response) {
                if (response) {
                    clearInterval(interval);

                    jQuery('button').prop('disabled', false);

                    var data = jQuery.parseJSON(response);
                    renderMessage('alert-success', 'Your word is <b>' + data.percent + '%</b> pronounceable');
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