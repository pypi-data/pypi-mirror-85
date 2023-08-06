import { __extends } from "tslib";
import React from 'react';
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
        return _this;
    }
    SpanGroup.prototype.renderSpanChildren = function () {
        if (!this.state.showSpanTree) {
            return null;
        }
        return this.props.renderedSpanChildren;
    };
    SpanGroup.prototype.render = function () {
        var _a = this.props, span = _a.span, treeDepth = _a.treeDepth, continuingTreeDepths = _a.continuingTreeDepths, spanNumber = _a.spanNumber, isLast = _a.isLast, isRoot = _a.isRoot, numOfSpanChildren = _a.numOfSpanChildren, generateBounds = _a.generateBounds;
        return (<React.Fragment>
        <SpanBar span={span} treeDepth={treeDepth} continuingTreeDepths={continuingTreeDepths} spanNumber={spanNumber} isLast={isLast} isRoot={isRoot} numOfSpanChildren={numOfSpanChildren} showSpanTree={this.state.showSpanTree} toggleSpanTree={this.toggleSpanTree} generateBounds={generateBounds}/>
        {this.renderSpanChildren()}
      </React.Fragment>);
    };
    return SpanGroup;
}(React.Component));
export default SpanGroup;
//# sourceMappingURL=spanGroup.jsx.map