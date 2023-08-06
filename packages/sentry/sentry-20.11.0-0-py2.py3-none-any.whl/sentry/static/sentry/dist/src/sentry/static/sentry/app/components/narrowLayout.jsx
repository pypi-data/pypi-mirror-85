import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import PropTypes from 'prop-types';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import { logout } from 'app/actionCreators/account';
import { Client } from 'app/api';
import { IconSentry } from 'app/icons';
var NarrowLayout = /** @class */ (function (_super) {
    __extends(NarrowLayout, _super);
    function NarrowLayout() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.api = new Client();
        _this.handleLogout = function () {
            logout(_this.api).then(function () { return window.location.assign('/auth/login'); });
        };
        return _this;
    }
    NarrowLayout.prototype.UNSAFE_componentWillMount = function () {
        document.body.classList.add('narrow');
    };
    NarrowLayout.prototype.componentWillUnmount = function () {
        this.api.clear();
        document.body.classList.remove('narrow');
    };
    NarrowLayout.prototype.render = function () {
        return (<div className="app">
        <div className="pattern-bg"/>
        <div className="container" style={{ maxWidth: this.props.maxWidth }}>
          <div className="box box-modal">
            <div className="box-header">
              <a href="/">
                <IconSentry size="lg"/>
              </a>
              {this.props.showLogout && (<a className="logout pull-right" onClick={this.handleLogout}>
                  <Logout>{t('Sign out')}</Logout>
                </a>)}
            </div>
            <div className="box-content with-padding">{this.props.children}</div>
          </div>
        </div>
      </div>);
    };
    NarrowLayout.propTypes = {
        showLogout: PropTypes.bool,
        maxWidth: PropTypes.string,
    };
    return NarrowLayout;
}(React.Component));
var Logout = styled('span')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-size: 16px;\n"], ["\n  font-size: 16px;\n"])));
export default NarrowLayout;
var templateObject_1;
//# sourceMappingURL=narrowLayout.jsx.map