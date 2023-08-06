import { __extends, __makeTemplateObject } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import * as qs from 'query-string';
import styled from '@emotion/styled';
import ConfigStore from 'app/stores/configStore';
import { callIfFunction } from 'app/utils/callIfFunction';
import { imageStyle } from './styles';
var Gravatar = /** @class */ (function (_super) {
    __extends(Gravatar, _super);
    function Gravatar() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            MD5: undefined,
        };
        _this._isMounted = false;
        _this.buildGravatarUrl = function () {
            var _a = _this.props, gravatarId = _a.gravatarId, remoteSize = _a.remoteSize, placeholder = _a.placeholder;
            var url = ConfigStore.getConfig().gravatarBaseUrl + '/avatar/';
            var md5 = callIfFunction(_this.state.MD5, gravatarId);
            if (md5) {
                url += md5;
            }
            var query = {
                s: remoteSize || undefined,
                // If gravatar is not found we need the request to return an error,
                // otherwise error handler will not trigger and avatar will not have a display a LetterAvatar backup.
                d: placeholder || '404',
            };
            url += '?' + qs.stringify(query);
            return url;
        };
        return _this;
    }
    Gravatar.prototype.componentDidMount = function () {
        var _this = this;
        this._isMounted = true;
        import(/* webpackChunkName: "MD5" */ 'crypto-js/md5')
            .then(function (mod) { return mod.default; })
            .then(function (MD5) {
            if (!_this._isMounted) {
                return;
            }
            _this.setState({ MD5: MD5 });
        });
    };
    Gravatar.prototype.componentWillUnmount = function () {
        // Need to track mounted state because `React.isMounted()` is deprecated and because of
        // dynamic imports
        this._isMounted = false;
    };
    Gravatar.prototype.render = function () {
        if (!this.state.MD5) {
            return null;
        }
        var _a = this.props, round = _a.round, onError = _a.onError, onLoad = _a.onLoad;
        return (<Image round={round} src={this.buildGravatarUrl()} onLoad={onLoad} onError={onError}/>);
    };
    Gravatar.propTypes = {
        remoteSize: PropTypes.number,
        gravatarId: PropTypes.string,
        placeholder: PropTypes.string,
        round: PropTypes.bool,
    };
    return Gravatar;
}(React.Component));
export default Gravatar;
var Image = styled('img')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), imageStyle);
var templateObject_1;
//# sourceMappingURL=gravatar.jsx.map