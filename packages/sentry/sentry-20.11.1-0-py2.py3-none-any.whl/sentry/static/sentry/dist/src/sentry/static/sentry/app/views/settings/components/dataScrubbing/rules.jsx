import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import space from 'app/styles/space';
import TextOverflow from 'app/components/textOverflow';
import { IconDelete, IconEdit } from 'app/icons';
import Button from 'app/components/button';
import { getMethodLabel, getRuleLabel } from './utils';
import { RuleType, MethodType } from './types';
var getListItemDescription = function (rule) {
    var method = rule.method, type = rule.type, source = rule.source;
    var methodLabel = getMethodLabel(method);
    var typeLabel = getRuleLabel(type);
    var descriptionDetails = [];
    descriptionDetails.push("[" + methodLabel.label + "]");
    descriptionDetails.push(rule.type === RuleType.PATTERN ? "[" + rule.pattern + "]" : "[" + typeLabel + "]");
    if (rule.method === MethodType.REPLACE && rule.placeholder) {
        descriptionDetails.push(" with [" + rule.placeholder + "]");
    }
    return descriptionDetails.join(' ') + " " + t('from') + " [" + source + "]";
};
var Rules = React.forwardRef(function RulesList(_a, ref) {
    var rules = _a.rules, onEditRule = _a.onEditRule, onDeleteRule = _a.onDeleteRule, disabled = _a.disabled;
    return (<List ref={ref} isDisabled={disabled} data-test-id="advanced-data-scrubbing-rules">
      {rules.map(function (rule) {
        var id = rule.id;
        return (<ListItem key={id}>
            <TextOverflow>{getListItemDescription(rule)}</TextOverflow>
            {onEditRule && (<Button label={t('Edit Rule')} size="small" onClick={onEditRule(id)} icon={<IconEdit />} disabled={disabled}/>)}
            {onDeleteRule && (<Button label={t('Delete Rule')} size="small" onClick={onDeleteRule(id)} icon={<IconDelete />} disabled={disabled}/>)}
          </ListItem>);
    })}
    </List>);
});
export default Rules;
var List = styled('ul')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  list-style: none;\n  margin: 0;\n  padding: 0;\n  margin-bottom: 0 !important;\n  ", "\n"], ["\n  list-style: none;\n  margin: 0;\n  padding: 0;\n  margin-bottom: 0 !important;\n  ",
    "\n"])), function (p) {
    return p.isDisabled &&
        "\n      color: " + p.theme.gray200 + ";\n      background: " + p.theme.backgroundSecondary + ";\n  ";
});
var ListItem = styled('li')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: auto max-content max-content;\n  grid-column-gap: ", ";\n  align-items: center;\n  padding: ", " ", ";\n  border-bottom: 1px solid ", ";\n  &:hover {\n    background-color: ", ";\n  }\n  &:last-child {\n    border-bottom: 0;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: auto max-content max-content;\n  grid-column-gap: ", ";\n  align-items: center;\n  padding: ", " ", ";\n  border-bottom: 1px solid ", ";\n  &:hover {\n    background-color: ", ";\n  }\n  &:last-child {\n    border-bottom: 0;\n  }\n"])), space(1), space(1), space(2), function (p) { return p.theme.border; }, function (p) { return p.theme.backgroundSecondary; });
var templateObject_1, templateObject_2;
//# sourceMappingURL=rules.jsx.map