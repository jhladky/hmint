"use strict";

// Extend jQuery with PUT and DELETE functions
$.extend({
    put: function (url, data, callback, type) {
        return utils._ajaxRequest(url, data, callback, type, "PUT");
    },
    delete_: function (url, data, callback, type) {
        return utils._ajaxRequest(url, data, callback, type, "DELETE");
    }
});

var app = {
    modules: {},
    utils: {}
};

app.setup = function () {
    var self = this, message;

    this.url = window.location.protocol + "//" + window.location.host + "/api";
    this.$messages = $("#messages");

    $(document).ajaxError(function () {
        alert("There was an error processing your request. " +
              "Please reload the page and try again. ");
    });

    this.setupSettings();

    message = app.utils.getQueryParam("message");
    if (message) {
        app.utils.info(decodeURIComponent(message).replace("+", " "));
    }
};

//Find a better way to do this later.
app.setupSettings = function () {
    var self = this;

    //We should be using knockout even for this stuff!!
    this.$settings = $("#settings");
    this.$settingsLnk = $("#nav-a a:nth-child(2)");

    this.$settingsLnk.click(function () {
        self.$settings.modal({
            "backdrop": "static",
            "show": true
        });
    });

};
