import { __extends, __read, __spread } from "tslib";
import React from 'react';
import { t } from 'app/locale';
import { IconClose } from 'app/icons/iconClose';
import Link from 'app/components/links/link';
import ConditionRow from './condition';
import { PlaceholderText, SelectListItem, AddText, SidebarLabel } from '../styles';
var Conditions = /** @class */ (function (_super) {
    __extends(Conditions, _super);
    function Conditions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Conditions.prototype.addRow = function () {
        this.props.onChange(__spread(this.props.value, [[null, null, null]]));
    };
    Conditions.prototype.removeRow = function (idx) {
        var conditions = this.props.value.slice();
        conditions.splice(idx, 1);
        this.props.onChange(conditions);
    };
    Conditions.prototype.handleChange = function (val, idx) {
        var conditions = this.props.value.slice();
        conditions[idx] = val;
        this.props.onChange(conditions);
    };
    Conditions.prototype.render = function () {
        var _this = this;
        var _a = this.props, value = _a.value, columns = _a.columns, disabled = _a.disabled;
        return (<div>
        <div>
          <SidebarLabel>{t('Conditions')}</SidebarLabel>
          {!disabled && (<AddText>
              (
              <Link to="" data-test-id="conditions-add-text-link" onClick={function () { return _this.addRow(); }}>
                {t('Add')}
              </Link>
              )
            </AddText>)}
        </div>
        {!value.length && (<PlaceholderText>{t('None, showing all events')}</PlaceholderText>)}
        {value.map(function (condition, idx) { return (<SelectListItem key={idx + "_" + condition[2]}>
            <ConditionRow value={condition} onChange={function (val) { return _this.handleChange(val, idx); }} columns={columns} disabled={disabled}/>
            <div>
              <a onClick={function () { return _this.removeRow(idx); }}>
                <IconClose isCircled/>
              </a>
            </div>
          </SelectListItem>); })}
      </div>);
    };
    return Conditions;
}(React.Component));
export default Conditions;
//# sourceMappingURL=index.jsx.map