import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import SelectControl from 'app/components/forms/selectControl';
import space from 'app/styles/space';
import { SidebarLabel } from '../styles';
var Orderby = /** @class */ (function (_super) {
    __extends(Orderby, _super);
    function Orderby() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Orderby.prototype.updateField = function (field) {
        var orderby = this.getInternal(this.props.value);
        orderby.field = field;
        this.props.onChange(this.getExternal(orderby));
    };
    Orderby.prototype.updateDirection = function (direction) {
        var orderby = this.getInternal(this.props.value);
        orderby.direction = direction;
        this.props.onChange(this.getExternal(orderby));
    };
    /**
     * @param value Object containing orderby information
     */
    Orderby.prototype.getExternal = function (value) {
        return "" + (value.direction === 'desc' ? '-' : '') + value.field;
    };
    /**
     * @param value String containing orderby information
     */
    Orderby.prototype.getInternal = function (value) {
        var direction = value.startsWith('-') ? 'desc' : 'asc';
        var field = value.replace(/^-/, '');
        return {
            direction: direction,
            field: field,
        };
    };
    Orderby.prototype.render = function () {
        var _this = this;
        var _a = this.props, disabled = _a.disabled, columns = _a.columns, value = _a.value;
        var _b = this.getInternal(value), direction = _b.direction, field = _b.field;
        return (<React.Fragment>
        <SidebarLabel className="control-label">{t('Order by')}</SidebarLabel>
        <Container>
          <OrderbyField>
            <SelectControl deprecatedSelectControl name="orderbyField" options={columns} value={field} onChange={function (val) { return _this.updateField(val.value); }} disabled={disabled}/>
          </OrderbyField>
          <OrderbyValue>
            <SelectControl deprecatedSelectControl name="orderbyDirection" options={[
            { value: 'asc', label: 'asc' },
            { value: 'desc', label: 'desc' },
        ]} value={direction} onChange={function (val) { return _this.updateDirection(val.value); }} disabled={disabled}/>
          </OrderbyValue>
        </Container>
      </React.Fragment>);
    };
    return Orderby;
}(React.Component));
export default Orderby;
var Container = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
var OrderbyField = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  width: calc(100% / 3 * 2);\n  padding-right: ", ";\n"], ["\n  width: calc(100% / 3 * 2);\n  padding-right: ", ";\n"])), space(1));
var OrderbyValue = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  width: calc(100% / 3);\n"], ["\n  width: calc(100% / 3);\n"])));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=orderby.jsx.map