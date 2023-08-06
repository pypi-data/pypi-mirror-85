import { __extends } from "tslib";
import React from 'react';
import { isGapSpan, getSpanID } from './utils';
import SpanBar from './spanBar';
var SpanGroup = /** @class */ (function (_super) {
    __extends(SpanGroup, _super);
    function SpanGroup() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            showSpanTree: true,
        };
        _this.toggleSpanTree = function () {
            _this.setState(function (state) { return ({
                showSpanTree: !state.showSpanTree,
            }); });
        };
        _this.renderSpanChildren = function () {
            if (!_this.state.showSpanTree) {
                return null;
            }
            return _this.props.renderedSpanChildren;
        };
        return _this;
    }
    SpanGroup.prototype.getSpanErrors = function () {
        var _a = this.props, span = _a.span, spansWithErrors = _a.spansWithErrors;
        var spanID = getSpanID(span);
        if (isGapSpan(span) || !(spansWithErrors === null || spansWithErrors === void 0 ? void 0 : spansWithErrors.data) || !spanID) {
            return [];
        }
        return spansWithErrors.data.filter(function (row) {
            return row['trace.span'] === spanID;
        });
    };
    SpanGroup.prototype.getTotalNumberOfErrors = function () {
        var spansWithErrors = this.props.spansWithErrors;
        var data = spansWithErrors === null || spansWithErrors === void 0 ? void 0 : spansWithErrors.data;
        if (Array.isArray(data)) {
            return data.length;
        }
        return 0;
    };
    SpanGroup.prototype.render = function () {
        var _a = this.props, spanBarColour = _a.spanBarColour, spanBarHatch = _a.spanBarHatch, span = _a.span, numOfSpanChildren = _a.numOfSpanChildren, trace = _a.trace, isLast = _a.isLast, isRoot = _a.isRoot, continuingTreeDepths = _a.continuingTreeDepths, generateBounds = _a.generateBounds, treeDepth = _a.treeDepth, spanNumber = _a.spanNumber, isCurrentSpanFilteredOut = _a.isCurrentSpanFilteredOut, orgId = _a.orgId, organization = _a.organization, event = _a.event;
        return (<React.Fragment>
        <SpanBar organization={organization} event={event} orgId={orgId} spanBarColour={spanBarColour} spanBarHatch={spanBarHatch} span={span} showSpanTree={this.state.showSpanTree} numOfSpanChildren={numOfSpanChildren} trace={trace} generateBounds={generateBounds} toggleSpanTree={this.toggleSpanTree} treeDepth={treeDepth} continuingTreeDepths={continuingTreeDepths} spanNumber={spanNumber} isLast={isLast} isRoot={isRoot} isCurrentSpanFilteredOut={isCurrentSpanFilteredOut} totalNumberOfErrors={this.getTotalNumberOfErrors()} spanErrors={this.getSpanErrors()}/>
        {this.renderSpanChildren()}
      </React.Fragment>);
    };
    return SpanGroup;
}(React.Component));
export default SpanGroup;
//# sourceMappingURL=spanGroup.jsx.map