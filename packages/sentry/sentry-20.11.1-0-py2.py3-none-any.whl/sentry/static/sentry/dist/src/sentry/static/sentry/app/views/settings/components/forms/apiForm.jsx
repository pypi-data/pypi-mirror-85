import { __extends, __rest } from "tslib";
import React from 'react';
import { Client } from 'app/api';
import { addLoadingMessage, clearIndicators } from 'app/actionCreators/indicator';
import { t } from 'app/locale';
import Form from 'app/views/settings/components/forms/form';
var ApiForm = /** @class */ (function (_super) {
    __extends(ApiForm, _super);
    function ApiForm() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.api = new Client();
        _this.onSubmit = function (data, onSuccess, onError) {
            _this.props.onSubmit && _this.props.onSubmit(data);
            addLoadingMessage(t('Saving changes\u2026'));
            _this.api.request(_this.props.apiEndpoint, {
                method: _this.props.apiMethod,
                data: data,
                success: function (response) {
                    clearIndicators();
                    onSuccess(response);
                },
                error: function (error) {
                    clearIndicators();
                    onError(error);
                },
            });
        };
        return _this;
    }
    ApiForm.prototype.componentWillUnmount = function () {
        this.api.clear();
    };
    ApiForm.prototype.render = function () {
        var _a = this.props, _onSubmit = _a.onSubmit, _apiMethod = _a.apiMethod, _apiEndpoint = _a.apiEndpoint, otherProps = __rest(_a, ["onSubmit", "apiMethod", "apiEndpoint"]);
        return <Form onSubmit={this.onSubmit} {...otherProps}/>;
    };
    return ApiForm;
}(React.Component));
export default ApiForm;
//# sourceMappingURL=apiForm.jsx.map