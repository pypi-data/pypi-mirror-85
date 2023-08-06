import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import PropTypes from 'prop-types';
import PluginIcon, { ICON_PATHS, DEFAULT_ICON } from 'app/plugins/components/pluginIcon';
var StyledIcon = styled('img')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  height: ", "px;\n  width: ", "px;\n  border-radius: 2px;\n  display: block;\n"], ["\n  height: ", "px;\n  width: ", "px;\n  border-radius: 2px;\n  display: block;\n"])), function (p) { return p.size; }, function (p) { return p.size; });
var Icon = /** @class */ (function (_super) {
    __extends(Icon, _super);
    function Icon() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            imgSrc: _this.props.integration.icon,
        };
        return _this;
    }
    Icon.prototype.render = function () {
        var _this = this;
        var _a = this.props, integration = _a.integration, size = _a.size;
        return (<StyledIcon size={size} src={this.state.imgSrc} onError={function () {
            _this.setState({ imgSrc: ICON_PATHS[integration.provider.key] || DEFAULT_ICON });
        }}/>);
    };
    return Icon;
}(React.Component));
var IntegrationIcon = function (_a) {
    var integration = _a.integration, _b = _a.size, size = _b === void 0 ? 32 : _b;
    return integration.icon ? (<Icon size={size} integration={integration}/>) : (<PluginIcon size={size} pluginId={integration.provider.key}/>);
};
IntegrationIcon.propTypes = {
    integration: PropTypes.object.isRequired,
    size: PropTypes.number,
};
export default IntegrationIcon;
var templateObject_1;
//# sourceMappingURL=integrationIcon.jsx.map