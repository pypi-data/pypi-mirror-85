import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Tooltip from 'app/components/tooltip';
import AnnotatedText from 'app/components/events/meta/annotatedText';
import { IconSliders } from 'app/icons';
import { t } from 'app/locale';
var REGISTER_VIEWS = [t('Hexadecimal'), t('Numeric')];
var frameRegistersValue = /** @class */ (function (_super) {
    __extends(frameRegistersValue, _super);
    function frameRegistersValue() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            view: 0,
        };
        _this.toggleView = function () {
            _this.setState(function (state) { return ({ view: (state.view + 1) % REGISTER_VIEWS.length }); });
        };
        _this.tooltipTitle = function () { return REGISTER_VIEWS[_this.state.view]; };
        _this.formatValue = function () {
            var value = _this.props.value;
            try {
                var parsed = typeof value === 'string' ? parseInt(value, 16) : value;
                if (isNaN(parsed)) {
                    return value;
                }
                switch (_this.state.view) {
                    case 1:
                        return "" + parsed;
                    case 0:
                    default:
                        return "0x" + ('0000000000000000' + parsed.toString(16)).substr(-16);
                }
            }
            catch (_a) {
                return value;
            }
        };
        return _this;
    }
    frameRegistersValue.prototype.render = function () {
        var formattedValue = this.formatValue();
        var meta = this.props.meta;
        return (<InlinePre data-test-id="frame-registers-value">
        <FixedWidth>
          <AnnotatedText value={formattedValue} meta={meta}/>
        </FixedWidth>
        <Tooltip title={this.tooltipTitle()}>
          <Toggle onClick={this.toggleView} size="xs"/>
        </Tooltip>
      </InlinePre>);
    };
    return frameRegistersValue;
}(React.Component));
export default frameRegistersValue;
var InlinePre = styled('pre')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: inline;\n"], ["\n  display: inline;\n"])));
var FixedWidth = styled('span')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  width: 11em;\n  display: inline-block;\n  text-align: right;\n  margin-right: 1ex;\n"], ["\n  width: 11em;\n  display: inline-block;\n  text-align: right;\n  margin-right: 1ex;\n"])));
var Toggle = styled(IconSliders)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  opacity: 0.33;\n  cursor: pointer;\n\n  &:hover {\n    opacity: 1;\n  }\n"], ["\n  opacity: 0.33;\n  cursor: pointer;\n\n  &:hover {\n    opacity: 1;\n  }\n"])));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=frameRegistersValue.jsx.map