import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
var NoEvents = function (_a) {
    var seriesCount = _a.seriesCount;
    return (<Container>
    <EmptyText seriesCount={seriesCount}>{t('No activity yet.')}</EmptyText>
  </Container>);
};
export default NoEvents;
var Container = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: absolute;\n  top: 0;\n  left: 0;\n  bottom: 0;\n  right: 0;\n"], ["\n  position: absolute;\n  top: 0;\n  left: 0;\n  bottom: 0;\n  right: 0;\n"])));
var EmptyText = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  margin-left: 4px;\n  margin-right: 4px;\n  height: ", ";\n  color: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  margin-left: 4px;\n  margin-right: 4px;\n  height: ", ";\n  color: ", ";\n"])), function (p) { return (p.seriesCount > 1 ? '90px' : '150px'); }, function (p) { return p.theme.gray300; });
var templateObject_1, templateObject_2;
//# sourceMappingURL=noEvents.jsx.map