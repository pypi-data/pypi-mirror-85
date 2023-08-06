import { __assign, __extends, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import pick from 'lodash/pick';
import { t, tct } from 'app/locale';
import { DEFAULT_RELATIVE_PERIODS } from 'app/constants';
import { URL_PARAM } from 'app/constants/globalSelectionHeader';
import { SectionHeading } from 'app/components/charts/styles';
import Button from 'app/components/button';
import EmptyStateWarning from 'app/components/emptyStateWarning';
import { Panel, PanelBody } from 'app/components/panels';
import space from 'app/styles/space';
import GroupList from 'app/components/issues/groupList';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import { stringifyQueryObject, QueryResults } from 'app/utils/tokenizeSearch';
var RelatedIssues = /** @class */ (function (_super) {
    __extends(RelatedIssues, _super);
    function RelatedIssues() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleOpenClick = function () {
            var organization = _this.props.organization;
            trackAnalyticsEvent({
                eventKey: 'performance_views.summary.open_issues',
                eventName: 'Performance Views: Open issues from transaction summary',
                organization_id: parseInt(organization.id, 10),
            });
        };
        _this.renderEmptyMessage = function () {
            var statsPeriod = _this.props.statsPeriod;
            var selectedTimePeriod = statsPeriod && DEFAULT_RELATIVE_PERIODS[statsPeriod];
            var displayedPeriod = selectedTimePeriod
                ? selectedTimePeriod.toLowerCase()
                : t('given timeframe');
            return (<Panel>
        <PanelBody>
          <EmptyStateWarning small withIcon={false}>
            {tct('No new issues for this transaction for the [timePeriod].', {
                timePeriod: displayedPeriod,
            })}
          </EmptyStateWarning>
        </PanelBody>
      </Panel>);
        };
        return _this;
    }
    RelatedIssues.prototype.getIssuesEndpoint = function () {
        var _a = this.props, transaction = _a.transaction, organization = _a.organization, start = _a.start, end = _a.end, statsPeriod = _a.statsPeriod, location = _a.location;
        var queryParams = __assign({ start: start,
            end: end,
            statsPeriod: statsPeriod, limit: 5, sort: 'new' }, pick(location.query, __spread(Object.values(URL_PARAM), ['cursor'])));
        return {
            path: "/organizations/" + organization.slug + "/issues/",
            queryParams: __assign(__assign({}, queryParams), { query: stringifyQueryObject(new QueryResults(['is:unresolved', "transaction:" + transaction])) }),
        };
    };
    RelatedIssues.prototype.render = function () {
        var organization = this.props.organization;
        var _a = this.getIssuesEndpoint(), path = _a.path, queryParams = _a.queryParams;
        var issueSearch = {
            pathname: "/organizations/" + organization.slug + "/issues/",
            query: queryParams,
        };
        return (<React.Fragment>
        <ControlsWrapper>
          <SectionHeading>{t('Related Issues')}</SectionHeading>
          <Button data-test-id="issues-open" size="small" to={issueSearch} onClick={this.handleOpenClick}>
            {t('Open in Issues')}
          </Button>
        </ControlsWrapper>

        <TableWrapper>
          <GroupList orgId={organization.slug} endpointPath={path} queryParams={queryParams} query="" canSelectGroups={false} renderEmptyMessage={this.renderEmptyMessage} withChart={false} withPagination={false}/>
        </TableWrapper>
      </React.Fragment>);
    };
    return RelatedIssues;
}(React.Component));
var ControlsWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n"])), space(1));
var TableWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-bottom: ", ";\n  ", " {\n    /* smaller space between table and pagination */\n    margin-bottom: -", ";\n  }\n"], ["\n  margin-bottom: ", ";\n  ", " {\n    /* smaller space between table and pagination */\n    margin-bottom: -", ";\n  }\n"])), space(4), Panel, space(1));
export default RelatedIssues;
var templateObject_1, templateObject_2;
//# sourceMappingURL=relatedIssues.jsx.map