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
    var self = this;

    this.url = window.location.protocol + "//" + window.location.host + "/api";
    this.$messages = $("#messages");

    $(document).ajaxError(function () {
        alert("There was an error processing your request. " +
              "Please reload the page and try again. ");
    });
};
