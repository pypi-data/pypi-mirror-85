import { __assign, __extends, __makeTemplateObject } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import isEqual from 'lodash/isEqual';
import styled from '@emotion/styled';
import { Form, FormState } from 'app/components/forms';
import { parseRepo } from 'app/utils';
import { t, tct } from 'app/locale';
import LoadingIndicator from 'app/components/loadingIndicator';
import PluginComponentBase from 'app/components/bases/pluginComponentBase';
import { trackIntegrationEvent } from 'app/utils/integrationUtil';
var PluginSettings = /** @class */ (function (_super) {
    __extends(PluginSettings, _super);
    function PluginSettings(props, context) {
        var _this = _super.call(this, props, context) || this;
        _this.trackPluginEvent = function (options) {
            trackIntegrationEvent(__assign({ integration: _this.props.plugin.id, integration_type: 'plugin', view: 'plugin_details', project_id: _this.props.project.id, already_installed: _this.state.wasConfiguredOnPageLoad }, options), _this.props.organization);
        };
        Object.assign(_this.state, {
            fieldList: null,
            initialData: null,
            formData: null,
            errors: {},
            rawData: {},
            // override default FormState.READY if api requests are
            // necessary to even load the form
            state: FormState.LOADING,
            wasConfiguredOnPageLoad: false,
        });
        return _this;
    }
    PluginSettings.prototype.componentDidMount = function () {
        this.fetchData();
    };
    PluginSettings.prototype.getPluginEndpoint = function () {
        var org = this.props.organization;
        var project = this.props.project;
        return "/projects/" + org.slug + "/" + project.slug + "/plugins/" + this.props.plugin.id + "/";
    };
    PluginSettings.prototype.changeField = function (name, value) {
        var formData = this.state.formData;
        formData[name] = value;
        // upon changing a field, remove errors
        var errors = this.state.errors;
        delete errors[name];
        this.setState({ formData: formData, errors: errors });
    };
    PluginSettings.prototype.onSubmit = function () {
        var _this = this;
        if (!this.state.wasConfiguredOnPageLoad) {
            //Users cannot install plugins like other integrations but we need the events for the funnel
            //we will treat a user saving a plugin that wasn't already configured as an installation event
            this.trackPluginEvent({
                eventKey: 'integrations.installation_start',
                eventName: 'Integrations: Installation Start',
            });
        }
        var repo = this.state.formData.repo;
        repo = repo && parseRepo(repo);
        var parsedFormData = __assign(__assign({}, this.state.formData), { repo: repo });
        this.api.request(this.getPluginEndpoint(), {
            data: parsedFormData,
            method: 'PUT',
            success: this.onSaveSuccess.bind(this, function (data) {
                var formData = {};
                var initialData = {};
                data.config.forEach(function (field) {
                    formData[field.name] = field.value || field.defaultValue;
                    initialData[field.name] = field.value;
                });
                _this.setState({
                    fieldList: data.config,
                    formData: formData,
                    initialData: initialData,
                    errors: {},
                });
                _this.trackPluginEvent({
                    eventKey: 'integrations.config_saved',
                    eventName: 'Integrations: Config Saved',
                });
                if (!_this.state.wasConfiguredOnPageLoad) {
                    _this.trackPluginEvent({
                        eventKey: 'integrations.installation_complete',
                        eventName: 'Integrations: Installation Complete',
                    });
                }
            }),
            error: this.onSaveError.bind(this, function (error) {
                _this.setState({
                    errors: (error.responseJSON || {}).errors || {},
                });
            }),
            complete: this.onSaveComplete,
        });
    };
    PluginSettings.prototype.fetchData = function () {
        var _this = this;
        this.api.request(this.getPluginEndpoint(), {
            success: function (data) {
                if (!data.config) {
                    _this.setState({
                        rawData: data,
                    }, _this.onLoadSuccess);
                    return;
                }
                var wasConfiguredOnPageLoad = false;
                var formData = {};
                var initialData = {};
                data.config.forEach(function (field) {
                    formData[field.name] = field.value || field.defaultValue;
                    initialData[field.name] = field.value;
                    //for simplicity sake, we will consider a plugin was configured if we have any value that is stored in the DB
                    wasConfiguredOnPageLoad = wasConfiguredOnPageLoad || !!field.value;
                });
                _this.setState({
                    fieldList: data.config,
                    formData: formData,
                    initialData: initialData,
                    wasConfiguredOnPageLoad: wasConfiguredOnPageLoad,
                }, _this.onLoadSuccess);
            },
            error: this.onLoadError,
        });
    };
    PluginSettings.prototype.render = function () {
        var _this = this;
        var _a;
        if (this.state.state === FormState.LOADING) {
            return <LoadingIndicator />;
        }
        var isSaving = this.state.state === FormState.SAVING;
        var hasChanges = !isEqual(this.state.initialData, this.state.formData);
        var data = this.state.rawData;
        if (data.config_error) {
            var authUrl = data.auth_url;
            if (authUrl.indexOf('?') === -1) {
                authUrl += '?next=' + encodeURIComponent(document.location.pathname);
            }
            else {
                authUrl += '&next=' + encodeURIComponent(document.location.pathname);
            }
            return (<div className="m-b-1">
          <div className="alert alert-warning m-b-1">{data.config_error}</div>
          <a className="btn btn-primary" href={authUrl}>
            {t('Associate Identity')}
          </a>
        </div>);
        }
        if (this.state.state === FormState.ERROR && !this.state.fieldList) {
            return (<div className="alert alert-error m-b-1">
          {tct('An unknown error occurred. Need help with this? [link:Contact support]', {
                link: <a href="https://sentry.io/support/"/>,
            })}
        </div>);
        }
        var fieldList = this.state.fieldList;
        if (!(fieldList === null || fieldList === void 0 ? void 0 : fieldList.length)) {
            return null;
        }
        return (<Form css={{ width: '100%' }} onSubmit={this.onSubmit} submitDisabled={isSaving || !hasChanges}>
        <Flex>
          {this.state.errors.__all__ && (<div className="alert alert-block alert-error">
              <ul>
                <li>{this.state.errors.__all__}</li>
              </ul>
            </div>)}
          {(_a = this.state.fieldList) === null || _a === void 0 ? void 0 : _a.map(function (f) {
            return _this.renderField({
                config: f,
                formData: _this.state.formData,
                formErrors: _this.state.errors,
                onChange: _this.changeField.bind(_this, f.name),
            });
        })}
        </Flex>
      </Form>);
    };
    PluginSettings.propTypes = {
        organization: PropTypes.object.isRequired,
        project: PropTypes.object.isRequired,
        plugin: PropTypes.object.isRequired,
    };
    return PluginSettings;
}(PluginComponentBase));
var Flex = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n"], ["\n  display: flex;\n  flex-direction: column;\n"])));
export default PluginSettings;
var templateObject_1;
//# sourceMappingURL=settings.jsx.map