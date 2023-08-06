import { __makeTemplateObject } from "tslib";
import React from 'react';
import PropTypes from 'prop-types';
import styled from '@emotion/styled';
import DropdownButton from 'app/components/dropdownButton';
import DropdownMenu from 'app/components/dropdownMenu';
import { InlineContainer, SectionHeading } from 'app/components/charts/styles';
import { DropdownItem } from 'app/components/dropdownControl';
import DropdownBubble from 'app/components/dropdownBubble';
import Tooltip from 'app/components/tooltip';
import space from 'app/styles/space';
function OptionSelector(_a) {
    var options = _a.options, onChange = _a.onChange, selected = _a.selected, title = _a.title, _b = _a.menuWidth, menuWidth = _b === void 0 ? 'auto' : _b;
    var selectedOption = options.find(function (opt) { return selected === opt.value; }) || options[0];
    return (<InlineContainer>
      <SectionHeading>{title}</SectionHeading>
      <MenuContainer>
        <DropdownMenu alwaysRenderMenu={false}>
          {function (_a) {
        var isOpen = _a.isOpen, getMenuProps = _a.getMenuProps, getActorProps = _a.getActorProps;
        return (<React.Fragment>
              <StyledDropdownButton {...getActorProps()} size="zero" isOpen={isOpen}>
                {selectedOption.label}
              </StyledDropdownButton>
              <StyledDropdownBubble {...getMenuProps()} alignMenu="right" width={menuWidth} isOpen={isOpen} blendWithActor={false} blendCorner>
                {options.map(function (opt) { return (<DropdownItem key={opt.value} onSelect={onChange} eventKey={opt.value} disabled={opt.disabled} isActive={selected === opt.value} data-test-id={"option-" + opt.value}>
                    <Tooltip title={opt.tooltip} containerDisplayMode="inline">
                      {opt.label}
                    </Tooltip>
                  </DropdownItem>); })}
              </StyledDropdownBubble>
            </React.Fragment>);
    }}
        </DropdownMenu>
      </MenuContainer>
    </InlineContainer>);
}
var MenuContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: inline-block;\n  position: relative;\n"], ["\n  display: inline-block;\n  position: relative;\n"])));
var StyledDropdownButton = styled(DropdownButton)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  padding: ", " ", ";\n  font-weight: normal;\n  color: ", ";\n  z-index: ", ";\n\n  &:hover,\n  &:focus,\n  &:active {\n    color: ", ";\n  }\n"], ["\n  padding: ", " ", ";\n  font-weight: normal;\n  color: ", ";\n  z-index: ", ";\n\n  &:hover,\n  &:focus,\n  &:active {\n    color: ", ";\n  }\n"])), space(1), space(2), function (p) { return p.theme.gray400; }, function (p) { return (p.isOpen ? p.theme.zIndex.dropdownAutocomplete.actor : 'auto'); }, function (p) { return p.theme.gray500; });
var StyledDropdownBubble = styled(DropdownBubble)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: ", ";\n"], ["\n  display: ", ";\n"])), function (p) { return (p.isOpen ? 'block' : 'none'); });
OptionSelector.propTypes = {
    options: PropTypes.array.isRequired,
    onChange: PropTypes.func.isRequired,
    title: PropTypes.string.isRequired,
    selected: PropTypes.string,
};
export default OptionSelector;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=optionSelector.jsx.map