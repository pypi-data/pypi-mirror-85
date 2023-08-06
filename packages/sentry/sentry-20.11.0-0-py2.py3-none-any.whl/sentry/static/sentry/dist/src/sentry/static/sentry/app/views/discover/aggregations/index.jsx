import { __extends, __read, __spread } from "tslib";
import React from 'react';
import { t } from 'app/locale';
import { IconClose } from 'app/icons/iconClose';
import Link from 'app/components/links/link';
import AggregationRow from './aggregation';
import { PlaceholderText, SelectListItem, AddText, SidebarLabel } from '../styles';
var Aggregations = /** @class */ (function (_super) {
    __extends(Aggregations, _super);
    function Aggregations() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Aggregations.prototype.addRow = function () {
        var aggregations = __spread(this.props.value, [[null, null, null]]);
        this.props.onChange(aggregations);
    };
    Aggregations.prototype.removeRow = function (idx) {
        var aggregations = this.props.value.slice();
        aggregations.splice(idx, 1);
        this.props.onChange(aggregations);
    };
    Aggregations.prototype.handleChange = function (val, idx) {
        var aggregations = this.props.value.slice();
        aggregations[idx] = val;
        this.props.onChange(aggregations);
    };
    Aggregations.prototype.render = function () {
        var _this = this;
        var _a = this.props, value = _a.value, columns = _a.columns, disabled = _a.disabled;
        return (<div>
        <div>
          <SidebarLabel>{t('Aggregation')}</SidebarLabel>
          {!disabled && (<AddText>
              (
              <Link to="" data-test-id="aggregation-add-text-link" onClick={function () { return _this.addRow(); }}>
                {t('Add')}
              </Link>
              )
            </AddText>)}
        </div>
        {!value.length && (<PlaceholderText>{t('None, showing raw event data')}</PlaceholderText>)}
        {value.map(function (aggregation, idx) { return (<SelectListItem key={idx + "_" + aggregation[2]}>
            <AggregationRow value={aggregation} onChange={function (val) { return _this.handleChange(val, idx); }} columns={columns} disabled={disabled}/>
            <div>
              <Link to="" onClick={function () { return _this.removeRow(idx); }}>
                <IconClose isCircled/>
              </Link>
            </div>
          </SelectListItem>); })}
      </div>);
    };
    return Aggregations;
}(React.Component));
export default Aggregations;
//# sourceMappingURL=index.jsx.map