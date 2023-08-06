import { __assign, __makeTemplateObject, __rest } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import Alert from 'app/components/alert';
import { IconInfo, IconClose, IconCheckmark, IconFlag } from 'app/icons';
import space from 'app/styles/space';
var DEFAULT_ICONS = {
    info: <IconInfo size="md"/>,
    error: <IconClose isCircled size="md"/>,
    warning: <IconFlag size="md"/>,
    success: <IconCheckmark isCircled size="md"/>,
};
// Margin bottom should probably be a different prop
var PanelAlert = styled(function (_a) {
    var icon = _a.icon, props = __rest(_a, ["icon"]);
    return (<Alert {...props} icon={icon || DEFAULT_ICONS[props.type]} system/>);
})(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin: 0 0 1px 0;\n  padding: ", ";\n  border-radius: 0;\n  box-shadow: none;\n\n  &:last-child {\n    border-bottom: none;\n    margin: 0;\n    border-radius: 0 0 4px 4px;\n  }\n"], ["\n  margin: 0 0 1px 0;\n  padding: ", ";\n  border-radius: 0;\n  box-shadow: none;\n\n  &:last-child {\n    border-bottom: none;\n    margin: 0;\n    border-radius: 0 0 4px 4px;\n  }\n"])), space(2));
PanelAlert.propTypes = __assign(__assign({}, Alert.propTypes), { type: PropTypes.oneOf(['info', 'warning', 'success', 'error', 'muted']) });
export default PanelAlert;
var templateObject_1;
//# sourceMappingURL=panelAlert.jsx.map