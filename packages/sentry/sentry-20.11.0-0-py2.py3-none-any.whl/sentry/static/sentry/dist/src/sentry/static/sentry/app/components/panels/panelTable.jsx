import { __makeTemplateObject } from "tslib";
import React from 'react';
import isPropValid from '@emotion/is-prop-valid';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import EmptyStateWarning from 'app/components/emptyStateWarning';
import LoadingIndicator from 'app/components/loadingIndicator';
import space from 'app/styles/space';
import Panel from './panel';
/**
 * Bare bones table generates a CSS grid template based on the content.
 *
 * The number of children elements should be a multiple of `this.props.columns` to have
 * it look ok.
 *
 *
 * Potential customizations:
 * - [ ] Add borders for columns to make them more like cells
 * - [ ] Add prop to disable borders for rows
 * - [ ] We may need to wrap `children` with our own component (similar to what we're doing
 *       with `headers`. Then we can get rid of that gross `> *` selector
 * - [ ] Allow customization of wrappers (Header and body cells if added)
 */
var PanelTable = function (_a) {
    var headers = _a.headers, children = _a.children, isLoading = _a.isLoading, isEmpty = _a.isEmpty, disablePadding = _a.disablePadding, className = _a.className, _b = _a.emptyMessage, emptyMessage = _b === void 0 ? t('There are no items to display') : _b, loader = _a.loader;
    var shouldShowLoading = isLoading === true;
    var shouldShowEmptyMessage = !shouldShowLoading && isEmpty;
    var shouldShowContent = !shouldShowLoading && !shouldShowEmptyMessage;
    return (<Wrapper columns={headers.length} disablePadding={disablePadding} className={className} hasRows={shouldShowContent}>
      {headers.map(function (header, i) { return (<PanelTableHeader key={i}>{header}</PanelTableHeader>); })}

      {shouldShowLoading && (<LoadingWrapper>{loader || <LoadingIndicator />}</LoadingWrapper>)}

      {shouldShowEmptyMessage && (<TableEmptyStateWarning>
          <p>{emptyMessage}</p>
        </TableEmptyStateWarning>)}

      {shouldShowContent && getContent(children)}
    </Wrapper>);
};
function getContent(children) {
    if (typeof children === 'function') {
        return children();
    }
    return children;
}
var LoadingWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject([""], [""])));
var TableEmptyStateWarning = styled(EmptyStateWarning)(templateObject_2 || (templateObject_2 = __makeTemplateObject([""], [""])));
var Wrapper = styled(Panel, {
    shouldForwardProp: function (p) { return isPropValid(p) && p !== 'columns'; },
})(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: repeat(", ", auto);\n\n  > * {\n    ", "\n\n    &:nth-last-child(n + ", ") {\n      border-bottom: 1px solid ", ";\n    }\n  }\n\n  > ", ", > ", " {\n    border: none;\n    grid-column: auto / span ", ";\n  }\n\n  /* safari needs an overflow value or the contents will spill out */\n  overflow: auto;\n"], ["\n  display: grid;\n  grid-template-columns: repeat(", ", auto);\n\n  > * {\n    ", "\n\n    &:nth-last-child(n + ", ") {\n      border-bottom: 1px solid ", ";\n    }\n  }\n\n  > " /* sc-selector */, ", > " /* sc-selector */, " {\n    border: none;\n    grid-column: auto / span ", ";\n  }\n\n  /* safari needs an overflow value or the contents will spill out */\n  overflow: auto;\n"])), function (p) { return p.columns; }, function (p) { return (p.disablePadding ? '' : "padding: " + space(2) + ";"); }, function (p) { return (p.hasRows ? p.columns + 1 : 0); }, function (p) { return p.theme.border; }, /* sc-selector */ TableEmptyStateWarning, /* sc-selector */ LoadingWrapper, function (p) { return p.columns; });
export var PanelTableHeader = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  color: ", ";\n  font-size: 13px;\n  font-weight: 600;\n  text-transform: uppercase;\n  border-radius: ", " ", " 0 0;\n  background: ", ";\n  line-height: 1;\n"], ["\n  color: ", ";\n  font-size: 13px;\n  font-weight: 600;\n  text-transform: uppercase;\n  border-radius: ", " ", " 0 0;\n  background: ", ";\n  line-height: 1;\n"])), function (p) { return p.theme.subText; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.backgroundSecondary; });
export default PanelTable;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=panelTable.jsx.map