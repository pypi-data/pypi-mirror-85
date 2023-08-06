import { __extends, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import theme from 'app/utils/theme';
import { t } from 'app/locale';
import space from 'app/styles/space';
import getDynamicText from 'app/utils/getDynamicText';
import DateTime from 'app/components/dateTime';
import Pill from 'app/components/pill';
import Pills from 'app/components/pills';
import { SpanDetailContainer } from 'app/components/events/interfaces/spans/spanDetail';
import { rawSpanKeys } from 'app/components/events/interfaces/spans/types';
import { getHumanDuration } from 'app/components/events/interfaces/spans/utils';
import { generateCSSWidth, getSpanDuration, } from './utils';
import { SpanBarRectangle } from './styles';
import SpanDetailContent from './spanDetailContent';
var getDurationDisplay = function (width) {
    if (!width) {
        return 'right';
    }
    switch (width.type) {
        case 'WIDTH_PIXEL': {
            return 'right';
        }
        case 'WIDTH_PERCENTAGE': {
            var spaceNeeded = 0.3;
            if (width.width < 1 - spaceNeeded) {
                return 'right';
            }
            return 'inset';
        }
        default: {
            var _exhaustiveCheck = width;
            return _exhaustiveCheck;
        }
    }
};
var SpanDetail = /** @class */ (function (_super) {
    __extends(SpanDetail, _super);
    function SpanDetail() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    SpanDetail.prototype.renderContent = function () {
        var _a = this.props, span = _a.span, bounds = _a.bounds;
        switch (span.comparisonResult) {
            case 'matched': {
                return (<MatchedSpanDetailsContent baselineSpan={span.baselineSpan} regressionSpan={span.regressionSpan} bounds={bounds}/>);
            }
            case 'regression': {
                return <SpanDetailContent span={span.regressionSpan}/>;
            }
            case 'baseline': {
                return <SpanDetailContent span={span.baselineSpan}/>;
            }
            default: {
                var _exhaustiveCheck = span;
                return _exhaustiveCheck;
            }
        }
    };
    SpanDetail.prototype.render = function () {
        return (<SpanDetailContainer onClick={function (event) {
            // prevent toggling the span detail
            event.stopPropagation();
        }}>
        {this.renderContent()}
      </SpanDetailContainer>);
    };
    return SpanDetail;
}(React.Component));
var MatchedSpanDetailsContent = function (props) {
    var _a, _b;
    var baselineSpan = props.baselineSpan, regressionSpan = props.regressionSpan, bounds = props.bounds;
    var dataKeys = new Set(__spread(Object.keys((_a = baselineSpan === null || baselineSpan === void 0 ? void 0 : baselineSpan.data) !== null && _a !== void 0 ? _a : {}), Object.keys((_b = regressionSpan === null || regressionSpan === void 0 ? void 0 : regressionSpan.data) !== null && _b !== void 0 ? _b : {})));
    var unknownKeys = new Set(__spread(Object.keys(baselineSpan).filter(function (key) {
        return !rawSpanKeys.has(key);
    }), Object.keys(regressionSpan).filter(function (key) {
        return !rawSpanKeys.has(key);
    })));
    return (<div>
      <SpanBars bounds={bounds} baselineSpan={baselineSpan} regressionSpan={regressionSpan}/>
      <Row baselineTitle={t('Baseline Span ID')} regressionTitle={t("This Event's Span ID")} renderBaselineContent={function () { return baselineSpan.span_id; }} renderRegressionContent={function () { return regressionSpan.span_id; }}/>
      <Row title={t('Parent Span ID')} renderBaselineContent={function () { return baselineSpan.parent_span_id || ''; }} renderRegressionContent={function () { return regressionSpan.parent_span_id || ''; }}/>
      <Row title={t('Trace ID')} renderBaselineContent={function () { return baselineSpan.trace_id; }} renderRegressionContent={function () { return regressionSpan.trace_id; }}/>
      <Row title={t('Description')} renderBaselineContent={function () { var _a; return (_a = baselineSpan.description) !== null && _a !== void 0 ? _a : ''; }} renderRegressionContent={function () { var _a; return (_a = regressionSpan.description) !== null && _a !== void 0 ? _a : ''; }}/>
      <Row title={t('Start Date')} renderBaselineContent={function () {
        return getDynamicText({
            fixed: 'Mar 16, 2020 9:10:12 AM UTC',
            value: (<React.Fragment>
                <DateTime date={baselineSpan.start_timestamp * 1000}/>
                {" (" + baselineSpan.start_timestamp + ")"}
              </React.Fragment>),
        });
    }} renderRegressionContent={function () {
        return getDynamicText({
            fixed: 'Mar 16, 2020 9:10:12 AM UTC',
            value: (<React.Fragment>
                <DateTime date={regressionSpan.start_timestamp * 1000}/>
                {" (" + baselineSpan.start_timestamp + ")"}
              </React.Fragment>),
        });
    }}/>
      <Row title={t('End Date')} renderBaselineContent={function () {
        return getDynamicText({
            fixed: 'Mar 16, 2020 9:10:12 AM UTC',
            value: (<React.Fragment>
                <DateTime date={baselineSpan.timestamp * 1000}/>
                {" (" + baselineSpan.timestamp + ")"}
              </React.Fragment>),
        });
    }} renderRegressionContent={function () {
        return getDynamicText({
            fixed: 'Mar 16, 2020 9:10:12 AM UTC',
            value: (<React.Fragment>
                <DateTime date={regressionSpan.timestamp * 1000}/>
                {" (" + regressionSpan.timestamp + ")"}
              </React.Fragment>),
        });
    }}/>
      <Row title={t('Duration')} renderBaselineContent={function () {
        var startTimestamp = baselineSpan.start_timestamp;
        var endTimestamp = baselineSpan.timestamp;
        var duration = (endTimestamp - startTimestamp) * 1000;
        return duration.toFixed(3) + "ms";
    }} renderRegressionContent={function () {
        var startTimestamp = regressionSpan.start_timestamp;
        var endTimestamp = regressionSpan.timestamp;
        var duration = (endTimestamp - startTimestamp) * 1000;
        return duration.toFixed(3) + "ms";
    }}/>
      <Row title={t('Operation')} renderBaselineContent={function () { return baselineSpan.op || ''; }} renderRegressionContent={function () { return regressionSpan.op || ''; }}/>
      <Row title={t('Same Process as Parent')} renderBaselineContent={function () { return String(!!baselineSpan.same_process_as_parent); }} renderRegressionContent={function () { return String(!!regressionSpan.same_process_as_parent); }}/>
      <Tags baselineSpan={baselineSpan} regressionSpan={regressionSpan}/>
      {Array.from(dataKeys).map(function (dataTitle) { return (<Row key={dataTitle} title={dataTitle} renderBaselineContent={function () {
        var _a;
        var data = (_a = baselineSpan === null || baselineSpan === void 0 ? void 0 : baselineSpan.data) !== null && _a !== void 0 ? _a : {};
        var value = data[dataTitle];
        return JSON.stringify(value, null, 4) || '';
    }} renderRegressionContent={function () {
        var _a;
        var data = (_a = regressionSpan === null || regressionSpan === void 0 ? void 0 : regressionSpan.data) !== null && _a !== void 0 ? _a : {};
        var value = data[dataTitle];
        return JSON.stringify(value, null, 4) || '';
    }}/>); })}
      {Array.from(unknownKeys).map(function (key) { return (<Row key={key} title={key} renderBaselineContent={function () {
        return JSON.stringify(baselineSpan[key], null, 4) || '';
    }} renderRegressionContent={function () {
        return JSON.stringify(regressionSpan[key], null, 4) || '';
    }}/>); })}
    </div>);
};
var RowSplitter = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: row;\n\n  > * + * {\n    border-left: 1px solid ", ";\n  }\n"], ["\n  display: flex;\n  flex-direction: row;\n\n  > * + * {\n    border-left: 1px solid ", ";\n  }\n"])), function (p) { return p.theme.border; });
var SpanBarContainer = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  position: relative;\n  height: 16px;\n  margin-top: ", ";\n  margin-bottom: ", ";\n"], ["\n  position: relative;\n  height: 16px;\n  margin-top: ", ";\n  margin-bottom: ", ";\n"])), space(3), space(2));
var SpanBars = function (props) {
    var bounds = props.bounds, baselineSpan = props.baselineSpan, regressionSpan = props.regressionSpan;
    var baselineDurationDisplay = getDurationDisplay(bounds.baseline);
    var regressionDurationDisplay = getDurationDisplay(bounds.regression);
    return (<RowSplitter>
      <RowContainer>
        <SpanBarContainer>
          <SpanBarRectangle style={{
        backgroundColor: theme.gray500,
        width: generateCSSWidth(bounds.baseline),
        position: 'absolute',
        height: '16px',
    }}>
            <DurationPill durationDisplay={baselineDurationDisplay} fontColors={{ right: theme.gray500, inset: theme.white }}>
              {getHumanDuration(getSpanDuration(baselineSpan))}
            </DurationPill>
          </SpanBarRectangle>
        </SpanBarContainer>
      </RowContainer>
      <RowContainer>
        <SpanBarContainer>
          <SpanBarRectangle style={{
        backgroundColor: theme.purple200,
        width: generateCSSWidth(bounds.regression),
        position: 'absolute',
        height: '16px',
    }}>
            <DurationPill durationDisplay={regressionDurationDisplay} fontColors={{ right: theme.gray500, inset: theme.gray500 }}>
              {getHumanDuration(getSpanDuration(regressionSpan))}
            </DurationPill>
          </SpanBarRectangle>
        </SpanBarContainer>
      </RowContainer>
    </RowSplitter>);
};
var Row = function (props) {
    var _a, _b;
    var title = props.title, baselineTitle = props.baselineTitle, regressionTitle = props.regressionTitle;
    var baselineContent = props.renderBaselineContent();
    var regressionContent = props.renderRegressionContent();
    if (!baselineContent && !regressionContent) {
        return null;
    }
    return (<RowSplitter>
      <RowCell title={(_a = baselineTitle !== null && baselineTitle !== void 0 ? baselineTitle : title) !== null && _a !== void 0 ? _a : ''}>{baselineContent}</RowCell>
      <RowCell title={(_b = regressionTitle !== null && regressionTitle !== void 0 ? regressionTitle : title) !== null && _b !== void 0 ? _b : ''}>{regressionContent}</RowCell>
    </RowSplitter>);
};
var RowContainer = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  width: 50%;\n  min-width: 50%;\n  max-width: 50%;\n  flex-basis: 50%;\n\n  padding-left: ", ";\n  padding-right: ", ";\n"], ["\n  width: 50%;\n  min-width: 50%;\n  max-width: 50%;\n  flex-basis: 50%;\n\n  padding-left: ", ";\n  padding-right: ", ";\n"])), space(2), space(2));
var RowTitle = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  font-size: 13px;\n  font-weight: 600;\n"], ["\n  font-size: 13px;\n  font-weight: 600;\n"])));
var RowCell = function (_a) {
    var title = _a.title, children = _a.children;
    return (<RowContainer>
      <RowTitle>{title}</RowTitle>
      <div>
        <pre className="val" style={{ marginBottom: space(1) }}>
          <span className="val-string">{children}</span>
        </pre>
      </div>
    </RowContainer>);
};
var getTags = function (span) {
    var tags = span === null || span === void 0 ? void 0 : span.tags;
    if (!tags) {
        return undefined;
    }
    var keys = Object.keys(tags);
    if (keys.length <= 0) {
        return undefined;
    }
    return tags;
};
var TagPills = function (_a) {
    var tags = _a.tags;
    if (!tags) {
        return null;
    }
    var keys = Object.keys(tags);
    if (keys.length <= 0) {
        return null;
    }
    return (<Pills>
      {keys.map(function (key, index) { return (<Pill key={index} name={key} value={String(tags[key]) || ''}/>); })}
    </Pills>);
};
var Tags = function (_a) {
    var baselineSpan = _a.baselineSpan, regressionSpan = _a.regressionSpan;
    var baselineTags = getTags(baselineSpan);
    var regressionTags = getTags(regressionSpan);
    if (!baselineTags && !regressionTags) {
        return null;
    }
    return (<RowSplitter>
      <RowContainer>
        <RowTitle>{t('Tags')}</RowTitle>
        <div>
          <TagPills tags={baselineTags}/>
        </div>
      </RowContainer>
      <RowContainer>
        <RowTitle>{t('Tags')}</RowTitle>
        <div>
          <TagPills tags={regressionTags}/>
        </div>
      </RowContainer>
    </RowSplitter>);
};
var DurationPill = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  position: absolute;\n  top: 50%;\n  display: flex;\n  align-items: center;\n  transform: translateY(-50%);\n  white-space: nowrap;\n  font-size: ", ";\n  color: ", ";\n\n  ", ";\n\n  @media (max-width: ", ") {\n    font-size: 10px;\n  }\n"], ["\n  position: absolute;\n  top: 50%;\n  display: flex;\n  align-items: center;\n  transform: translateY(-50%);\n  white-space: nowrap;\n  font-size: ", ";\n  color: ", ";\n\n  ",
    ";\n\n  @media (max-width: ", ") {\n    font-size: 10px;\n  }\n"])), function (p) { return p.theme.fontSizeExtraSmall; }, function (p) { return p.fontColors.right; }, function (p) {
    switch (p.durationDisplay) {
        case 'right':
            return "left: calc(100% + " + space(0.75) + ");";
        default:
            return "\n          right: " + space(0.75) + ";\n          color: " + p.fontColors.inset + ";\n        ";
    }
}, function (p) { return p.theme.breakpoints[1]; });
export default SpanDetail;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=spanDetail.jsx.map