import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import space from 'app/styles/space';
import Tag from 'app/components/tagDeprecated';
import Link from 'app/components/links/link';
import { IconOpen } from 'app/icons';
import { stringifyQueryObject, QueryResults } from 'app/utils/tokenizeSearch';
import overflowEllipsis from 'app/styles/overflowEllipsis';
var DeployBadge = function (_a) {
    var deploy = _a.deploy, orgSlug = _a.orgSlug, projectId = _a.projectId, version = _a.version, className = _a.className;
    var shouldLinkToIssues = !!orgSlug && !!version;
    var badge = (<Badge className={className}>
      <Label>{deploy.environment}</Label>
      {shouldLinkToIssues && <Icon size="xs"/>}
    </Badge>);
    if (!shouldLinkToIssues) {
        return badge;
    }
    return (<Link to={{
        pathname: "/organizations/" + orgSlug + "/issues/",
        query: {
            project: projectId !== null && projectId !== void 0 ? projectId : null,
            environment: deploy.environment,
            query: stringifyQueryObject(new QueryResults(["release:" + version])),
        },
    }} title={t('Open in Issues')}>
      {badge}
    </Link>);
};
var Badge = styled(Tag)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  background-color: ", ";\n  color: ", ";\n  font-size: ", ";\n  align-items: center;\n  height: 20px;\n"], ["\n  background-color: ", ";\n  color: ", ";\n  font-size: ", ";\n  align-items: center;\n  height: 20px;\n"])), function (p) { return p.theme.textColor; }, function (p) { return p.theme.background; }, function (p) { return p.theme.fontSizeSmall; });
var Label = styled('span')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  max-width: 100px;\n  line-height: 20px;\n  ", "\n"], ["\n  max-width: 100px;\n  line-height: 20px;\n  ", "\n"])), overflowEllipsis);
var Icon = styled(IconOpen)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-left: ", ";\n  flex-shrink: 0;\n"], ["\n  margin-left: ", ";\n  flex-shrink: 0;\n"])), space(0.5));
export default DeployBadge;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=deployBadge.jsx.map