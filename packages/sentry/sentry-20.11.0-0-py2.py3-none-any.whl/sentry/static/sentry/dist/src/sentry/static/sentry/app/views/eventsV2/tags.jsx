import { __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import PropTypes from 'prop-types';
import styled from '@emotion/styled';
import * as Sentry from '@sentry/react';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { fetchTagFacets } from 'app/actionCreators/events';
import SentryTypes from 'app/sentryTypes';
import { SectionHeading } from 'app/components/charts/styles';
import EmptyStateWarning from 'app/components/emptyStateWarning';
import { IconWarning } from 'app/icons';
import Placeholder from 'app/components/placeholder';
import TagDistributionMeter from 'app/components/tagDistributionMeter';
import withApi from 'app/utils/withApi';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import { isAPIPayloadSimilar } from 'app/utils/discover/eventView';
var Tags = /** @class */ (function (_super) {
    __extends(Tags, _super);
    function Tags() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: true,
            tags: [],
            totalValues: null,
            error: '',
        };
        _this.shouldRefetchData = function (prevProps) {
            var thisAPIPayload = _this.props.eventView.getFacetsAPIPayload(_this.props.location);
            var otherAPIPayload = prevProps.eventView.getFacetsAPIPayload(prevProps.location);
            return !isAPIPayloadSimilar(thisAPIPayload, otherAPIPayload);
        };
        _this.fetchData = function (forceFetchData) {
            if (forceFetchData === void 0) { forceFetchData = false; }
            return __awaiter(_this, void 0, void 0, function () {
                var _a, api, organization, eventView, location, confirmedQuery, tags, err_1;
                return __generator(this, function (_b) {
                    switch (_b.label) {
                        case 0:
                            _a = this.props, api = _a.api, organization = _a.organization, eventView = _a.eventView, location = _a.location, confirmedQuery = _a.confirmedQuery;
                            this.setState({ loading: true, error: '', tags: [] });
                            // Fetch should be forced after mounting as confirmedQuery isn't guaranteed
                            // since this component can mount/unmount via show/hide tags separate from
                            // data being loaded for the rest of the page.
                            if (!forceFetchData && confirmedQuery === false) {
                                return [2 /*return*/];
                            }
                            _b.label = 1;
                        case 1:
                            _b.trys.push([1, 3, , 4]);
                            return [4 /*yield*/, fetchTagFacets(api, organization.slug, eventView.getFacetsAPIPayload(location))];
                        case 2:
                            tags = _b.sent();
                            this.setState({ loading: false, tags: tags });
                            return [3 /*break*/, 4];
                        case 3:
                            err_1 = _b.sent();
                            Sentry.captureException(err_1);
                            this.setState({ loading: false, error: err_1 });
                            return [3 /*break*/, 4];
                        case 4: return [2 /*return*/];
                    }
                });
            });
        };
        _this.handleTagClick = function (tag) {
            var organization = _this.props.organization;
            // metrics
            trackAnalyticsEvent({
                eventKey: 'discover_v2.facet_map.clicked',
                eventName: 'Discoverv2: Clicked on a tag on the facet map',
                tag: tag,
                organization_id: parseInt(organization.id, 10),
            });
        };
        _this.renderBody = function () {
            var _a = _this.state, loading = _a.loading, error = _a.error, tags = _a.tags;
            if (loading) {
                return _this.renderPlaceholders();
            }
            if (error) {
                return <EmptyStateWarning small/>;
            }
            if (tags.length > 0) {
                return tags.map(function (tag) { return _this.renderTag(tag); });
            }
            else {
                return (<StyledError>
          <StyledIconWarning color="gray300" size="lg"/>
          {t('No tags found')}
        </StyledError>);
            }
        };
        return _this;
    }
    Tags.prototype.componentDidMount = function () {
        this.fetchData(true);
    };
    Tags.prototype.componentDidUpdate = function (prevProps) {
        if (this.shouldRefetchData(prevProps) ||
            prevProps.confirmedQuery !== this.props.confirmedQuery) {
            this.fetchData();
        }
    };
    Tags.prototype.renderTag = function (tag) {
        var _a = this.props, generateUrl = _a.generateUrl, totalValues = _a.totalValues;
        var segments = tag.topValues.map(function (segment) {
            segment.url = generateUrl(tag.key, segment.value);
            return segment;
        });
        // Ensure we don't show >100% if there's a slight mismatch between the facets
        // endpoint and the totals endpoint
        var maxTotalValues = segments.length > 0
            ? Math.max(Number(totalValues), segments[0].count)
            : totalValues;
        return (<TagDistributionMeter key={tag.key} title={tag.key} segments={segments} totalValues={Number(maxTotalValues)} renderLoading={function () { return <StyledPlaceholder height="16px"/>; }} onTagClick={this.handleTagClick} showReleasePackage/>);
    };
    Tags.prototype.renderPlaceholders = function () {
        return (<React.Fragment>
        <StyledPlaceholderTitle key="title-1"/>
        <StyledPlaceholder key="bar-1"/>
        <StyledPlaceholderTitle key="title-2"/>
        <StyledPlaceholder key="bar-2"/>
        <StyledPlaceholderTitle key="title-3"/>
        <StyledPlaceholder key="bar-3"/>
      </React.Fragment>);
    };
    Tags.prototype.render = function () {
        return (<React.Fragment>
        <SectionHeading>{t('Tag Summary')}</SectionHeading>
        {this.renderBody()}
      </React.Fragment>);
    };
    Tags.propTypes = {
        api: PropTypes.object.isRequired,
        organization: SentryTypes.Organization.isRequired,
        location: PropTypes.object.isRequired,
        eventView: PropTypes.object.isRequired,
        confirmedQuery: PropTypes.bool,
    };
    return Tags;
}(React.Component));
var StyledError = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  color: ", ";\n  display: flex;\n  align-items: center;\n"], ["\n  color: ", ";\n  display: flex;\n  align-items: center;\n"])), function (p) { return p.theme.gray300; });
var StyledIconWarning = styled(IconWarning)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(1));
var StyledPlaceholder = styled(Placeholder)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  border-radius: ", ";\n  height: 16px;\n  margin-bottom: ", ";\n"], ["\n  border-radius: ", ";\n  height: 16px;\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.borderRadius; }, space(1.5));
var StyledPlaceholderTitle = styled(Placeholder)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  width: 100px;\n  height: 12px;\n  margin-bottom: ", ";\n"], ["\n  width: 100px;\n  height: 12px;\n  margin-bottom: ", ";\n"])), space(0.5));
export { Tags };
export default withApi(Tags);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=tags.jsx.map