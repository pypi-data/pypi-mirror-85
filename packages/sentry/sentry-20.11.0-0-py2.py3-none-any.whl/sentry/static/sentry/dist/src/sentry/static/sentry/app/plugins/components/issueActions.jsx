import { __assign, __awaiter, __extends, __generator } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import { Form, FormState } from 'app/components/forms';
import GroupActions from 'app/actions/groupActions';
import LoadingError from 'app/components/loadingError';
import LoadingIndicator from 'app/components/loadingIndicator';
import PluginComponentBase from 'app/components/bases/pluginComponentBase';
import { t } from 'app/locale';
var IssueActions = /** @class */ (function (_super) {
    __extends(IssueActions, _super);
    function IssueActions(props, context) {
        var _this = _super.call(this, props, context) || this;
        _this.loadOptionsForDependentField = function (field) { return __awaiter(_this, void 0, void 0, function () {
            var formData, groupId, pluginSlug, url, dependentFormValues, query, result, err_1;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        formData = this.getFormData();
                        groupId = this.getGroup().id;
                        pluginSlug = this.props.plugin.slug;
                        url = "/issues/" + groupId + "/plugins/" + pluginSlug + "/options/";
                        dependentFormValues = Object.fromEntries(field.depends.map(function (fieldKey) { return [fieldKey, formData[fieldKey]]; }));
                        query = __assign({ option_field: field.name }, dependentFormValues);
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        this.setDependentFieldState(field.name, FormState.LOADING);
                        return [4 /*yield*/, this.api.requestPromise(url, { query: query })];
                    case 2:
                        result = _a.sent();
                        this.updateOptionsOfDependentField(field, result[field.name]);
                        this.setDependentFieldState(field.name, FormState.READY);
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _a.sent();
                        this.setDependentFieldState(field.name, FormState.ERROR);
                        this.errorHandler(err_1);
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.updateOptionsOfDependentField = function (field, choices) {
            var formListKey = _this.getFieldListKey();
            var fieldList = _this.state[formListKey];
            if (!fieldList) {
                return;
            }
            //find the location of the field in our list and replace it
            var indexOfField = fieldList.findIndex(function (_a) {
                var name = _a.name;
                return name === field.name;
            });
            field = __assign(__assign({}, field), { choices: choices });
            //make a copy of the array to avoid mutation
            fieldList = fieldList.slice();
            fieldList[indexOfField] = field;
            _this.setState(function (prevState) {
                var _a;
                return (__assign(__assign({}, prevState), (_a = {}, _a[formListKey] = fieldList, _a)));
            });
        };
        _this.resetOptionsOfDependentField = function (field) {
            _this.updateOptionsOfDependentField(field, []);
            var formDataKey = _this.getFormDataKey();
            var formData = __assign({}, _this.state[formDataKey]);
            formData[field.name] = '';
            _this.setState(function (prevState) {
                var _a;
                return (__assign(__assign({}, prevState), (_a = {}, _a[formDataKey] = formData, _a)));
            });
            _this.setDependentFieldState(field.name, FormState.DISABLED);
        };
        _this.createIssue = _this.onSave.bind(_this, _this.createIssue.bind(_this));
        _this.linkIssue = _this.onSave.bind(_this, _this.linkIssue.bind(_this));
        _this.unlinkIssue = _this.onSave.bind(_this, _this.unlinkIssue.bind(_this));
        _this.onSuccess = _this.onSaveSuccess.bind(_this, _this.onSuccess.bind(_this));
        _this.errorHandler = _this.onLoadError.bind(_this, _this.errorHandler.bind(_this));
        _this.state = __assign(__assign({}, _this.state), { loading: ['link', 'create'].includes(_this.props.actionType), state: ['link', 'create'].includes(_this.props.actionType)
                ? FormState.LOADING
                : FormState.READY, createFormData: {}, linkFormData: {}, dependentFieldState: {} });
        return _this;
    }
    IssueActions.prototype.getGroup = function () {
        return this.props.group;
    };
    IssueActions.prototype.getProject = function () {
        return this.props.project;
    };
    IssueActions.prototype.getOrganization = function () {
        return this.props.organization;
    };
    IssueActions.prototype.getFieldListKey = function () {
        switch (this.props.actionType) {
            case 'link':
                return 'linkFieldList';
            case 'unlink':
                return 'unlinkFieldList';
            case 'create':
                return 'createFieldList';
            default:
                throw new Error('Unexpeced action type');
        }
    };
    IssueActions.prototype.getFormDataKey = function (actionType) {
        switch (actionType || this.props.actionType) {
            case 'link':
                return 'linkFormData';
            case 'unlink':
                return 'unlinkFormData';
            case 'create':
                return 'createFormData';
            default:
                throw new Error('Unexpeced action type');
        }
    };
    IssueActions.prototype.getFormData = function () {
        var key = this.getFormDataKey();
        return this.state[key] || {};
    };
    IssueActions.prototype.getFieldList = function () {
        var key = this.getFieldListKey();
        return this.state[key] || [];
    };
    IssueActions.prototype.componentDidMount = function () {
        var plugin = this.props.plugin;
        if (!plugin.issue && this.props.actionType !== 'unlink') {
            this.fetchData();
        }
    };
    IssueActions.prototype.getPluginCreateEndpoint = function () {
        return ('/issues/' + this.getGroup().id + '/plugins/' + this.props.plugin.slug + '/create/');
    };
    IssueActions.prototype.getPluginLinkEndpoint = function () {
        return ('/issues/' + this.getGroup().id + '/plugins/' + this.props.plugin.slug + '/link/');
    };
    IssueActions.prototype.getPluginUnlinkEndpoint = function () {
        return ('/issues/' + this.getGroup().id + '/plugins/' + this.props.plugin.slug + '/unlink/');
    };
    IssueActions.prototype.setDependentFieldState = function (fieldName, state) {
        var _a;
        var dependentFieldState = __assign(__assign({}, this.state.dependentFieldState), (_a = {}, _a[fieldName] = state, _a));
        this.setState({ dependentFieldState: dependentFieldState });
    };
    IssueActions.prototype.getInputProps = function (field) {
        var props = {};
        //special logic for fields that have dependencies
        if (field.depends && field.depends.length > 0) {
            switch (this.state.dependentFieldState[field.name]) {
                case FormState.LOADING:
                    props.isLoading = true;
                    props.readonly = true;
                    break;
                case FormState.DISABLED:
                case FormState.ERROR:
                    props.readonly = true;
                    break;
                default:
                    break;
            }
        }
        return props;
    };
    IssueActions.prototype.setError = function (error, defaultMessage) {
        var errorBody;
        if (error.status === 400 && error.responseJSON) {
            errorBody = error.responseJSON;
        }
        else {
            errorBody = { message: defaultMessage };
        }
        this.setState({ error: errorBody });
    };
    IssueActions.prototype.errorHandler = function (error) {
        var state = {
            loading: false,
        };
        if (error.status === 400 && error.responseJSON) {
            state.error = error.responseJSON;
        }
        else {
            state.error = { message: t('An unknown error occurred.') };
        }
        this.setState(state);
    };
    IssueActions.prototype.onLoadSuccess = function () {
        var _this = this;
        _super.prototype.onLoadSuccess.call(this);
        //dependent fields need to be set to disabled upon loading
        var fieldList = this.getFieldList();
        fieldList.forEach(function (field) {
            if (field.depends && field.depends.length > 0) {
                _this.setDependentFieldState(field.name, FormState.DISABLED);
            }
        });
    };
    IssueActions.prototype.fetchData = function () {
        var _this = this;
        if (this.props.actionType === 'create') {
            this.api.request(this.getPluginCreateEndpoint(), {
                success: function (data) {
                    var createFormData = {};
                    data.forEach(function (field) {
                        createFormData[field.name] = field.default;
                    });
                    _this.setState({
                        createFieldList: data,
                        error: undefined,
                        loading: false,
                        createFormData: createFormData,
                    }, _this.onLoadSuccess);
                },
                error: this.errorHandler,
            });
        }
        else if (this.props.actionType === 'link') {
            this.api.request(this.getPluginLinkEndpoint(), {
                success: function (data) {
                    var linkFormData = {};
                    data.forEach(function (field) {
                        linkFormData[field.name] = field.default;
                    });
                    _this.setState({
                        linkFieldList: data,
                        error: undefined,
                        loading: false,
                        linkFormData: linkFormData,
                    }, _this.onLoadSuccess);
                },
                error: this.errorHandler,
            });
        }
    };
    IssueActions.prototype.onSuccess = function (data) {
        GroupActions.updateSuccess(null, [this.getGroup().id], { stale: true });
        this.props.onSuccess && this.props.onSuccess(data);
    };
    IssueActions.prototype.createIssue = function () {
        var _this = this;
        this.api.request(this.getPluginCreateEndpoint(), {
            data: this.state.createFormData,
            success: this.onSuccess,
            error: this.onSaveError.bind(this, function (error) {
                _this.setError(error, t('There was an error creating the issue.'));
            }),
            complete: this.onSaveComplete,
        });
    };
    IssueActions.prototype.linkIssue = function () {
        var _this = this;
        this.api.request(this.getPluginLinkEndpoint(), {
            data: this.state.linkFormData,
            success: this.onSuccess,
            error: this.onSaveError.bind(this, function (error) {
                _this.setError(error, t('There was an error linking the issue.'));
            }),
            complete: this.onSaveComplete,
        });
    };
    IssueActions.prototype.unlinkIssue = function () {
        var _this = this;
        this.api.request(this.getPluginUnlinkEndpoint(), {
            success: this.onSuccess,
            error: this.onSaveError.bind(this, function (error) {
                _this.setError(error, t('There was an error unlinking the issue.'));
            }),
            complete: this.onSaveComplete,
        });
    };
    IssueActions.prototype.changeField = function (action, name, value) {
        var _this = this;
        var _a;
        var formDataKey = this.getFormDataKey(action);
        //copy so we don't mutate
        var formData = __assign({}, this.state[formDataKey]);
        var fieldList = this.getFieldList();
        formData[name] = value;
        var callback = function () { };
        //only works with one impacted field
        var impactedField = fieldList.find(function (_a) {
            var depends = _a.depends;
            if (!depends || !depends.length) {
                return false;
            }
            // must be dependent on the field we just set
            return depends.includes(name);
        });
        if (impactedField) {
            //if every dependent field is set, then search
            if (!((_a = impactedField.depends) === null || _a === void 0 ? void 0 : _a.some(function (dependentField) { return !formData[dependentField]; }))) {
                callback = function () { return _this.loadOptionsForDependentField(impactedField); };
            }
            else {
                //otherwise reset the options
                callback = function () { return _this.resetOptionsOfDependentField(impactedField); };
            }
        }
        this.setState(function (prevState) {
            var _a;
            return (__assign(__assign({}, prevState), (_a = {}, _a[formDataKey] = formData, _a)));
        }, callback);
    };
    IssueActions.prototype.renderForm = function () {
        var _this = this;
        switch (this.props.actionType) {
            case 'create':
                if (this.state.createFieldList) {
                    return (<Form onSubmit={this.createIssue} submitLabel={t('Create Issue')} footerClass="">
              {this.state.createFieldList.map(function (field) {
                        if (field.has_autocomplete) {
                            field = Object.assign({
                                url: '/api/0/issues/' +
                                    _this.getGroup().id +
                                    '/plugins/' +
                                    _this.props.plugin.slug +
                                    '/autocomplete',
                            }, field);
                        }
                        return (<div key={field.name}>
                    {_this.renderField({
                            config: __assign(__assign({}, field), _this.getInputProps(field)),
                            formData: _this.state.createFormData,
                            onChange: _this.changeField.bind(_this, 'create', field.name),
                        })}
                  </div>);
                    })}
            </Form>);
                }
                break;
            case 'link':
                if (this.state.linkFieldList) {
                    return (<Form onSubmit={this.linkIssue} submitLabel={t('Link Issue')} footerClass="">
              {this.state.linkFieldList.map(function (field) {
                        if (field.has_autocomplete) {
                            field = Object.assign({
                                url: '/api/0/issues/' +
                                    _this.getGroup().id +
                                    '/plugins/' +
                                    _this.props.plugin.slug +
                                    '/autocomplete',
                            }, field);
                        }
                        return (<div key={field.name}>
                    {_this.renderField({
                            config: __assign(__assign({}, field), _this.getInputProps(field)),
                            formData: _this.state.linkFormData,
                            onChange: _this.changeField.bind(_this, 'link', field.name),
                        })}
                  </div>);
                    })}
            </Form>);
                }
                break;
            case 'unlink':
                return (<div>
            <p>{t('Are you sure you want to unlink this issue?')}</p>
            <button onClick={this.unlinkIssue} className="btn btn-danger">
              {t('Unlink Issue')}
            </button>
          </div>);
            default:
                return null;
        }
        return null;
    };
    IssueActions.prototype.getPluginConfigureUrl = function () {
        var org = this.getOrganization();
        var project = this.getProject();
        var plugin = this.props.plugin;
        return '/' + org.slug + '/' + project.slug + '/settings/plugins/' + plugin.slug;
    };
    IssueActions.prototype.renderError = function () {
        var _a;
        var error = this.state.error;
        if (!error) {
            return null;
        }
        if (error.error_type === 'auth') {
            var authUrl = error.auth_url;
            if ((authUrl === null || authUrl === void 0 ? void 0 : authUrl.indexOf('?')) === -1) {
                authUrl += '?next=' + encodeURIComponent(document.location.pathname);
            }
            else {
                authUrl += '&next=' + encodeURIComponent(document.location.pathname);
            }
            return (<div>
          <div className="alert alert-warning m-b-1">
            {'You need to associate an identity with ' +
                this.props.plugin.name +
                ' before you can create issues with this service.'}
          </div>
          <a className="btn btn-primary" href={authUrl}>
            Associate Identity
          </a>
        </div>);
        }
        else if (error.error_type === 'config') {
            return (<div className="alert alert-block">
          {!error.has_auth_configured ? (<div>
              <p>
                {'Your server administrator will need to configure authentication with '}
                <strong>{this.props.plugin.name}</strong>
                {' before you can use this integration.'}
              </p>
              <p>The following settings must be configured:</p>
              <ul>
                {(_a = error.required_auth_settings) === null || _a === void 0 ? void 0 : _a.map(function (setting, i) { return (<li key={i}>
                    <code>{setting}</code>
                  </li>); })}
              </ul>
            </div>) : (<p>
              You still need to{' '}
              <a href={this.getPluginConfigureUrl()}>configure this plugin</a> before you
              can use it.
            </p>)}
        </div>);
        }
        else if (error.error_type === 'validation') {
            var errors = [];
            for (var name_1 in error.errors) {
                errors.push(<p key={name_1}>{error.errors[name_1]}</p>);
            }
            return <div className="alert alert-error alert-block">{errors}</div>;
        }
        else if (error.message) {
            return (<div className="alert alert-error alert-block">
          <p>{error.message}</p>
        </div>);
        }
        return <LoadingError />;
    };
    IssueActions.prototype.render = function () {
        if (this.state.state === FormState.LOADING) {
            return <LoadingIndicator />;
        }
        return (<div>
        {this.renderError()}
        {this.renderForm()}
      </div>);
    };
    IssueActions.propTypes = {
        plugin: PropTypes.object.isRequired,
        actionType: PropTypes.oneOf(['unlink', 'link', 'create']).isRequired,
        onSuccess: PropTypes.func,
    };
    return IssueActions;
}(PluginComponentBase));
export default IssueActions;
//# sourceMappingURL=issueActions.jsx.map