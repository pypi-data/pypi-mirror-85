import { __extends, __makeTemplateObject, __rest } from "tslib";
import styled from '@emotion/styled';
import React from 'react';
import omit from 'lodash/omit';
import Link from 'app/components/links/link';
import ExternalLink from 'app/components/links/externalLink';
import { IconChevron } from 'app/icons';
import space from 'app/styles/space';
var AlertLink = /** @class */ (function (_super) {
    __extends(AlertLink, _super);
    function AlertLink() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    AlertLink.prototype.render = function () {
        var _a = this.props, size = _a.size, priority = _a.priority, icon = _a.icon, children = _a.children, onClick = _a.onClick, withoutMarginBottom = _a.withoutMarginBottom, openInNewTab = _a.openInNewTab, to = _a.to, href = _a.href, dataTestId = _a["data-test-id"];
        return (<StyledLink data-test-id={dataTestId} to={to} href={href} onClick={onClick} size={size} priority={priority} withoutMarginBottom={withoutMarginBottom} openInNewTab={openInNewTab}>
        {icon && <IconWrapper>{icon}</IconWrapper>}
        <AlertLinkText>{children}</AlertLinkText>
        <IconLink>
          <IconChevron direction="right"/>
        </IconLink>
      </StyledLink>);
    };
    AlertLink.defaultProps = {
        priority: 'warning',
        size: 'normal',
        withoutMarginBottom: false,
        openInNewTab: false,
    };
    return AlertLink;
}(React.Component));
export default AlertLink;
var StyledLink = styled(function (_a) {
    var openInNewTab = _a.openInNewTab, to = _a.to, href = _a.href, props = __rest(_a, ["openInNewTab", "to", "href"]);
    var linkProps = omit(props, ['withoutMarginBottom', 'priority', 'size']);
    if (href) {
        return <ExternalLink {...linkProps} href={href} openInNewTab={openInNewTab}/>;
    }
    return <Link {...linkProps} to={to || ''}/>;
})(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  background-color: ", ";\n  color: ", ";\n  border: 1px dashed ", ";\n  padding: ", ";\n  margin-bottom: ", ";\n  border-radius: 0.25em;\n  transition: 0.2s border-color;\n\n  &.focus-visible {\n    outline: none;\n    box-shadow: ", "7f 0 0 0 2px;\n  }\n"], ["\n  display: flex;\n  background-color: ", ";\n  color: ", ";\n  border: 1px dashed ", ";\n  padding: ", ";\n  margin-bottom: ", ";\n  border-radius: 0.25em;\n  transition: 0.2s border-color;\n\n  &.focus-visible {\n    outline: none;\n    box-shadow: ", "7f 0 0 0 2px;\n  }\n"])), function (p) { return p.theme.alert[p.priority].backgroundLight; }, function (p) { return p.theme.textColor; }, function (p) { return p.theme.alert[p.priority].border; }, function (p) { return (p.size === 'small' ? space(1) + " " + space(1.5) : space(2)); }, function (p) { return (p.withoutMarginBottom ? 0 : space(3)); }, function (p) { return p.theme.alert[p.priority].border; });
var IconWrapper = styled('span')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  margin: ", " ", " ", " 0;\n"], ["\n  display: flex;\n  margin: ", " ", " ", " 0;\n"])), space(0.5), space(1.5), space(0.5));
var IconLink = styled(IconWrapper)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin: ", " 0;\n"], ["\n  margin: ", " 0;\n"])), space(0.5));
var AlertLinkText = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  line-height: 1.5;\n  flex-grow: 1;\n"], ["\n  line-height: 1.5;\n  flex-grow: 1;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=alertLink.jsx.map