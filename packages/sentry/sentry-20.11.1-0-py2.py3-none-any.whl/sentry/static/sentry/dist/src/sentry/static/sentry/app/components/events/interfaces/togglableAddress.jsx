import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Tooltip from 'app/components/tooltip';
import space from 'app/styles/space';
import { t } from 'app/locale';
import { IconFilter } from 'app/icons';
import { formatAddress, parseAddress } from 'app/components/events/interfaces/utils';
import overflowEllipsis from 'app/styles/overflowEllipsis';
var TogglableAddress = function (_a) {
    var startingAddress = _a.startingAddress, address = _a.address, relativeAddressMaxlength = _a.relativeAddressMaxlength, isInlineFrame = _a.isInlineFrame, isFoundByStackScanning = _a.isFoundByStackScanning, isAbsolute = _a.isAbsolute, onToggle = _a.onToggle;
    var convertAbsoluteAddressToRelative = function () {
        if (!startingAddress) {
            return '';
        }
        var relativeAddress = formatAddress(parseAddress(address) - parseAddress(startingAddress), relativeAddressMaxlength);
        return "+" + relativeAddress;
    };
    var getAddressTooltip = function () {
        if (isInlineFrame && isFoundByStackScanning) {
            return t('Inline frame, found by stack scanning');
        }
        if (isInlineFrame) {
            return t('Inline frame');
        }
        if (isFoundByStackScanning) {
            return t('Found by stack scanning');
        }
        return undefined;
    };
    var relativeAddress = convertAbsoluteAddressToRelative();
    var canBeConverted = !!(onToggle && relativeAddress);
    var formattedAddress = !relativeAddress || isAbsolute ? address : relativeAddress;
    var tooltipTitle = getAddressTooltip();
    return (<Wrapper>
      {canBeConverted && (<AddressIconTooltip title={isAbsolute ? t('Switch to absolute') : t('Switch to relative')} containerDisplayMode="inline-flex">
          <AddressToggleIcon onClick={onToggle} size="xs" color="purple300"/>
        </AddressIconTooltip>)}
      <Tooltip title={tooltipTitle} disabled={!(isFoundByStackScanning || isInlineFrame)}>
        <Address isFoundByStackScanning={isFoundByStackScanning} isInlineFrame={isInlineFrame} canBeConverted={canBeConverted}>
          {formattedAddress}
        </Address>
      </Tooltip>
    </Wrapper>);
};
var AddressIconTooltip = styled(Tooltip)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  align-items: center;\n  margin-right: ", ";\n"], ["\n  align-items: center;\n  margin-right: ", ";\n"])), space(0.75));
var AddressToggleIcon = styled(IconFilter)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  cursor: pointer;\n  visibility: hidden;\n  display: none;\n  @media (min-width: ", ") {\n    display: block;\n  }\n"], ["\n  cursor: pointer;\n  visibility: hidden;\n  display: none;\n  @media (min-width: ", ") {\n    display: block;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
var getAddresstextBorderBottom = function (p) {
    if (p.isFoundByStackScanning) {
        return "1px dashed " + p.theme.red300;
    }
    if (p.isInlineFrame) {
        return "1px dashed " + p.theme.blue300;
    }
    return 'none';
};
var Address = styled('span')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  padding-left: ", ";\n  border-bottom: ", ";\n  ", ";\n  max-width: 93px;\n"], ["\n  padding-left: ", ";\n  border-bottom: ", ";\n  ", ";\n  max-width: 93px;\n"])), function (p) { return (p.canBeConverted ? null : '18px'); }, getAddresstextBorderBottom, overflowEllipsis);
var Wrapper = styled('span')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  font-family: ", ";\n  font-size: ", ";\n  color: ", ";\n  letter-spacing: -0.25px;\n  width: 100%;\n  flex-grow: 0;\n  flex-shrink: 0;\n  display: inline-flex;\n  align-items: center;\n  padding: 0 ", " 0 0;\n  order: 1;\n\n  @media (min-width: ", ") {\n    padding: 0 ", ";\n    order: 0;\n  }\n"], ["\n  font-family: ", ";\n  font-size: ", ";\n  color: ", ";\n  letter-spacing: -0.25px;\n  width: 100%;\n  flex-grow: 0;\n  flex-shrink: 0;\n  display: inline-flex;\n  align-items: center;\n  padding: 0 ", " 0 0;\n  order: 1;\n\n  @media (min-width: ", ") {\n    padding: 0 ", ";\n    order: 0;\n  }\n"])), function (p) { return p.theme.text.familyMono; }, function (p) { return p.theme.fontSizeExtraSmall; }, function (p) { return p.theme.textColor; }, space(0.5), function (props) { return props.theme.breakpoints[0]; }, space(0.5));
export default TogglableAddress;
export { AddressToggleIcon };
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=togglableAddress.jsx.map