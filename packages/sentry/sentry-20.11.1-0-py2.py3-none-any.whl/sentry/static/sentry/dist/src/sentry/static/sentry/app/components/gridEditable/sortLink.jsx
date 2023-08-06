import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import omit from 'lodash/omit';
import { IconArrow } from 'app/icons';
import Link from 'app/components/links/link';
var SortLink = /** @class */ (function (_super) {
    __extends(SortLink, _super);
    function SortLink() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    SortLink.prototype.renderArrow = function () {
        var direction = this.props.direction;
        if (!direction) {
            return null;
        }
        if (direction === 'desc') {
            return <StyledIconArrow size="xs" direction="down"/>;
        }
        return <StyledIconArrow size="xs" direction="up"/>;
    };
    SortLink.prototype.render = function () {
        var _a = this.props, align = _a.align, title = _a.title, canSort = _a.canSort, generateSortLink = _a.generateSortLink, onClick = _a.onClick;
        var target = generateSortLink();
        if (!target || !canSort) {
            return <StyledNonLink align={align}>{title}</StyledNonLink>;
        }
        return (<StyledLink align={align} to={target} onClick={onClick}>
        {title} {this.renderArrow()}
      </StyledLink>);
    };
    return SortLink;
}(React.Component));
var StyledLink = styled(function (props) {
    var forwardProps = omit(props, ['align']);
    return <Link {...forwardProps}/>;
})(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: block;\n  width: 100%;\n  white-space: nowrap;\n  color: inherit;\n\n  &:hover,\n  &:active,\n  &:focus,\n  &:visited {\n    color: inherit;\n  }\n\n  ", "\n"], ["\n  display: block;\n  width: 100%;\n  white-space: nowrap;\n  color: inherit;\n\n  &:hover,\n  &:active,\n  &:focus,\n  &:visited {\n    color: inherit;\n  }\n\n  ", "\n"])), function (p) { return (p.align ? "text-align: " + p.align + ";" : ''); });
var StyledNonLink = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: block;\n  width: 100%;\n  white-space: nowrap;\n  ", "\n"], ["\n  display: block;\n  width: 100%;\n  white-space: nowrap;\n  ", "\n"])), function (p) { return (p.align ? "text-align: " + p.align + ";" : ''); });
var StyledIconArrow = styled(IconArrow)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  vertical-align: top;\n"], ["\n  vertical-align: top;\n"])));
export default SortLink;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=sortLink.jsx.map