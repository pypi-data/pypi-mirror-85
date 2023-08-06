import { __makeTemplateObject } from "tslib";
import React from 'react';
import { Link, withRouter } from 'react-router';
import styled from '@emotion/styled';
import { IconChat } from 'app/icons';
import { tct } from 'app/locale';
import EventAnnotation from 'app/components/events/eventAnnotation';
import ProjectBadge from 'app/components/idBadge/projectBadge';
import ShortId from 'app/components/shortId';
import Times from 'app/components/group/times';
import space from 'app/styles/space';
import withOrganization from 'app/utils/withOrganization';
import UnhandledTag from 'app/views/organizationGroupDetails/unhandledTag';
function EventOrGroupExtraDetails(_a) {
    var data = _a.data, showAssignee = _a.showAssignee, params = _a.params, organization = _a.organization;
    var _b = data, id = _b.id, lastSeen = _b.lastSeen, firstSeen = _b.firstSeen, subscriptionDetails = _b.subscriptionDetails, numComments = _b.numComments, logger = _b.logger, assignedTo = _b.assignedTo, annotations = _b.annotations, shortId = _b.shortId, project = _b.project, lifetime = _b.lifetime, isUnhandled = _b.isUnhandled;
    var issuesPath = "/organizations/" + params.orgId + "/issues/";
    var orgFeatures = new Set(organization.features);
    var hasInbox = orgFeatures.has('inbox');
    return (<GroupExtra>
      {isUnhandled && hasInbox && (<TagWrapper>
          <UnhandledTag />
        </TagWrapper>)}
      {shortId && (<GroupShortId shortId={shortId} avatar={project && <ProjectBadge project={project} avatarSize={14} hideName/>} onClick={function (e) {
        // prevent the clicks from propagating so that the short id can be selected
        e.stopPropagation();
    }}/>)}
      {!hasInbox && (<StyledTimes lastSeen={(lifetime === null || lifetime === void 0 ? void 0 : lifetime.lastSeen) || lastSeen} firstSeen={(lifetime === null || lifetime === void 0 ? void 0 : lifetime.firstSeen) || firstSeen}/>)}
      {numComments > 0 && (<CommentsLink to={"" + issuesPath + id + "/activity/"} className="comments">
          <IconChat size="xs" color={(subscriptionDetails === null || subscriptionDetails === void 0 ? void 0 : subscriptionDetails.reason) === 'mentioned' ? 'green300' : undefined}/>
          <span>{numComments}</span>
        </CommentsLink>)}
      {logger && (<LoggerAnnotation>
          <Link to={{
        pathname: issuesPath,
        query: {
            query: "logger:" + logger,
        },
    }}>
            {logger}
          </Link>
        </LoggerAnnotation>)}
      {annotations &&
        annotations.map(function (annotation, key) { return (<AnnotationNoMargin dangerouslySetInnerHTML={{
            __html: annotation,
        }} key={key}/>); })}

      {showAssignee && assignedTo && (<div>{tct('Assigned to [name]', { name: assignedTo.name })}</div>)}
    </GroupExtra>);
}
var GroupExtra = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: inline-grid;\n  grid-auto-flow: column dense;\n  grid-gap: ", ";\n  justify-content: start;\n  align-items: center;\n  color: ", ";\n  font-size: ", ";\n  position: relative;\n  min-width: 500px;\n  white-space: nowrap;\n\n  a {\n    color: inherit;\n  }\n"], ["\n  display: inline-grid;\n  grid-auto-flow: column dense;\n  grid-gap: ", ";\n  justify-content: start;\n  align-items: center;\n  color: ", ";\n  font-size: ", ";\n  position: relative;\n  min-width: 500px;\n  white-space: nowrap;\n\n  a {\n    color: inherit;\n  }\n"])), space(2), function (p) { return p.theme.subText; }, function (p) { return p.theme.fontSizeSmall; });
var TagWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  & > div {\n    margin-right: 0;\n  }\n"], ["\n  & > div {\n    margin-right: 0;\n  }\n"])));
var StyledTimes = styled(Times)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-right: 0;\n"], ["\n  margin-right: 0;\n"])));
var CommentsLink = styled(Link)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: inline-grid;\n  grid-gap: ", ";\n  align-items: center;\n  grid-auto-flow: column;\n  color: ", ";\n"], ["\n  display: inline-grid;\n  grid-gap: ", ";\n  align-items: center;\n  grid-auto-flow: column;\n  color: ", ";\n"])), space(0.5), function (p) { return p.theme.textColor; });
var GroupShortId = styled(ShortId)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  flex-shrink: 0;\n  font-size: ", ";\n  color: ", ";\n"], ["\n  flex-shrink: 0;\n  font-size: ", ";\n  color: ", ";\n"])), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.subText; });
var AnnotationNoMargin = styled(EventAnnotation)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  margin-left: 0;\n  padding-left: ", ";\n"], ["\n  margin-left: 0;\n  padding-left: ", ";\n"])), space(2));
var LoggerAnnotation = styled(AnnotationNoMargin)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.textColor; });
export default withRouter(withOrganization(EventOrGroupExtraDetails));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=eventOrGroupExtraDetails.jsx.map