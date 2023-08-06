import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import { Panel } from 'app/components/panels';
import * as Layout from 'app/components/layouts/thirds';
import Breadcrumb from 'app/views/performance/breadcrumb';
import { decodeScalar } from 'app/utils/queryString';
import TraceView from './traceView';
import TransactionSummary from './transactionSummary';
import { isTransactionEvent } from './utils';
import { FilterViews } from '../landing';
var TransactionComparisonContent = /** @class */ (function (_super) {
    __extends(TransactionComparisonContent, _super);
    function TransactionComparisonContent() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    TransactionComparisonContent.prototype.getTransactionName = function () {
        var _a = this.props, baselineEvent = _a.baselineEvent, regressionEvent = _a.regressionEvent;
        if (isTransactionEvent(baselineEvent) && isTransactionEvent(regressionEvent)) {
            if (baselineEvent.title === regressionEvent.title) {
                return baselineEvent.title;
            }
            return t('mixed transaction names');
        }
        if (isTransactionEvent(baselineEvent)) {
            return baselineEvent.title;
        }
        if (isTransactionEvent(regressionEvent)) {
            return regressionEvent.title;
        }
        return t('no transaction title found');
    };
    TransactionComparisonContent.prototype.render = function () {
        var _a;
        var _b = this.props, baselineEvent = _b.baselineEvent, regressionEvent = _b.regressionEvent, organization = _b.organization, location = _b.location, params = _b.params;
        var isFromTrends = decodeScalar((_a = location.query) === null || _a === void 0 ? void 0 : _a.view) === FilterViews.TRENDS;
        var transactionName = baselineEvent.title === regressionEvent.title && !isFromTrends
            ? baselineEvent.title
            : undefined;
        return (<React.Fragment>
        <Layout.Header>
          <Layout.HeaderContent>
            <Breadcrumb organization={organization} location={location} transactionName={transactionName} transactionComparison/>
            <Layout.Title>{this.getTransactionName()}</Layout.Title>
          </Layout.HeaderContent>
          <Layout.HeaderActions>
            <TransactionSummary organization={organization} location={location} params={params} baselineEvent={baselineEvent} regressionEvent={regressionEvent}/>
          </Layout.HeaderActions>
        </Layout.Header>
        <Layout.Body>
          <StyledPanel>
            <TraceView baselineEvent={baselineEvent} regressionEvent={regressionEvent}/>
          </StyledPanel>
        </Layout.Body>
      </React.Fragment>);
    };
    return TransactionComparisonContent;
}(React.Component));
var StyledPanel = styled(Panel)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  grid-column: 1 / span 2;\n  overflow: hidden;\n"], ["\n  grid-column: 1 / span 2;\n  overflow: hidden;\n"])));
export default TransactionComparisonContent;
var templateObject_1;
//# sourceMappingURL=content.jsx.map