import { __assign, __awaiter, __extends, __generator } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import * as Sentry from '@sentry/react';
import { t } from 'app/locale';
import { ChartControls, InlineContainer, SectionHeading, SectionValue, } from 'app/components/charts/styles';
import { fetchTotalCount } from 'app/actionCreators/events';
import OptionSelector from 'app/components/charts/optionSelector';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import { isAPIPayloadSimilar } from 'app/utils/discover/eventView';
import { getAxisOptions } from '../data';
var ChartFooter = /** @class */ (function (_super) {
    __extends(ChartFooter, _super);
    function ChartFooter() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            totalValues: null,
        };
        _this.shouldRefetchData = function (prevProps) {
            var thisAPIPayload = _this.props.eventView.getEventsAPIPayload(_this.props.location);
            var otherAPIPayload = prevProps.eventView.getEventsAPIPayload(prevProps.location);
            return !isAPIPayloadSimilar(thisAPIPayload, otherAPIPayload);
        };
        _this.mounted = false;
        return _this;
    }
    ChartFooter.prototype.componentDidMount = function () {
        this.mounted = true;
        this.fetchTotalCount();
    };
    ChartFooter.prototype.componentDidUpdate = function (prevProps) {
        var orgSlugHasChanged = this.props.organization.slug !== prevProps.organization.slug;
        var shouldRefetch = this.shouldRefetchData(prevProps);
        if ((orgSlugHasChanged || shouldRefetch) && this.props.eventView.isValid()) {
            this.fetchTotalCount();
        }
    };
    ChartFooter.prototype.componentWillUnmount = function () {
        this.mounted = false;
    };
    ChartFooter.prototype.handleSelectorChange = function (key, value) {
        var _a;
        var _b = this.props, location = _b.location, organization = _b.organization;
        trackAnalyticsEvent({
            eventKey: 'performance_views.overview.change_chart',
            eventName: 'Performance Views: Change Overview Chart',
            organization_id: parseInt(organization.id, 10),
            metric: value,
        });
        browserHistory.push({
            pathname: location.pathname,
            query: __assign(__assign({}, location.query), (_a = {}, _a[key] = value, _a)),
        });
    };
    ChartFooter.prototype.fetchTotalCount = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, api, organization, location, eventView, totals, err_1;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, organization = _a.organization, location = _a.location, eventView = _a.eventView;
                        if (!eventView.isValid() || !this.mounted) {
                            return [2 /*return*/];
                        }
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, fetchTotalCount(api, organization.slug, eventView.getEventsAPIPayload(location))];
                    case 2:
                        totals = _b.sent();
                        if (this.mounted) {
                            this.setState({ totalValues: totals });
                        }
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _b.sent();
                        Sentry.captureException(err_1);
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    ChartFooter.prototype.render = function () {
        var _this = this;
        var _a = this.props, leftAxis = _a.leftAxis, organization = _a.organization, rightAxis = _a.rightAxis;
        var totalValues = this.state.totalValues;
        var value = typeof totalValues === 'number' ? totalValues.toLocaleString() : '-';
        var options = getAxisOptions(organization);
        var leftOptions = options.map(function (opt) { return (__assign(__assign({}, opt), { disabled: opt.value === rightAxis })); });
        var rightOptions = options.map(function (opt) { return (__assign(__assign({}, opt), { disabled: opt.value === leftAxis })); });
        return (<ChartControls>
        <InlineContainer>
          <SectionHeading>{t('Total Events')}</SectionHeading>
          <SectionValue>{value}</SectionValue>
        </InlineContainer>
        <InlineContainer>
          <OptionSelector title={t('Display 1')} selected={leftAxis} options={leftOptions} onChange={function (val) { return _this.handleSelectorChange('left', val); }} menuWidth="200px"/>
          <OptionSelector title={t('Display 2')} selected={rightAxis} options={rightOptions} onChange={function (val) { return _this.handleSelectorChange('right', val); }} menuWidth="200px"/>
        </InlineContainer>
      </ChartControls>);
    };
    return ChartFooter;
}(React.Component));
export default ChartFooter;
//# sourceMappingURL=footer.jsx.map