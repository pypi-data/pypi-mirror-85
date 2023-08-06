import { __assign, __extends, __makeTemplateObject } from "tslib";
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import React from 'react';
import { t, tct } from 'app/locale';
import AsyncComponent from 'app/components/asyncComponent';
import AutoSelectText from 'app/components/autoSelectText';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import Button from 'app/components/button';
import ExternalLink from 'app/components/links/externalLink';
import PlatformPicker from 'app/components/platformPicker';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import TextBlock from 'app/views/settings/components/text/textBlock';
import recreateRoute from 'app/utils/recreateRoute';
import space from 'app/styles/space';
import withOrganization from 'app/utils/withOrganization';
var ProjectInstallOverview = /** @class */ (function (_super) {
    __extends(ProjectInstallOverview, _super);
    function ProjectInstallOverview() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.redirectToDocs = function (platform) {
            var _a = _this.props.params, orgId = _a.orgId, projectId = _a.projectId;
            var installUrl = _this.isGettingStarted
                ? "/organizations/" + orgId + "/projects/" + projectId + "/getting-started/" + platform + "/"
                : recreateRoute("install/" + platform + "/", __assign(__assign({}, _this.props), { stepBack: -3 }));
            browserHistory.push(installUrl);
        };
        _this.toggleDsn = function () {
            _this.setState(function (state) { return ({ showDsn: !state.showDsn }); });
        };
        return _this;
    }
    Object.defineProperty(ProjectInstallOverview.prototype, "isGettingStarted", {
        get: function () {
            return window.location.href.indexOf('getting-started') > 0;
        },
        enumerable: false,
        configurable: true
    });
    ProjectInstallOverview.prototype.getEndpoints = function () {
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
        return [['keyList', "/projects/" + orgId + "/" + projectId + "/keys/"]];
    };
    ProjectInstallOverview.prototype.render = function () {
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
        var _b = this.state, keyList = _b.keyList, showDsn = _b.showDsn;
        var issueStreamLink = "/organizations/" + orgId + "/issues/#welcome";
        return (<div>
        <SentryDocumentTitle title={t('Instrumentation')} objSlug={projectId}/>
        <SettingsPageHeader title={t('Configure your application')}/>
        <TextBlock>
          {t('Get started by selecting the platform or language that powers your application.')}
        </TextBlock>

        {showDsn ? (<DsnInfo>
            <DsnContainer>
              <strong>{t('DSN')}</strong>
              <DsnValue>{keyList === null || keyList === void 0 ? void 0 : keyList[0].dsn.public}</DsnValue>
            </DsnContainer>

            <Button priority="primary" to={issueStreamLink}>
              {t('Got it! Take me to the Issue Stream.')}
            </Button>
          </DsnInfo>) : (<p>
            <small>
              {tct('Already have things setup? [link:Get your DSN]', {
            link: <Button priority="link" onClick={this.toggleDsn}/>,
        })}
              .
            </small>
          </p>)}
        <PlatformPicker setPlatform={this.redirectToDocs} showOther={false}/>
        <p>
          {tct("For a complete list of client integrations, please see\n             [docLink:our in-depth documentation].", { docLink: <ExternalLink href="https://docs.sentry.io"/> })}
        </p>
      </div>);
    };
    return ProjectInstallOverview;
}(AsyncComponent));
var DsnValue = styled(function (p) { return (<code {...p}>
    <AutoSelectText>{p.children}</AutoSelectText>
  </code>); })(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  overflow: hidden;\n"], ["\n  overflow: hidden;\n"])));
var DsnInfo = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(3));
var DsnContainer = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", " ", ";\n  align-items: center;\n  margin-bottom: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", " ", ";\n  align-items: center;\n  margin-bottom: ", ";\n"])), space(1.5), space(2), space(2));
export default withOrganization(ProjectInstallOverview);
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=overview.jsx.map