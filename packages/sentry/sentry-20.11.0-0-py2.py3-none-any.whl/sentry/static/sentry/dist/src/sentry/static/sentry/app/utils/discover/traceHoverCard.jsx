import { __extends, __makeTemplateObject, __values } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import withApi from 'app/utils/withApi';
import Hovercard from 'app/components/hovercard';
import Version from 'app/components/version';
import space from 'app/styles/space';
import Clipboard from 'app/components/clipboard';
import { IconCopy } from 'app/icons';
import LoadingIndicator from 'app/components/loadingIndicator';
import LoadingError from 'app/components/loadingError';
import EventView from './eventView';
import DiscoverQuery from './discoverQuery';
var TraceHoverCard = /** @class */ (function (_super) {
    __extends(TraceHoverCard, _super);
    function TraceHoverCard() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    TraceHoverCard.prototype.renderHeader = function () {
        var traceId = this.props.traceId;
        return (<HeaderWrapper>
        <span>{t('Trace')}</span>
        <TraceWrapper>
          <StyledTrace version={traceId} truncate anchor={false}/>
          <Clipboard value={traceId}>
            <ClipboardIconWrapper>
              <IconCopy size="xs"/>
            </ClipboardIconWrapper>
          </Clipboard>
        </TraceWrapper>
      </HeaderWrapper>);
    };
    TraceHoverCard.prototype.renderBody = function (_a) {
        var e_1, _b;
        var _c, _d;
        var tableData = _a.tableData, isLoading = _a.isLoading, error = _a.error;
        if (isLoading) {
            return (<LoadingWrapper>
          <LoadingIndicator mini/>
        </LoadingWrapper>);
        }
        if (error) {
            return <LoadingError />;
        }
        if (!tableData) {
            return null;
        }
        var numOfTransactions = 0;
        var numOfErrors = 0;
        try {
            // aggregate transaction and error (default, csp, error) counts
            for (var _e = __values(tableData.data), _f = _e.next(); !_f.done; _f = _e.next()) {
                var row = _f.value;
                if (row['event.type'] === 'transaction') {
                    numOfTransactions = (_c = row.count) !== null && _c !== void 0 ? _c : 0;
                }
                else {
                    numOfErrors += (_d = row.count) !== null && _d !== void 0 ? _d : 0;
                }
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (_f && !_f.done && (_b = _e.return)) _b.call(_e);
            }
            finally { if (e_1) throw e_1.error; }
        }
        return (<CardBodyWrapper>
        <EventCountWrapper>
          <h6>{t('Transactions')}</h6>
          <div className="count-since">{numOfTransactions.toLocaleString()}</div>
        </EventCountWrapper>
        <EventCountWrapper>
          <h6>{t('Errors')}</h6>
          <div className="count-since">{numOfErrors.toLocaleString()}</div>
        </EventCountWrapper>
      </CardBodyWrapper>);
    };
    TraceHoverCard.prototype.render = function () {
        var _this = this;
        var _a = this.props, traceId = _a.traceId, location = _a.location, api = _a.api, orgId = _a.orgId;
        // used to fetch number of transactions to display in hovercard
        var numTransactionsEventView = EventView.fromNewQueryWithLocation({
            id: undefined,
            name: "Transactions with Trace ID " + traceId,
            fields: ['event.type', 'count()'],
            query: "trace:" + traceId,
            projects: [],
            version: 2,
        }, location);
        // used to create link to discover page with relevant query
        var traceEventView = EventView.fromNewQueryWithLocation({
            id: undefined,
            name: "Events with Trace ID " + traceId,
            fields: ['transaction', 'project', 'trace.span', 'event.type', 'timestamp'],
            orderby: '-timestamp',
            query: "trace:" + traceId,
            projects: [],
            version: 2,
        }, location);
        var to = traceEventView.getResultsViewUrlTarget(orgId);
        return (<DiscoverQuery api={api} location={location} eventView={numTransactionsEventView} orgSlug={orgId}>
        {function (_a) {
            var isLoading = _a.isLoading, error = _a.error, tableData = _a.tableData;
            return (<Hovercard {..._this.props} header={_this.renderHeader()} body={_this.renderBody({ isLoading: isLoading, error: error, tableData: tableData })}>
              {_this.props.children({ to: to })}
            </Hovercard>);
        }}
      </DiscoverQuery>);
    };
    return TraceHoverCard;
}(React.Component));
var HeaderWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n"])));
var TraceWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  flex: 1;\n  align-items: center;\n  justify-content: flex-end;\n"], ["\n  display: flex;\n  flex: 1;\n  align-items: center;\n  justify-content: flex-end;\n"])));
var StyledTrace = styled(Version)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-right: ", ";\n  max-width: 190px;\n"], ["\n  margin-right: ", ";\n  max-width: 190px;\n"])), space(0.5));
var ClipboardIconWrapper = styled('span')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  &:hover {\n    cursor: pointer;\n  }\n"], ["\n  &:hover {\n    cursor: pointer;\n  }\n"])));
var LoadingWrapper = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n"])));
var CardBodyWrapper = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
var EventCountWrapper = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  flex: 1;\n"], ["\n  flex: 1;\n"])));
export default withApi(TraceHoverCard);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=traceHoverCard.jsx.map