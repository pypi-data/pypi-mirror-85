import { __assign, __makeTemplateObject, __read } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import Button from 'app/components/button';
import SentryTypes from 'app/sentryTypes';
import TextOverflow from 'app/components/textOverflow';
import TimeSince from 'app/components/timeSince';
import Version from 'app/components/version';
import space from 'app/styles/space';
import getDynamicText from 'app/utils/getDynamicText';
import { IconReleases } from 'app/icons';
var DEPLOY_COUNT = 2;
var Deploys = function (_a) {
    var project = _a.project;
    var flattenedDeploys = Object.entries(project.latestDeploys || {}).map(function (_a) {
        var _b = __read(_a, 2), environment = _b[0], value = _b[1];
        return (__assign({ environment: environment }, value));
    });
    var deploys = (flattenedDeploys || [])
        .sort(function (a, b) { return new Date(b.dateFinished).getTime() - new Date(a.dateFinished).getTime(); })
        .slice(0, DEPLOY_COUNT);
    if (!deploys.length) {
        return <NoDeploys />;
    }
    return (<DeployRows>
      {deploys.map(function (deploy) { return (<Deploy key={deploy.environment + "-" + deploy.version} deploy={deploy} project={project}/>); })}
    </DeployRows>);
};
Deploys.propTypes = {
    project: SentryTypes.Project.isRequired,
};
export default Deploys;
var Deploy = function (_a) {
    var deploy = _a.deploy, project = _a.project;
    return (<React.Fragment>
    <IconReleases size="sm"/>
    <TextOverflow>
      <Environment>{deploy.environment}</Environment>
      <Version version={deploy.version} projectId={project.id} tooltipRawVersion truncate/>
    </TextOverflow>

    <DeployTime>
      {getDynamicText({
        fixed: '3 hours ago',
        value: <TimeSince date={deploy.dateFinished}/>,
    })}
    </DeployTime>
  </React.Fragment>);
};
Deploy.propTypes = {
    deploy: SentryTypes.Deploy.isRequired,
    project: SentryTypes.Project.isRequired,
};
var NoDeploys = function () { return (<GetStarted>
    <Button size="small" href="https://docs.sentry.io/learn/releases/" external>
      {t('Track deploys')}
    </Button>
  </GetStarted>); };
var DeployContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: ", ";\n  height: 115px;\n"], ["\n  padding: ", ";\n  height: 115px;\n"])), space(2));
var DeployRows = styled(DeployContainer)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 30px 1fr 1fr;\n  grid-template-rows: auto;\n  grid-column-gap: ", ";\n  grid-row-gap: ", ";\n  font-size: ", ";\n  line-height: 1.2;\n"], ["\n  display: grid;\n  grid-template-columns: 30px 1fr 1fr;\n  grid-template-rows: auto;\n  grid-column-gap: ", ";\n  grid-row-gap: ", ";\n  font-size: ", ";\n  line-height: 1.2;\n"])), space(1), space(1), function (p) { return p.theme.fontSizeMedium; });
var Environment = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  color: ", ";\n  margin: 0;\n"], ["\n  color: ", ";\n  margin: 0;\n"])), function (p) { return p.theme.textColor; });
var DeployTime = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  color: ", ";\n  overflow: hidden;\n  text-align: right;\n  text-overflow: ellipsis;\n"], ["\n  color: ", ";\n  overflow: hidden;\n  text-align: right;\n  text-overflow: ellipsis;\n"])), function (p) { return p.theme.gray300; });
var GetStarted = styled(DeployContainer)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=deploys.jsx.map