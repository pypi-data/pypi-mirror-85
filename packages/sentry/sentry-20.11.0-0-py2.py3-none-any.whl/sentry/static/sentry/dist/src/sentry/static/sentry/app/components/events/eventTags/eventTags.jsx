import { __makeTemplateObject } from "tslib";
import React from 'react';
import isEmpty from 'lodash/isEmpty';
import styled from '@emotion/styled';
import EventDataSection from 'app/components/events/eventDataSection';
import { defined, generateQueryWithTag } from 'app/utils';
import { t } from 'app/locale';
import Pills from 'app/components/pills';
import space from 'app/styles/space';
import EventTagsPill from './eventTagsPill';
var EventTags = function (_a) {
    var tags = _a.event.tags, orgId = _a.orgId, projectId = _a.projectId, location = _a.location, hasQueryFeature = _a.hasQueryFeature;
    if (isEmpty(tags)) {
        return null;
    }
    var streamPath = "/organizations/" + orgId + "/issues/";
    var releasesPath = "/organizations/" + orgId + "/releases/";
    return (<StyledEventDataSection title={t('Tags')} type="tags">
      <Pills>
        {tags.map(function (tag, index) { return (<EventTagsPill key={!defined(tag.key) ? "tag-pill-" + index : tag.key} tag={tag} projectId={projectId} orgId={orgId} location={location} query={generateQueryWithTag(location.query, tag)} streamPath={streamPath} releasesPath={releasesPath} hasQueryFeature={hasQueryFeature}/>); })}
      </Pills>
    </StyledEventDataSection>);
};
export default EventTags;
var StyledEventDataSection = styled(EventDataSection)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  @media (min-width: ", ") {\n    margin-bottom: ", ";\n  }\n"], ["\n  @media (min-width: ", ") {\n    margin-bottom: ", ";\n  }\n"])), function (p) { return p.theme.breakpoints[1]; }, space(3));
var templateObject_1;
//# sourceMappingURL=eventTags.jsx.map