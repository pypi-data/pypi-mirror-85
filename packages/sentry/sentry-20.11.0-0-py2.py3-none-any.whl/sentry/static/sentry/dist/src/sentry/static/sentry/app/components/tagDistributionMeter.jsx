import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import { Link } from 'react-router';
import PropTypes from 'prop-types';
import styled from '@emotion/styled';
import isPropValid from '@emotion/is-prop-valid';
import { t } from 'app/locale';
import space from 'app/styles/space';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import { percent } from 'app/utils';
import Tooltip from 'app/components/tooltip';
import Version from 'app/components/version';
var TagDistributionMeter = /** @class */ (function (_super) {
    __extends(TagDistributionMeter, _super);
    function TagDistributionMeter() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    TagDistributionMeter.prototype.renderTitle = function () {
        var _a = this.props, segments = _a.segments, totalValues = _a.totalValues, title = _a.title, isLoading = _a.isLoading, hasError = _a.hasError, showReleasePackage = _a.showReleasePackage;
        if (!Array.isArray(segments) || segments.length <= 0) {
            return (<Title>
          <TitleType>{title}</TitleType>
        </Title>);
        }
        var largestSegment = segments[0];
        var pct = percent(largestSegment.count, totalValues);
        var pctLabel = Math.floor(pct);
        var renderLabel = function () {
            switch (title) {
                case 'release':
                    return (<Label>
              <Version version={largestSegment.name} anchor={false} tooltipRawVersion withPackage={showReleasePackage} truncate/>
            </Label>);
                default:
                    return <Label>{largestSegment.name || t('n/a')}</Label>;
            }
        };
        return (<Title>
        <TitleType>{title}</TitleType>
        <TitleDescription>
          {renderLabel()}
          {isLoading || hasError ? null : <Percent>{pctLabel}%</Percent>}
        </TitleDescription>
      </Title>);
    };
    TagDistributionMeter.prototype.renderSegments = function () {
        var _a = this.props, segments = _a.segments, onTagClick = _a.onTagClick, title = _a.title, isLoading = _a.isLoading, hasError = _a.hasError, totalValues = _a.totalValues, renderLoading = _a.renderLoading, renderError = _a.renderError, renderEmpty = _a.renderEmpty, showReleasePackage = _a.showReleasePackage;
        if (isLoading) {
            return renderLoading();
        }
        if (hasError) {
            return <SegmentBar>{renderError()}</SegmentBar>;
        }
        if (totalValues === 0) {
            return <SegmentBar>{renderEmpty()}</SegmentBar>;
        }
        return (<SegmentBar>
        {segments.map(function (value, index) {
            var pct = percent(value.count, totalValues);
            var pctLabel = Math.floor(pct);
            var renderTooltipValue = function () {
                switch (title) {
                    case 'release':
                        return (<Version version={value.name} anchor={false} withPackage={showReleasePackage}/>);
                    default:
                        return value.name || t('n/a');
                }
            };
            var tooltipHtml = (<React.Fragment>
              <div className="truncate">{renderTooltipValue()}</div>
              {pctLabel}%
            </React.Fragment>);
            var segmentProps = {
                index: index,
                to: value.url,
                onClick: function () {
                    if (onTagClick) {
                        onTagClick(title, value);
                    }
                },
            };
            return (<div key={value.value} style={{ width: pct + '%' }}>
              <Tooltip title={tooltipHtml} containerDisplayMode="block">
                {value.isOther ? <OtherSegment /> : <Segment {...segmentProps}/>}
              </Tooltip>
            </div>);
        })}
      </SegmentBar>);
    };
    TagDistributionMeter.prototype.render = function () {
        var _a = this.props, segments = _a.segments, totalValues = _a.totalValues;
        var totalVisible = segments.reduce(function (sum, value) { return sum + value.count; }, 0);
        var hasOther = totalVisible < totalValues;
        if (hasOther) {
            segments.push({
                isOther: true,
                name: t('Other'),
                value: 'other',
                count: totalValues - totalVisible,
                url: '',
            });
        }
        return (<TagSummary>
        {this.renderTitle()}
        {this.renderSegments()}
      </TagSummary>);
    };
    TagDistributionMeter.propTypes = {
        title: PropTypes.string.isRequired,
        totalValues: PropTypes.number,
        isLoading: PropTypes.bool,
        hasError: PropTypes.bool,
        segments: PropTypes.arrayOf(PropTypes.shape({
            count: PropTypes.number.isRequired,
            name: PropTypes.oneOfType([PropTypes.string, PropTypes.number, PropTypes.array]),
            value: PropTypes.oneOfType([PropTypes.string, PropTypes.number, PropTypes.array]),
            url: PropTypes.oneOfType([PropTypes.string, PropTypes.object]).isRequired,
        })).isRequired,
        renderEmpty: PropTypes.func,
        renderLoading: PropTypes.func,
        renderError: PropTypes.func,
        onTagClick: PropTypes.func,
    };
    TagDistributionMeter.defaultProps = {
        isLoading: false,
        hasError: false,
        renderLoading: function () { return null; },
        renderEmpty: function () { return <p>{t('No recent data.')}</p>; },
        renderError: function () { return null; },
        showReleasePackage: false,
    };
    return TagDistributionMeter;
}(React.Component));
export default TagDistributionMeter;
var COLORS = [
    '#3A3387',
    '#5F40A3',
    '#8C4FBD',
    '#B961D3',
    '#DE76E4',
    '#EF91E8',
    '#F7B2EC',
    '#FCD8F4',
    '#FEEBF9',
];
var TagSummary = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(1));
var SegmentBar = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  overflow: hidden;\n  border-radius: 2px;\n"], ["\n  display: flex;\n  overflow: hidden;\n  border-radius: 2px;\n"])));
var Title = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  font-size: ", ";\n  justify-content: space-between;\n"], ["\n  display: flex;\n  font-size: ", ";\n  justify-content: space-between;\n"])), function (p) { return p.theme.fontSizeSmall; });
var TitleType = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  color: ", ";\n  font-weight: bold;\n  ", ";\n"], ["\n  color: ", ";\n  font-weight: bold;\n  ", ";\n"])), function (p) { return p.theme.textColor; }, overflowEllipsis);
var TitleDescription = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: flex;\n  color: ", ";\n  text-align: right;\n"], ["\n  display: flex;\n  color: ", ";\n  text-align: right;\n"])), function (p) { return p.theme.gray300; });
var Label = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  ", ";\n  max-width: 150px;\n"], ["\n  ", ";\n  max-width: 150px;\n"])), overflowEllipsis);
var Percent = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  font-weight: bold;\n  padding-left: ", ";\n  color: ", ";\n"], ["\n  font-weight: bold;\n  padding-left: ", ";\n  color: ", ";\n"])), space(0.5), function (p) { return p.theme.textColor; });
var OtherSegment = styled('span')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  display: block;\n  width: 100%;\n  height: 16px;\n  color: inherit;\n  outline: none;\n  background-color: ", ";\n"], ["\n  display: block;\n  width: 100%;\n  height: 16px;\n  color: inherit;\n  outline: none;\n  background-color: ", ";\n"])), COLORS[COLORS.length - 1]);
var Segment = styled(Link, { shouldForwardProp: isPropValid })(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  display: block;\n  width: 100%;\n  height: 16px;\n  color: inherit;\n  outline: none;\n  background-color: ", ";\n"], ["\n  display: block;\n  width: 100%;\n  height: 16px;\n  color: inherit;\n  outline: none;\n  background-color: ", ";\n"])), function (p) { return COLORS[p.index]; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9;
//# sourceMappingURL=tagDistributionMeter.jsx.map