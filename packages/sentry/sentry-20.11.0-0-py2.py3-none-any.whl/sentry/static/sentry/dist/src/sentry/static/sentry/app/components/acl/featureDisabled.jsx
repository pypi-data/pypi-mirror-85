import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { selectText } from 'app/utils/selectText';
import { IconInfo, IconChevron, IconLock, IconCopy } from 'app/icons';
import { t, tct } from 'app/locale';
import Alert from 'app/components/alert';
import Button from 'app/components/button';
import Clipboard from 'app/components/clipboard';
import ExternalLink from 'app/components/links/externalLink';
import space from 'app/styles/space';
import { CONFIG_DOCS_URL } from 'app/constants';
var installText = function (features, featureName) {
    return "# " + t('Enables the %s feature', featureName) + "\n" + features
        .map(function (f) { return "SENTRY_FEATURES['" + f + "'] = True"; })
        .join('\n');
};
/**
 * DisabledInfo renders a component informing that a feature has been disabled.
 *
 * By default this component will render a help button which toggles more
 * information about why the feature is disabled, showing the missing feature
 * flag and linking to documentation for managing sentry server feature flags.
 */
var FeatureDisabled = /** @class */ (function (_super) {
    __extends(FeatureDisabled, _super);
    function FeatureDisabled() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            showHelp: false,
        };
        _this.toggleHelp = function (e) {
            e.preventDefault();
            _this.setState(function (state) { return ({ showHelp: !state.showHelp }); });
        };
        return _this;
    }
    FeatureDisabled.prototype.renderFeatureDisabled = function () {
        var showHelp = this.state.showHelp;
        var _a = this.props, message = _a.message, features = _a.features, featureName = _a.featureName, hideHelpToggle = _a.hideHelpToggle;
        var showDescription = hideHelpToggle || showHelp;
        return (<React.Fragment>
        <FeatureDisabledMessage>
          {message}
          {!hideHelpToggle && (<HelpButton icon={showHelp ? (<IconChevron direction="down" size="xs"/>) : (<IconInfo size="xs"/>)} priority="link" size="xsmall" onClick={this.toggleHelp}>
              {t('Help')}
            </HelpButton>)}
        </FeatureDisabledMessage>
        {showDescription && (<HelpDescription onClick={function (e) {
            e.stopPropagation();
            e.preventDefault();
        }}>
            <p>
              {tct("Enable this feature on your sentry installation by adding the\n              following configuration into your [configFile:sentry.conf.py].\n              See [configLink:the configuration documentation] for more\n              details.", {
            configFile: <code />,
            configLink: <ExternalLink href={CONFIG_DOCS_URL}/>,
        })}
            </p>
            <Clipboard hideUnsupported value={installText(features, featureName)}>
              <Button borderless size="xsmall" onClick={function (e) {
            e.stopPropagation();
            e.preventDefault();
        }} icon={<IconCopy />}>
                {t('Copy to Clipboard')}
              </Button>
            </Clipboard>
            <pre onClick={function (e) { return selectText(e.target); }}>
              <code>{installText(features, featureName)}</code>
            </pre>
          </HelpDescription>)}
      </React.Fragment>);
    };
    FeatureDisabled.prototype.render = function () {
        var alert = this.props.alert;
        if (!alert) {
            return this.renderFeatureDisabled();
        }
        var AlertComponent = typeof alert === 'boolean' ? Alert : alert;
        return (<AlertComponent type="warning" icon={<IconLock size="xs"/>}>
        <AlertWrapper>{this.renderFeatureDisabled()}</AlertWrapper>
      </AlertComponent>);
    };
    FeatureDisabled.defaultProps = {
        message: t('This feature is not enabled on your Sentry installation.'),
    };
    return FeatureDisabled;
}(React.Component));
var FeatureDisabledMessage = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n"], ["\n  display: flex;\n  justify-content: space-between;\n"])));
var HelpButton = styled(Button)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  font-size: 0.8em;\n"], ["\n  font-size: 0.8em;\n"])));
var HelpDescription = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-size: 0.9em;\n  margin-top: ", ";\n\n  p {\n    line-height: 1.5em;\n  }\n\n  pre,\n  code {\n    margin-bottom: 0;\n    white-space: pre;\n  }\n"], ["\n  font-size: 0.9em;\n  margin-top: ", ";\n\n  p {\n    line-height: 1.5em;\n  }\n\n  pre,\n  code {\n    margin-bottom: 0;\n    white-space: pre;\n  }\n"])), space(1));
var AlertWrapper = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  ", " {\n    color: #6d6319;\n    &:hover {\n      color: #88750b;\n    }\n  }\n\n  pre,\n  code {\n    background: #fbf7e0;\n  }\n"], ["\n  ", " {\n    color: #6d6319;\n    &:hover {\n      color: #88750b;\n    }\n  }\n\n  pre,\n  code {\n    background: #fbf7e0;\n  }\n"])), HelpButton);
export default FeatureDisabled;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=featureDisabled.jsx.map