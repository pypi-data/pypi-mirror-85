import { __extends } from "tslib";
import React from 'react';
import DropdownLink from 'app/components/dropdownLink';
import MenuItem from 'app/components/menuItem';
import { IconDownload } from 'app/icons';
import { t } from 'app/locale';
import { ResultViewActions, ResultViewButtons, ResultViewDropdownButtons, DownloadCsvButton, } from '../styles';
var VisualizationsToggle = /** @class */ (function (_super) {
    __extends(VisualizationsToggle, _super);
    function VisualizationsToggle() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.getMenuItem = function (opt) { return (<MenuItem key={opt.id} onSelect={_this.props.handleChange} eventKey={opt.id} isActive={opt.id === _this.props.visualization}>
      {opt.name}
    </MenuItem>); };
        _this.getButtonItems = function (opt) {
            var active = opt.id === _this.props.visualization;
            return (<li key={opt.id} className={active ? 'active' : undefined}>
        <a onClick={function () { return _this.props.handleChange(opt.id); }}>{opt.name}</a>
      </li>);
        };
        _this.getDownloadCsvButton = function () {
            var handleCsvDownload = _this.props.handleCsvDownload;
            return (<DownloadCsvButton onClick={handleCsvDownload} icon={<IconDownload size="xs"/>} size="xsmall">
        {t('Export CSV')}
      </DownloadCsvButton>);
        };
        return _this;
    }
    VisualizationsToggle.prototype.render = function () {
        var _this = this;
        var _a = this.props, options = _a.options, visualization = _a.visualization;
        var name = options.find(function (opt) { return opt.id === visualization; }).name;
        var dropdownTitle = t("View: " + name);
        return (<ResultViewActions>
        <ResultViewButtons>
          {options.map(function (opt) { return _this.getButtonItems(opt); })}
        </ResultViewButtons>
        <ResultViewDropdownButtons>
          <DropdownLink title={dropdownTitle} className="btn btn-default btn-sm">
            {options.map(function (opt) { return _this.getMenuItem(opt); })}
          </DropdownLink>
        </ResultViewDropdownButtons>
        {this.getDownloadCsvButton()}
      </ResultViewActions>);
    };
    return VisualizationsToggle;
}(React.Component));
export default VisualizationsToggle;
//# sourceMappingURL=visualizationsToggle.jsx.map