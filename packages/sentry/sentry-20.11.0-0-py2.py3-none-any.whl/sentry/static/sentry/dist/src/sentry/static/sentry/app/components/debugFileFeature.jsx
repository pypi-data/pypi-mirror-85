import { __makeTemplateObject } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import Tooltip from 'app/components/tooltip';
import { IconCheckmark, IconClose } from 'app/icons';
import { t } from 'app/locale';
import Tag from 'app/components/tagDeprecated';
var FEATURE_TOOLTIPS = {
    symtab: t('Symbol tables are used as a fallback when full debug information is not available'),
    debug: t('Debug information provides function names and resolves inlined frames during symbolication'),
    unwind: t('Stack unwinding information improves the quality of stack traces extracted from minidumps'),
    sources: t('Source code information allows Sentry to display source code context for stack frames'),
};
var DebugFileFeature = function (_a) {
    var available = _a.available, feature = _a.feature;
    var icon = null;
    if (available === true) {
        icon = (<IconWrapper>
        <IconCheckmark size="sm" color="green300"/>
      </IconWrapper>);
    }
    else if (available === false) {
        icon = (<IconWrapper>
        <IconClose size="sm" color="red300"/>
      </IconWrapper>);
    }
    return (<Tooltip title={FEATURE_TOOLTIPS[feature]}>
      <Tag inline>
        {icon}
        {feature}
      </Tag>
    </Tooltip>);
};
DebugFileFeature.defaultProps = {
    available: true,
};
DebugFileFeature.propTypes = {
    available: PropTypes.bool,
    feature: PropTypes.oneOf(Object.keys(FEATURE_TOOLTIPS)).isRequired,
};
DebugFileFeature.defaultProps = {
    available: true,
};
var IconWrapper = styled('span')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-right: 1ex;\n"], ["\n  margin-right: 1ex;\n"])));
export default DebugFileFeature;
var templateObject_1;
//# sourceMappingURL=debugFileFeature.jsx.map