import { __extends, __makeTemplateObject, __read } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import 'intersection-observer'; // this is a polyfill
import { t } from 'app/locale';
import { defined } from 'app/utils';
import space from 'app/styles/space';
import Count from 'app/components/count';
import Tooltip from 'app/components/tooltip';
import { IconChevron, IconWarning } from 'app/icons';
import globalTheme from 'app/utils/theme';
import { toPercent, getHumanDuration, getSpanID, getSpanOperation, isOrphanSpan, unwrapTreeDepth, isOrphanTreeDepth, isEventFromBrowserJavaScriptSDK, durationlessBrowserOps, getMeasurements, getMeasurementBounds, } from './utils';
import { MINIMAP_CONTAINER_HEIGHT, MINIMAP_SPAN_BAR_HEIGHT, NUM_OF_SPANS_FIT_IN_MINI_MAP, } from './header';
import { SPAN_ROW_HEIGHT, SPAN_ROW_PADDING, SpanRow, zIndex, getHatchPattern, } from './styles';
import * as DividerHandlerManager from './dividerHandlerManager';
import * as CursorGuideHandler from './cursorGuideHandler';
import * as MeasurementsManager from './measurementsManager';
import SpanDetail from './spanDetail';
// TODO: maybe use babel-plugin-preval
// for (let i = 0; i <= 1.0; i += 0.01) {
//   INTERSECTION_THRESHOLDS.push(i);
// }
var INTERSECTION_THRESHOLDS = [
    0,
    0.01,
    0.02,
    0.03,
    0.04,
    0.05,
    0.06,
    0.07,
    0.08,
    0.09,
    0.1,
    0.11,
    0.12,
    0.13,
    0.14,
    0.15,
    0.16,
    0.17,
    0.18,
    0.19,
    0.2,
    0.21,
    0.22,
    0.23,
    0.24,
    0.25,
    0.26,
    0.27,
    0.28,
    0.29,
    0.3,
    0.31,
    0.32,
    0.33,
    0.34,
    0.35,
    0.36,
    0.37,
    0.38,
    0.39,
    0.4,
    0.41,
    0.42,
    0.43,
    0.44,
    0.45,
    0.46,
    0.47,
    0.48,
    0.49,
    0.5,
    0.51,
    0.52,
    0.53,
    0.54,
    0.55,
    0.56,
    0.57,
    0.58,
    0.59,
    0.6,
    0.61,
    0.62,
    0.63,
    0.64,
    0.65,
    0.66,
    0.67,
    0.68,
    0.69,
    0.7,
    0.71,
    0.72,
    0.73,
    0.74,
    0.75,
    0.76,
    0.77,
    0.78,
    0.79,
    0.8,
    0.81,
    0.82,
    0.83,
    0.84,
    0.85,
    0.86,
    0.87,
    0.88,
    0.89,
    0.9,
    0.91,
    0.92,
    0.93,
    0.94,
    0.95,
    0.96,
    0.97,
    0.98,
    0.99,
    1.0,
];
var TOGGLE_BUTTON_MARGIN_RIGHT = 16;
var TOGGLE_BUTTON_MAX_WIDTH = 30;
export var TOGGLE_BORDER_BOX = TOGGLE_BUTTON_MAX_WIDTH + TOGGLE_BUTTON_MARGIN_RIGHT;
var MARGIN_LEFT = 0;
var getDurationDisplay = function (_a) {
    var width = _a.width, left = _a.left;
    var spaceNeeded = 0.3;
    if (left === undefined || width === undefined) {
        return 'inset';
    }
    if (left + width < 1 - spaceNeeded) {
        return 'right';
    }
    if (left > spaceNeeded) {
        return 'left';
    }
    return 'inset';
};
export var getBackgroundColor = function (_a) {
    var showStriping = _a.showStriping, showDetail = _a.showDetail, theme = _a.theme;
    if (!theme) {
        return theme.background;
    }
    if (showDetail) {
        return theme.textColor;
    }
    return showStriping ? theme.backgroundSecondary : theme.background;
};
var SpanBar = /** @class */ (function (_super) {
    __extends(SpanBar, _super);
    function SpanBar() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            showDetail: false,
        };
        _this.spanRowDOMRef = React.createRef();
        _this.intersectionObserver = void 0;
        _this.zoomLevel = 1; // assume initial zoomLevel is 100%
        _this._mounted = false;
        _this.toggleDisplayDetail = function () {
            _this.setState(function (state) { return ({
                showDetail: !state.showDetail,
            }); });
        };
        return _this;
    }
    SpanBar.prototype.componentDidMount = function () {
        this._mounted = true;
        if (this.spanRowDOMRef.current) {
            this.connectObservers();
        }
    };
    SpanBar.prototype.componentWillUnmount = function () {
        this._mounted = false;
        this.disconnectObservers();
    };
    SpanBar.prototype.renderDetail = function (_a) {
        var isVisible = _a.isVisible;
        if (!this.state.showDetail || !isVisible) {
            return null;
        }
        var _b = this.props, span = _b.span, orgId = _b.orgId, organization = _b.organization, isRoot = _b.isRoot, trace = _b.trace, totalNumberOfErrors = _b.totalNumberOfErrors, spanErrors = _b.spanErrors, event = _b.event;
        return (<SpanDetail span={span} orgId={orgId} organization={organization} event={event} isRoot={!!isRoot} trace={trace} totalNumberOfErrors={totalNumberOfErrors} spanErrors={spanErrors}/>);
    };
    SpanBar.prototype.getBounds = function () {
        var _a = this.props, event = _a.event, span = _a.span, generateBounds = _a.generateBounds;
        var bounds = generateBounds({
            startTimestamp: span.start_timestamp,
            endTimestamp: span.timestamp,
        });
        var shouldHideSpanWarnings = isEventFromBrowserJavaScriptSDK(event);
        switch (bounds.type) {
            case 'TRACE_TIMESTAMPS_EQUAL': {
                return {
                    warning: t('Trace times are equal'),
                    left: void 0,
                    width: void 0,
                    isSpanVisibleInView: bounds.isSpanVisibleInView,
                };
            }
            case 'INVALID_VIEW_WINDOW': {
                return {
                    warning: t('Invalid view window'),
                    left: void 0,
                    width: void 0,
                    isSpanVisibleInView: bounds.isSpanVisibleInView,
                };
            }
            case 'TIMESTAMPS_EQUAL': {
                var warning = shouldHideSpanWarnings &&
                    'op' in span &&
                    span.op &&
                    durationlessBrowserOps.includes(span.op)
                    ? void 0
                    : t('Equal start and end times');
                return {
                    warning: warning,
                    left: bounds.start,
                    width: 0.00001,
                    isSpanVisibleInView: bounds.isSpanVisibleInView,
                };
            }
            case 'TIMESTAMPS_REVERSED': {
                return {
                    warning: t('Reversed start and end times'),
                    left: bounds.start,
                    width: bounds.end - bounds.start,
                    isSpanVisibleInView: bounds.isSpanVisibleInView,
                };
            }
            case 'TIMESTAMPS_STABLE': {
                return {
                    warning: void 0,
                    left: bounds.start,
                    width: bounds.end - bounds.start,
                    isSpanVisibleInView: bounds.isSpanVisibleInView,
                };
            }
            default: {
                var _exhaustiveCheck = bounds;
                return _exhaustiveCheck;
            }
        }
    };
    SpanBar.prototype.renderMeasurements = function () {
        var _a = this.props, event = _a.event, generateBounds = _a.generateBounds;
        if (this.state.showDetail) {
            return null;
        }
        var measurements = getMeasurements(event);
        return (<React.Fragment>
        {Array.from(measurements).map(function (_a) {
            var _b = __read(_a, 2), timestamp = _b[0], verticalMark = _b[1];
            var names = Object.keys(verticalMark.marks);
            var bounds = getMeasurementBounds(timestamp, generateBounds);
            var shouldDisplay = defined(bounds.left) && defined(bounds.width);
            if (!shouldDisplay || !bounds.isSpanVisibleInView) {
                return null;
            }
            var measurementName = names.join('');
            return (<MeasurementsManager.Consumer key={String(timestamp)}>
              {function (_a) {
                var hoveringMeasurement = _a.hoveringMeasurement, notHovering = _a.notHovering;
                return (<MeasurementMarker style={{
                    left: "clamp(0%, " + toPercent(bounds.left || 0) + ", calc(100% - 1px))",
                }} failedThreshold={verticalMark.failedThreshold} onMouseEnter={function () {
                    hoveringMeasurement(measurementName);
                }} onMouseLeave={function () {
                    notHovering();
                }} onMouseOver={function () {
                    hoveringMeasurement(measurementName);
                }}/>);
            }}
            </MeasurementsManager.Consumer>);
        })}
      </React.Fragment>);
    };
    SpanBar.prototype.renderSpanTreeConnector = function (_a) {
        var hasToggler = _a.hasToggler;
        var _b = this.props, isLast = _b.isLast, isRoot = _b.isRoot, spanTreeDepth = _b.treeDepth, continuingTreeDepths = _b.continuingTreeDepths, span = _b.span, showSpanTree = _b.showSpanTree;
        var spanID = getSpanID(span);
        if (isRoot) {
            if (hasToggler) {
                return (<ConnectorBar style={{ right: '16px', height: '10px', bottom: '-5px', top: 'auto' }} key={spanID + "-last"} orphanBranch={false}/>);
            }
            return null;
        }
        var connectorBars = continuingTreeDepths.map(function (treeDepth) {
            var depth = unwrapTreeDepth(treeDepth);
            if (depth === 0) {
                // do not render a connector bar at depth 0,
                // if we did render a connector bar, this bar would be placed at depth -1
                // which does not exist.
                return null;
            }
            var left = ((spanTreeDepth - depth) * (TOGGLE_BORDER_BOX / 2) + 1) * -1;
            return (<ConnectorBar style={{ left: left }} key={spanID + "-" + depth} orphanBranch={isOrphanTreeDepth(treeDepth)}/>);
        });
        if (hasToggler && showSpanTree) {
            // if there is a toggle button, we add a connector bar to create an attachment
            // between the toggle button and any connector bars below the toggle button
            connectorBars.push(<ConnectorBar style={{
                right: '16px',
                height: '10px',
                bottom: isLast ? "-" + SPAN_ROW_HEIGHT / 2 + "px" : '0',
                top: 'auto',
            }} key={spanID + "-last"} orphanBranch={false}/>);
        }
        return (<SpanTreeConnector isLast={isLast} hasToggler={hasToggler} orphanBranch={isOrphanSpan(span)}>
        {connectorBars}
      </SpanTreeConnector>);
    };
    SpanBar.prototype.renderSpanTreeToggler = function (_a) {
        var _this = this;
        var left = _a.left;
        var _b = this.props, numOfSpanChildren = _b.numOfSpanChildren, isRoot = _b.isRoot, showSpanTree = _b.showSpanTree;
        var chevron = <StyledIconChevron direction={showSpanTree ? 'up' : 'down'}/>;
        if (numOfSpanChildren <= 0) {
            return (<SpanTreeTogglerContainer style={{ left: left + "px" }}>
          {this.renderSpanTreeConnector({ hasToggler: false })}
        </SpanTreeTogglerContainer>);
        }
        var chevronElement = !isRoot ? <div>{chevron}</div> : null;
        return (<SpanTreeTogglerContainer style={{ left: left + "px" }} hasToggler>
        {this.renderSpanTreeConnector({ hasToggler: true })}
        <SpanTreeToggler disabled={!!isRoot} isExpanded={showSpanTree} onClick={function (event) {
            event.stopPropagation();
            if (isRoot) {
                return;
            }
            _this.props.toggleSpanTree();
        }}>
          <Count value={numOfSpanChildren}/>
          {chevronElement}
        </SpanTreeToggler>
      </SpanTreeTogglerContainer>);
    };
    SpanBar.prototype.renderTitle = function () {
        var _a;
        var _b = this.props, span = _b.span, treeDepth = _b.treeDepth, spanErrors = _b.spanErrors;
        var operationName = getSpanOperation(span) ? (<strong>
        <OperationName spanErrors={spanErrors}>{getSpanOperation(span)}</OperationName>
        {" \u2014 "}
      </strong>) : ('');
        var description = (_a = span === null || span === void 0 ? void 0 : span.description) !== null && _a !== void 0 ? _a : getSpanID(span);
        var left = treeDepth * (TOGGLE_BORDER_BOX / 2) + MARGIN_LEFT;
        return (<SpanBarTitleContainer>
        {this.renderSpanTreeToggler({ left: left })}
        <SpanBarTitle style={{
            left: left + "px",
            width: '100%',
        }}>
          <span>
            {operationName}
            {description}
          </span>
        </SpanBarTitle>
      </SpanBarTitleContainer>);
    };
    SpanBar.prototype.connectObservers = function () {
        var _this = this;
        if (!this.spanRowDOMRef.current) {
            return;
        }
        this.disconnectObservers();
        /**
    
        We track intersections events between the span bar's DOM element
        and the viewport's (root) intersection area. the intersection area is sized to
        exclude the minimap. See below.
    
        By default, the intersection observer's root intersection is the viewport.
        We adjust the margins of this root intersection area to exclude the minimap's
        height. The minimap's height is always fixed.
    
          VIEWPORT (ancestor element used for the intersection events)
        +--+-------------------------+--+
        |  |                         |  |
        |  |       MINIMAP           |  |
        |  |                         |  |
        |  +-------------------------+  |  ^
        |  |                         |  |  |
        |  |       SPANS             |  |  | ROOT
        |  |                         |  |  | INTERSECTION
        |  |                         |  |  | OBSERVER
        |  |                         |  |  | HEIGHT
        |  |                         |  |  |
        |  |                         |  |  |
        |  |                         |  |  |
        |  +-------------------------+  |  |
        |                               |  |
        +-------------------------------+  v
    
         */
        this.intersectionObserver = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (!_this._mounted) {
                    return;
                }
                var shouldMoveMinimap = _this.props.trace.numOfSpans > NUM_OF_SPANS_FIT_IN_MINI_MAP;
                if (!shouldMoveMinimap) {
                    return;
                }
                var spanNumber = _this.props.spanNumber;
                var minimapSlider = document.getElementById('minimap-background-slider');
                if (!minimapSlider) {
                    return;
                }
                // NOTE: THIS IS HACKY.
                //
                // IntersectionObserver.rootMargin is un-affected by the browser's zoom level.
                // The margins of the intersection area needs to be adjusted.
                // Thus, IntersectionObserverEntry.rootBounds may not be what we expect.
                //
                // We address this below.
                //
                // Note that this function was called whenever an intersection event occurred wrt
                // the thresholds.
                //
                if (entry.rootBounds) {
                    // After we create the IntersectionObserver instance with rootMargin set as:
                    // -${MINIMAP_CONTAINER_HEIGHT * this.zoomLevel}px 0px 0px 0px
                    //
                    // we can introspect the rootBounds to infer the zoomlevel.
                    //
                    // we always expect entry.rootBounds.top to equal MINIMAP_CONTAINER_HEIGHT
                    var actualRootTop = Math.ceil(entry.rootBounds.top);
                    if (actualRootTop !== MINIMAP_CONTAINER_HEIGHT && actualRootTop > 0) {
                        // we revert the actualRootTop value by the current zoomLevel factor
                        var normalizedActualTop = actualRootTop / _this.zoomLevel;
                        var zoomLevel = MINIMAP_CONTAINER_HEIGHT / normalizedActualTop;
                        _this.zoomLevel = zoomLevel;
                        // we reconnect the observers; the callback functions may be invoked
                        _this.connectObservers();
                        // NOTE: since we cannot guarantee that the callback function is invoked on
                        //       the newly connected observers, we continue running this function.
                    }
                }
                // root refers to the root intersection rectangle used for the IntersectionObserver
                var rectRelativeToRoot = entry.boundingClientRect;
                var bottomYCoord = rectRelativeToRoot.y + rectRelativeToRoot.height;
                // refers to if the rect is out of view from the viewport
                var isOutOfViewAbove = rectRelativeToRoot.y < 0 && bottomYCoord < 0;
                if (isOutOfViewAbove) {
                    return;
                }
                var relativeToMinimap = {
                    top: rectRelativeToRoot.y - MINIMAP_CONTAINER_HEIGHT,
                    bottom: bottomYCoord - MINIMAP_CONTAINER_HEIGHT,
                };
                var rectBelowMinimap = relativeToMinimap.top > 0 && relativeToMinimap.bottom > 0;
                if (rectBelowMinimap) {
                    // if the first span is below the minimap, we scroll the minimap
                    // to the top. this addresses spurious scrolling to the top of the page
                    if (spanNumber <= 1) {
                        minimapSlider.style.top = '0px';
                        return;
                    }
                    return;
                }
                var inAndAboveMinimap = relativeToMinimap.bottom <= 0;
                if (inAndAboveMinimap) {
                    return;
                }
                // invariant: spanNumber >= 1
                var numberOfMovedSpans = spanNumber - 1;
                var totalHeightOfHiddenSpans = numberOfMovedSpans * MINIMAP_SPAN_BAR_HEIGHT;
                var currentSpanHiddenRatio = 1 - entry.intersectionRatio;
                var panYPixels = totalHeightOfHiddenSpans + currentSpanHiddenRatio * MINIMAP_SPAN_BAR_HEIGHT;
                // invariant: this.props.trace.numOfSpansend - spanNumberToStopMoving + 1 = NUM_OF_SPANS_FIT_IN_MINI_MAP
                var spanNumberToStopMoving = _this.props.trace.numOfSpans + 1 - NUM_OF_SPANS_FIT_IN_MINI_MAP;
                if (spanNumber > spanNumberToStopMoving) {
                    // if the last span bar appears on the minimap, we do not want the minimap
                    // to keep panning upwards
                    minimapSlider.style.top = "-" + spanNumberToStopMoving * MINIMAP_SPAN_BAR_HEIGHT + "px";
                    return;
                }
                minimapSlider.style.top = "-" + panYPixels + "px";
            });
        }, {
            threshold: INTERSECTION_THRESHOLDS,
            rootMargin: "-" + MINIMAP_CONTAINER_HEIGHT * this.zoomLevel + "px 0px 0px 0px",
        });
        this.intersectionObserver.observe(this.spanRowDOMRef.current);
    };
    SpanBar.prototype.disconnectObservers = function () {
        if (this.intersectionObserver) {
            this.intersectionObserver.disconnect();
        }
    };
    SpanBar.prototype.renderCursorGuide = function () {
        return (<CursorGuideHandler.Consumer>
        {function (_a) {
            var showCursorGuide = _a.showCursorGuide, traceViewMouseLeft = _a.traceViewMouseLeft;
            if (!showCursorGuide || !traceViewMouseLeft) {
                return null;
            }
            return (<CursorGuide style={{
                left: toPercent(traceViewMouseLeft),
            }}/>);
        }}
      </CursorGuideHandler.Consumer>);
    };
    SpanBar.prototype.renderDivider = function (dividerHandlerChildrenProps) {
        if (this.state.showDetail) {
            // Mock component to preserve layout spacing
            return (<DividerLine style={{
                position: 'relative',
                backgroundColor: getBackgroundColor({
                    theme: globalTheme,
                    showDetail: true,
                }),
            }}/>);
        }
        var addDividerLineRef = dividerHandlerChildrenProps.addDividerLineRef;
        return (<DividerLine ref={addDividerLineRef()} style={{
            position: 'relative',
        }} onMouseEnter={function () {
            dividerHandlerChildrenProps.setHover(true);
        }} onMouseLeave={function () {
            dividerHandlerChildrenProps.setHover(false);
        }} onMouseOver={function () {
            dividerHandlerChildrenProps.setHover(true);
        }} onMouseDown={dividerHandlerChildrenProps.onDragStart} onClick={function (event) {
            // we prevent the propagation of the clicks from this component to prevent
            // the span detail from being opened.
            event.stopPropagation();
        }}/>);
    };
    SpanBar.prototype.renderWarningText = function (_a) {
        var warningText = (_a === void 0 ? {} : _a).warningText;
        if (!warningText) {
            return null;
        }
        return (<Tooltip containerDisplayMode="flex" title={warningText}>
        <StyledIconWarning size="xs"/>
      </Tooltip>);
    };
    SpanBar.prototype.renderHeader = function (dividerHandlerChildrenProps) {
        var _this = this;
        var _a = this.props, span = _a.span, spanBarColour = _a.spanBarColour, spanBarHatch = _a.spanBarHatch, spanNumber = _a.spanNumber;
        var startTimestamp = span.start_timestamp;
        var endTimestamp = span.timestamp;
        var duration = Math.abs(endTimestamp - startTimestamp);
        var durationString = getHumanDuration(duration);
        var bounds = this.getBounds();
        var dividerPosition = dividerHandlerChildrenProps.dividerPosition, addGhostDividerLineRef = dividerHandlerChildrenProps.addGhostDividerLineRef;
        var displaySpanBar = defined(bounds.left) && defined(bounds.width);
        var durationDisplay = getDurationDisplay(bounds);
        return (<SpanRowCellContainer showDetail={this.state.showDetail}>
        <SpanRowCell data-type="span-row-cell" showDetail={this.state.showDetail} style={{
            width: "calc(" + toPercent(dividerPosition) + " - 0.5px)",
        }} onClick={function () {
            _this.toggleDisplayDetail();
        }}>
          {this.renderTitle()}
        </SpanRowCell>
        {this.renderDivider(dividerHandlerChildrenProps)}
        <SpanRowCell data-type="span-row-cell" showDetail={this.state.showDetail} showStriping={spanNumber % 2 !== 0} style={{
            width: "calc(" + toPercent(1 - dividerPosition) + " - 0.5px)",
        }} onClick={function () {
            _this.toggleDisplayDetail();
        }}>
          {displaySpanBar && (<SpanBarRectangle spanBarHatch={!!spanBarHatch} style={{
            backgroundColor: spanBarColour,
            left: "clamp(0%, " + toPercent(bounds.left || 0) + ", calc(100% - 1px))",
            width: toPercent(bounds.width || 0),
        }}>
              <DurationPill durationDisplay={durationDisplay} showDetail={this.state.showDetail} spanBarHatch={!!spanBarHatch}>
                {durationString}
                {this.renderWarningText({ warningText: bounds.warning })}
              </DurationPill>
            </SpanBarRectangle>)}
          {this.renderMeasurements()}
          {this.renderCursorGuide()}
        </SpanRowCell>
        {!this.state.showDetail && (<DividerLineGhostContainer style={{
            width: "calc(" + toPercent(dividerPosition) + " + 0.5px)",
            display: 'none',
        }}>
            <DividerLine ref={addGhostDividerLineRef()} style={{
            right: 0,
        }} className="hovering" onClick={function (event) {
            // the ghost divider line should not be interactive.
            // we prevent the propagation of the clicks from this component to prevent
            // the span detail from being opened.
            event.stopPropagation();
        }}/>
          </DividerLineGhostContainer>)}
      </SpanRowCellContainer>);
    };
    SpanBar.prototype.render = function () {
        var _this = this;
        var isCurrentSpanFilteredOut = this.props.isCurrentSpanFilteredOut;
        var bounds = this.getBounds();
        var isSpanVisibleInView = bounds.isSpanVisibleInView;
        var isSpanVisible = isSpanVisibleInView && !isCurrentSpanFilteredOut;
        return (<SpanRow ref={this.spanRowDOMRef} visible={isSpanVisible} showBorder={this.state.showDetail} data-test-id="span-row">
        <DividerHandlerManager.Consumer>
          {function (dividerHandlerChildrenProps) { return _this.renderHeader(dividerHandlerChildrenProps); }}
        </DividerHandlerManager.Consumer>
        {this.renderDetail({ isVisible: isSpanVisible })}
      </SpanRow>);
    };
    return SpanBar;
}(React.Component));
export var SpanRowCell = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: relative;\n  height: 100%;\n  overflow: hidden;\n  background-color: ", ";\n  transition: background-color 125ms ease-in-out;\n  color: ", ";\n"], ["\n  position: relative;\n  height: 100%;\n  overflow: hidden;\n  background-color: ", ";\n  transition: background-color 125ms ease-in-out;\n  color: ", ";\n"])), function (p) { return getBackgroundColor(p); }, function (p) { return (p.showDetail ? p.theme.background : 'inherit'); });
export var SpanRowCellContainer = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  position: relative;\n  height: ", "px;\n\n  user-select: none;\n\n  &:hover > div[data-type='span-row-cell'] {\n    background-color: ", ";\n  }\n"], ["\n  display: flex;\n  position: relative;\n  height: ", "px;\n\n  user-select: none;\n\n  &:hover > div[data-type='span-row-cell'] {\n    background-color: ",
    ";\n  }\n"])), SPAN_ROW_HEIGHT, function (p) {
    return p.showDetail ? p.theme.textColor : p.theme.backgroundSecondary;
});
var CursorGuide = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  position: absolute;\n  top: 0;\n  width: 1px;\n  background-color: ", ";\n  transform: translateX(-50%);\n  height: 100%;\n"], ["\n  position: absolute;\n  top: 0;\n  width: 1px;\n  background-color: ", ";\n  transform: translateX(-50%);\n  height: 100%;\n"])), function (p) { return p.theme.red300; });
export var DividerLine = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  background-color: ", ";\n  position: absolute;\n  height: 100%;\n  width: 1px;\n  transition: background-color 125ms ease-in-out;\n  z-index: ", ";\n\n  /* enhanced hit-box */\n  &:after {\n    content: '';\n    z-index: -1;\n    position: absolute;\n    left: -2px;\n    top: 0;\n    width: 5px;\n    height: 100%;\n  }\n\n  &.hovering {\n    background-color: ", ";\n    width: 3px;\n    transform: translateX(-1px);\n    margin-right: -2px;\n\n    cursor: ew-resize;\n\n    &:after {\n      left: -2px;\n      width: 7px;\n    }\n  }\n"], ["\n  background-color: ", ";\n  position: absolute;\n  height: 100%;\n  width: 1px;\n  transition: background-color 125ms ease-in-out;\n  z-index: ", ";\n\n  /* enhanced hit-box */\n  &:after {\n    content: '';\n    z-index: -1;\n    position: absolute;\n    left: -2px;\n    top: 0;\n    width: 5px;\n    height: 100%;\n  }\n\n  &.hovering {\n    background-color: ", ";\n    width: 3px;\n    transform: translateX(-1px);\n    margin-right: -2px;\n\n    cursor: ew-resize;\n\n    &:after {\n      left: -2px;\n      width: 7px;\n    }\n  }\n"])), function (p) { return p.theme.gray200; }, zIndex.dividerLine, function (p) { return p.theme.textColor; });
export var DividerLineGhostContainer = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  position: absolute;\n  width: 100%;\n  height: 100%;\n"], ["\n  position: absolute;\n  width: 100%;\n  height: 100%;\n"])));
export var SpanBarTitleContainer = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  height: 100%;\n  position: absolute;\n  left: 0;\n  top: 0;\n  width: 100%;\n  user-select: none;\n"], ["\n  display: flex;\n  align-items: center;\n  height: 100%;\n  position: absolute;\n  left: 0;\n  top: 0;\n  width: 100%;\n  user-select: none;\n"])));
export var SpanBarTitle = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  position: relative;\n  height: 100%;\n  font-size: ", ";\n  white-space: nowrap;\n  display: flex;\n  flex: 1;\n  align-items: center;\n"], ["\n  position: relative;\n  height: 100%;\n  font-size: ", ";\n  white-space: nowrap;\n  display: flex;\n  flex: 1;\n  align-items: center;\n"])), function (p) { return p.theme.fontSizeSmall; });
export var SpanTreeTogglerContainer = styled('div')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  position: relative;\n  height: ", "px;\n  width: ", ";\n  min-width: ", ";\n  margin-right: ", ";\n  z-index: ", ";\n  display: flex;\n  justify-content: flex-end;\n  align-items: center;\n"], ["\n  position: relative;\n  height: ", "px;\n  width: ", ";\n  min-width: ", ";\n  margin-right: ", ";\n  z-index: ", ";\n  display: flex;\n  justify-content: flex-end;\n  align-items: center;\n"])), SPAN_ROW_HEIGHT, function (p) { return (p.hasToggler ? '40px' : '12px'); }, function (p) { return (p.hasToggler ? '40px' : '12px'); }, function (p) { return (p.hasToggler ? space(0.5) : space(1)); }, zIndex.spanTreeToggler);
export var SpanTreeConnector = styled('div')(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  height: ", "px;\n  width: 100%;\n  border-left: 1px ", " ", ";\n  position: absolute;\n  top: 0;\n\n  &:before {\n    content: '';\n    height: 1px;\n    border-bottom: 1px ", "\n      ", ";\n\n    width: 100%;\n    position: absolute;\n    bottom: ", ";\n  }\n\n  &:after {\n    content: '';\n    background-color: ", ";\n    border-radius: 4px;\n    height: 3px;\n    width: 3px;\n    position: absolute;\n    right: 0;\n    top: ", "px;\n  }\n"], ["\n  height: ", "px;\n  width: 100%;\n  border-left: 1px ", " ", ";\n  position: absolute;\n  top: 0;\n\n  &:before {\n    content: '';\n    height: 1px;\n    border-bottom: 1px ", "\n      ", ";\n\n    width: 100%;\n    position: absolute;\n    bottom: ", ";\n  }\n\n  &:after {\n    content: '';\n    background-color: ", ";\n    border-radius: 4px;\n    height: 3px;\n    width: 3px;\n    position: absolute;\n    right: 0;\n    top: ", "px;\n  }\n"])), function (p) { return (p.isLast ? SPAN_ROW_HEIGHT / 2 : SPAN_ROW_HEIGHT); }, function (p) { return (p.orphanBranch ? 'dashed' : 'solid'); }, function (p) { return p.theme.border; }, function (p) { return (p.orphanBranch ? 'dashed' : 'solid'); }, function (p) { return p.theme.border; }, function (p) { return (p.isLast ? '0' : '50%'); }, function (p) { return p.theme.gray200; }, SPAN_ROW_HEIGHT / 2 - 2);
export var ConnectorBar = styled('div')(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  height: 250%;\n\n  border-left: 1px ", " ", ";\n  top: -5px;\n  position: absolute;\n"], ["\n  height: 250%;\n\n  border-left: 1px ", " ", ";\n  top: -5px;\n  position: absolute;\n"])), function (p) { return (p.orphanBranch ? 'dashed' : 'solid'); }, function (p) { return p.theme.border; });
var getTogglerTheme = function (_a) {
    var isExpanded = _a.isExpanded, theme = _a.theme, disabled = _a.disabled;
    var buttonTheme = isExpanded ? theme.button.default : theme.button.primary;
    if (disabled) {
        return "\n    background: " + buttonTheme.background + ";\n    border: 1px solid " + theme.border + ";\n    color: " + buttonTheme.color + ";\n    cursor: default;\n  ";
    }
    return "\n    background: " + buttonTheme.background + ";\n    border: 1px solid " + theme.border + ";\n    color: " + buttonTheme.color + ";\n  ";
};
export var SpanTreeToggler = styled('div')(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  height: 16px;\n  white-space: nowrap;\n  min-width: 30px;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  border-radius: 99px;\n  transition: all 0.15s ease-in-out;\n  font-size: 10px;\n  line-height: 0;\n  z-index: 1;\n\n  ", "\n"], ["\n  height: 16px;\n  white-space: nowrap;\n  min-width: 30px;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  border-radius: 99px;\n  transition: all 0.15s ease-in-out;\n  font-size: 10px;\n  line-height: 0;\n  z-index: 1;\n\n  ", "\n"])), function (p) { return getTogglerTheme(p); });
var getDurationPillAlignment = function (_a) {
    var durationDisplay = _a.durationDisplay, theme = _a.theme, spanBarHatch = _a.spanBarHatch;
    switch (durationDisplay) {
        case 'left':
            return "right: calc(100% + " + space(0.5) + ");";
        case 'right':
            return "left: calc(100% + " + space(0.75) + ");";
        default:
            return "\n        right: " + space(0.75) + ";\n        color: " + (spanBarHatch === true ? theme.gray300 : theme.white) + ";\n      ";
    }
};
var DurationPill = styled('div')(templateObject_12 || (templateObject_12 = __makeTemplateObject(["\n  position: absolute;\n  top: 50%;\n  display: flex;\n  align-items: center;\n  transform: translateY(-50%);\n  white-space: nowrap;\n  font-size: ", ";\n  color: ", ";\n\n  ", "\n\n  @media (max-width: ", ") {\n    font-size: 10px;\n  }\n"], ["\n  position: absolute;\n  top: 50%;\n  display: flex;\n  align-items: center;\n  transform: translateY(-50%);\n  white-space: nowrap;\n  font-size: ", ";\n  color: ", ";\n\n  ", "\n\n  @media (max-width: ", ") {\n    font-size: 10px;\n  }\n"])), function (p) { return p.theme.fontSizeExtraSmall; }, function (p) { return (p.showDetail === true ? p.theme.gray200 : p.theme.gray300); }, getDurationPillAlignment, function (p) { return p.theme.breakpoints[1]; });
export var SpanBarRectangle = styled('div')(templateObject_13 || (templateObject_13 = __makeTemplateObject(["\n  position: absolute;\n  height: ", "px;\n  top: ", "px;\n  left: 0;\n  min-width: 1px;\n  user-select: none;\n  transition: border-color 0.15s ease-in-out;\n  ", "\n"], ["\n  position: absolute;\n  height: ", "px;\n  top: ", "px;\n  left: 0;\n  min-width: 1px;\n  user-select: none;\n  transition: border-color 0.15s ease-in-out;\n  ", "\n"])), SPAN_ROW_HEIGHT - 2 * SPAN_ROW_PADDING, SPAN_ROW_PADDING, function (p) { return getHatchPattern(p, '#dedae3', '#f4f2f7'); });
var MeasurementMarker = styled('div')(templateObject_14 || (templateObject_14 = __makeTemplateObject(["\n  position: absolute;\n  top: 0;\n  height: ", "px;\n  user-select: none;\n  width: 1px;\n  background: repeating-linear-gradient(\n      to bottom,\n      transparent 0 4px,\n      ", " 4px 8px\n    )\n    80%/2px 100% no-repeat;\n  z-index: ", ";\n  color: ", ";\n"], ["\n  position: absolute;\n  top: 0;\n  height: ", "px;\n  user-select: none;\n  width: 1px;\n  background: repeating-linear-gradient(\n      to bottom,\n      transparent 0 4px,\n      ", " 4px 8px\n    )\n    80%/2px 100% no-repeat;\n  z-index: ", ";\n  color: ", ";\n"])), SPAN_ROW_HEIGHT, function (p) { return (p.failedThreshold ? p.theme.red300 : 'black'); }, zIndex.dividerLine, function (p) { return p.theme.textColor; });
var StyledIconWarning = styled(IconWarning)(templateObject_15 || (templateObject_15 = __makeTemplateObject(["\n  margin-left: ", ";\n  margin-bottom: ", ";\n"], ["\n  margin-left: ", ";\n  margin-bottom: ", ";\n"])), space(0.25), space(0.25));
export var StyledIconChevron = styled(IconChevron)(templateObject_16 || (templateObject_16 = __makeTemplateObject(["\n  width: 7px;\n  margin-left: ", ";\n"], ["\n  width: 7px;\n  margin-left: ", ";\n"])), space(0.25));
export var OperationName = styled('span')(templateObject_17 || (templateObject_17 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return (p.spanErrors.length ? p.theme.error : 'inherit'); });
export default SpanBar;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13, templateObject_14, templateObject_15, templateObject_16, templateObject_17;
//# sourceMappingURL=spanBar.jsx.map