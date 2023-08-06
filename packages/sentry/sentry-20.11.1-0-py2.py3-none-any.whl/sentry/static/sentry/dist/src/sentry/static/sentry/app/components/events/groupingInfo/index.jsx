import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import AsyncComponent from 'app/components/asyncComponent';
import EventDataSection from 'app/components/events/eventDataSection';
import { t } from 'app/locale';
import withOrganization from 'app/utils/withOrganization';
import space from 'app/styles/space';
import Button from 'app/components/button';
import LoadingIndicator from 'app/components/loadingIndicator';
import GroupVariant from './groupingVariant';
import GroupingConfigSelect from './groupingConfigSelect';
var EventGroupingInfo = /** @class */ (function (_super) {
    __extends(EventGroupingInfo, _super);
    function EventGroupingInfo() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.toggle = function () {
            _this.setState(function (state) { return ({
                isOpen: !state.isOpen,
                configOverride: state.isOpen ? null : state.configOverride,
            }); });
        };
        _this.handleConfigSelect = function (selection) {
            _this.setState({ configOverride: selection.value }, function () { return _this.reloadData(); });
        };
        return _this;
    }
    EventGroupingInfo.prototype.getEndpoints = function () {
        var _a;
        var _b = this.props, organization = _b.organization, event = _b.event, projectId = _b.projectId;
        var path = "/projects/" + organization.slug + "/" + projectId + "/events/" + event.id + "/grouping-info/";
        if ((_a = this.state) === null || _a === void 0 ? void 0 : _a.configOverride) {
            path = path + "?config=" + this.state.configOverride;
        }
        return [['groupInfo', path]];
    };
    EventGroupingInfo.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { isOpen: false, configOverride: null });
    };
    EventGroupingInfo.prototype.renderGroupInfoSummary = function () {
        var groupInfo = this.state.groupInfo;
        if (!groupInfo) {
            return null;
        }
        var groupedBy = Object.values(groupInfo)
            .filter(function (variant) { return variant.hash !== null && variant.description !== null; })
            .map(function (variant) { return variant.description; })
            .sort(function (a, b) { return a.toLowerCase().localeCompare(b.toLowerCase()); })
            .join(', ');
        return (<SummaryGroupedBy data-test-id="loaded-grouping-info">{"(" + t('grouped by') + " " + (groupedBy || t('nothing')) + ")"}</SummaryGroupedBy>);
    };
    EventGroupingInfo.prototype.renderGroupConfigSelect = function () {
        var configOverride = this.state.configOverride;
        var event = this.props.event;
        var configId = configOverride !== null && configOverride !== void 0 ? configOverride : event.groupingConfig.id;
        return (<GroupConfigWrapper>
        <GroupingConfigSelect eventConfigId={event.groupingConfig.id} configId={configId} onSelect={this.handleConfigSelect}/>
      </GroupConfigWrapper>);
    };
    EventGroupingInfo.prototype.renderGroupInfo = function () {
        var _a = this.state, groupInfo = _a.groupInfo, loading = _a.loading;
        var showGroupingConfig = this.props.showGroupingConfig;
        var variants = groupInfo
            ? Object.values(groupInfo).sort(function (a, b) {
                var _a, _b, _c, _d;
                return a.hash && !b.hash
                    ? -1
                    : (_d = (_a = a.description) === null || _a === void 0 ? void 0 : _a.toLowerCase().localeCompare((_c = (_b = b.description) === null || _b === void 0 ? void 0 : _b.toLowerCase()) !== null && _c !== void 0 ? _c : '')) !== null && _d !== void 0 ? _d : 1;
            })
            : [];
        return (<React.Fragment>
        {showGroupingConfig && this.renderGroupConfigSelect()}

        {loading ? (<LoadingIndicator />) : (variants.map(function (variant, index) { return (<React.Fragment key={variant.key}>
              <GroupVariant variant={variant} showGroupingConfig={showGroupingConfig}/>
              {index < variants.length - 1 && <VariantDivider />}
            </React.Fragment>); }))}
      </React.Fragment>);
    };
    EventGroupingInfo.prototype.renderLoading = function () {
        return this.renderBody();
    };
    EventGroupingInfo.prototype.renderBody = function () {
        var isOpen = this.state.isOpen;
        var title = (<React.Fragment>
        {t('Event Grouping Information')}
        {!isOpen && this.renderGroupInfoSummary()}
      </React.Fragment>);
        var actions = (<ToggleButton onClick={this.toggle} priority="link">
        {isOpen ? t('Hide Details') : t('Show Details')}
      </ToggleButton>);
        return (<EventDataSection type="grouping-info" title={title} actions={actions}>
        {isOpen && this.renderGroupInfo()}
      </EventDataSection>);
    };
    return EventGroupingInfo;
}(AsyncComponent));
var SummaryGroupedBy = styled('small')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  @media (max-width: ", ") {\n    display: block;\n    margin: 0 !important;\n  }\n"], ["\n  @media (max-width: ", ") {\n    display: block;\n    margin: 0 !important;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
var ToggleButton = styled(Button)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  font-weight: 700;\n  color: ", ";\n  &:hover,\n  &:focus {\n    color: ", ";\n  }\n"], ["\n  font-weight: 700;\n  color: ", ";\n  &:hover,\n  &:focus {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.subText; }, function (p) { return p.theme.textColor; });
var GroupConfigWrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-bottom: ", ";\n  margin-top: -", ";\n"], ["\n  margin-bottom: ", ";\n  margin-top: -", ";\n"])), space(1.5), space(1));
export var GroupingConfigItem = styled('span')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  font-family: ", ";\n  opacity: ", ";\n  font-weight: ", ";\n  font-size: ", ";\n"], ["\n  font-family: ", ";\n  opacity: ", ";\n  font-weight: ", ";\n  font-size: ", ";\n"])), function (p) { return p.theme.text.familyMono; }, function (p) { return (p.isHidden ? 0.5 : null); }, function (p) { return (p.isActive ? 'bold' : null); }, function (p) { return p.theme.fontSizeSmall; });
var VariantDivider = styled('hr')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  padding-top: ", ";\n"], ["\n  padding-top: ", ";\n"])), space(1));
export default withOrganization(EventGroupingInfo);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=index.jsx.map