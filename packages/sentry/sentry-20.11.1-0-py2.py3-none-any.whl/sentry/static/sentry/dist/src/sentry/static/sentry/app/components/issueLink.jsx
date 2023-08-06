import { __makeTemplateObject } from "tslib";
import { Link } from 'react-router';
import React from 'react';
import classNames from 'classnames';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import Count from 'app/components/count';
import EventAnnotation from 'app/components/events/eventAnnotation';
import EventMessage from 'app/components/events/eventMessage';
import EventOrGroupTitle from 'app/components/eventOrGroupTitle';
import Hovercard from 'app/components/hovercard';
import TimeSince from 'app/components/timeSince';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
import { getMessage } from 'app/utils/events';
var IssueLink = function (_a) {
    var children = _a.children, orgId = _a.orgId, issue = _a.issue, to = _a.to, _b = _a.card, card = _b === void 0 ? true : _b;
    if (!card) {
        return <Link to={to}>{children}</Link>;
    }
    var message = getMessage(issue);
    var className = classNames({
        isBookmarked: issue.isBookmarked,
        hasSeen: issue.hasSeen,
        isResolved: issue.status === 'resolved',
    });
    var streamPath = "/organizations/" + orgId + "/issues/";
    var hovercardBody = (<div className={className}>
      <Section>
        <Title>
          <EventOrGroupTitle data={issue}/>
        </Title>

        <HovercardEventMessage level={issue.level} levelIndicatorSize="9px" message={message} annotations={<React.Fragment>
              {issue.logger && (<EventAnnotation>
                  <Link to={{
        pathname: streamPath,
        query: { query: "logger:" + issue.logger },
    }}>
                    {issue.logger}
                  </Link>
                </EventAnnotation>)}
              {issue.annotations.map(function (annotation, i) { return (<EventAnnotation key={i} dangerouslySetInnerHTML={{ __html: annotation }}/>); })}
            </React.Fragment>}/>
      </Section>

      <Grid>
        <div>
          <GridHeader>{t('First Seen')}</GridHeader>
          <StyledTimeSince date={issue.firstSeen}/>
        </div>
        <div>
          <GridHeader>{t('Last Seen')}</GridHeader>
          <StyledTimeSince date={issue.lastSeen}/>
        </div>
        <div>
          <GridHeader>{t('Occurrences')}</GridHeader>
          <Count value={issue.count}/>
        </div>
        <div>
          <GridHeader>{t('Users Affected')}</GridHeader>
          <Count value={issue.userCount}/>
        </div>
      </Grid>
    </div>);
    return (<Hovercard body={hovercardBody} header={issue.shortId}>
      <Link to={to}>{children}</Link>
    </Hovercard>);
};
export default IssueLink;
var Title = styled('h3')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-size: ", ";\n  margin: 0 0 ", ";\n  ", ";\n\n  em {\n    font-style: normal;\n    font-weight: 400;\n    color: ", ";\n    font-size: 90%;\n  }\n"], ["\n  font-size: ", ";\n  margin: 0 0 ", ";\n  ", ";\n\n  em {\n    font-style: normal;\n    font-weight: 400;\n    color: ", ";\n    font-size: 90%;\n  }\n"])), function (p) { return p.theme.fontSizeMedium; }, space(0.5), overflowEllipsis, function (p) { return p.theme.gray300; });
var Section = styled('section')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(2));
var Grid = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr 1fr;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: 1fr 1fr;\n  grid-gap: ", ";\n"])), space(2));
var HovercardEventMessage = styled(EventMessage)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  font-size: 12px;\n"], ["\n  font-size: 12px;\n"])));
var GridHeader = styled('h5')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  color: ", ";\n  font-size: 11px;\n  margin-bottom: ", ";\n  text-transform: uppercase;\n"], ["\n  color: ", ";\n  font-size: 11px;\n  margin-bottom: ", ";\n  text-transform: uppercase;\n"])), function (p) { return p.theme.gray300; }, space(0.5));
var StyledTimeSince = styled(TimeSince)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  color: inherit;\n"], ["\n  color: inherit;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=issueLink.jsx.map