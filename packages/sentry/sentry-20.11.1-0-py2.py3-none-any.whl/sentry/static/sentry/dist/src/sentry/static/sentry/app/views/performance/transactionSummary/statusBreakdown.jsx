import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import BreakdownBars from 'app/components/charts/breakdownBars';
import { SectionHeading } from 'app/components/charts/styles';
import Placeholder from 'app/components/placeholder';
import EmptyStateWarning from 'app/components/emptyStateWarning';
import ErrorPanel from 'app/components/charts/errorPanel';
import { IconWarning } from 'app/icons';
import QuestionTooltip from 'app/components/questionTooltip';
import DiscoverQuery from 'app/utils/discover/discoverQuery';
import { getTermHelp } from 'app/views/performance/data';
import space from 'app/styles/space';
function StatusBreakdown(_a) {
    var eventView = _a.eventView, location = _a.location, organization = _a.organization;
    var breakdownView = eventView
        .withColumns([
        { kind: 'function', function: ['count', '', ''] },
        { kind: 'field', field: 'transaction.status' },
    ])
        .withSorts([{ kind: 'desc', field: 'count' }]);
    return (<Container>
      <SectionHeading>
        {t('Status Breakdown')}
        <QuestionTooltip position="top" title={getTermHelp(organization, 'statusBreakdown')} size="sm"/>
      </SectionHeading>
      <DiscoverQuery eventView={breakdownView} location={location} orgSlug={organization.slug}>
        {function (_a) {
        var isLoading = _a.isLoading, error = _a.error, tableData = _a.tableData;
        if (isLoading) {
            return <Placeholder height="125px"/>;
        }
        if (error) {
            return (<ErrorPanel height="125px">
                <IconWarning color="gray300" size="lg"/>
              </ErrorPanel>);
        }
        if (!tableData || tableData.data.length === 0) {
            return <EmptyStateWarning small>{t('No data available')}</EmptyStateWarning>;
        }
        var points = tableData.data.map(function (row) { return ({
            label: String(row['transaction.status']),
            value: parseInt(String(row.count), 10),
        }); });
        return <BreakdownBars data={points}/>;
    }}
      </DiscoverQuery>
    </Container>);
}
export default StatusBreakdown;
var Container = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(4));
var templateObject_1;
//# sourceMappingURL=statusBreakdown.jsx.map