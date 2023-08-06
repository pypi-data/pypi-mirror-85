import { __makeTemplateObject } from "tslib";
import 'react-date-range/dist/styles.css';
import 'react-date-range/dist/theme/default.css';
import { Calendar } from 'react-date-range';
import React from 'react';
import moment from 'moment';
import styled from '@emotion/styled';
import { inputStyles } from 'app/styles/input';
import DropdownMenu from 'app/components/dropdownMenu';
import { IconCalendar } from 'app/icons';
import space from 'app/styles/space';
import InputField from './inputField';
function handleChangeDate(onChange, onBlur, date, close) {
    onChange(date);
    onBlur(date);
    // close dropdown menu
    close();
}
export default function DatePickerField(props) {
    return (<InputField {...props} field={function (_a) {
        var onChange = _a.onChange, onBlur = _a.onBlur, value = _a.value, disabled = _a.disabled, id = _a.id;
        var dateObj = new Date(value);
        var inputValue = !isNaN(dateObj.getTime()) ? dateObj : new Date();
        var dateString = moment(inputValue).format('LL');
        return (<DropdownMenu keepMenuOpen>
            {function (_a) {
            var isOpen = _a.isOpen, getRootProps = _a.getRootProps, getActorProps = _a.getActorProps, getMenuProps = _a.getMenuProps, actions = _a.actions;
            return (<div {...getRootProps()}>
                <InputWrapper id={id} {...getActorProps()} isOpen={isOpen}>
                  <StyledInput readOnly value={dateString}/>
                  <CalendarIcon>
                    <IconCalendar />
                  </CalendarIcon>
                </InputWrapper>

                {isOpen && (<CalendarMenu {...getMenuProps()}>
                    <Calendar disabled={disabled} date={inputValue} onChange={function (date) {
                return handleChangeDate(onChange, onBlur, date, actions.close);
            }}/>
                  </CalendarMenu>)}
              </div>);
        }}
          </DropdownMenu>);
    }}/>);
}
var InputWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  ", "\n  cursor: text;\n  display: flex;\n  z-index: ", ";\n  ", "\n"], ["\n  ", "\n  cursor: text;\n  display: flex;\n  z-index: ", ";\n  ", "\n"])), inputStyles, function (p) { return p.theme.zIndex.dropdownAutocomplete.actor; }, function (p) { return p.isOpen && 'border-bottom-left-radius: 0'; });
var StyledInput = styled('input')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  border: none;\n  outline: none;\n  flex: 1;\n"], ["\n  border: none;\n  outline: none;\n  flex: 1;\n"])));
var CalendarMenu = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  background: ", ";\n  position: absolute;\n  left: 0;\n  border: 1px solid ", ";\n  border-top: none;\n  z-index: ", ";\n  margin-top: -1px;\n\n  .rdrMonthAndYearWrapper {\n    height: 50px;\n    padding-top: 0;\n  }\n"], ["\n  display: flex;\n  background: ", ";\n  position: absolute;\n  left: 0;\n  border: 1px solid ", ";\n  border-top: none;\n  z-index: ", ";\n  margin-top: -1px;\n\n  .rdrMonthAndYearWrapper {\n    height: 50px;\n    padding-top: 0;\n  }\n"])), function (p) { return p.theme.background; }, function (p) { return p.theme.border; }, function (p) { return p.theme.zIndex.dropdownAutocomplete.menu; });
var CalendarIcon = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  padding: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  padding: ", ";\n"])), space(1));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=datePickerField.jsx.map