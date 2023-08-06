import { __assign, __extends, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import * as DividerHandlerManager from 'app/components/events/interfaces/spans/dividerHandlerManager';
import { diffTransactions, getSpanID, boundsGenerator, isOrphanDiffSpan, } from './utils';
import SpanGroup from './spanGroup';
var SpanTree = /** @class */ (function (_super) {
    __extends(SpanTree, _super);
    function SpanTree() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.traceViewRef = React.createRef();
        return _this;
    }
    SpanTree.prototype.renderSpan = function (_a) {
        var _this = this;
        var _b;
        var span = _a.span, childSpans = _a.childSpans, spanNumber = _a.spanNumber, treeDepth = _a.treeDepth, continuingTreeDepths = _a.continuingTreeDepths, isLast = _a.isLast, isRoot = _a.isRoot, generateBounds = _a.generateBounds;
        var spanChildren = (_b = childSpans === null || childSpans === void 0 ? void 0 : childSpans[getSpanID(span)]) !== null && _b !== void 0 ? _b : [];
        // Mark descendents as being rendered. This is to address potential recursion issues due to malformed data.
        // For example if a span has a span_id that's identical to its parent_span_id.
        childSpans = __assign({}, childSpans);
        delete childSpans[getSpanID(span)];
        var treeDepthEntry = isOrphanDiffSpan(span)
            ? { type: 'orphan', depth: treeDepth }
            : treeDepth;
        var treeArr = isLast
            ? continuingTreeDepths
            : __spread(continuingTreeDepths, [treeDepthEntry]);
        var reduced = spanChildren.reduce(function (acc, spanChild, index) {
            var key = "" + getSpanID(spanChild);
            var results = _this.renderSpan({
                spanNumber: acc.nextSpanNumber,
                isLast: index + 1 === spanChildren.length,
                isRoot: false,
                span: spanChild,
                childSpans: childSpans,
                continuingTreeDepths: treeArr,
                treeDepth: treeDepth + 1,
                generateBounds: generateBounds,
            });
            acc.renderedSpanChildren.push(<React.Fragment key={key}>{results.spanTree}</React.Fragment>);
            acc.nextSpanNumber = results.nextSpanNumber;
            return acc;
        }, {
            renderedSpanChildren: [],
            nextSpanNumber: spanNumber + 1,
        });
        var spanTree = (<React.Fragment>
        <SpanGroup spanNumber={spanNumber} span={span} renderedSpanChildren={reduced.renderedSpanChildren} treeDepth={treeDepth} continuingTreeDepths={continuingTreeDepths} isRoot={isRoot} isLast={isLast} numOfSpanChildren={spanChildren.length} generateBounds={generateBounds}/>
      </React.Fragment>);
        return {
            nextSpanNumber: reduced.nextSpanNumber,
            spanTree: spanTree,
        };
    };
    SpanTree.prototype.renderRootSpans = function () {
        var _this = this;
        var _a = this.props, baselineEvent = _a.baselineEvent, regressionEvent = _a.regressionEvent;
        var comparisonReport = diffTransactions({
            baselineEvent: baselineEvent,
            regressionEvent: regressionEvent,
        });
        var rootSpans = comparisonReport.rootSpans, childSpans = comparisonReport.childSpans;
        var generateBounds = boundsGenerator(rootSpans);
        var nextSpanNumber = 1;
        var spanTree = (<React.Fragment key="root-spans-tree">
        {rootSpans.map(function (rootSpan, index) {
            var renderedRootSpan = _this.renderSpan({
                isLast: index + 1 === rootSpans.length,
                isRoot: true,
                span: rootSpan,
                childSpans: childSpans,
                spanNumber: nextSpanNumber,
                treeDepth: 0,
                continuingTreeDepths: [],
                generateBounds: generateBounds,
            });
            nextSpanNumber = renderedRootSpan.nextSpanNumber;
            return (<React.Fragment key={String(index)}>
              {renderedRootSpan.spanTree}
            </React.Fragment>);
        })}
      </React.Fragment>);
        return {
            spanTree: spanTree,
            nextSpanNumber: nextSpanNumber,
        };
    };
    SpanTree.prototype.render = function () {
        var spanTree = this.renderRootSpans().spanTree;
        return (<DividerHandlerManager.Provider interactiveLayerRef={this.traceViewRef}>
        <TraceViewContainer ref={this.traceViewRef}>{spanTree}</TraceViewContainer>
      </DividerHandlerManager.Provider>);
    };
    return SpanTree;
}(React.Component));
var TraceViewContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  overflow-x: hidden;\n  border-bottom-left-radius: 3px;\n  border-bottom-right-radius: 3px;\n"], ["\n  overflow-x: hidden;\n  border-bottom-left-radius: 3px;\n  border-bottom-right-radius: 3px;\n"])));
export default SpanTree;
var templateObject_1;
//# sourceMappingURL=spanTree.jsx.map