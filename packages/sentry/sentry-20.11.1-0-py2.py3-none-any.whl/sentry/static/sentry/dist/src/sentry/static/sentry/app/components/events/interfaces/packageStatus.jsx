import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { IconCircle, IconCheckmark, IconFlag } from 'app/icons';
import Tooltip from 'app/components/tooltip';
import space from 'app/styles/space';
var PackageStatus = function (_a) {
    var status = _a.status, tooltip = _a.tooltip;
    var getIcon = function () {
        switch (status) {
            case 'success':
                return <IconCheckmark isCircled color="green300" size="xs"/>;
            case 'empty':
                return <IconCircle size="xs"/>;
            case 'error':
            default:
                return <IconFlag color="red300" size="xs"/>;
        }
    };
    var icon = getIcon();
    if (status === 'empty') {
        return null;
    }
    return (<StyledTooltip title={tooltip} disabled={!(tooltip && tooltip.length)} containerDisplayMode="inline-flex">
      <PackageStatusIcon>{icon}</PackageStatusIcon>
    </StyledTooltip>);
};
var StyledTooltip = styled(Tooltip)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space(0.75));
export var PackageStatusIcon = styled('span')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  height: 12px;\n  align-items: center;\n  cursor: pointer;\n  visibility: hidden;\n  display: none;\n  @media (min-width: ", ") {\n    display: block;\n  }\n"], ["\n  height: 12px;\n  align-items: center;\n  cursor: pointer;\n  visibility: hidden;\n  display: none;\n  @media (min-width: ", ") {\n    display: block;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
export default PackageStatus;
var templateObject_1, templateObject_2;
//# sourceMappingURL=packageStatus.jsx.map