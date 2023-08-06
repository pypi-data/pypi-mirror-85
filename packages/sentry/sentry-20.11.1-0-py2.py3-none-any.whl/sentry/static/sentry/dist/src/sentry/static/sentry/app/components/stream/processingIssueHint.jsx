import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Alert from 'app/components/alert';
import Button from 'app/components/button';
import { IconWarning, IconSettings } from 'app/icons';
import TimeSince from 'app/components/timeSince';
import { t, tn, tct } from 'app/locale';
import space from 'app/styles/space';
function ProcessingIssueHint(_a) {
    var orgId = _a.orgId, projectId = _a.projectId, issue = _a.issue, showProject = _a.showProject;
    var link = "/settings/" + orgId + "/projects/" + projectId + "/processing-issues/";
    var showButton = false;
    var text = '';
    var lastEvent = null;
    var icon = null;
    var alertType = 'error';
    var project = null;
    if (showProject) {
        project = (<React.Fragment>
        <strong>{projectId}</strong> &mdash;{' '}
      </React.Fragment>);
    }
    if (issue.numIssues > 0) {
        icon = <IconWarning size="sm" color="red300"/>;
        text = tn('There is %s issue blocking event processing', 'There are %s issues blocking event processing', issue.numIssues);
        lastEvent = (<React.Fragment>
        (
        {tct('last event from [ago]', {
            ago: <TimeSince date={issue.lastSeen}/>,
        })}
        )
      </React.Fragment>);
        alertType = 'error';
        showButton = true;
    }
    else if (issue.issuesProcessing > 0) {
        icon = <IconSettings size="sm" color="blue300"/>;
        alertType = 'info';
        text = tn('Reprocessing %s event …', 'Reprocessing %s events …', issue.issuesProcessing);
    }
    else if (issue.resolveableIssues > 0) {
        icon = <IconSettings size="sm" color="yellow300"/>;
        alertType = 'warning';
        text = tn('There is %s event pending reprocessing.', 'There are %s events pending reprocessing.', issue.resolveableIssues);
        showButton = true;
    }
    else {
        /* we should not go here but what do we know */
        return null;
    }
    return (<StyledAlert type={alertType} icon={icon}>
      <Wrapper>
        <div>
          {project} <strong>{text}</strong> {lastEvent}
        </div>
        {showButton && (<div>
            <StyledButton size="xsmall" to={link}>
              {t('Show details')}
            </StyledButton>
          </div>)}
      </Wrapper>
    </StyledAlert>);
}
export default ProcessingIssueHint;
var StyledAlert = styled(Alert)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  border-width: 1px 0;\n  border-radius: 0;\n  margin: 0;\n  font-size: ", ";\n"], ["\n  border-width: 1px 0;\n  border-radius: 0;\n  margin: 0;\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; });
var Wrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n"], ["\n  display: flex;\n  justify-content: space-between;\n"])));
var StyledButton = styled(Button)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  white-space: nowrap;\n  margin-left: ", ";\n"], ["\n  white-space: nowrap;\n  margin-left: ", ";\n"])), space(1));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=processingIssueHint.jsx.map