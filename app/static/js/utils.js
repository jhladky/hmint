"use strict";

app.utils.orAlert = function (success, thisArg) {
    var self = this, $ctr = thisArg && thisArg.$messages || app.$messages;

    return function (data) {
        if (data.success) {
            success.call(thisArg || null, data);
        } else {
            $ctr.empty();
            data.errors.forEach(function (error) {
                self.info({msg: error, $ctr: $ctr});
            });
        }
    };
};

app.utils._alert = function (color, alert) {
    var $dismiss,
        $container = alert.$ctr || this.$messages,
        $frame = $("<div>").addClass("alert alert-" + color);

    $frame.html((typeof alert === "string") ? alert : alert.msg);

    if (!alert.noDismiss) {
        $dismiss = $("<button type=\"button\" data-dismiss=\"alert\">")
            .html("&times;")
            .addClass("close");
        $frame.addClass("alert-dismissable").append($dismiss);
    }

    if (alert.empty) {
        $container.empty();
    }

    $container.append($frame);
};

app.utils.success = app.utils._alert.bind(app, "success");
app.utils.info    = app.utils._alert.bind(app, "info");
app.utils.warning = app.utils._alert.bind(app, "warning");
app.utils.danger  = app.utils._alert.bind(app, "danger");
