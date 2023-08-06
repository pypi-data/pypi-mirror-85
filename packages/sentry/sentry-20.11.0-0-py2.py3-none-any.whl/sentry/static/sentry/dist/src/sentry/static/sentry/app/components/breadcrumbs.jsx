import { __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import space from 'app/styles/space';
import { IconChevron } from 'app/icons';
import Link from 'app/components/links/link';
import GlobalSelectionLink from 'app/components/globalSelectionLink';
import overflowEllipsis from 'app/styles/overflowEllipsis';
/**
 * Page breadcrumbs used for navigation, not to be confused with sentry's event breadcrumbs
 */
var Breadcrumbs = function (_a) {
    var crumbs = _a.crumbs, _b = _a.linkLastItem, linkLastItem = _b === void 0 ? false : _b, props = __rest(_a, ["crumbs", "linkLastItem"]);
    if (crumbs.length === 0) {
        return null;
    }
    if (!linkLastItem) {
        crumbs[crumbs.length - 1].to = null;
    }
    return (<BreadcrumbList {...props}>
      {crumbs.map(function (_a, index) {
        var label = _a.label, to = _a.to, preserveGlobalSelection = _a.preserveGlobalSelection, key = _a.key;
        var labelKey = typeof label === 'string' ? label : '';
        var mapKey = (key !== null && key !== void 0 ? key : typeof to === 'string') ? "" + labelKey + to : "" + labelKey + index;
        return (<React.Fragment key={mapKey}>
            {to ? (<BreadcrumbLink to={to} preserveGlobalSelection={preserveGlobalSelection}>
                {label}
              </BreadcrumbLink>) : (<BreadcrumbItem>{label}</BreadcrumbItem>)}

            {index < crumbs.length - 1 && (<BreadcrumbDividerIcon size="xs" direction="right"/>)}
          </React.Fragment>);
    })}
    </BreadcrumbList>);
};
var getBreadcrumbListItemStyles = function (p) { return "\n  color: " + p.theme.gray300 + ";\n  " + overflowEllipsis + ";\n  width: auto;\n\n  &:last-child {\n    color: " + p.theme.textColor + ";\n  }\n"; };
var BreadcrumbList = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  padding: ", " 0;\n"], ["\n  display: flex;\n  align-items: center;\n  padding: ", " 0;\n"])), space(1));
var BreadcrumbLink = styled(function (_a) {
    var preserveGlobalSelection = _a.preserveGlobalSelection, props = __rest(_a, ["preserveGlobalSelection"]);
    return preserveGlobalSelection ? <GlobalSelectionLink {...props}/> : <Link {...props}/>;
})(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  ", "\n\n  &:hover,\n  &:active {\n    color: ", ";\n  }\n"], ["\n  ", "\n\n  &:hover,\n  &:active {\n    color: ", ";\n  }\n"])), getBreadcrumbListItemStyles, function (p) { return p.theme.subText; });
var BreadcrumbItem = styled('span')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), getBreadcrumbListItemStyles);
var BreadcrumbDividerIcon = styled(IconChevron)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  color: ", ";\n  margin: 0 ", ";\n  flex-shrink: 0;\n"], ["\n  color: ", ";\n  margin: 0 ", ";\n  flex-shrink: 0;\n"])), function (p) { return p.theme.gray300; }, space(1));
export default Breadcrumbs;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=breadcrumbs.jsx.map