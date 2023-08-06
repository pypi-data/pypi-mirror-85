import { __assign, __extends, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import isEqual from 'lodash/isEqual';
import { t } from 'app/locale';
import { loadOrganizationTags } from 'app/actionCreators/tags';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import GlobalSelectionHeader from 'app/components/organizations/globalSelectionHeader';
import { PageContent } from 'app/styles/organization';
import EventView from 'app/utils/discover/eventView';
import { getAggregateAlias, isAggregateField, } from 'app/utils/discover/fields';
import { decodeScalar } from 'app/utils/queryString';
import { tokenizeSearch, stringifyQueryObject } from 'app/utils/tokenizeSearch';
import LightWeightNoProjectMessage from 'app/components/lightWeightNoProjectMessage';
import LoadingIndicator from 'app/components/loadingIndicator';
import DiscoverQuery from 'app/utils/discover/discoverQuery';
import withApi from 'app/utils/withApi';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import withOrganization from 'app/utils/withOrganization';
import withProjects from 'app/utils/withProjects';
import SummaryContent from './content';
import { addRoutePerformanceContext, getTransactionName } from '../utils';
import { PERCENTILE as VITAL_PERCENTILE, VITAL_GROUPS, } from '../transactionVitals/constants';
var TransactionSummary = /** @class */ (function (_super) {
    __extends(TransactionSummary, _super);
    function TransactionSummary() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            eventView: generateSummaryEventView(_this.props.location, getTransactionName(_this.props.location)),
        };
        return _this;
    }
    TransactionSummary.getDerivedStateFromProps = function (nextProps, prevState) {
        return __assign(__assign({}, prevState), { eventView: generateSummaryEventView(nextProps.location, getTransactionName(nextProps.location)) });
    };
    TransactionSummary.prototype.componentDidMount = function () {
        var _a = this.props, api = _a.api, organization = _a.organization, selection = _a.selection;
        loadOrganizationTags(api, organization.slug, selection);
        addRoutePerformanceContext(selection);
    };
    TransactionSummary.prototype.componentDidUpdate = function (prevProps) {
        var _a = this.props, api = _a.api, organization = _a.organization, selection = _a.selection;
        if (!isEqual(prevProps.selection.projects, selection.projects) ||
            !isEqual(prevProps.selection.datetime, selection.datetime)) {
            loadOrganizationTags(api, organization.slug, selection);
            addRoutePerformanceContext(selection);
        }
    };
    TransactionSummary.prototype.getDocumentTitle = function () {
        var name = getTransactionName(this.props.location);
        var hasTransactionName = typeof name === 'string' && String(name).trim().length > 0;
        if (hasTransactionName) {
            return [String(name).trim(), t('Performance')].join(' - ');
        }
        return [t('Summary'), t('Performance')].join(' - ');
    };
    TransactionSummary.prototype.getTotalsEventView = function (organization, eventView) {
        var threshold = organization.apdexThreshold.toString();
        var vitals = VITAL_GROUPS.map(function (_a) {
            var vs = _a.vitals;
            return vs;
        }).reduce(function (keys, vs) {
            vs.forEach(function (vital) { return keys.push(vital); });
            return keys;
        }, []);
        var totalsView = eventView.withColumns(__spread([
            {
                kind: 'function',
                function: ['apdex', threshold, undefined],
            },
            {
                kind: 'function',
                function: ['user_misery', threshold, undefined],
            },
            {
                kind: 'function',
                function: ['p95', '', undefined],
            },
            {
                kind: 'function',
                function: ['count', '', undefined],
            },
            {
                kind: 'function',
                function: ['count_unique', 'user', undefined],
            }
        ], vitals.map(function (vital) {
            return ({
                kind: 'function',
                function: ['percentile', vital, VITAL_PERCENTILE.toString()],
            });
        })));
        var emptyValues = totalsView.fields.reduce(function (values, field) {
            values[getAggregateAlias(field.field)] = 0;
            return values;
        }, {});
        return [totalsView, emptyValues];
    };
    TransactionSummary.prototype.render = function () {
        var _a = this.props, organization = _a.organization, location = _a.location;
        var eventView = this.state.eventView;
        var transactionName = getTransactionName(location);
        if (!eventView || transactionName === undefined) {
            // If there is no transaction name, redirect to the Performance landing page
            browserHistory.replace({
                pathname: "/organizations/" + organization.slug + "/performance/",
                query: __assign({}, location.query),
            });
            return null;
        }
        var _b = __read(this.getTotalsEventView(organization, eventView), 2), totalsView = _b[0], emptyValues = _b[1];
        return (<SentryDocumentTitle title={this.getDocumentTitle()} objSlug={organization.slug}>
        <GlobalSelectionHeader>
          <StyledPageContent>
            <LightWeightNoProjectMessage organization={organization}>
              <DiscoverQuery eventView={totalsView} orgSlug={organization.slug} location={location}>
                {function (_a) {
            var tableData = _a.tableData, isLoading = _a.isLoading;
            if (isLoading) {
                return <LoadingIndicator />;
            }
            var totals = (tableData && tableData.data.length
                ? tableData.data[0]
                : emptyValues);
            return (<SummaryContent location={location} organization={organization} eventView={eventView} transactionName={transactionName} totalValues={totals}/>);
        }}
              </DiscoverQuery>
            </LightWeightNoProjectMessage>
          </StyledPageContent>
        </GlobalSelectionHeader>
      </SentryDocumentTitle>);
    };
    return TransactionSummary;
}(React.Component));
var StyledPageContent = styled(PageContent)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: 0;\n"], ["\n  padding: 0;\n"])));
function generateSummaryEventView(location, transactionName) {
    if (transactionName === undefined) {
        return undefined;
    }
    // Use the user supplied query but overwrite any transaction or event type
    // conditions they applied.
    var query = decodeScalar(location.query.query) || '';
    var conditions = tokenizeSearch(query);
    conditions
        .setTagValues('event.type', ['transaction'])
        .setTagValues('transaction', [transactionName]);
    Object.keys(conditions.tagValues).forEach(function (field) {
        if (isAggregateField(field))
            conditions.removeTag(field);
    });
    // Handle duration filters from the latency chart
    if (location.query.startDuration || location.query.endDuration) {
        conditions.setTagValues('transaction.duration', [
            decodeScalar(location.query.startDuration),
            decodeScalar(location.query.endDuration),
        ]
            .filter(function (item) { return item; })
            .map(function (item, index) { return (index === 0 ? ">" + item : "<" + item); }));
    }
    return EventView.fromNewQueryWithLocation({
        id: undefined,
        version: 2,
        name: transactionName,
        fields: ['id', 'user.display', 'transaction.duration', 'timestamp'],
        query: stringifyQueryObject(conditions),
        projects: [],
    }, location);
}
export default withApi(withGlobalSelection(withProjects(withOrganization(TransactionSummary))));
var templateObject_1;
//# sourceMappingURL=index.jsx.map