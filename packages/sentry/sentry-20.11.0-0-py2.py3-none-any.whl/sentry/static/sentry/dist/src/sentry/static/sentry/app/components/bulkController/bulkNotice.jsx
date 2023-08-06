import { __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { tn, tct, t } from 'app/locale';
import { defined } from 'app/utils';
import { PanelAlert } from '../panels';
import Button from '../button';
function getSelectAllText(allRowsCount, bulkLimit) {
    if (!defined(allRowsCount)) {
        return {
            noticeText: t('Selected all items across all pages.'),
            actionText: t('Select all items across all pages.'),
        };
    }
    if (bulkLimit && allRowsCount > bulkLimit) {
        return {
            noticeText: tct('Selected up to the first [count] items.', {
                count: bulkLimit,
            }),
            actionText: tct('Select the first [count] items.', {
                count: bulkLimit,
            }),
        };
    }
    return {
        noticeText: tct('Selected all [count] items.', {
            count: allRowsCount,
        }),
        actionText: tct('Select all [count] items.', {
            count: allRowsCount,
        }),
    };
}
function BulkNotice(_a) {
    var selectedRowsCount = _a.selectedRowsCount, columnsCount = _a.columnsCount, isPageSelected = _a.isPageSelected, isAllSelected = _a.isAllSelected, onSelectAllRows = _a.onSelectAllRows, onUnselectAllRows = _a.onUnselectAllRows, bulkLimit = _a.bulkLimit, allRowsCount = _a.allRowsCount, className = _a.className;
    if ((allRowsCount && allRowsCount <= selectedRowsCount) || !isPageSelected) {
        return null;
    }
    var _b = getSelectAllText(allRowsCount, bulkLimit), noticeText = _b.noticeText, actionText = _b.actionText;
    return (<Wrapper columnsCount={columnsCount} className={className}>
      {isAllSelected ? (<React.Fragment>
          {noticeText}{' '}
          <AlertButton priority="link" onClick={onUnselectAllRows}>
            {t('Cancel selection.')}
          </AlertButton>
        </React.Fragment>) : (<React.Fragment>
          {tn('%s item on this page selected.', '%s items on this page selected.', selectedRowsCount)}{' '}
          <AlertButton priority="link" onClick={onSelectAllRows}>
            {actionText}
          </AlertButton>
        </React.Fragment>)}
    </Wrapper>);
}
var Wrapper = styled(function (_a) {
    var _columnsCount = _a.columnsCount, props = __rest(_a, ["columnsCount"]);
    return (<PanelAlert {...props}/>);
})(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  grid-column: span ", ";\n  text-align: center;\n"], ["\n  grid-column: span ", ";\n  text-align: center;\n"])), function (p) { return p.columnsCount; });
var AlertButton = styled(Button)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  &,\n  &:hover,\n  &:active,\n  &:focus {\n    /* match the styles of an <a> tag inside Alert */\n    color: ", ";\n    border: none;\n    border-radius: 0;\n    border-bottom: 1px dotted ", ";\n    padding-bottom: 1px;\n    font-size: 15px;\n  }\n"], ["\n  &,\n  &:hover,\n  &:active,\n  &:focus {\n    /* match the styles of an <a> tag inside Alert */\n    color: ", ";\n    border: none;\n    border-radius: 0;\n    border-bottom: 1px dotted ", ";\n    padding-bottom: 1px;\n    font-size: 15px;\n  }\n"])), function (p) { return p.theme.textColor; }, function (p) { return p.theme.textColor; });
export default BulkNotice;
var templateObject_1, templateObject_2;
//# sourceMappingURL=bulkNotice.jsx.map