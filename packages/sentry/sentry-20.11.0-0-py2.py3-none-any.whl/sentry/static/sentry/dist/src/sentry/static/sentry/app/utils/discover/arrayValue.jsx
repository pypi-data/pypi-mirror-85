import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
import { t } from 'app/locale';
var ArrayValue = /** @class */ (function (_super) {
    __extends(ArrayValue, _super);
    function ArrayValue() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            expanded: false,
        };
        _this.handleToggle = function () {
            _this.setState(function (prevState) { return ({
                expanded: !prevState.expanded,
            }); });
        };
        return _this;
    }
    ArrayValue.prototype.render = function () {
        var expanded = this.state.expanded;
        var value = this.props.value;
        return (<ArrayContainer>
        {expanded &&
            value
                .slice(0, value.length - 1)
                .map(function (item, i) { return <ArrayItem key={i + ":" + item}>{item}</ArrayItem>; })}
        <span>
          {value.slice(-1)[0]}
          {value.length > 1 ? (<button onClick={this.handleToggle}>
              {expanded ? t('[collapse]') : t('[+%s more]', value.length - 1)}
            </button>) : null}
        </span>
      </ArrayContainer>);
    };
    return ArrayValue;
}(React.Component));
var ArrayContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  ", ";\n\n  & button {\n    background: none;\n    border: 0;\n    outline: none;\n    padding: 0;\n    cursor: pointer;\n    color: ", ";\n    margin-left: ", ";\n  }\n"], ["\n  ", ";\n\n  & button {\n    background: none;\n    border: 0;\n    outline: none;\n    padding: 0;\n    cursor: pointer;\n    color: ", ";\n    margin-left: ", ";\n  }\n"])), overflowEllipsis, function (p) { return p.theme.blue300; }, space(0.5));
var ArrayItem = styled('span')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: block;\n  ", ";\n"], ["\n  display: block;\n  ", ";\n"])), overflowEllipsis);
export default ArrayValue;
var templateObject_1, templateObject_2;
//# sourceMappingURL=arrayValue.jsx.map