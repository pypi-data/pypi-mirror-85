import { __extends, __makeTemplateObject, __values } from "tslib";
import React from 'react';
import DocumentTitle from 'react-document-title';
import { css } from '@emotion/core';
import styled from '@emotion/styled';
import AsyncView from 'app/views/asyncView';
import { t } from 'app/locale';
import ConfigStore from 'app/stores/configStore';
import { ApiForm } from 'app/components/forms';
import sentryPattern from 'app/../images/pattern/sentry-pattern.png';
import space from 'app/styles/space';
import Alert from 'app/components/alert';
import { IconWarning } from 'app/icons';
import { getOptionDefault, getOptionField, getForm } from '../options';
var InstallWizard = /** @class */ (function (_super) {
    __extends(InstallWizard, _super);
    function InstallWizard() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    InstallWizard.prototype.getEndpoints = function () {
        return [['data', '/internal/options/?query=is:required']];
    };
    InstallWizard.prototype.renderFormFields = function () {
        var e_1, _a;
        var options = this.state.data;
        var missingOptions = new Set(Object.keys(options).filter(function (option) { return !options[option].field.isSet; }));
        // This is to handle the initial installation case.
        // Even if all options are filled out, we want to prompt to confirm
        // them. This is a bit of a hack because we're assuming that
        // the backend only spit back all filled out options for
        // this case.
        if (missingOptions.size === 0) {
            missingOptions = new Set(Object.keys(options));
        }
        // A mapping of option name to Field object
        var fields = {};
        try {
            for (var missingOptions_1 = __values(missingOptions), missingOptions_1_1 = missingOptions_1.next(); !missingOptions_1_1.done; missingOptions_1_1 = missingOptions_1.next()) {
                var key = missingOptions_1_1.value;
                var option = options[key];
                if (option.field.disabled) {
                    continue;
                }
                fields[key] = getOptionField(key, option.field);
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (missingOptions_1_1 && !missingOptions_1_1.done && (_a = missingOptions_1.return)) _a.call(missingOptions_1);
            }
            finally { if (e_1) throw e_1.error; }
        }
        return getForm(fields);
    };
    InstallWizard.prototype.getInitialData = function () {
        var options = this.state.data;
        var data = {};
        Object.keys(options).forEach(function (optionName) {
            var option = options[optionName];
            if (option.field.disabled) {
                return;
            }
            // TODO(dcramer): we need to rethink this logic as doing multiple "is this value actually set"
            // is problematic
            // all values to their server-defaults (as client-side defaults dont really work)
            var displayValue = option.value || getOptionDefault(optionName);
            if (
            // XXX(dcramer): we need the user to explicitly choose beacon.anonymous
            // vs using an implied default so effectively this is binding
            optionName !== 'beacon.anonymous' &&
                // XXX(byk): if we don't have a set value but have a default value filled
                // instead, from the client, set it on the data so it is sent to the server
                !option.field.isSet &&
                displayValue !== undefined) {
                data[optionName] = displayValue;
            }
        });
        return data;
    };
    InstallWizard.prototype.getTitle = function () {
        return t('Setup Sentry');
    };
    InstallWizard.prototype.render = function () {
        var version = ConfigStore.get('version');
        return (<DocumentTitle title={this.getTitle()}>
        <Wrapper>
          <Pattern />
          <SetupWizard>
            <Heading>
              <span>{t('Welcome to Sentry')}</span>
              <Version>{version.current}</Version>
            </Heading>
            {this.state.loading
            ? this.renderLoading()
            : this.state.error
                ? this.renderError()
                : this.renderBody()}
          </SetupWizard>
        </Wrapper>
      </DocumentTitle>);
    };
    InstallWizard.prototype.renderError = function () {
        return (<Alert type="error" icon={<IconWarning />}>
        {t('We were unable to load the required configuration from the Sentry server. Please take a look at the service logs.')}
      </Alert>);
    };
    InstallWizard.prototype.renderBody = function () {
        return (<ApiForm apiMethod="PUT" apiEndpoint={this.getEndpoints()[0][1]} submitLabel={t('Continue')} initialData={this.getInitialData()} onSubmitSuccess={this.props.onConfigured}>
        <p>{t('Complete setup by filling out the required configuration.')}</p>

        {this.renderFormFields()}
      </ApiForm>);
    };
    return InstallWizard;
}(AsyncView));
export default InstallWizard;
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  justify-content: center;\n"], ["\n  display: flex;\n  justify-content: center;\n"])));
var fixedStyle = css(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  position: fixed;\n  top: 0;\n  right: 0;\n  bottom: 0;\n  left: 0;\n"], ["\n  position: fixed;\n  top: 0;\n  right: 0;\n  bottom: 0;\n  left: 0;\n"])));
var Pattern = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  &::before {\n    ", "\n    content: '';\n    background-image: linear-gradient(\n      to right,\n      ", " 0%,\n      ", " 100%\n    );\n    background-repeat: repeat-y;\n  }\n\n  &::after {\n    ", "\n    content: '';\n    background: url(", ");\n    background-size: 400px;\n    opacity: 0.8;\n  }\n"], ["\n  &::before {\n    ", "\n    content: '';\n    background-image: linear-gradient(\n      to right,\n      ", " 0%,\n      ", " 100%\n    );\n    background-repeat: repeat-y;\n  }\n\n  &::after {\n    ", "\n    content: '';\n    background: url(", ");\n    background-size: 400px;\n    opacity: 0.8;\n  }\n"])), fixedStyle, function (p) { return p.theme.purple200; }, function (p) { return p.theme.purple300; }, fixedStyle, sentryPattern);
var Heading = styled('h1')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  justify-content: space-between;\n  grid-auto-flow: column;\n  line-height: 36px;\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  justify-content: space-between;\n  grid-auto-flow: column;\n  line-height: 36px;\n"])), space(1));
var Version = styled('small')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  font-size: ", ";\n  line-height: inherit;\n"], ["\n  font-size: ", ";\n  line-height: inherit;\n"])), function (p) { return p.theme.fontSizeExtraLarge; });
var SetupWizard = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  background: ", ";\n  border-radius: ", ";\n  box-shadow: ", ";\n  margin-top: 40px;\n  padding: 40px 40px 20px;\n  width: 600px;\n  z-index: ", ";\n"], ["\n  background: ", ";\n  border-radius: ", ";\n  box-shadow: ", ";\n  margin-top: 40px;\n  padding: 40px 40px 20px;\n  width: 600px;\n  z-index: ", ";\n"])), function (p) { return p.theme.background; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.dropShadowHeavy; }, function (p) { return p.theme.zIndex.initial; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=index.jsx.map