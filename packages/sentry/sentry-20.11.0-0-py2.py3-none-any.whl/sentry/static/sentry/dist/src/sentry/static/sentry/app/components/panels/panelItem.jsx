import { __makeTemplateObject } from "tslib";
// eslint-disable-next-line no-restricted-imports
import { Flex } from 'reflexbox';
import PropTypes from 'prop-types';
import styled from '@emotion/styled';
var PanelItem = styled(Flex)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  border-bottom: 1px solid ", ";\n\n  &:last-child {\n    border: 0;\n  }\n"], ["\n  border-bottom: 1px solid ", ";\n\n  &:last-child {\n    border: 0;\n  }\n"])), function (p) { return p.theme.innerBorder; });
PanelItem.propTypes = {
    p: PropTypes.number,
};
PanelItem.defaultProps = {
    p: 2,
};
export default PanelItem;
var templateObject_1;
//# sourceMappingURL=panelItem.jsx.map