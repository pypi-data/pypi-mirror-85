import { __assign, __awaiter, __extends, __generator, __read } from "tslib";
import React from 'react';
import PropTypes from 'prop-types';
import * as queryString from 'query-string';
import * as Sentry from '@sentry/react';
import debounce from 'lodash/debounce';
import { addSuccessMessage } from 'app/actionCreators/indicator';
import AsyncComponent from 'app/components/asyncComponent';
import FieldFromConfig from 'app/views/settings/components/forms/fieldFromConfig';
import Form from 'app/views/settings/components/forms/form';
import SentryTypes from 'app/sentryTypes';
import { t } from 'app/locale';
var MESSAGES_BY_ACTION = {
    link: t('Successfully linked issue.'),
    create: t('Successfully created issue.'),
};
var SUBMIT_LABEL_BY_ACTION = {
    link: t('Link Issue'),
    create: t('Create Issue'),
};
var ExternalIssueForm = /** @class */ (function (_super) {
    __extends(ExternalIssueForm, _super);
    function ExternalIssueForm() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.shouldRenderBadRequests = true;
        _this.startTransaction = function (type) {
            var _a = _this.props, action = _a.action, group = _a.group, integration = _a.integration;
            var transaction = Sentry.startTransaction({ name: "externalIssueForm." + type });
            transaction.setTag('issueAction', action);
            transaction.setTag('groupID', group.id);
            transaction.setTag('projectID', group.project.id);
            transaction.setTag('integrationSlug', integration.provider.slug);
            transaction.setTag('integrationType', 'firstParty');
            return transaction;
        };
        _this.handlePreSubmit = function () {
            _this.submitTransaction = _this.startTransaction('submit');
        };
        _this.onSubmitSuccess = function (data) {
            var _a;
            _this.props.onSubmitSuccess(data, function () {
                return addSuccessMessage(MESSAGES_BY_ACTION[_this.props.action]);
            });
            (_a = _this.submitTransaction) === null || _a === void 0 ? void 0 : _a.finish();
        };
        _this.handleSubmitError = function () {
            var _a;
            (_a = _this.submitTransaction) === null || _a === void 0 ? void 0 : _a.finish();
        };
        _this.onRequestError = function () {
            var _a;
            (_a = _this.loadTransasaction) === null || _a === void 0 ? void 0 : _a.finish();
        };
        _this.refetchConfig = function () {
            var dynamicFieldValues = _this.state.dynamicFieldValues;
            var _a = _this.props, action = _a.action, group = _a.group, integration = _a.integration;
            var endpoint = "/groups/" + group.id + "/integrations/" + integration.id + "/";
            var query = __assign({ action: action }, dynamicFieldValues);
            _this.api.request(endpoint, {
                method: 'GET',
                query: query,
                success: function (data, _, jqXHR) {
                    _this.handleRequestSuccess({ stateKey: 'integrationDetails', data: data, jqXHR: jqXHR }, true);
                },
                error: function (error) {
                    _this.handleError(error, ['integrationDetails', endpoint, null, null]);
                },
            });
        };
        _this.onFieldChange = function (label, value) {
            var dynamicFields = _this.getDynamicFields();
            if (label in dynamicFields) {
                var dynamicFieldValues = _this.state.dynamicFieldValues || {};
                dynamicFieldValues[label] = value;
                _this.setState({
                    dynamicFieldValues: dynamicFieldValues,
                    reloading: true,
                    error: false,
                    remainingRequests: 1,
                }, _this.refetchConfig);
            }
        };
        _this.getOptions = function (field, input) {
            return new Promise(function (resolve, reject) {
                if (!input) {
                    var choices = field.choices || [];
                    var options = choices.map(function (_a) {
                        var _b = __read(_a, 2), value = _b[0], label = _b[1];
                        return ({ value: value, label: label });
                    });
                    return resolve({ options: options });
                }
                return _this.debouncedOptionLoad(field, input, function (err, result) {
                    if (err) {
                        reject(err);
                    }
                    else {
                        resolve(result);
                    }
                });
            });
        };
        _this.debouncedOptionLoad = debounce(function (field, input, cb) { return __awaiter(_this, void 0, void 0, function () {
            var query, url, separator, response, _a, _b, _c, err_1;
            var _d;
            return __generator(this, function (_e) {
                switch (_e.label) {
                    case 0:
                        query = queryString.stringify(__assign(__assign({}, this.state.dynamicFieldValues), { field: field.name, query: input }));
                        url = field.url || '';
                        separator = url.includes('?') ? '&' : '?';
                        _e.label = 1;
                    case 1:
                        _e.trys.push([1, 6, , 7]);
                        return [4 /*yield*/, fetch(url + separator + query)];
                    case 2:
                        response = _e.sent();
                        _a = cb;
                        _b = [null];
                        _d = {};
                        if (!response.ok) return [3 /*break*/, 4];
                        return [4 /*yield*/, response.json()];
                    case 3:
                        _c = _e.sent();
                        return [3 /*break*/, 5];
                    case 4:
                        _c = [];
                        _e.label = 5;
                    case 5:
                        _a.apply(void 0, _b.concat([(_d.options = _c, _d)]));
                        return [3 /*break*/, 7];
                    case 6:
                        err_1 = _e.sent();
                        cb(err_1);
                        return [3 /*break*/, 7];
                    case 7: return [2 /*return*/];
                }
            });
        }); }, 200, { trailing: true });
        _this.getFieldProps = function (field) {
            return field.url
                ? {
                    loadOptions: function (input) { return _this.getOptions(field, input); },
                    async: true,
                    cache: false,
                    onSelectResetsInput: false,
                    onCloseResetsInput: false,
                    onBlurResetsInput: false,
                    autoload: true,
                }
                : {};
        };
        return _this;
    }
    ExternalIssueForm.prototype.componentDidMount = function () {
        this.loadTransasaction = this.startTransaction('load');
    };
    ExternalIssueForm.prototype.getEndpoints = function () {
        var _a = this.props, group = _a.group, integration = _a.integration, action = _a.action;
        return [
            [
                'integrationDetails',
                "/groups/" + group.id + "/integrations/" + integration.id + "/?action=" + action,
            ],
        ];
    };
    ExternalIssueForm.prototype.onRequestSuccess = function (_a) {
        var stateKey = _a.stateKey, data = _a.data;
        if (stateKey === 'integrationDetails' && !this.state.dynamicFieldValues) {
            this.setState({
                dynamicFieldValues: this.getDynamicFields(data),
            });
        }
    };
    ExternalIssueForm.prototype.onLoadAllEndpointsSuccess = function () {
        var _a;
        (_a = this.loadTransasaction) === null || _a === void 0 ? void 0 : _a.finish();
    };
    ExternalIssueForm.prototype.getDynamicFields = function (integrationDetails) {
        integrationDetails = integrationDetails || this.state.integrationDetails;
        var action = this.props.action;
        var config = integrationDetails[action + "IssueConfig"];
        return Object.fromEntries(config
            .filter(function (field) { return field.updatesForm; })
            .map(function (field) { return [field.name, field.default]; }));
    };
    ExternalIssueForm.prototype.renderBody = function () {
        var _this = this;
        var integrationDetails = this.state.integrationDetails;
        var _a = this.props, action = _a.action, group = _a.group, integration = _a.integration;
        var config = integrationDetails[action + "IssueConfig"];
        var initialData = {};
        config.forEach(function (field) {
            // passing an empty array breaks multi select
            // TODO(jess): figure out why this is breaking and fix
            initialData[field.name] = field.multiple ? '' : field.default;
        });
        return (<Form apiEndpoint={"/groups/" + group.id + "/integrations/" + integration.id + "/"} apiMethod={action === 'create' ? 'POST' : 'PUT'} onSubmitSuccess={this.onSubmitSuccess} initialData={initialData} onFieldChange={this.onFieldChange} submitLabel={SUBMIT_LABEL_BY_ACTION[action]} submitDisabled={this.state.reloading} footerClass="modal-footer" onPreSubmit={this.handlePreSubmit} onSubmitError={this.handleSubmitError}>
        {config.map(function (field) { return (<FieldFromConfig key={field.name + "-" + field.default + "-" + field.required} field={field} inline={false} stacked flexibleControlStateSize disabled={_this.state.reloading} {..._this.getFieldProps(field)}/>); })}
      </Form>);
    };
    ExternalIssueForm.propTypes = {
        group: SentryTypes.Group.isRequired,
        integration: PropTypes.object.isRequired,
        action: PropTypes.oneOf(['link', 'create']),
        onSubmitSuccess: PropTypes.func.isRequired,
    };
    return ExternalIssueForm;
}(AsyncComponent));
export default ExternalIssueForm;
//# sourceMappingURL=externalIssueForm.jsx.map