import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t, tn } from 'app/locale';
import Tooltip from 'app/components/tooltip';
import Link from 'app/components/links/link';
import Count from 'app/components/count';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
import { getReleaseNewIssuesUrl } from '../../utils';
var IssuesQuantity = function (_a) {
    var orgSlug = _a.orgSlug, newGroups = _a.newGroups, projectId = _a.projectId, releaseVersion = _a.releaseVersion, _b = _a.isCompact, isCompact = _b === void 0 ? false : _b;
    return (<Tooltip title={t('Open in Issues')}>
    <Link to={getReleaseNewIssuesUrl(orgSlug, projectId, releaseVersion)}>
      {isCompact ? (<Issues>
          <StyledCount value={newGroups}/>
          <span>{tn('issue', 'issues', newGroups)}</span>
        </Issues>) : (<Count value={newGroups}/>)}
    </Link>
  </Tooltip>);
};
export default IssuesQuantity;
var Issues = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: auto max-content;\n  justify-content: flex-end;\n  align-items: center;\n  text-align: end;\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: auto max-content;\n  justify-content: flex-end;\n  align-items: center;\n  text-align: end;\n"])), space(0.5));
// overflowEllipsis is useful if the count's value is over 1000000000
var StyledCount = styled(Count)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), overflowEllipsis);
var templateObject_1, templateObject_2;
//# sourceMappingURL=issuesQuantity.jsx.map