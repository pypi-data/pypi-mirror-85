import { __extends, __rest } from "tslib";
import React from 'react';
/**
 * Wrapper for autoplaying video.
 *
 * Because of react limitations and browser controls we need to
 * use refs.
 *
 * Note, video needs `muted` for `autoplay` to work on Chrome
 * See https://developer.mozilla.org/en-US/docs/Web/HTML/Element/video
 */
var AutoplayVideo = /** @class */ (function (_super) {
    __extends(AutoplayVideo, _super);
    function AutoplayVideo() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.videoRef = React.createRef();
        return _this;
    }
    AutoplayVideo.prototype.componentDidMount = function () {
        if (this.videoRef.current) {
            // Set muted as more browsers allow autoplay with muted video.
            // We can't use the muted prop because of a react bug.
            // https://github.com/facebook/react/issues/10389
            // So we need to set the muted property then trigger play.
            this.videoRef.current.muted = true;
            var playPromise = this.videoRef.current.play();
            // non-chromium Edge and jsdom don't return a promise.
            playPromise === null || playPromise === void 0 ? void 0 : playPromise.catch(function () {
                // Do nothing. Interrupting this playback is fine.
            });
        }
    };
    AutoplayVideo.prototype.render = function () {
        var _a = this.props, className = _a.className, src = _a.src, props = __rest(_a, ["className", "src"]);
        return (<video className={className} ref={this.videoRef} playsInline disablePictureInPicture loop {...props}>
        <source src={src} type="video/mp4"/>
      </video>);
    };
    return AutoplayVideo;
}(React.Component));
export default AutoplayVideo;
//# sourceMappingURL=autoplayVideo.jsx.map