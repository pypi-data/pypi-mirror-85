import { __extends, __makeTemplateObject, __read } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import PlatformIcon from 'platformicons';
import Line from 'app/components/events/interfaces/frame/line';
import { t } from 'app/locale';
import { parseAddress, getImageRange } from 'app/components/events/interfaces/utils';
var defaultProps = {
    includeSystemFrames: true,
    expandFirstFrame: true,
};
var StacktraceContent = /** @class */ (function (_super) {
    __extends(StacktraceContent, _super);
    function StacktraceContent() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            showingAbsoluteAddresses: false,
            showCompleteFunctionName: false,
        };
        _this.renderOmittedFrames = function (firstFrameOmitted, lastFrameOmitted) {
            var props = {
                className: 'frame frames-omitted',
                key: 'omitted',
            };
            var text = t('Frames %d until %d were omitted and not available.', firstFrameOmitted, lastFrameOmitted);
            return <li {...props}>{text}</li>;
        };
        _this.frameIsVisible = function (frame, nextFrame) {
            var includeSystemFrames = _this.props.includeSystemFrames;
            return (includeSystemFrames ||
                frame.inApp ||
                (nextFrame && nextFrame.inApp) ||
                // the last non-app frame
                (!frame.inApp && !nextFrame));
        };
        _this.handleToggleAddresses = function (event) {
            event.stopPropagation(); // to prevent collapsing if collapsable
            _this.setState(function (prevState) { return ({
                showingAbsoluteAddresses: !prevState.showingAbsoluteAddresses,
            }); });
        };
        _this.handleToggleFunctionName = function (event) {
            event.stopPropagation(); // to prevent collapsing if collapsable
            _this.setState(function (prevState) { return ({
                showCompleteFunctionName: !prevState.showCompleteFunctionName,
            }); });
        };
        return _this;
    }
    StacktraceContent.prototype.isFrameAfterLastNonApp = function () {
        var data = this.props.data;
        var frames = data.frames;
        if (!frames.length || frames.length < 2) {
            return false;
        }
        var lastFrame = frames[frames.length - 1];
        var penultimateFrame = frames[frames.length - 2];
        return penultimateFrame.inApp && !lastFrame.inApp;
    };
    StacktraceContent.prototype.findImageForAddress = function (address) {
        var _a, _b;
        var images = (_b = (_a = this.props.event.entries.find(function (entry) { return entry.type === 'debugmeta'; })) === null || _a === void 0 ? void 0 : _a.data) === null || _b === void 0 ? void 0 : _b.images;
        return images && address
            ? images.find(function (img) {
                var _a = __read(getImageRange(img), 2), startAddress = _a[0], endAddress = _a[1];
                return address >= startAddress && address < endAddress;
            })
            : null;
    };
    StacktraceContent.prototype.getClassName = function () {
        var _a = this.props, _b = _a.className, className = _b === void 0 ? '' : _b, includeSystemFrames = _a.includeSystemFrames;
        if (includeSystemFrames) {
            return className + " traceback full-traceback";
        }
        return className + " traceback in-app-traceback";
    };
    StacktraceContent.prototype.render = function () {
        var _this = this;
        var _a = this.props, data = _a.data, event = _a.event, newestFirst = _a.newestFirst, expandFirstFrame = _a.expandFirstFrame, platform = _a.platform, includeSystemFrames = _a.includeSystemFrames;
        var _b = this.state, showingAbsoluteAddresses = _b.showingAbsoluteAddresses, showCompleteFunctionName = _b.showCompleteFunctionName;
        var firstFrameOmitted = null;
        var lastFrameOmitted = null;
        if (data.framesOmitted) {
            firstFrameOmitted = data.framesOmitted[0];
            lastFrameOmitted = data.framesOmitted[1];
        }
        var lastFrameIdx = null;
        data.frames.forEach(function (frame, frameIdx) {
            if (frame.inApp) {
                lastFrameIdx = frameIdx;
            }
        });
        if (lastFrameIdx === null) {
            lastFrameIdx = data.frames.length - 1;
        }
        var frames = [];
        var nRepeats = 0;
        var maxLengthOfAllRelativeAddresses = data.frames.reduce(function (maxLengthUntilThisPoint, frame) {
            var correspondingImage = _this.findImageForAddress(frame.instructionAddr);
            try {
                var relativeAddress = (parseAddress(frame.instructionAddr) -
                    parseAddress(correspondingImage.image_addr)).toString(16);
                return maxLengthUntilThisPoint > relativeAddress.length
                    ? maxLengthUntilThisPoint
                    : relativeAddress.length;
            }
            catch (_a) {
                return maxLengthUntilThisPoint;
            }
        }, 0);
        var isFrameAfterLastNonApp = this.isFrameAfterLastNonApp();
        data.frames.forEach(function (frame, frameIdx) {
            var prevFrame = data.frames[frameIdx - 1];
            var nextFrame = data.frames[frameIdx + 1];
            var repeatedFrame = nextFrame &&
                frame.lineNo === nextFrame.lineNo &&
                frame.instructionAddr === nextFrame.instructionAddr &&
                frame.package === nextFrame.package &&
                frame.module === nextFrame.module &&
                frame.function === nextFrame.function;
            if (repeatedFrame) {
                nRepeats++;
            }
            if (_this.frameIsVisible(frame, nextFrame) && !repeatedFrame) {
                var image = _this.findImageForAddress(frame.instructionAddr);
                frames.push(<Line key={frameIdx} event={event} data={frame} isExpanded={expandFirstFrame && lastFrameIdx === frameIdx} emptySourceNotation={lastFrameIdx === frameIdx && frameIdx === 0} isOnlyFrame={data.frames.length === 1} nextFrame={nextFrame} prevFrame={prevFrame} platform={platform} timesRepeated={nRepeats} showingAbsoluteAddress={showingAbsoluteAddresses} onAddressToggle={_this.handleToggleAddresses} image={image} maxLengthOfRelativeAddress={maxLengthOfAllRelativeAddresses} registers={{}} //TODO: Fix registers
                 isFrameAfterLastNonApp={isFrameAfterLastNonApp} includeSystemFrames={includeSystemFrames} onFunctionNameToggle={_this.handleToggleFunctionName} showCompleteFunctionName={showCompleteFunctionName}/>);
            }
            if (!repeatedFrame) {
                nRepeats = 0;
            }
            if (frameIdx === firstFrameOmitted) {
                frames.push(_this.renderOmittedFrames(firstFrameOmitted, lastFrameOmitted));
            }
        });
        if (frames.length > 0 && data.registers) {
            var lastFrame = frames.length - 1;
            frames[lastFrame] = React.cloneElement(frames[lastFrame], {
                registers: data.registers,
            });
        }
        if (newestFirst) {
            frames.reverse();
        }
        var className = this.getClassName();
        return (<Wrapper className={className}>
        <StyledPlatformIcon platform={platform} size="20px" style={{ borderRadius: '3px 0 0 3px' }}/>
        <StyledList>{frames}</StyledList>
      </Wrapper>);
    };
    StacktraceContent.defaultProps = {
        includeSystemFrames: true,
        expandFirstFrame: true,
    };
    return StacktraceContent;
}(React.Component));
export default StacktraceContent;
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
var StyledPlatformIcon = styled(PlatformIcon)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  position: absolute;\n  top: -1px;\n  left: -20px;\n"], ["\n  position: absolute;\n  top: -1px;\n  left: -20px;\n"])));
var StyledList = styled('ul')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  list-style: none;\n"], ["\n  list-style: none;\n"])));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=stacktraceContent.jsx.map