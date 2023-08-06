import { __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Tag from 'app/components/tagDeprecated';
import Tooltip from 'app/components/tooltip';
import space from 'app/styles/space';
import { t } from 'app/locale';
import theme from 'app/utils/theme';
import CircleIndicator from 'app/components/circleIndicator';
var defaultTitles = {
    alpha: t('This feature is in alpha and may be unstable'),
    beta: t('This feature is in beta and may change in the future'),
    new: t('This is a new feature'),
};
var labels = {
    alpha: t('alpha'),
    beta: t('beta'),
    new: t('new'),
};
var FeaturedBadge = function (_a) {
    var type = _a.type, _b = _a.variant, variant = _b === void 0 ? 'badge' : _b, title = _a.title, noTooltip = _a.noTooltip, p = __rest(_a, ["type", "variant", "title", "noTooltip"]);
    return (<div {...p}>
    <Tooltip title={title !== null && title !== void 0 ? title : defaultTitles[type]} disabled={noTooltip} position="right">
      <React.Fragment>
        {variant === 'badge' && <StyledTag priority={type}>{labels[type]}</StyledTag>}
        {variant === 'indicator' && (<CircleIndicator color={theme.badge[type].indicatorColor} size={8}/>)}
      </React.Fragment>
    </Tooltip>
  </div>);
};
var StyledTag = styled(Tag)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: 3px ", ";\n"], ["\n  padding: 3px ", ";\n"])), space(0.75));
var StyledFeatureBadge = styled(FeaturedBadge)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: inline-flex;\n  align-items: center;\n  margin-left: ", ";\n  position: relative;\n  top: -1px;\n"], ["\n  display: inline-flex;\n  align-items: center;\n  margin-left: ", ";\n  position: relative;\n  top: -1px;\n"])), space(0.75));
export default StyledFeatureBadge;
var templateObject_1, templateObject_2;
//# sourceMappingURL=featureBadge.jsx.map