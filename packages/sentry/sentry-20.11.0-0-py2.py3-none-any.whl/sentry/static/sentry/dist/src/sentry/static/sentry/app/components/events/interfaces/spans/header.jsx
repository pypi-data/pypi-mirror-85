import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import space from 'app/styles/space';
import { rectOfContent, toPercent, getHumanDuration, pickSpanBarColour, boundsGenerator, getSpanID, getSpanOperation, } from './utils';
import * as CursorGuideHandler from './cursorGuideHandler';
import { TickAlignment, } from './types';
import { zIndex } from './styles';
export var MINIMAP_CONTAINER_HEIGHT = 106;
export var MINIMAP_SPAN_BAR_HEIGHT = 4;
var MINIMAP_HEIGHT = 120;
export var NUM_OF_SPANS_FIT_IN_MINI_MAP = MINIMAP_HEIGHT / MINIMAP_SPAN_BAR_HEIGHT;
var TIME_AXIS_HEIGHT = 20;
var VIEW_HANDLE_HEIGHT = 18;
var TraceViewHeader = /** @class */ (function (_super) {
    __extends(TraceViewHeader, _super);
    function TraceViewHeader() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    TraceViewHeader.prototype.renderCursorGuide = function (_a) {
        var cursorGuideHeight = _a.cursorGuideHeight, showCursorGuide = _a.showCursorGuide, mouseLeft = _a.mouseLeft;
        if (!showCursorGuide || !mouseLeft) {
            return null;
        }
        return (<CursorGuide style={{
            left: toPercent(mouseLeft),
            height: cursorGuideHeight + "px",
        }}/>);
    };
    TraceViewHeader.prototype.renderViewHandles = function (_a) {
        var isDragging = _a.isDragging, onLeftHandleDragStart = _a.onLeftHandleDragStart, leftHandlePosition = _a.leftHandlePosition, onRightHandleDragStart = _a.onRightHandleDragStart, rightHandlePosition = _a.rightHandlePosition, viewWindowStart = _a.viewWindowStart, viewWindowEnd = _a.viewWindowEnd;
        var leftHandleGhost = isDragging ? (<Handle left={viewWindowStart} onMouseDown={function () {
            // do nothing
        }} isDragging={false}/>) : null;
        var leftHandle = (<Handle left={leftHandlePosition} onMouseDown={onLeftHandleDragStart} isDragging={isDragging}/>);
        var rightHandle = (<Handle left={rightHandlePosition} onMouseDown={onRightHandleDragStart} isDragging={isDragging}/>);
        var rightHandleGhost = isDragging ? (<Handle left={viewWindowEnd} onMouseDown={function () {
            // do nothing
        }} isDragging={false}/>) : null;
        return (<React.Fragment>
        {leftHandleGhost}
        {rightHandleGhost}
        {leftHandle}
        {rightHandle}
      </React.Fragment>);
    };
    TraceViewHeader.prototype.renderFog = function (dragProps) {
        return (<React.Fragment>
        <Fog style={{ height: '100%', width: toPercent(dragProps.viewWindowStart) }}/>
        <Fog style={{
            height: '100%',
            width: toPercent(1 - dragProps.viewWindowEnd),
            left: toPercent(dragProps.viewWindowEnd),
        }}/>
      </React.Fragment>);
    };
    TraceViewHeader.prototype.renderDurationGuide = function (_a) {
        var showCursorGuide = _a.showCursorGuide, mouseLeft = _a.mouseLeft;
        if (!showCursorGuide || !mouseLeft) {
            return null;
        }
        var interactiveLayer = this.props.minimapInteractiveRef.current;
        if (!interactiveLayer) {
            return null;
        }
        var rect = rectOfContent(interactiveLayer);
        var trace = this.props.trace;
        var duration = mouseLeft * Math.abs(trace.traceEndTimestamp - trace.traceStartTimestamp);
        var style = { top: 0, left: "calc(" + mouseLeft * 100 + "% + 4px)" };
        var alignLeft = (1 - mouseLeft) * rect.width <= 100;
        return (<DurationGuideBox style={style} alignLeft={alignLeft}>
        <span>{getHumanDuration(duration)}</span>
      </DurationGuideBox>);
    };
    TraceViewHeader.prototype.renderTimeAxis = function (_a) {
        var showCursorGuide = _a.showCursorGuide, mouseLeft = _a.mouseLeft;
        var trace = this.props.trace;
        var duration = Math.abs(trace.traceEndTimestamp - trace.traceStartTimestamp);
        var firstTick = (<TickLabel align={TickAlignment.Left} hideTickMarker duration={0} style={{
            left: space(1),
        }}/>);
        var secondTick = (<TickLabel duration={duration * 0.25} style={{
            left: '25%',
        }}/>);
        var thirdTick = (<TickLabel duration={duration * 0.5} style={{
            left: '50%',
        }}/>);
        var fourthTick = (<TickLabel duration={duration * 0.75} style={{
            left: '75%',
        }}/>);
        var lastTick = (<TickLabel duration={duration} align={TickAlignment.Right} hideTickMarker style={{
            right: space(1),
        }}/>);
        return (<TimeAxis>
        {firstTick}
        {secondTick}
        {thirdTick}
        {fourthTick}
        {lastTick}
        {this.renderCursorGuide({
            showCursorGuide: showCursorGuide,
            mouseLeft: mouseLeft,
            cursorGuideHeight: TIME_AXIS_HEIGHT,
        })}
        {this.renderDurationGuide({
            showCursorGuide: showCursorGuide,
            mouseLeft: mouseLeft,
        })}
      </TimeAxis>);
    };
    TraceViewHeader.prototype.renderWindowSelection = function (dragProps) {
        if (!dragProps.isWindowSelectionDragging) {
            return null;
        }
        var left = Math.min(dragProps.windowSelectionInitial, dragProps.windowSelectionCurrent);
        return (<WindowSelection style={{
            left: toPercent(left),
            width: toPercent(dragProps.windowSelectionSize),
        }}/>);
    };
    TraceViewHeader.prototype.render = function () {
        var _this = this;
        return (<HeaderContainer>
        <ActualMinimap trace={this.props.trace}/>
        <CursorGuideHandler.Consumer>
          {function (_a) {
            var displayCursorGuide = _a.displayCursorGuide, hideCursorGuide = _a.hideCursorGuide, mouseLeft = _a.mouseLeft, showCursorGuide = _a.showCursorGuide;
            return (<div ref={_this.props.minimapInteractiveRef} style={{
                width: '100%',
                height: MINIMAP_HEIGHT + TIME_AXIS_HEIGHT + "px",
                position: 'absolute',
                left: 0,
                top: 0,
            }} onMouseEnter={function (event) {
                displayCursorGuide(event.pageX);
            }} onMouseLeave={function () {
                hideCursorGuide();
            }} onMouseMove={function (event) {
                displayCursorGuide(event.pageX);
            }} onMouseDown={function (event) {
                var target = event.target;
                if (target instanceof Element &&
                    target.getAttribute &&
                    target.getAttribute('data-ignore')) {
                    // ignore this event if we need to
                    return;
                }
                _this.props.dragProps.onWindowSelectionDragStart(event);
            }}>
              <MinimapContainer>
                {_this.renderFog(_this.props.dragProps)}
                {_this.renderCursorGuide({
                showCursorGuide: showCursorGuide,
                mouseLeft: mouseLeft,
                cursorGuideHeight: MINIMAP_HEIGHT,
            })}
                {_this.renderViewHandles(_this.props.dragProps)}
                {_this.renderWindowSelection(_this.props.dragProps)}
              </MinimapContainer>
              {_this.renderTimeAxis({
                showCursorGuide: showCursorGuide,
                mouseLeft: mouseLeft,
            })}
            </div>);
        }}
        </CursorGuideHandler.Consumer>
      </HeaderContainer>);
    };
    return TraceViewHeader;
}(React.Component));
var ActualMinimap = /** @class */ (function (_super) {
    __extends(ActualMinimap, _super);
    function ActualMinimap() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ActualMinimap.prototype.renderRootSpan = function () {
        var trace = this.props.trace;
        var generateBounds = boundsGenerator({
            traceStartTimestamp: trace.traceStartTimestamp,
            traceEndTimestamp: trace.traceEndTimestamp,
            viewStart: 0,
            viewEnd: 1,
        });
        var rootSpan = {
            trace_id: trace.traceID,
            span_id: trace.rootSpanID,
            start_timestamp: trace.traceStartTimestamp,
            timestamp: trace.traceEndTimestamp,
            op: trace.op,
            data: {},
        };
        return this.renderSpan({
            spanNumber: 0,
            generateBounds: generateBounds,
            span: rootSpan,
            childSpans: trace.childSpans,
        }).spanTree;
    };
    ActualMinimap.prototype.getBounds = function (bounds) {
        switch (bounds.type) {
            case 'TRACE_TIMESTAMPS_EQUAL':
            case 'INVALID_VIEW_WINDOW': {
                return {
                    left: toPercent(0),
                    width: '0px',
                };
            }
            case 'TIMESTAMPS_EQUAL': {
                return {
                    left: toPercent(bounds.start),
                    width: bounds.width + "px",
                };
            }
            case 'TIMESTAMPS_REVERSED':
            case 'TIMESTAMPS_STABLE': {
                return {
                    left: toPercent(bounds.start),
                    width: toPercent(bounds.end - bounds.start),
                };
            }
            default: {
                var _exhaustiveCheck = bounds;
                return _exhaustiveCheck;
            }
        }
    };
    ActualMinimap.prototype.renderSpan = function (_a) {
        var _this = this;
        var _b;
        var spanNumber = _a.spanNumber, childSpans = _a.childSpans, generateBounds = _a.generateBounds, span = _a.span;
        var spanBarColour = pickSpanBarColour(getSpanOperation(span));
        var bounds = generateBounds({
            startTimestamp: span.start_timestamp,
            endTimestamp: span.timestamp,
        });
        var _c = this.getBounds(bounds), spanLeft = _c.left, spanWidth = _c.width;
        var spanChildren = (_b = childSpans === null || childSpans === void 0 ? void 0 : childSpans[getSpanID(span)]) !== null && _b !== void 0 ? _b : [];
        // Mark descendents as being rendered. This is to address potential recursion issues due to malformed data.
        // For example if a span has a span_id that's identical to its parent_span_id.
        childSpans = __assign({}, childSpans);
        delete childSpans[getSpanID(span)];
        var reduced = spanChildren.reduce(function (acc, spanChild, index) {
            var key = "" + getSpanID(spanChild, String(index));
            var results = _this.renderSpan({
                spanNumber: acc.nextSpanNumber,
                childSpans: childSpans,
                generateBounds: generateBounds,
                span: spanChild,
            });
            acc.renderedSpanChildren.push(<React.Fragment key={key}>{results.spanTree}</React.Fragment>);
            acc.nextSpanNumber = results.nextSpanNumber;
            return acc;
        }, {
            renderedSpanChildren: [],
            nextSpanNumber: spanNumber + 1,
        });
        return {
            nextSpanNumber: reduced.nextSpanNumber,
            spanTree: (<React.Fragment>
          <MinimapSpanBar style={{
                backgroundColor: spanBarColour,
                left: spanLeft,
                width: spanWidth,
            }}/>
          {reduced.renderedSpanChildren}
        </React.Fragment>),
        };
    };
    ActualMinimap.prototype.render = function () {
        return (<MinimapBackground>
        <BackgroundSlider id="minimap-background-slider">
          {this.renderRootSpan()}
        </BackgroundSlider>
      </MinimapBackground>);
    };
    return ActualMinimap;
}(React.PureComponent));
var TimeAxis = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  width: 100%;\n  position: absolute;\n  left: 0;\n  bottom: 0;\n  border-top: 1px solid ", ";\n  height: ", "px;\n  background-color: ", ";\n  color: ", ";\n  font-size: 10px;\n  font-weight: 500;\n"], ["\n  width: 100%;\n  position: absolute;\n  left: 0;\n  bottom: 0;\n  border-top: 1px solid ", ";\n  height: ", "px;\n  background-color: ", ";\n  color: ", ";\n  font-size: 10px;\n  font-weight: 500;\n"])), function (p) { return p.theme.border; }, TIME_AXIS_HEIGHT, function (p) { return p.theme.background; }, function (p) { return p.theme.gray300; });
var TickLabelContainer = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  height: ", "px;\n  position: absolute;\n  top: 0;\n  display: flex;\n  align-items: center;\n  user-select: none;\n"], ["\n  height: ", "px;\n  position: absolute;\n  top: 0;\n  display: flex;\n  align-items: center;\n  user-select: none;\n"])), TIME_AXIS_HEIGHT);
var TickText = styled('span')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  position: absolute;\n  line-height: 1;\n  white-space: nowrap;\n\n  ", ";\n"], ["\n  position: absolute;\n  line-height: 1;\n  white-space: nowrap;\n\n  ",
    ";\n"])), function (_a) {
    var align = _a.align;
    switch (align) {
        case TickAlignment.Center: {
            return 'transform: translateX(-50%)';
        }
        case TickAlignment.Left: {
            return null;
        }
        case TickAlignment.Right: {
            return 'transform: translateX(-100%)';
        }
        default: {
            throw Error("Invalid tick alignment: " + align);
        }
    }
});
var TickMarker = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  width: 1px;\n  height: 4px;\n  background-color: ", ";\n  position: absolute;\n  top: 0;\n  left: 0;\n  transform: translateX(-50%);\n"], ["\n  width: 1px;\n  height: 4px;\n  background-color: ", ";\n  position: absolute;\n  top: 0;\n  left: 0;\n  transform: translateX(-50%);\n"])), function (p) { return p.theme.gray200; });
var TickLabel = function (props) {
    var style = props.style, duration = props.duration, _a = props.hideTickMarker, hideTickMarker = _a === void 0 ? false : _a, _b = props.align, align = _b === void 0 ? TickAlignment.Center : _b;
    return (<TickLabelContainer style={style}>
      {hideTickMarker ? null : <TickMarker />}
      <TickText align={align}>{getHumanDuration(duration)}</TickText>
    </TickLabelContainer>);
};
var DurationGuideBox = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  position: absolute;\n  background-color: ", ";\n  padding: 4px;\n  height: 100%;\n  border-radius: 3px;\n  border: 1px solid rgba(0, 0, 0, 0.1);\n  line-height: 1;\n  white-space: nowrap;\n\n  ", ";\n"], ["\n  position: absolute;\n  background-color: ", ";\n  padding: 4px;\n  height: 100%;\n  border-radius: 3px;\n  border: 1px solid rgba(0, 0, 0, 0.1);\n  line-height: 1;\n  white-space: nowrap;\n\n  ",
    ";\n"])), function (p) { return p.theme.background; }, function (_a) {
    var alignLeft = _a.alignLeft;
    if (!alignLeft) {
        return null;
    }
    return 'transform: translateX(-100%) translateX(-8px);';
});
var HeaderContainer = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  width: 100%;\n  position: sticky;\n  left: 0;\n  top: 0;\n  z-index: ", ";\n  background-color: ", ";\n  border-bottom: 1px solid ", ";\n  height: ", "px;\n"], ["\n  width: 100%;\n  position: sticky;\n  left: 0;\n  top: 0;\n  z-index: ", ";\n  background-color: ", ";\n  border-bottom: 1px solid ", ";\n  height: ", "px;\n"])), zIndex.minimapContainer, function (p) { return p.theme.background; }, function (p) { return p.theme.border; }, MINIMAP_HEIGHT + TIME_AXIS_HEIGHT + 1);
var MinimapBackground = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  height: ", "px;\n  max-height: ", "px;\n  overflow: hidden;\n  width: 100%;\n  position: absolute;\n  top: 0;\n  left: 0;\n"], ["\n  height: ", "px;\n  max-height: ", "px;\n  overflow: hidden;\n  width: 100%;\n  position: absolute;\n  top: 0;\n  left: 0;\n"])), MINIMAP_HEIGHT, MINIMAP_HEIGHT);
var MinimapContainer = styled('div')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  height: ", "px;\n  width: 100%;\n  position: relative;\n  left: 0;\n"], ["\n  height: ", "px;\n  width: 100%;\n  position: relative;\n  left: 0;\n"])), MINIMAP_HEIGHT);
var ViewHandleContainer = styled('div')(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  position: absolute;\n  top: 0;\n  height: ", "px;\n"], ["\n  position: absolute;\n  top: 0;\n  height: ", "px;\n"])), MINIMAP_HEIGHT);
var ViewHandleLine = styled('div')(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  height: ", "px;\n  width: 2px;\n  background-color: ", ";\n"], ["\n  height: ", "px;\n  width: 2px;\n  background-color: ", ";\n"])), MINIMAP_HEIGHT - VIEW_HANDLE_HEIGHT, function (p) { return p.theme.textColor; });
var ViewHandle = styled('div')(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  position: absolute;\n  background-color: ", ";\n  cursor: col-resize;\n  width: 8px;\n  height: ", "px;\n  bottom: 0;\n  left: -3px;\n"], ["\n  position: absolute;\n  background-color: ", ";\n  cursor: col-resize;\n  width: 8px;\n  height: ", "px;\n  bottom: 0;\n  left: -3px;\n"])), function (p) { return p.theme.textColor; }, VIEW_HANDLE_HEIGHT);
var Fog = styled('div')(templateObject_12 || (templateObject_12 = __makeTemplateObject(["\n  background-color: rgba(108, 95, 199, 0.1);\n  position: absolute;\n  top: 0;\n"], ["\n  background-color: rgba(108, 95, 199, 0.1);\n  position: absolute;\n  top: 0;\n"])));
var MinimapSpanBar = styled('div')(templateObject_13 || (templateObject_13 = __makeTemplateObject(["\n  position: relative;\n  height: 2px;\n  min-height: 2px;\n  max-height: 2px;\n  margin: 2px 0;\n  min-width: 1px;\n  border-radius: 1px;\n"], ["\n  position: relative;\n  height: 2px;\n  min-height: 2px;\n  max-height: 2px;\n  margin: 2px 0;\n  min-width: 1px;\n  border-radius: 1px;\n"])));
var BackgroundSlider = styled('div')(templateObject_14 || (templateObject_14 = __makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
var CursorGuide = styled('div')(templateObject_15 || (templateObject_15 = __makeTemplateObject(["\n  position: absolute;\n  top: 0;\n  width: 1px;\n  background-color: ", ";\n  transform: translateX(-50%);\n"], ["\n  position: absolute;\n  top: 0;\n  width: 1px;\n  background-color: ", ";\n  transform: translateX(-50%);\n"])), function (p) { return p.theme.red300; });
var Handle = function (_a) {
    var left = _a.left, onMouseDown = _a.onMouseDown, isDragging = _a.isDragging;
    return (<ViewHandleContainer style={{
        left: toPercent(left),
    }}>
    <ViewHandleLine />
    <ViewHandle data-ignore="true" onMouseDown={onMouseDown} isDragging={isDragging} style={{
        height: VIEW_HANDLE_HEIGHT + "px",
    }}/>
  </ViewHandleContainer>);
};
var WindowSelection = styled('div')(templateObject_16 || (templateObject_16 = __makeTemplateObject(["\n  position: absolute;\n  top: 0;\n  height: ", "px;\n  background-color: rgba(69, 38, 80, 0.1);\n"], ["\n  position: absolute;\n  top: 0;\n  height: ", "px;\n  background-color: rgba(69, 38, 80, 0.1);\n"])), MINIMAP_HEIGHT);
export default TraceViewHeader;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13, templateObject_14, templateObject_15, templateObject_16;
//# sourceMappingURL=header.jsx.map