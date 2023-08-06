import { __assign, __extends, __makeTemplateObject, __rest } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import classNames from 'classnames';
import * as qs from 'query-string';
import styled from '@emotion/styled';
import LetterAvatar from 'app/components/letterAvatar';
import Tooltip from 'app/components/tooltip';
import { imageStyle } from './styles';
import Gravatar from './gravatar';
var DEFAULT_GRAVATAR_SIZE = 64;
var ALLOWED_SIZES = [20, 32, 36, 48, 52, 64, 80, 96, 120];
var DEFAULT_REMOTE_SIZE = 120;
var defaultProps = {
    // No default size to ease transition from CSS defined sizes
    // size: 64,
    style: {},
    /**
     * Enable to display tooltips.
     */
    hasTooltip: false,
    /**
     * The type of avatar being rendered.
     */
    type: 'letter_avatar',
    /**
     * Path to uploaded avatar (differs based on model type)
     */
    uploadPath: 'avatar',
    /**
     * Should avatar be round instead of a square
     */
    round: false,
};
var BaseAvatar = /** @class */ (function (_super) {
    __extends(BaseAvatar, _super);
    function BaseAvatar(props) {
        var _this = _super.call(this, props) || this;
        _this.getRemoteImageSize = function () {
            var _a = _this.props, remoteImageSize = _a.remoteImageSize, size = _a.size;
            // Try to make sure remote image size is >= requested size
            // If requested size > allowed size then use the largest allowed size
            var allowed = size &&
                (ALLOWED_SIZES.find(function (allowedSize) { return allowedSize >= size; }) ||
                    ALLOWED_SIZES[ALLOWED_SIZES.length - 1]);
            return remoteImageSize || allowed || DEFAULT_GRAVATAR_SIZE;
        };
        _this.buildUploadUrl = function () {
            var _a = _this.props, uploadPath = _a.uploadPath, uploadId = _a.uploadId;
            return "/" + (uploadPath || 'avatar') + "/" + uploadId + "/?" + qs.stringify({
                s: DEFAULT_REMOTE_SIZE,
            });
        };
        _this.handleLoad = function () {
            _this.setState({ showBackupAvatar: false, hasLoaded: true });
        };
        _this.handleError = function () {
            _this.setState({ showBackupAvatar: true, loadError: true, hasLoaded: true });
        };
        _this.renderImg = function () {
            if (_this.state.loadError) {
                return null;
            }
            var _a = _this.props, type = _a.type, round = _a.round, gravatarId = _a.gravatarId;
            var eventProps = {
                onError: _this.handleError,
                onLoad: _this.handleLoad,
            };
            if (type === 'gravatar') {
                return (<Gravatar placeholder={_this.props.default} gravatarId={gravatarId} round={round} remoteSize={DEFAULT_REMOTE_SIZE} {...eventProps}/>);
            }
            if (type === 'upload') {
                return <Image round={round} src={_this.buildUploadUrl()} {...eventProps}/>;
            }
            return _this.renderLetterAvatar();
        };
        _this.state = {
            showBackupAvatar: false,
            hasLoaded: props.type !== 'upload',
            loadError: false,
        };
        return _this;
    }
    BaseAvatar.prototype.renderLetterAvatar = function () {
        var _a = this.props, title = _a.title, letterId = _a.letterId, round = _a.round;
        return <LetterAvatar round={round} displayName={title} identifier={letterId}/>;
    };
    BaseAvatar.prototype.render = function () {
        var _a = this.props, className = _a.className, style = _a.style, round = _a.round, hasTooltip = _a.hasTooltip, size = _a.size, tooltip = _a.tooltip, tooltipOptions = _a.tooltipOptions, forwardedRef = _a.forwardedRef, props = __rest(_a, ["className", "style", "round", "hasTooltip", "size", "tooltip", "tooltipOptions", "forwardedRef"]);
        var sizeStyle = {};
        if (size) {
            sizeStyle = {
                width: size + "px",
                height: size + "px",
            };
        }
        return (<Tooltip title={tooltip} disabled={!hasTooltip} {...tooltipOptions}>
        <StyledBaseAvatar ref={forwardedRef} loaded={this.state.hasLoaded} className={classNames('avatar', className)} round={!!round} style={__assign(__assign({}, sizeStyle), style)} {...props}>
          {this.state.showBackupAvatar && this.renderLetterAvatar()}
          {this.renderImg()}
        </StyledBaseAvatar>
      </Tooltip>);
    };
    BaseAvatar.propTypes = {
        size: PropTypes.number,
        /**
         * This is the size of the remote image to request.
         */
        remoteImageSize: PropTypes.oneOf(ALLOWED_SIZES),
        /**
         * Default gravatar to display
         */
        default: PropTypes.string,
        /**
         * Enable to display tooltips.
         */
        hasTooltip: PropTypes.bool,
        /**
         * The type of avatar being rendered.
         */
        type: PropTypes.string,
        /**
         * Path to uploaded avatar (differs based on model type)
         */
        uploadPath: PropTypes.oneOf([
            'avatar',
            'team-avatar',
            'organization-avatar',
            'project-avatar',
        ]),
        uploadId: PropTypes.string,
        gravatarId: PropTypes.string,
        letterId: PropTypes.string,
        title: PropTypes.string,
        /**
         * The content for the tooltip. Requires hasTooltip to display
         */
        tooltip: PropTypes.oneOfType([PropTypes.string, PropTypes.element]),
        /**
         * Additional props for the tooltip
         */
        tooltipOptions: PropTypes.object,
        /**
         * Should avatar be round instead of a square
         */
        round: PropTypes.bool,
    };
    BaseAvatar.defaultProps = defaultProps;
    return BaseAvatar;
}(React.Component));
export default BaseAvatar;
// Note: Avatar will not always be a child of a flex layout, but this seems like a
// sensible default.
var StyledBaseAvatar = styled('span')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  flex-shrink: 0;\n  ", ";\n  ", ";\n"], ["\n  flex-shrink: 0;\n  ", ";\n  ", ";\n"])), function (p) { return !p.loaded && 'background-color: rgba(200, 200, 200, 0.1);'; }, function (p) { return p.round && 'border-radius: 100%;'; });
var Image = styled('img')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), imageStyle);
var templateObject_1, templateObject_2;
//# sourceMappingURL=baseAvatar.jsx.map