import { __assign, __awaiter, __extends, __generator, __read } from "tslib";
import React from 'react';
import PropTypes from 'prop-types';
import debounce from 'lodash/debounce';
import { createFilter } from 'react-select';
import { addErrorMessage } from 'app/actionCreators/indicator';
import { addQueryParamsToExistingUrl } from 'app/utils/queryString';
import FieldFromConfig from 'app/views/settings/components/forms/fieldFromConfig';
import Form from 'app/views/settings/components/forms/form';
import SentryTypes from 'app/sentryTypes';
import { t } from 'app/locale';
import ExternalIssueStore from 'app/stores/externalIssueStore';
import getStacktraceBody from 'app/utils/getStacktraceBody';
import withApi from 'app/utils/withApi';
import FormModel from 'app/views/settings/components/forms/model';
import { replaceAtArrayIndex } from 'app/utils/replaceAtArrayIndex';
//0 is a valid choice but empty string, undefined, and null are not
var hasValue = function (value) { return !!value || value === 0; };
var SentryAppExternalIssueForm = /** @class */ (function (_super) {
    __extends(SentryAppExternalIssueForm, _super);
    function SentryAppExternalIssueForm() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = { optionsByField: new Map() };
        _this.model = new FormModel();
        _this.onSubmitSuccess = function (issue) {
            ExternalIssueStore.add(issue);
            _this.props.onSubmitSuccess(issue);
        };
        _this.onSubmitError = function () {
            var _a = _this.props, action = _a.action, appName = _a.appName;
            addErrorMessage(t('Unable to %s %s issue.', action, appName));
        };
        _this.getOptions = function (field, input) {
            return new Promise(function (resolve) {
                _this.debouncedOptionLoad(field, input, resolve);
            });
        };
        _this.debouncedOptionLoad = debounce(
        // debounce is used to prevent making a request for every input change and
        // instead makes the requests every 200ms
        function (field, input, resolve) { return __awaiter(_this, void 0, void 0, function () {
            var choices, options, optionsByField;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, this.makeExternalRequest(field, input)];
                    case 1:
                        choices = _a.sent();
                        options = choices.map(function (_a) {
                            var _b = __read(_a, 2), value = _b[0], label = _b[1];
                            return ({ value: value, label: label });
                        });
                        optionsByField = new Map(this.state.optionsByField);
                        optionsByField.set(field.name, options);
                        this.setState({
                            optionsByField: optionsByField,
                        });
                        return [2 /*return*/, resolve(options)];
                }
            });
        }); }, 200, { trailing: true });
        _this.makeExternalRequest = function (field, input) { return __awaiter(_this, void 0, void 0, function () {
            var install, projectId, query, dependentData, choices;
            var _this = this;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        install = this.props.sentryAppInstallation;
                        projectId = this.props.group.project.id;
                        query = {
                            projectId: projectId,
                            uri: field.uri,
                            query: input,
                        };
                        if (field.depends_on) {
                            dependentData = field.depends_on.reduce(function (accum, dependentField) {
                                accum[dependentField] = _this.model.getValue(dependentField);
                                return accum;
                            }, {});
                            //stringify the data
                            query.dependentData = JSON.stringify(dependentData);
                        }
                        return [4 /*yield*/, this.props.api.requestPromise("/sentry-app-installations/" + install.uuid + "/external-requests/", {
                                query: query,
                            })];
                    case 1:
                        choices = (_a.sent()).choices;
                        return [2 /*return*/, choices || []];
                }
            });
        }); };
        /**
         * This function determines which fields need to be reset and new options fetched
         * based on the dependencies defined with the depends_on attribute.
         * This is done because the autoload flag causes fields to load at different times
         * if you have multiple dependent fields while this solution updates state at once.
         */
        _this.handleFieldChange = function (id) { return __awaiter(_this, void 0, void 0, function () {
            var config, requiredFields, optionalFields, fieldList, impactedFields, choiceArray;
            var _this = this;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        config = this.state;
                        requiredFields = config.required_fields || [];
                        optionalFields = config.optional_fields || [];
                        fieldList = requiredFields.concat(optionalFields);
                        impactedFields = fieldList.filter(function (_a) {
                            var depends_on = _a.depends_on;
                            if (!depends_on) {
                                return false;
                            }
                            // must be dependent on the field we just set
                            return depends_on.includes(id);
                        });
                        return [4 /*yield*/, Promise.all(impactedFields.map(function (field) {
                                //reset all impacted fields first
                                _this.model.setValue(field.name || '', '', { quiet: true });
                                return _this.makeExternalRequest(field, '');
                            }))];
                    case 1:
                        choiceArray = _a.sent();
                        this.setState(function (state) {
                            //pull the field lists from latest state
                            requiredFields = state.required_fields || [];
                            optionalFields = state.optional_fields || [];
                            //iterate through all the impacted fields and get new values
                            impactedFields.forEach(function (impactedField, i) {
                                var choices = choiceArray[i];
                                var requiredIndex = requiredFields.indexOf(impactedField);
                                var optionalIndex = optionalFields.indexOf(impactedField);
                                var updatedField = __assign(__assign({}, impactedField), { choices: choices });
                                //immutably update the lists with the updated field depending where we got it from
                                if (requiredIndex > -1) {
                                    requiredFields = replaceAtArrayIndex(requiredFields, requiredIndex, updatedField);
                                }
                                else if (optionalIndex > -1) {
                                    optionalFields = replaceAtArrayIndex(optionalFields, optionalIndex, updatedField);
                                }
                            });
                            return {
                                required_fields: requiredFields,
                                optional_fields: optionalFields,
                            };
                        });
                        return [2 /*return*/];
                }
            });
        }); };
        _this.renderField = function (field, required) {
            //This function converts the field we get from the backend into
            //the field we need to pass down
            var fieldToPass = __assign(__assign({}, field), { inline: false, stacked: true, flexibleControlStateSize: true, required: required });
            //async only used for select components
            var isAsync = typeof field.async === 'undefined' ? true : !!field.async; //default to true
            if (fieldToPass.type === 'select') {
                // find the options from state to pass down
                var defaultOptions = (field.choices || []).map(function (_a) {
                    var _b = __read(_a, 2), value = _b[0], label = _b[1];
                    return ({
                        value: value,
                        label: label,
                    });
                });
                var options = _this.state.optionsByField.get(field.name) || defaultOptions;
                //filter by what the user is typing
                var filterOption = createFilter({});
                fieldToPass = __assign(__assign({}, fieldToPass), { options: options,
                    defaultOptions: defaultOptions,
                    filterOption: filterOption });
                //default message for async select fields
                if (isAsync) {
                    fieldToPass.noOptionsMessage = function () { return 'Type to search'; };
                }
            }
            else if (['text', 'textarea'].includes(fieldToPass.type || '') && field.default) {
                fieldToPass = __assign(__assign({}, fieldToPass), { defaultValue: _this.getFieldDefault(field) });
            }
            if (field.depends_on) {
                //check if this is dependent on other fields which haven't been set yet
                var shouldDisable = field.depends_on.some(function (dependentField) { return !hasValue(_this.model.getValue(dependentField)); });
                if (shouldDisable) {
                    fieldToPass = __assign(__assign({}, fieldToPass), { disabled: true });
                }
            }
            //if we have a uri, we need to set extra parameters
            var extraProps = field.uri
                ? {
                    loadOptions: function (input) { return _this.getOptions(field, input); },
                    async: isAsync,
                    cache: false,
                    onSelectResetsInput: false,
                    onCloseResetsInput: false,
                    onBlurResetsInput: false,
                    autoload: false,
                }
                : {};
            return (<FieldFromConfig deprecatedSelectControl={false} key={field.name} field={fieldToPass} data-test-id={field.name} {...extraProps}/>);
        };
        return _this;
    }
    SentryAppExternalIssueForm.prototype.componentDidMount = function () {
        this.resetStateFromProps();
    };
    SentryAppExternalIssueForm.prototype.componentDidUpdate = function (prevProps) {
        if (prevProps.action !== this.props.action) {
            this.model.reset();
            this.resetStateFromProps();
        }
    };
    //reset the state when we mount or the action changes
    SentryAppExternalIssueForm.prototype.resetStateFromProps = function () {
        var _a = this.props, config = _a.config, action = _a.action, group = _a.group;
        this.setState({
            required_fields: config.required_fields,
            optional_fields: config.optional_fields,
        });
        //we need to pass these fields in the API so just set them as values so we don't need hidden form fields
        this.model.setInitialData({
            action: action,
            groupId: group.id,
            uri: config.uri,
        });
    };
    SentryAppExternalIssueForm.prototype.getStacktrace = function () {
        var evt = this.props.event;
        var contentArr = getStacktraceBody(evt);
        if (contentArr && contentArr.length > 0) {
            return '\n\n```\n' + contentArr[0] + '\n```';
        }
        else {
            return '';
        }
    };
    SentryAppExternalIssueForm.prototype.getFieldDefault = function (field) {
        var _a = this.props, group = _a.group, appName = _a.appName;
        if (field.type === 'textarea') {
            field.maxRows = 10;
            field.autosize = true;
        }
        switch (field.default) {
            case 'issue.title':
                return group.title;
            case 'issue.description':
                var stacktrace = this.getStacktrace();
                var queryParams = { referrer: appName };
                var url = addQueryParamsToExistingUrl(group.permalink, queryParams);
                var shortId = group.shortId;
                return t('Sentry Issue: [%s](%s)%s', shortId, url, stacktrace);
            default:
                return '';
        }
    };
    SentryAppExternalIssueForm.prototype.render = function () {
        var _this = this;
        var _a = this.props, sentryAppInstallation = _a.sentryAppInstallation, action = _a.action;
        var requiredFields = this.state.required_fields || [];
        var optionalFields = this.state.optional_fields || [];
        if (!sentryAppInstallation) {
            return '';
        }
        return (<Form key={action} apiEndpoint={"/sentry-app-installations/" + sentryAppInstallation.uuid + "/external-issues/"} apiMethod="POST" onSubmitSuccess={this.onSubmitSuccess} onSubmitError={this.onSubmitError} onFieldChange={this.handleFieldChange} model={this.model}>
        {requiredFields.map(function (field) {
            return _this.renderField(field, true);
        })}

        {optionalFields.map(function (field) {
            return _this.renderField(field, false);
        })}
      </Form>);
    };
    SentryAppExternalIssueForm.propTypes = {
        api: PropTypes.object.isRequired,
        group: SentryTypes.Group.isRequired,
        sentryAppInstallation: PropTypes.object,
        appName: PropTypes.string,
        config: PropTypes.object.isRequired,
        action: PropTypes.oneOf(['link', 'create']),
        event: SentryTypes.Event,
        onSubmitSuccess: PropTypes.func,
    };
    return SentryAppExternalIssueForm;
}(React.Component));
export { SentryAppExternalIssueForm };
export default withApi(SentryAppExternalIssueForm);
//# sourceMappingURL=sentryAppExternalIssueForm.jsx.map