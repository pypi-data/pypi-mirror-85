import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import classNames from 'classnames';
import { css } from '@emotion/core';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import { openDiffModal } from 'app/actionCreators/modal';
import Checkbox from 'app/components/checkbox';
import Count from 'app/components/count';
import EventOrGroupExtraDetails from 'app/components/eventOrGroupExtraDetails';
import EventOrGroupHeader from 'app/components/eventOrGroupHeader';
import FlowLayout from 'app/components/flowLayout';
import GroupingActions from 'app/actions/groupingActions';
import GroupingStore from 'app/stores/groupingStore';
import Hovercard from 'app/components/hovercard';
import ScoreBar from 'app/components/scoreBar';
import SimilarScoreCard from 'app/components/similarScoreCard';
import Button from 'app/components/button';
import SpreadLayout from 'app/components/spreadLayout';
import space from 'app/styles/space';
import { callIfFunction } from 'app/utils/callIfFunction';
var similarInterfaces = ['exception', 'message'];
var initialState = { visible: true, checked: false, busy: false };
var Item = /** @class */ (function (_super) {
    __extends(Item, _super);
    function Item() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = initialState;
        _this.listener = GroupingStore.listen(function (data) { return _this.onGroupChange(data); }, undefined);
        _this.handleToggle = function () {
            var issue = _this.props.issue;
            // clicking anywhere in the row will toggle the checkbox
            if (!_this.state.busy) {
                GroupingActions.toggleMerge(issue.id);
            }
        };
        _this.handleShowDiff = function (event) {
            var _a = _this.props, orgId = _a.orgId, baseIssueId = _a.groupId, issue = _a.issue, project = _a.project;
            var targetIssueId = issue.id;
            openDiffModal({ baseIssueId: baseIssueId, targetIssueId: targetIssueId, project: project, orgId: orgId });
            event.stopPropagation();
        };
        _this.handleCheckClick = function () {
            // noop to appease React warnings
            // This is controlled via row click instead of only Checkbox
        };
        _this.onGroupChange = function (_a) {
            var mergeState = _a.mergeState;
            if (!mergeState) {
                return;
            }
            var issue = _this.props.issue;
            var stateForId = mergeState.has(issue.id) && mergeState.get(issue.id);
            if (!stateForId) {
                return;
            }
            Object.keys(stateForId).forEach(function (key) {
                if (stateForId[key] === _this.state[key]) {
                    return;
                }
                _this.setState(function (prevState) {
                    var _a;
                    return (__assign(__assign({}, prevState), (_a = {}, _a[key] = stateForId[key], _a)));
                });
            });
        };
        return _this;
    }
    Item.prototype.componentWillUnmount = function () {
        callIfFunction(this.listener);
    };
    Item.prototype.render = function () {
        var _a = this.props, aggregate = _a.aggregate, scoresByInterface = _a.scoresByInterface, issue = _a.issue;
        var _b = this.state, visible = _b.visible, busy = _b.busy;
        if (!visible) {
            return null;
        }
        var cx = classNames('group', 'similar-issue', {
            isResolved: issue.status === 'resolved',
            busy: busy,
        });
        return (<SpreadLayout data-test-id="similar-item-row" className={cx} onClick={this.handleToggle} responsive>
        <FlowLayout truncate>
          <FlowLayout truncate>
            <ActionColumn>
              <Checkbox id={issue.id} value={issue.id} checked={this.state.checked} onChange={this.handleCheckClick}/>
            </ActionColumn>
            <EventDetails className="event-details">
              <EventOrGroupHeader data={issue} includeLink size="normal"/>
              <EventOrGroupExtraDetails data={__assign(__assign({}, issue), { lastSeen: '' })} showAssignee/>
            </EventDetails>
          </FlowLayout>
          <StyledButton onClick={this.handleShowDiff} size="small">
            {t('Diff')}
          </StyledButton>
        </FlowLayout>

        <Columns>
          <StyledCount value={issue.count}/>

          {similarInterfaces.map(function (interfaceName) {
            var avgScore = aggregate === null || aggregate === void 0 ? void 0 : aggregate[interfaceName];
            var scoreList = (scoresByInterface === null || scoresByInterface === void 0 ? void 0 : scoresByInterface[interfaceName]) || [];
            // Check for valid number (and not NaN)
            var scoreValue = typeof avgScore === 'number' && !Number.isNaN(avgScore) ? avgScore : 0;
            return (<Column key={interfaceName}>
                <Hovercard body={scoreList.length && <SimilarScoreCard scoreList={scoreList}/>}>
                  <ScoreBar vertical score={Math.round(scoreValue * 5)}/>
                </Hovercard>
              </Column>);
        })}
        </Columns>
      </SpreadLayout>);
    };
    return Item;
}(React.Component));
export default Item;
var Columns = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  flex-shrink: 0;\n  min-width: 300px;\n  width: 300px;\n"], ["\n  display: flex;\n  align-items: center;\n  flex-shrink: 0;\n  min-width: 300px;\n  width: 300px;\n"])));
var columnStyle = css(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  flex: 1;\n  flex-shrink: 0;\n  display: flex;\n  justify-content: center;\n  padding: ", " 0;\n"], ["\n  flex: 1;\n  flex-shrink: 0;\n  display: flex;\n  justify-content: center;\n  padding: ", " 0;\n"])), space(0.5));
var Column = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), columnStyle);
var StyledCount = styled(Count)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), columnStyle);
var StyledButton = styled(Button)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(0.25));
var ActionColumn = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  text-align: center;\n  width: 54px;\n"], ["\n  text-align: center;\n  width: 54px;\n"])));
var EventDetails = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  flex: 1;\n"], ["\n  flex: 1;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=item.jsx.map