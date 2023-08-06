import { __makeTemplateObject, __read } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import space from 'app/styles/space';
import QueryCount from 'app/components/queryCount';
import * as Layout from 'app/components/layouts/thirds';
var queries = [
    ['is:inbox', t('Inbox')],
    ['!is:inbox is:unresolved', t('Backlog')],
    ['is:ignored', t('Ignored')],
    ['is:resolved', t('Resolved')],
];
function IssueListHeader(_a) {
    var query = _a.query, queryCount = _a.queryCount, queryMaxCount = _a.queryMaxCount, onTabChange = _a.onTabChange;
    var count = <StyledQueryCount count={queryCount} max={queryMaxCount}/>;
    return (<React.Fragment>
      <BorderlessHeader>
        <StyledHeaderContent>
          <StyledLayoutTitle>{t('Issues')}</StyledLayoutTitle>
        </StyledHeaderContent>
      </BorderlessHeader>
      <TabLayoutHeader>
        <Layout.HeaderNavTabs underlined>
          {queries.map(function (_a) {
        var _b = __read(_a, 2), tabQuery = _b[0], queryName = _b[1];
        return (<li key={tabQuery} className={query === tabQuery ? 'active' : ''}>
              <a onClick={function () { return onTabChange(tabQuery); }}>
                {queryName} {query === tabQuery && count}
              </a>
            </li>);
    })}
        </Layout.HeaderNavTabs>
      </TabLayoutHeader>
    </React.Fragment>);
}
export default IssueListHeader;
var StyledLayoutTitle = styled(Layout.Title)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space(0.5));
var BorderlessHeader = styled(Layout.Header)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  border-bottom: 0;\n"], ["\n  border-bottom: 0;\n"])));
var TabLayoutHeader = styled(Layout.Header)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  padding-top: 0;\n\n  @media (max-width: ", ") {\n    padding-top: 0;\n  }\n"], ["\n  padding-top: 0;\n\n  @media (max-width: ", ") {\n    padding-top: 0;\n  }\n"])), function (p) { return p.theme.breakpoints[1]; });
var StyledHeaderContent = styled(Layout.HeaderContent)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin-bottom: 0;\n"], ["\n  margin-bottom: 0;\n"])));
var StyledQueryCount = styled(QueryCount)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.gray300; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=header.jsx.map