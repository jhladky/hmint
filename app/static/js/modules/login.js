"use strict";

app.modules.login = {};

app.modules.login.setup = function () {
    this.$mod = $("div.panel");
    this.form = ko.mapping.fromJS({
        email: "",
        password: ""
    });

    this.login = (function () {
        var json = JSON.stringify(ko.mapping.toJS(this.form));

        $.post(app.url + "/login/", json, app.utils.orAlert(function (data) {
            location.reload();
        }, this));
    }).bind(this);

    ko.applyBindings(this, this.$mod[0]);
};
