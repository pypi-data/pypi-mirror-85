import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import PropTypes from 'prop-types';
import ScrollToTop from 'app/views/settings/components/scrollToTop';
import space from 'app/styles/space';
import withLatestContext from 'app/utils/withLatestContext';
var SettingsWrapper = /** @class */ (function (_super) {
    __extends(SettingsWrapper, _super);
    function SettingsWrapper() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        // save current context
        _this.state = {
            lastAppContext: _this.getLastAppContext(),
        };
        _this.handleShouldDisableScrollToTop = function (location, prevLocation) {
            var _a, _b;
            // we do not want to scroll to top when user just perform a search
            return (location.pathname === prevLocation.pathname &&
                ((_a = location.query) === null || _a === void 0 ? void 0 : _a.query) !== ((_b = prevLocation.query) === null || _b === void 0 ? void 0 : _b.query));
        };
        return _this;
    }
    SettingsWrapper.prototype.getChildContext = function () {
        return {
            lastAppContext: this.state.lastAppContext,
        };
    };
    SettingsWrapper.prototype.getLastAppContext = function () {
        var _a = this.props, project = _a.project, organization = _a.organization;
        if (!!project) {
            return 'project';
        }
        if (!!organization) {
            return 'organization';
        }
        return null;
    };
    SettingsWrapper.prototype.render = function () {
        var _a = this.props, location = _a.location, children = _a.children;
        return (<StyledSettingsWrapper>
        <ScrollToTop location={location} disable={this.handleShouldDisableScrollToTop}>
          {children}
        </ScrollToTop>
      </StyledSettingsWrapper>);
    };
    SettingsWrapper.childContextTypes = {
        lastAppContext: PropTypes.oneOf(['project', 'organization']),
    };
    return SettingsWrapper;
}(React.Component));
export default withLatestContext(SettingsWrapper);
var StyledSettingsWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  flex: 1;\n  font-size: ", ";\n  color: ", ";\n  margin-bottom: -", "; /* to account for footer margin top */\n  line-height: 1;\n\n  .messages-container {\n    margin: 0;\n  }\n"], ["\n  display: flex;\n  flex: 1;\n  font-size: ", ";\n  color: ", ";\n  margin-bottom: -", "; /* to account for footer margin top */\n  line-height: 1;\n\n  .messages-container {\n    margin: 0;\n  }\n"])), function (p) { return p.theme.fontSizeLarge; }, function (p) { return p.theme.textColor; }, space(3));
var templateObject_1;
//# sourceMappingURL=settingsWrapper.jsx.map