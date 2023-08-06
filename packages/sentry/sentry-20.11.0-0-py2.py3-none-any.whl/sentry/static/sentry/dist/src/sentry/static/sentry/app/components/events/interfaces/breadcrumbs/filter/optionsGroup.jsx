import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import space from 'app/styles/space';
import CheckboxFancy from 'app/components/checkboxFancy/checkboxFancy';
var OptionsGroup = function (_a) {
    var type = _a.type, options = _a.options, onClick = _a.onClick;
    var handleClick = function (option) { return function (event) {
        event.stopPropagation();
        onClick(type, option);
    }; };
    return (<div>
      <Header>{type === 'type' ? t('Type') : t('Level')}</Header>
      <List>
        {options.map(function (option) { return (<ListItem key={option.type} isChecked={option.isChecked} onClick={handleClick(option)}>
            {option.symbol}
            <ListItemDescription>{option.description}</ListItemDescription>
            <CheckboxFancy isChecked={option.isChecked}/>
          </ListItem>); })}
      </List>
    </div>);
};
export default OptionsGroup;
var Header = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  margin: 0;\n  background-color: ", ";\n  color: ", ";\n  font-weight: normal;\n  font-size: ", ";\n  padding: ", " ", ";\n  border-bottom: 1px solid ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  margin: 0;\n  background-color: ", ";\n  color: ", ";\n  font-weight: normal;\n  font-size: ", ";\n  padding: ", " ", ";\n  border-bottom: 1px solid ", ";\n"])), function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.gray300; }, function (p) { return p.theme.fontSizeMedium; }, space(1), space(2), function (p) { return p.theme.border; });
var List = styled('ul')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  list-style: none;\n  margin: 0;\n  padding: 0;\n"], ["\n  list-style: none;\n  margin: 0;\n  padding: 0;\n"])));
var ListItem = styled('li')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr max-content;\n  grid-column-gap: ", ";\n  align-items: center;\n  padding: ", " ", ";\n  border-bottom: 1px solid ", ";\n  :hover {\n    background-color: ", ";\n  }\n  ", " {\n    opacity: ", ";\n  }\n\n  &:hover ", " {\n    opacity: 1;\n  }\n\n  &:hover span {\n    color: ", ";\n    text-decoration: underline;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr max-content;\n  grid-column-gap: ", ";\n  align-items: center;\n  padding: ", " ", ";\n  border-bottom: 1px solid ", ";\n  :hover {\n    background-color: ", ";\n  }\n  ", " {\n    opacity: ", ";\n  }\n\n  &:hover ", " {\n    opacity: 1;\n  }\n\n  &:hover span {\n    color: ", ";\n    text-decoration: underline;\n  }\n"])), space(1), space(1), space(2), function (p) { return p.theme.border; }, function (p) { return p.theme.backgroundSecondary; }, CheckboxFancy, function (p) { return (p.isChecked ? 1 : 0.3); }, CheckboxFancy, function (p) { return p.theme.blue300; });
var ListItemDescription = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=optionsGroup.jsx.map