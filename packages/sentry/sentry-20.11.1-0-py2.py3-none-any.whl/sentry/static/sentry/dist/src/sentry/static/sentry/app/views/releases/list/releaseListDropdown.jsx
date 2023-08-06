import React from 'react';
import DropdownControl, { DropdownItem } from 'app/components/dropdownControl';
var ReleaseListDropdown = function (_a) {
    var _b;
    var label = _a.label, options = _a.options, selected = _a.selected, onSelect = _a.onSelect;
    var selectedOption = (_b = options.find(function (option) { return option.key === selected; })) === null || _b === void 0 ? void 0 : _b.label;
    return (<DropdownControl buttonProps={{ prefix: label }} label={selectedOption}>
      {options.map(function (option) { return (<DropdownItem key={option.key} onSelect={onSelect} eventKey={option.key} isActive={selected === option.key}>
          {option.label}
        </DropdownItem>); })}
    </DropdownControl>);
};
export default ReleaseListDropdown;
//# sourceMappingURL=releaseListDropdown.jsx.map