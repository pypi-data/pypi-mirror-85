import { __extends, __makeTemplateObject } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import { IconCopy, IconRefresh } from 'app/icons';
import space from 'app/styles/space';
import AutoSelectText from 'app/components/autoSelectText';
import Button from 'app/components/button';
import Clipboard from 'app/components/clipboard';
import Confirm from 'app/components/confirm';
import DropdownLink from 'app/components/dropdownLink';
import LoadingIndicator from 'app/components/loadingIndicator';
import Switch from 'app/components/switch';
import overflowEllipsis from 'app/styles/overflowEllipsis';
var ShareUrlContainer = /** @class */ (function (_super) {
    __extends(ShareUrlContainer, _super);
    function ShareUrlContainer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        // Select URL when its container is clicked
        _this.handleCopyClick = function () {
            var _a;
            (_a = _this.urlRef) === null || _a === void 0 ? void 0 : _a.selectText();
        };
        _this.handleUrlMount = function (ref) {
            var _a;
            _this.urlRef = ref;
            // Always select url if it's available
            (_a = _this.urlRef) === null || _a === void 0 ? void 0 : _a.selectText();
        };
        return _this;
    }
    ShareUrlContainer.prototype.render = function () {
        var _this = this;
        var _a = this.props, shareUrl = _a.shareUrl, onConfirming = _a.onConfirming, onCancel = _a.onCancel, onConfirm = _a.onConfirm;
        return (<UrlContainer>
        <TextContainer>
          <StyledAutoSelectText ref={function (ref) { return _this.handleUrlMount(ref); }}>
            {shareUrl}
          </StyledAutoSelectText>
        </TextContainer>

        <Clipboard hideUnsupported value={shareUrl}>
          <ClipboardButton title={t('Copy to clipboard')} borderless size="xsmall" onClick={this.handleCopyClick} icon={<IconCopy />}/>
        </Clipboard>

        <Confirm message={t('You are about to regenerate a new shared URL. Your previously shared URL will no longer work. Do you want to continue?')} onCancel={onCancel} onConfirming={onConfirming} onConfirm={onConfirm}>
          <ReshareButton title={t('Generate new URL')} borderless size="xsmall" icon={<IconRefresh />}/>
        </Confirm>
      </UrlContainer>);
    };
    return ShareUrlContainer;
}(React.Component));
var ShareIssue = /** @class */ (function (_super) {
    __extends(ShareIssue, _super);
    function ShareIssue() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.hasConfirmModal = false;
        _this.handleToggleShare = function (e) {
            e.preventDefault();
            _this.props.onToggle();
        };
        _this.handleOpen = function () {
            var _a = _this.props, loading = _a.loading, isShared = _a.isShared, onToggle = _a.onToggle;
            if (!loading && !isShared) {
                // Starts sharing as soon as dropdown is opened
                onToggle();
            }
        };
        // State of confirm modal so we can keep dropdown menu opn
        _this.handleConfirmCancel = function () {
            _this.hasConfirmModal = false;
        };
        _this.handleConfirmReshare = function () {
            _this.hasConfirmModal = true;
        };
        return _this;
    }
    ShareIssue.prototype.render = function () {
        var _this = this;
        var _a = this.props, loading = _a.loading, isShared = _a.isShared, shareUrl = _a.shareUrl, onReshare = _a.onReshare;
        return (<DropdownLink className="share-issue btn-sm btn btn-default" shouldIgnoreClickOutside={function () { return _this.hasConfirmModal; }} title={<DropdownTitleContent>
            <IndicatorDot isShared={isShared}/>
            {t('Share')}
          </DropdownTitleContent>} onOpen={this.handleOpen} keepMenuOpen>
        <DropdownContent>
          <Header>
            <Title>{t('Enable public share link')}</Title>
            <Switch isActive={isShared} size="sm" toggle={this.handleToggleShare}/>
          </Header>

          {loading && (<LoadingContainer>
              <LoadingIndicator mini/>
            </LoadingContainer>)}

          {!loading && isShared && shareUrl && (<ShareUrlContainer shareUrl={shareUrl} onCancel={this.handleConfirmCancel} onConfirming={this.handleConfirmReshare} onConfirm={onReshare}/>)}
        </DropdownContent>
      </DropdownLink>);
    };
    ShareIssue.propTypes = {
        loading: PropTypes.bool.isRequired,
        isShared: PropTypes.bool,
        shareUrl: PropTypes.string,
        onToggle: PropTypes.func.isRequired,
        onReshare: PropTypes.func.isRequired,
    };
    return ShareIssue;
}(React.Component));
export default ShareIssue;
var UrlContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: stretch;\n  border: 1px solid ", ";\n  border-radius: ", ";\n"], ["\n  display: flex;\n  align-items: stretch;\n  border: 1px solid ", ";\n  border-radius: ", ";\n"])), function (p) { return p.theme.border; }, space(0.5));
var LoadingContainer = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  justify-content: center;\n"], ["\n  display: flex;\n  justify-content: center;\n"])));
var DropdownTitleContent = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  margin-right: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  margin-right: ", ";\n"])), space(0.5));
var DropdownContent = styled('li')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  padding: ", " ", ";\n\n  > div:not(:last-of-type) {\n    margin-bottom: ", ";\n  }\n"], ["\n  padding: ", " ", ";\n\n  > div:not(:last-of-type) {\n    margin-bottom: ", ";\n  }\n"])), space(1.5), space(2), space(1.5));
var Header = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n"], ["\n  display: flex;\n  justify-content: space-between;\n"])));
var Title = styled('h6')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  margin: 0;\n  padding-right: ", ";\n  white-space: nowrap;\n"], ["\n  margin: 0;\n  padding-right: ", ";\n  white-space: nowrap;\n"])), space(4));
var IndicatorDot = styled('span')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  display: inline-block;\n  margin-right: ", ";\n  border-radius: 50%;\n  width: 10px;\n  height: 10px;\n  background: ", ";\n"], ["\n  display: inline-block;\n  margin-right: ", ";\n  border-radius: 50%;\n  width: 10px;\n  height: 10px;\n  background: ", ";\n"])), space(0.5), function (p) { return (p.isShared ? p.theme.green300 : p.theme.border); });
var StyledAutoSelectText = styled(AutoSelectText)(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  flex: 1;\n  padding: ", " 0 ", " ", ";\n  ", "\n"], ["\n  flex: 1;\n  padding: ", " 0 ", " ", ";\n  ", "\n"])), space(0.5), space(0.5), space(0.75), overflowEllipsis);
var TextContainer = styled('div')(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  position: relative;\n  display: flex;\n  flex: 1;\n  background-color: transparent;\n  border-right: 1px solid ", ";\n  max-width: 288px;\n"], ["\n  position: relative;\n  display: flex;\n  flex: 1;\n  background-color: transparent;\n  border-right: 1px solid ", ";\n  max-width: 288px;\n"])), function (p) { return p.theme.border; });
var ClipboardButton = styled(Button)(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  border-radius: 0;\n  border-right: 1px solid ", ";\n  height: 100%;\n\n  &:hover {\n    border-right: 1px solid ", ";\n  }\n"], ["\n  border-radius: 0;\n  border-right: 1px solid ", ";\n  height: 100%;\n\n  &:hover {\n    border-right: 1px solid ", ";\n  }\n"])), function (p) { return p.theme.border; }, function (p) { return p.theme.border; });
var ReshareButton = styled(Button)(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  height: 100%;\n"], ["\n  height: 100%;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11;
//# sourceMappingURL=shareIssue.jsx.map