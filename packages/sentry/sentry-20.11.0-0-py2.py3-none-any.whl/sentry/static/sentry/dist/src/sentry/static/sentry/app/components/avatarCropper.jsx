import { __assign, __extends, __makeTemplateObject } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import { addErrorMessage } from 'app/actionCreators/indicator';
import { AVATAR_URL_MAP } from 'app/constants';
import { t, tct } from 'app/locale';
import Well from 'app/components/well';
var resizerPositions = {
    nw: ['top', 'left'],
    ne: ['top', 'right'],
    se: ['bottom', 'right'],
    sw: ['bottom', 'left'],
};
var AvatarCropper = /** @class */ (function (_super) {
    __extends(AvatarCropper, _super);
    function AvatarCropper() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            file: null,
            objectURL: null,
            mousePosition: { pageX: 0, pageY: 0 },
            resizeDimensions: { top: 0, left: 0, size: 0 },
            resizeDirection: null,
        };
        _this.file = React.createRef();
        _this.canvas = React.createRef();
        _this.image = React.createRef();
        _this.cropContainer = React.createRef();
        // These values must be synced with the avatar endpoint in backend.
        _this.MIN_DIMENSION = 256;
        _this.MAX_DIMENSION = 1024;
        _this.ALLOWED_MIMETYPES = 'image/gif,image/jpeg,image/png';
        _this.onSelectFile = function (ev) {
            var file = ev.target.files && ev.target.files[0];
            // No file selected (e.g. user clicked "cancel")
            if (!file) {
                return;
            }
            if (!/^image\//.test(file.type)) {
                addErrorMessage(t('That is not a supported file type.'));
                return;
            }
            _this.revokeObjectUrl();
            var updateDataUrlState = _this.props.updateDataUrlState;
            var objectURL = window.URL.createObjectURL(file);
            _this.setState({ file: file, objectURL: objectURL }, function () { return updateDataUrlState({ savedDataUrl: null }); });
        };
        _this.revokeObjectUrl = function () {
            return _this.state.objectURL && window.URL.revokeObjectURL(_this.state.objectURL);
        };
        _this.onImageLoad = function () {
            var error = _this.validateImage();
            if (error) {
                _this.revokeObjectUrl();
                _this.setState({ objectURL: null });
                addErrorMessage(error);
                return;
            }
            var image = _this.image.current;
            if (!image) {
                return;
            }
            var dimension = Math.min(image.clientHeight, image.clientWidth);
            var state = { resizeDimensions: { size: dimension, top: 0, left: 0 } };
            _this.setState(state, _this.drawToCanvas);
        };
        _this.updateDimensions = function (ev) {
            var cropContainer = _this.cropContainer.current;
            if (!cropContainer) {
                return;
            }
            var _a = _this.state, mousePosition = _a.mousePosition, resizeDimensions = _a.resizeDimensions;
            var pageY = ev.pageY;
            var pageX = ev.pageX;
            var top = resizeDimensions.top + (pageY - mousePosition.pageY);
            var left = resizeDimensions.left + (pageX - mousePosition.pageX);
            if (top < 0) {
                top = 0;
                pageY = mousePosition.pageY;
            }
            else if (top + resizeDimensions.size > cropContainer.clientHeight) {
                top = cropContainer.clientHeight - resizeDimensions.size;
                pageY = mousePosition.pageY;
            }
            if (left < 0) {
                left = 0;
                pageX = mousePosition.pageX;
            }
            else if (left + resizeDimensions.size > cropContainer.clientWidth) {
                left = cropContainer.clientWidth - resizeDimensions.size;
                pageX = mousePosition.pageX;
            }
            _this.setState(function (state) { return ({
                resizeDimensions: __assign(__assign({}, state.resizeDimensions), { top: top, left: left }),
                mousePosition: { pageX: pageX, pageY: pageY },
            }); });
        };
        _this.onMouseDown = function (ev) {
            ev.preventDefault();
            _this.setState({ mousePosition: { pageY: ev.pageY, pageX: ev.pageX } });
            document.addEventListener('mousemove', _this.updateDimensions);
            document.addEventListener('mouseup', _this.onMouseUp);
        };
        _this.onMouseUp = function (ev) {
            ev.preventDefault();
            document.removeEventListener('mousemove', _this.updateDimensions);
            document.removeEventListener('mouseup', _this.onMouseUp);
            _this.drawToCanvas();
        };
        _this.startResize = function (direction, ev) {
            ev.stopPropagation();
            ev.preventDefault();
            document.addEventListener('mousemove', _this.updateSize);
            document.addEventListener('mouseup', _this.stopResize);
            _this.setState({
                resizeDirection: direction,
                mousePosition: { pageY: ev.pageY, pageX: ev.pageX },
            });
        };
        _this.stopResize = function (ev) {
            ev.stopPropagation();
            ev.preventDefault();
            document.removeEventListener('mousemove', _this.updateSize);
            document.removeEventListener('mouseup', _this.stopResize);
            _this.setState({ resizeDirection: null });
            _this.drawToCanvas();
        };
        _this.updateSize = function (ev) {
            var cropContainer = _this.cropContainer.current;
            if (!cropContainer) {
                return;
            }
            var mousePosition = _this.state.mousePosition;
            var yDiff = ev.pageY - mousePosition.pageY;
            var xDiff = ev.pageX - mousePosition.pageX;
            _this.setState({
                resizeDimensions: _this.getNewDimensions(cropContainer, yDiff, xDiff),
                mousePosition: { pageX: ev.pageX, pageY: ev.pageY },
            });
        };
        // Normalize diff across dimensions so that negative diffs are always making
        // the cropper smaller and positive ones are making the cropper larger
        _this.getDiffNW = function (yDiff, xDiff) {
            return (yDiff - yDiff * 2 + (xDiff - xDiff * 2)) / 2;
        };
        _this.getDiffNE = function (yDiff, xDiff) { return (yDiff - yDiff * 2 + xDiff) / 2; };
        _this.getDiffSW = function (yDiff, xDiff) { return (yDiff + (xDiff - xDiff * 2)) / 2; };
        _this.getDiffSE = function (yDiff, xDiff) { return (yDiff + xDiff) / 2; };
        _this.getNewDimensions = function (container, yDiff, xDiff) {
            var _a = _this.state, oldDimensions = _a.resizeDimensions, resizeDirection = _a.resizeDirection;
            var diff = _this['getDiff' + resizeDirection.toUpperCase()](yDiff, xDiff);
            var height = container.clientHeight - oldDimensions.top;
            var width = container.clientWidth - oldDimensions.left;
            // Depending on the direction, we update different dimensions:
            // nw: size, top, left
            // ne: size, top
            // sw: size, left
            // se: size
            var editingTop = resizeDirection === 'nw' || resizeDirection === 'ne';
            var editingLeft = resizeDirection === 'nw' || resizeDirection === 'sw';
            var newDimensions = {
                top: 0,
                left: 0,
                size: oldDimensions.size + diff,
            };
            if (editingTop) {
                newDimensions.top = oldDimensions.top - diff;
                height = container.clientHeight - newDimensions.top;
            }
            if (editingLeft) {
                newDimensions.left = oldDimensions.left - diff;
                width = container.clientWidth - newDimensions.left;
            }
            if (newDimensions.top < 0) {
                newDimensions.size = newDimensions.size + newDimensions.top;
                if (editingLeft) {
                    newDimensions.left = newDimensions.left - newDimensions.top;
                }
                newDimensions.top = 0;
            }
            if (newDimensions.left < 0) {
                newDimensions.size = newDimensions.size + newDimensions.left;
                if (editingTop) {
                    newDimensions.top = newDimensions.top - newDimensions.left;
                }
                newDimensions.left = 0;
            }
            var maxSize = Math.min(width, height);
            if (newDimensions.size > maxSize) {
                if (editingTop) {
                    newDimensions.top = newDimensions.top + newDimensions.size - maxSize;
                }
                if (editingLeft) {
                    newDimensions.left = newDimensions.left + newDimensions.size - maxSize;
                }
                newDimensions.size = maxSize;
            }
            else if (newDimensions.size < _this.MIN_DIMENSION) {
                if (editingTop) {
                    newDimensions.top = newDimensions.top + newDimensions.size - _this.MIN_DIMENSION;
                }
                if (editingLeft) {
                    newDimensions.left = newDimensions.left + newDimensions.size - _this.MIN_DIMENSION;
                }
                newDimensions.size = _this.MIN_DIMENSION;
            }
            return __assign(__assign({}, oldDimensions), newDimensions);
        };
        _this.uploadClick = function (ev) {
            ev.preventDefault();
            _this.file.current && _this.file.current.click();
        };
        return _this;
    }
    AvatarCropper.prototype.componentWillUnmount = function () {
        this.revokeObjectUrl();
    };
    AvatarCropper.prototype.validateImage = function () {
        var img = this.image.current;
        if (!img) {
            return null;
        }
        if (img.naturalWidth < this.MIN_DIMENSION || img.naturalHeight < this.MIN_DIMENSION) {
            return tct('Please upload an image larger than [size]px by [size]px.', {
                size: this.MIN_DIMENSION - 1,
            });
        }
        if (img.naturalWidth > this.MAX_DIMENSION || img.naturalHeight > this.MAX_DIMENSION) {
            return tct('Please upload an image smaller than [size]px by [size]px.', {
                size: this.MAX_DIMENSION,
            });
        }
        return null;
    };
    AvatarCropper.prototype.drawToCanvas = function () {
        var canvas = this.canvas.current;
        if (!canvas) {
            return;
        }
        var image = this.image.current;
        if (!image) {
            return;
        }
        var _a = this.state.resizeDimensions, left = _a.left, top = _a.top, size = _a.size;
        // Calculate difference between natural dimensions and rendered dimensions
        var ratio = (image.naturalHeight / image.clientHeight +
            image.naturalWidth / image.clientWidth) /
            2;
        canvas.width = size * ratio;
        canvas.height = size * ratio;
        canvas
            .getContext('2d')
            .drawImage(image, left * ratio, top * ratio, size * ratio, size * ratio, 0, 0, size * ratio, size * ratio);
        this.props.updateDataUrlState({ dataUrl: canvas.toDataURL() });
    };
    Object.defineProperty(AvatarCropper.prototype, "imageSrc", {
        get: function () {
            var _a;
            var _b = this.props, savedDataUrl = _b.savedDataUrl, model = _b.model, type = _b.type;
            var uuid = (_a = model.avatar) === null || _a === void 0 ? void 0 : _a.avatarUuid;
            var photoUrl = uuid && "/" + (AVATAR_URL_MAP[type] || 'avatar') + "/" + uuid + "/";
            return savedDataUrl || this.state.objectURL || photoUrl;
        },
        enumerable: false,
        configurable: true
    });
    AvatarCropper.prototype.renderImageCrop = function () {
        var _this = this;
        var src = this.imageSrc;
        if (!src) {
            return null;
        }
        var _a = this.state, resizeDimensions = _a.resizeDimensions, resizeDirection = _a.resizeDirection;
        var style = {
            top: resizeDimensions.top,
            left: resizeDimensions.left,
            width: resizeDimensions.size,
            height: resizeDimensions.size,
        };
        return (<ImageCropper resizeDirection={resizeDirection}>
        <CropContainer ref={this.cropContainer}>
          <img ref={this.image} src={src} onLoad={this.onImageLoad} onDragStart={function (e) { return e.preventDefault(); }}/>
          <Cropper style={style} onMouseDown={this.onMouseDown}>
            {Object.keys(resizerPositions).map(function (pos) { return (<Resizer key={pos} position={pos} onMouseDown={_this.startResize.bind(_this, pos)}/>); })}
          </Cropper>
        </CropContainer>
      </ImageCropper>);
    };
    AvatarCropper.prototype.render = function () {
        var src = this.imageSrc;
        var upload = <a onClick={this.uploadClick}/>;
        var uploader = (<Well hasImage centered>
        <p>{tct('[upload:Upload a photo] to get started.', { upload: upload })}</p>
      </Well>);
        return (<React.Fragment>
        {!src && uploader}
        {src && <HiddenCanvas ref={this.canvas}/>}
        {this.renderImageCrop()}
        <div className="form-group">
          {src && <a onClick={this.uploadClick}>{t('Change Photo')}</a>}
          <UploadInput ref={this.file} type="file" accept={this.ALLOWED_MIMETYPES} onChange={this.onSelectFile}/>
        </div>
      </React.Fragment>);
    };
    AvatarCropper.propTypes = {
        model: PropTypes.object.isRequired,
        updateDataUrlState: PropTypes.func.isRequired,
        type: PropTypes.oneOf(['user', 'team', 'organization', 'project']),
        savedDataUrl: PropTypes.string,
    };
    return AvatarCropper;
}(React.Component));
export default AvatarCropper;
var UploadInput = styled('input')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: absolute;\n  opacity: 0;\n"], ["\n  position: absolute;\n  opacity: 0;\n"])));
var ImageCropper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  cursor: ", ";\n  text-align: center;\n  margin-bottom: 20px;\n  background-size: 20px 20px;\n  background-position: 0 0, 0 10px, 10px -10px, -10px 0px;\n  background-color: ", ";\n  background-image: linear-gradient(45deg, #eee 25%, rgba(0, 0, 0, 0) 25%),\n    linear-gradient(-45deg, #eee 25%, rgba(0, 0, 0, 0) 25%),\n    linear-gradient(45deg, rgba(0, 0, 0, 0) 75%, #eee 75%),\n    linear-gradient(-45deg, rgba(0, 0, 0, 0) 75%, #eee 75%);\n"], ["\n  cursor: ", ";\n  text-align: center;\n  margin-bottom: 20px;\n  background-size: 20px 20px;\n  background-position: 0 0, 0 10px, 10px -10px, -10px 0px;\n  background-color: ", ";\n  background-image: linear-gradient(45deg, #eee 25%, rgba(0, 0, 0, 0) 25%),\n    linear-gradient(-45deg, #eee 25%, rgba(0, 0, 0, 0) 25%),\n    linear-gradient(45deg, rgba(0, 0, 0, 0) 75%, #eee 75%),\n    linear-gradient(-45deg, rgba(0, 0, 0, 0) 75%, #eee 75%);\n"])), function (p) { return (p.resizeDirection ? p.resizeDirection + "-resize" : 'default'); }, function (p) { return p.theme.background; });
var CropContainer = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: inline-block;\n  position: relative;\n  max-width: 100%;\n"], ["\n  display: inline-block;\n  position: relative;\n  max-width: 100%;\n"])));
var Cropper = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  position: absolute;\n  border: 2px dashed ", ";\n"], ["\n  position: absolute;\n  border: 2px dashed ", ";\n"])), function (p) { return p.theme.gray300; });
var Resizer = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  border-radius: 5px;\n  width: 10px;\n  height: 10px;\n  position: absolute;\n  background-color: ", ";\n  cursor: ", ";\n  ", "\n"], ["\n  border-radius: 5px;\n  width: 10px;\n  height: 10px;\n  position: absolute;\n  background-color: ", ";\n  cursor: ", ";\n  ", "\n"])), function (p) { return p.theme.gray300; }, function (p) { return p.position + "-resize"; }, function (p) { return resizerPositions[p.position].map(function (pos) { return pos + ": -5px;"; }); });
var HiddenCanvas = styled('canvas')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  display: none;\n"], ["\n  display: none;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=avatarCropper.jsx.map