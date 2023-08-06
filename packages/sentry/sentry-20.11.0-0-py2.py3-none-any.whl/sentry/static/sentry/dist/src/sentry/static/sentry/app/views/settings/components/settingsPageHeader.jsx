import { __extends, __makeTemplateObject, __rest } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import space from 'app/styles/space';
import { HeaderTitle } from 'app/styles/organization';
var SettingsPageHeading = /** @class */ (function (_super) {
    __extends(SettingsPageHeading, _super);
    function SettingsPageHeading() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    SettingsPageHeading.prototype.render = function () {
        var _a = this.props, icon = _a.icon, title = _a.title, action = _a.action, tabs = _a.tabs, noTitleStyles = _a.noTitleStyles, props = __rest(_a, ["icon", "title", "action", "tabs", "noTitleStyles"]);
        return (<div {...props}>
        <TitleAndActions>
          {icon && <Icon>{icon}</Icon>}
          {title && (<Title tabs={tabs} styled={noTitleStyles}>
              <HeaderTitle>{title}</HeaderTitle>
            </Title>)}
          {action && <Action tabs={tabs}>{action}</Action>}
        </TitleAndActions>

        {tabs && <div>{tabs}</div>}
      </div>);
    };
    SettingsPageHeading.propTypes = {
        icon: PropTypes.node,
        title: PropTypes.node.isRequired,
        action: PropTypes.node,
        tabs: PropTypes.node,
        // Disables font styles in the title. Allows for more custom titles.
        noTitleStyles: PropTypes.bool,
    };
    SettingsPageHeading.defaultProps = {
        noTitleStyles: false,
    };
    return SettingsPageHeading;
}(React.Component));
var TitleAndActions = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var Title = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  ", ";\n  margin: ", ";\n  flex: 1;\n"], ["\n  ",
    ";\n  margin: ",
    ";\n  flex: 1;\n"])), function (p) {
    return !p.styled &&
        "\n    font-size: 20px;\n    font-weight: bold;";
}, function (p) {
    return p.tabs
        ? space(4) + " " + space(2) + " " + space(2) + " 0"
        : space(4) + " " + space(2) + " " + space(4) + " 0";
});
var Icon = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(1));
var Action = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), function (p) { return (p.tabs ? "margin-top: " + space(2) : null); });
var StyledSettingsPageHeading = styled(SettingsPageHeading)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  font-size: 14px;\n  margin-top: -", ";\n"], ["\n  font-size: 14px;\n  margin-top: -", ";\n"])), space(4));
export default StyledSettingsPageHeading;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=settingsPageHeader.jsx.map