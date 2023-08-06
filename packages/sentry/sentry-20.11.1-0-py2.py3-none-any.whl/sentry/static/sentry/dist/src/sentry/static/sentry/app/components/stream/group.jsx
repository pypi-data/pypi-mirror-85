import { __assign, __extends, __makeTemplateObject, __rest } from "tslib";
import $ from 'jquery';
// eslint-disable-next-line no-restricted-imports
import { Flex, Box } from 'reflexbox';
import React from 'react';
import styled from '@emotion/styled';
import classNames from 'classnames';
import { PanelItem } from 'app/components/panels';
import { valueIsEqual } from 'app/utils';
import AssigneeSelector from 'app/components/assigneeSelector';
import Count from 'app/components/count';
import DropdownMenu from 'app/components/dropdownMenu';
import EventOrGroupExtraDetails from 'app/components/eventOrGroupExtraDetails';
import EventOrGroupHeader from 'app/components/eventOrGroupHeader';
import GroupChart from 'app/components/stream/groupChart';
import GroupCheckBox from 'app/components/stream/groupCheckBox';
import GroupStore from 'app/stores/groupStore';
import GuideAnchor from 'app/components/assistant/guideAnchor';
import MenuItem from 'app/components/menuItem';
import SelectedGroupStore from 'app/stores/selectedGroupStore';
import space from 'app/styles/space';
import { getRelativeSummary } from 'app/components/organizations/timeRangeSelector/utils';
import { DEFAULT_STATS_PERIOD } from 'app/constants';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import withOrganization from 'app/utils/withOrganization';
import EventView from 'app/utils/discover/eventView';
import { t } from 'app/locale';
import Link from 'app/components/links/link';
import { queryToObj } from 'app/utils/stream';
import { callIfFunction } from 'app/utils/callIfFunction';
import TimesBadge from 'app/components/group/timesBadge';
import InboxReason from 'app/components/group/inboxReason';
var DiscoveryExclusionFields = [
    'query',
    'status',
    'bookmarked_by',
    'assigned',
    'assigned_to',
    'unassigned',
    'subscribed_by',
    'active_at',
    'first_release',
    'first_seen',
    'is',
    '__text',
];
var defaultProps = {
    statsPeriod: '24h',
    canSelect: true,
    withChart: true,
    useFilteredStats: false,
};
var StreamGroup = /** @class */ (function (_super) {
    __extends(StreamGroup, _super);
    function StreamGroup() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = _this.getInitialState();
        _this.listener = GroupStore.listen(function (itemIds) { return _this.onGroupChange(itemIds); }, undefined);
        _this.toggleSelect = function (evt) {
            var _a, _b;
            if (((_a = evt.target) === null || _a === void 0 ? void 0 : _a.tagName) === 'A') {
                return;
            }
            if (((_b = evt.target) === null || _b === void 0 ? void 0 : _b.tagName) === 'INPUT') {
                return;
            }
            if ($(evt.target).parents('a').length !== 0) {
                return;
            }
            SelectedGroupStore.toggleSelect(_this.state.data.id);
        };
        return _this;
    }
    StreamGroup.prototype.getInitialState = function () {
        var _a = this.props, id = _a.id, useFilteredStats = _a.useFilteredStats;
        var data = GroupStore.get(id);
        return {
            data: __assign(__assign({}, data), { filtered: useFilteredStats ? data.filtered : undefined }),
        };
    };
    StreamGroup.prototype.componentWillReceiveProps = function (nextProps) {
        if (nextProps.id !== this.props.id ||
            nextProps.useFilteredStats !== this.props.useFilteredStats) {
            var data = GroupStore.get(this.props.id);
            this.setState({
                data: __assign(__assign({}, data), { filtered: nextProps.useFilteredStats ? data.filtered : undefined }),
            });
        }
    };
    StreamGroup.prototype.shouldComponentUpdate = function (nextProps, nextState) {
        if (nextProps.statsPeriod !== this.props.statsPeriod) {
            return true;
        }
        if (!valueIsEqual(this.state.data, nextState.data)) {
            return true;
        }
        return false;
    };
    StreamGroup.prototype.componentWillUnmount = function () {
        callIfFunction(this.listener);
    };
    StreamGroup.prototype.onGroupChange = function (itemIds) {
        var id = this.props.id;
        if (!itemIds.has(id)) {
            return;
        }
        var data = GroupStore.get(id);
        this.setState({ data: data });
    };
    StreamGroup.prototype.getDiscoverUrl = function (isFiltered) {
        var _a = this.props, organization = _a.organization, query = _a.query, selection = _a.selection;
        var data = this.state.data;
        // when there is no discover feature open events page
        var hasDiscoverQuery = organization.features.includes('discover-basic');
        var queryTerms = [];
        if (isFiltered && query) {
            var queryObj = queryToObj(query);
            for (var queryTag in queryObj)
                if (!DiscoveryExclusionFields.includes(queryTag)) {
                    var queryVal = queryObj[queryTag].includes(' ')
                        ? "\"" + queryObj[queryTag] + "\""
                        : queryObj[queryTag];
                    queryTerms.push(queryTag + ":" + queryVal);
                }
            if (queryObj.__text) {
                queryTerms.push(queryObj.__text);
            }
        }
        var commonQuery = { projects: [Number(data.project.id)] };
        var searchQuery = (queryTerms.length ? ' ' : '') + queryTerms.join(' ');
        if (hasDiscoverQuery) {
            var _b = selection.datetime || {}, period = _b.period, start = _b.start, end = _b.end;
            var discoverQuery = __assign(__assign({}, commonQuery), { id: undefined, name: data.title || data.type, fields: ['title', 'release', 'environment', 'user', 'timestamp'], orderby: '-timestamp', query: "issue.id:" + data.id + searchQuery, version: 2 });
            if (!!start && !!end) {
                discoverQuery.start = String(start);
                discoverQuery.end = String(end);
            }
            else {
                discoverQuery.range = period || DEFAULT_STATS_PERIOD;
            }
            var discoverView = EventView.fromSavedQuery(discoverQuery);
            return discoverView.getResultsViewUrlTarget(organization.slug);
        }
        return {
            pathname: "/organizations/" + organization.slug + "/issues/" + data.id + "/events/",
            query: __assign(__assign({}, commonQuery), { query: searchQuery }),
        };
    };
    StreamGroup.prototype.render = function () {
        var _this = this;
        var _a, _b;
        var data = this.state.data;
        var _c = this.props, query = _c.query, hasGuideAnchor = _c.hasGuideAnchor, canSelect = _c.canSelect, memberList = _c.memberList, withChart = _c.withChart, statsPeriod = _c.statsPeriod, selection = _c.selection, organization = _c.organization, hasInboxReason = _c.hasInboxReason;
        var _d = selection.datetime || {}, period = _d.period, start = _d.start, end = _d.end;
        var summary = !!start && !!end
            ? 'time range'
            : getRelativeSummary(period || DEFAULT_STATS_PERIOD).toLowerCase();
        var primaryCount = data.filtered ? data.filtered.count : data.count;
        var secondaryCount = data.filtered ? data.count : undefined;
        var primaryUserCount = data.filtered ? data.filtered.userCount : data.userCount;
        var secondaryUserCount = data.filtered ? data.userCount : undefined;
        var showSecondaryPoints = Boolean(withChart && data && data.filtered && statsPeriod);
        var hasInbox = organization.features.includes('inbox');
        return (<Wrapper data-test-id="group" onClick={this.toggleSelect}>
        {canSelect && (<GroupCheckbox ml={2}>
            <GroupCheckBox id={data.id}/>
          </GroupCheckbox>)}
        <GroupSummary width={[8 / 12, 8 / 12, 6 / 12]} ml={canSelect ? 1 : 2} mr={1} flex="1">
          <EventOrGroupHeader includeLink data={data} query={query} size="normal"/>
          <EventOrGroupExtraDetails data={data}/>
        </GroupSummary>
        {hasGuideAnchor && <GuideAnchor target="issue_stream"/>}
        {withChart && (<Box width={160} mx={2} className="hidden-xs hidden-sm">
            <GroupChart statsPeriod={statsPeriod} data={data} showSecondaryPoints={showSecondaryPoints}/>
          </Box>)}
        <Flex width={[40, 60, 80, 80]} mx={2} justifyContent="flex-end">
          <DropdownMenu isNestedDropdown>
            {function (_a) {
            var isOpen = _a.isOpen, getRootProps = _a.getRootProps, getActorProps = _a.getActorProps, getMenuProps = _a.getMenuProps;
            var topLevelCx = classNames('dropdown', {
                'anchor-middle': true,
                open: isOpen,
            });
            return (<GuideAnchor target="dynamic_counts" disabled={!hasGuideAnchor}>
                  <span {...getRootProps({
                className: topLevelCx,
            })}>
                    <span {...getActorProps({})}>
                      <div className="dropdown-actor-title">
                        <PrimaryCount value={primaryCount}/>
                        {secondaryCount !== undefined && (<SecondaryCount value={secondaryCount}/>)}
                      </div>
                    </span>
                    <StyledDropdownList {...getMenuProps({ className: 'dropdown-menu inverted' })}>
                      {data.filtered && (<React.Fragment>
                          <StyledMenuItem to={_this.getDiscoverUrl(true)}>
                            <MenuItemText>{t('Matching search filters')}</MenuItemText>
                            <MenuItemCount value={data.filtered.count}/>
                          </StyledMenuItem>
                          <MenuItem divider/>
                        </React.Fragment>)}

                      <StyledMenuItem to={_this.getDiscoverUrl()}>
                        <MenuItemText>{t("Total in " + summary)}</MenuItemText>
                        <MenuItemCount value={data.count}/>
                      </StyledMenuItem>

                      {data.lifetime && (<React.Fragment>
                          <MenuItem divider/>
                          <StyledMenuItem>
                            <MenuItemText>{t('Since issue began')}</MenuItemText>
                            <MenuItemCount value={data.lifetime.count}/>
                          </StyledMenuItem>
                        </React.Fragment>)}
                    </StyledDropdownList>
                  </span>
                </GuideAnchor>);
        }}
          </DropdownMenu>
        </Flex>
        <Flex width={[40, 60, 80, 80]} mx={2} justifyContent="flex-end">
          <DropdownMenu isNestedDropdown>
            {function (_a) {
            var isOpen = _a.isOpen, getRootProps = _a.getRootProps, getActorProps = _a.getActorProps, getMenuProps = _a.getMenuProps;
            var topLevelCx = classNames('dropdown', {
                'anchor-middle': true,
                open: isOpen,
            });
            return (<span {...getRootProps({
                className: topLevelCx,
            })}>
                  <span {...getActorProps({})}>
                    <div className="dropdown-actor-title">
                      <PrimaryCount value={primaryUserCount}/>
                      {secondaryUserCount !== undefined && (<SecondaryCount dark value={secondaryUserCount}/>)}
                    </div>
                  </span>
                  <StyledDropdownList {...getMenuProps({ className: 'dropdown-menu inverted' })}>
                    {data.filtered && (<React.Fragment>
                        <StyledMenuItem to={_this.getDiscoverUrl(true)}>
                          <MenuItemText>{t('Matching search filters')}</MenuItemText>
                          <MenuItemCount value={data.filtered.userCount}/>
                        </StyledMenuItem>
                        <MenuItem divider/>
                      </React.Fragment>)}

                    <StyledMenuItem to={_this.getDiscoverUrl()}>
                      <MenuItemText>{t("Total in " + summary)}</MenuItemText>
                      <MenuItemCount value={data.userCount}/>
                    </StyledMenuItem>

                    {data.lifetime && (<React.Fragment>
                        <MenuItem divider/>
                        <StyledMenuItem>
                          <MenuItemText>{t('Since issue began')}</MenuItemText>
                          <MenuItemCount value={data.lifetime.userCount}/>
                        </StyledMenuItem>
                      </React.Fragment>)}
                  </StyledDropdownList>
                </span>);
        }}
          </DropdownMenu>
        </Flex>
        <Box width={80} mx={2} className="hidden-xs hidden-sm">
          <AssigneeSelector id={data.id} memberList={memberList}/>
        </Box>
        {hasInbox && (<React.Fragment>
            {hasInboxReason && (<ReasonBox width={95} mx={2} className="hidden-xs hidden-sm">
                <BadgeWrapper>
                  {data.inbox ? <InboxReason inbox={data.inbox}/> : <div />}
                </BadgeWrapper>
              </ReasonBox>)}
            <TimesBox width={170} mx={2} className="hidden-xs hidden-sm">
              <BadgeWrapper>
                <TimesBadge lastSeen={((_a = data.lifetime) === null || _a === void 0 ? void 0 : _a.lastSeen) || data.lastSeen} firstSeen={((_b = data.lifetime) === null || _b === void 0 ? void 0 : _b.firstSeen) || data.firstSeen}/>
              </BadgeWrapper>
            </TimesBox>
          </React.Fragment>)}
      </Wrapper>);
    };
    StreamGroup.defaultProps = defaultProps;
    return StreamGroup;
}(React.Component));
var Wrapper = styled(PanelItem)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: ", " 0;\n  align-items: center;\n  line-height: 1.1;\n"], ["\n  padding: ", " 0;\n  align-items: center;\n  line-height: 1.1;\n"])), space(1));
var GroupSummary = styled(Box)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  overflow: hidden;\n"], ["\n  overflow: hidden;\n"])));
var ReasonBox = styled(Box)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin: 0 ", " 0 ", ";\n"], ["\n  margin: 0 ", " 0 ", ";\n"])), space(0.25), space(1));
var TimesBox = styled(Box)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin: 0 ", " 0 ", ";\n"], ["\n  margin: 0 ", " 0 ", ";\n"])), space(1.5), space(0.5));
var GroupCheckbox = styled(Box)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  align-self: flex-start;\n  & input[type='checkbox'] {\n    margin: 0;\n    display: block;\n  }\n"], ["\n  align-self: flex-start;\n  & input[type='checkbox'] {\n    margin: 0;\n    display: block;\n  }\n"])));
var PrimaryCount = styled(Count)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeLarge; });
var SecondaryCount = styled(function (_a) {
    var value = _a.value, p = __rest(_a, ["value"]);
    return <Count {...p} value={value}/>;
})(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  font-size: ", ";\n\n  :before {\n    content: '/';\n    padding-left: ", ";\n    padding-right: 2px;\n    color: ", ";\n  }\n"], ["\n  font-size: ", ";\n\n  :before {\n    content: '/';\n    padding-left: ", ";\n    padding-right: 2px;\n    color: ", ";\n  }\n"])), function (p) { return p.theme.fontSizeLarge; }, space(0.25), function (p) { return p.theme.gray300; });
var StyledDropdownList = styled('ul')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  z-index: ", ";\n"], ["\n  z-index: ", ";\n"])), function (p) { return p.theme.zIndex.hovercard; });
var StyledMenuItem = styled(function (_a) {
    var to = _a.to, children = _a.children, p = __rest(_a, ["to", "children"]);
    return (<MenuItem noAnchor>
    {to ? (
    // @ts-expect-error allow target _blank for this link to open in new window
    <Link to={to} target="_blank">
        <div {...p}>{children}</div>
      </Link>) : (<div className="dropdown-toggle">
        <div {...p}>{children}</div>
      </div>)}
  </MenuItem>);
})(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  margin: 0;\n  display: flex;\n  flex-direction: row;\n  justify-content: space-between;\n"], ["\n  margin: 0;\n  display: flex;\n  flex-direction: row;\n  justify-content: space-between;\n"])));
var MenuItemCount = styled(function (_a) {
    var value = _a.value, p = __rest(_a, ["value"]);
    return (<div {...p}>
    <Count value={value}/>
  </div>);
})(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  text-align: right;\n  font-weight: bold;\n  padding-left: ", ";\n"], ["\n  text-align: right;\n  font-weight: bold;\n  padding-left: ", ";\n"])), space(1));
var MenuItemText = styled('div')(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  white-space: nowrap;\n  font-weight: normal;\n  text-align: left;\n  padding-right: ", ";\n"], ["\n  white-space: nowrap;\n  font-weight: normal;\n  text-align: left;\n  padding-right: ", ";\n"])), space(1));
var BadgeWrapper = styled('div')(templateObject_12 || (templateObject_12 = __makeTemplateObject(["\n  display: flex;\n  justify-content: center;\n"], ["\n  display: flex;\n  justify-content: center;\n"])));
export default withGlobalSelection(withOrganization(StreamGroup));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12;
//# sourceMappingURL=group.jsx.map