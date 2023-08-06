import React from 'react';
import { IconCheckmark, IconSubtract } from 'app/icons';
var CheckboxFancyContent = function (_a) {
    var isChecked = _a.isChecked, isIndeterminate = _a.isIndeterminate;
    if (isIndeterminate) {
        return <IconSubtract size="70%" color="white"/>;
    }
    if (isChecked) {
        return <IconCheckmark size="70%" color="white"/>;
    }
    return null;
};
export default CheckboxFancyContent;
//# sourceMappingURL=checkboxFancyContent.jsx.map