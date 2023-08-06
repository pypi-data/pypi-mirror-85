import { __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import capitalize from 'lodash/capitalize';
import { IconWarning } from 'app/icons';
import Tooltip from 'app/components/tooltip';
import { t } from 'app/locale';
import space from 'app/styles/space';
import List from 'app/components/list';
import ListItem from 'app/components/list/listItem';
import { getTooltipText } from './utils';
import ValueElement from './valueElement';
import Chunks from './chunks';
var AnnotatedText = function (_a) {
    var value = _a.value, meta = _a.meta, props = __rest(_a, ["value", "meta"]);
    var renderValue = function () {
        var _a, _b;
        if (((_a = meta === null || meta === void 0 ? void 0 : meta.chunks) === null || _a === void 0 ? void 0 : _a.length) && meta.chunks.length > 1) {
            return <Chunks chunks={meta.chunks}/>;
        }
        var element = <ValueElement value={value} meta={meta}/>;
        if ((_b = meta === null || meta === void 0 ? void 0 : meta.rem) === null || _b === void 0 ? void 0 : _b.length) {
            var title = getTooltipText({ rule_id: meta.rem[0][0], remark: meta.rem[0][1] });
            return <Tooltip title={title}>{element}</Tooltip>;
        }
        return element;
    };
    var getErrorMessage = function (error) {
        var _a;
        var errorMessage = [];
        if (error[0]) {
            errorMessage.push(capitalize(error[0].replace('_', ' ')));
        }
        if ((_a = error[1]) === null || _a === void 0 ? void 0 : _a.reason) {
            errorMessage.push("(" + error[1].reason + ")");
        }
        return errorMessage.join(' ');
    };
    var getTooltipTitle = function (errors) {
        if (errors.length === 1) {
            return <TooltipTitle>{t('Error: %s', getErrorMessage(errors[0]))}</TooltipTitle>;
        }
        return (<TooltipTitle>
        <span>{t('Errors:')}</span>
        <StyledList symbol="bullet">
          {errors.map(function (error, index) { return (<ListItem key={index}>{getErrorMessage(error)}</ListItem>); })}
        </StyledList>
      </TooltipTitle>);
    };
    var renderErrors = function (errors) {
        if (!errors.length) {
            return null;
        }
        return (<StyledTooltipError title={getTooltipTitle(errors)}>
        <StyledIconWarning color="red300"/>
      </StyledTooltipError>);
    };
    return (<span {...props}>
      {renderValue()}
      {(meta === null || meta === void 0 ? void 0 : meta.err) && renderErrors(meta.err)}
    </span>);
};
export default AnnotatedText;
var StyledTooltipError = styled(Tooltip)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-left: ", ";\n  vertical-align: middle;\n"], ["\n  margin-left: ", ";\n  vertical-align: middle;\n"])), space(0.75));
var StyledList = styled(List)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  li {\n    padding-left: ", ";\n    word-break: break-all;\n    :before {\n      border-color: ", ";\n      top: 6px;\n    }\n  }\n"], ["\n  li {\n    padding-left: ", ";\n    word-break: break-all;\n    :before {\n      border-color: ", ";\n      top: 6px;\n    }\n  }\n"])), space(3), function (p) { return p.theme.white; });
var TooltipTitle = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  text-align: left;\n"], ["\n  text-align: left;\n"])));
var StyledIconWarning = styled(IconWarning)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  vertical-align: middle;\n"], ["\n  vertical-align: middle;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=index.jsx.map