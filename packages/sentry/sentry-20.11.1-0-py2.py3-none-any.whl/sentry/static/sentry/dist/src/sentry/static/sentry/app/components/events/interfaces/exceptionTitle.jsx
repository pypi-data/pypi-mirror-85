import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import space from 'app/styles/space';
import Tooltip from 'app/components/tooltip';
import { tct } from 'app/locale';
import { defined } from 'app/utils';
var ExceptionTitle = function (_a) {
    var type = _a.type, exceptionModule = _a.exceptionModule;
    if (defined(exceptionModule)) {
        return (<Tooltip title={tct('from [exceptionModule]', { exceptionModule: exceptionModule })}>
        <Title>{type}</Title>
      </Tooltip>);
    }
    return <Title>{type}</Title>;
};
export default ExceptionTitle;
var Title = styled('h5')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: ", ";\n  overflow-wrap: break-word;\n  word-wrap: break-word;\n  word-break: break-word;\n"], ["\n  margin-bottom: ", ";\n  overflow-wrap: break-word;\n  word-wrap: break-word;\n  word-break: break-word;\n"])), space(0.5));
var templateObject_1;
//# sourceMappingURL=exceptionTitle.jsx.map