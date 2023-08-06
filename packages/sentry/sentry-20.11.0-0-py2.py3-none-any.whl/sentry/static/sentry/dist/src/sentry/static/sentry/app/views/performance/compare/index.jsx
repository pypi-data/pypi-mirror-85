import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import * as Sentry from '@sentry/react';
import { t } from 'app/locale';
import withOrganization from 'app/utils/withOrganization';
import { PageContent } from 'app/styles/organization';
import LightWeightNoProjectMessage from 'app/components/lightWeightNoProjectMessage';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import NotFound from 'app/components/errors/notFound';
import LoadingIndicator from 'app/components/loadingIndicator';
import LoadingError from 'app/components/loadingError';
import FetchEvent from './fetchEvent';
import TransactionComparisonContent from './content';
var TransactionComparisonPage = /** @class */ (function (_super) {
    __extends(TransactionComparisonPage, _super);
    function TransactionComparisonPage() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    TransactionComparisonPage.prototype.getEventSlugs = function () {
        var _a = this.props.params, baselineEventSlug = _a.baselineEventSlug, regressionEventSlug = _a.regressionEventSlug;
        var validatedBaselineEventSlug = typeof baselineEventSlug === 'string' ? baselineEventSlug.trim() : undefined;
        var validatedRegressionEventSlug = typeof regressionEventSlug === 'string' ? regressionEventSlug.trim() : undefined;
        return {
            baselineEventSlug: validatedBaselineEventSlug,
            regressionEventSlug: validatedRegressionEventSlug,
        };
    };
    TransactionComparisonPage.prototype.fetchEvent = function (eventSlug, renderFunc) {
        if (!eventSlug) {
            return <NotFound />;
        }
        var organization = this.props.organization;
        return (<FetchEvent orgSlug={organization.slug} eventSlug={eventSlug}>
        {renderFunc}
      </FetchEvent>);
    };
    TransactionComparisonPage.prototype.renderComparison = function (_a) {
        var _this = this;
        var baselineEventSlug = _a.baselineEventSlug, regressionEventSlug = _a.regressionEventSlug;
        return this.fetchEvent(baselineEventSlug, function (baselineEventResults) {
            return _this.fetchEvent(regressionEventSlug, function (regressionEventResults) {
                if (baselineEventResults.isLoading || regressionEventResults.isLoading) {
                    return <LoadingIndicator />;
                }
                if (baselineEventResults.error || regressionEventResults.error) {
                    if (baselineEventResults.error) {
                        Sentry.captureException(baselineEventResults.error);
                    }
                    if (regressionEventResults.error) {
                        Sentry.captureException(regressionEventResults.error);
                    }
                    return <LoadingError />;
                }
                if (!baselineEventResults.event || !regressionEventResults.event) {
                    return <NotFound />;
                }
                var _a = _this.props, organization = _a.organization, location = _a.location, params = _a.params;
                return (<TransactionComparisonContent organization={organization} location={location} params={params} baselineEvent={baselineEventResults.event} regressionEvent={regressionEventResults.event}/>);
            });
        });
    };
    TransactionComparisonPage.prototype.getDocumentTitle = function (_a) {
        var baselineEventSlug = _a.baselineEventSlug, regressionEventSlug = _a.regressionEventSlug;
        if (typeof baselineEventSlug === 'string' &&
            typeof regressionEventSlug === 'string') {
            var title = t('Comparing %s to %s', baselineEventSlug, regressionEventSlug);
            return [title, t('Performance')].join(' - ');
        }
        return [t('Transaction Comparison'), t('Performance')].join(' - ');
    };
    TransactionComparisonPage.prototype.render = function () {
        var organization = this.props.organization;
        var _a = this.getEventSlugs(), baselineEventSlug = _a.baselineEventSlug, regressionEventSlug = _a.regressionEventSlug;
        return (<SentryDocumentTitle title={this.getDocumentTitle({ baselineEventSlug: baselineEventSlug, regressionEventSlug: regressionEventSlug })} objSlug={organization.slug}>
        <React.Fragment>
          <StyledPageContent>
            <LightWeightNoProjectMessage organization={organization}>
              {this.renderComparison({ baselineEventSlug: baselineEventSlug, regressionEventSlug: regressionEventSlug })}
            </LightWeightNoProjectMessage>
          </StyledPageContent>
        </React.Fragment>
      </SentryDocumentTitle>);
    };
    return TransactionComparisonPage;
}(React.PureComponent));
var StyledPageContent = styled(PageContent)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: 0;\n"], ["\n  padding: 0;\n"])));
export default withOrganization(TransactionComparisonPage);
var templateObject_1;
//# sourceMappingURL=index.jsx.map