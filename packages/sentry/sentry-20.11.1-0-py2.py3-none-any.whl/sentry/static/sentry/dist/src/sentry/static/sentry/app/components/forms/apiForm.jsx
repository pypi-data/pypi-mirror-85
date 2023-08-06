import { __assign, __extends } from "tslib";
import PropTypes from 'prop-types';
import { Client } from 'app/api';
import { addLoadingMessage, clearIndicators, addErrorMessage, } from 'app/actionCreators/indicator';
import { t } from 'app/locale';
import Form from 'app/components/forms/form';
import FormState from 'app/components/forms/state';
var ApiForm = /** @class */ (function (_super) {
    __extends(ApiForm, _super);
    function ApiForm() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.api = new Client();
        _this.onSubmit = function (e) {
            e.preventDefault();
            if (_this.state.state === FormState.SAVING) {
                return;
            }
            var data = _this.state.data;
            _this.props.onSubmit && _this.props.onSubmit(data);
            _this.setState({
                state: FormState.SAVING,
            }, function () {
                addLoadingMessage(_this.props.submitLoadingMessage);
                _this.api.request(_this.props.apiEndpoint, {
                    method: _this.props.apiMethod,
                    data: data,
                    success: function (result) {
                        clearIndicators();
                        _this.onSubmitSuccess(result);
                    },
                    error: function (error) {
                        addErrorMessage(_this.props.submitErrorMessage);
                        _this.onSubmitError(error);
                    },
                });
            });
        };
        return _this;
    }
    ApiForm.prototype.componentWillUnmount = function () {
        this.api.clear();
    };
    ApiForm.propTypes = __assign(__assign({}, Form.propTypes), { onSubmit: PropTypes.func, apiMethod: PropTypes.string.isRequired, apiEndpoint: PropTypes.string.isRequired, submitLoadingMessage: PropTypes.string, submitErrorMessage: PropTypes.string });
    ApiForm.defaultProps = __assign(__assign({}, Form.defaultProps), { submitErrorMessage: t('There was an error saving your changes.'), submitLoadingMessage: t('Saving changes\u2026') });
    return ApiForm;
}(Form));
export default ApiForm;
//# sourceMappingURL=apiForm.jsx.map