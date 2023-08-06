import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import Highlight from 'app/components/highlight';
import Tag from 'app/components/tagDeprecated';
import { BreadcrumbLevelType } from './types';
var Level = React.memo(function (_a) {
    var level = _a.level, _b = _a.searchTerm, searchTerm = _b === void 0 ? '' : _b;
    switch (level) {
        case BreadcrumbLevelType.FATAL:
            return (<StyledTag color="red300">
          <Highlight text={searchTerm}>{t('fatal')}</Highlight>
        </StyledTag>);
        case BreadcrumbLevelType.ERROR:
            return (<StyledTag color="red300">
          <Highlight text={searchTerm}>{t('error')}</Highlight>
        </StyledTag>);
        case BreadcrumbLevelType.INFO:
            return (<StyledTag color="blue300">
          <Highlight text={searchTerm}>{t('info')}</Highlight>
        </StyledTag>);
        case BreadcrumbLevelType.WARNING:
            return (<StyledTag color="orange400">
          <Highlight text={searchTerm}>{t('warning')}</Highlight>
        </StyledTag>);
        default:
            return (<Tag>
          <Highlight text={searchTerm}>{level || t('undefined')}</Highlight>
        </Tag>);
    }
});
export default Level;
// TODO(style): Update the tag component with the new colors
var StyledTag = styled(Tag)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  background-color: ", ";\n  color: ", ";\n"], ["\n  background-color: ", ";\n  color: ", ";\n"])), function (p) { return p.theme[p.color]; }, function (p) { return p.theme.white; });
var templateObject_1;
//# sourceMappingURL=level.jsx.map