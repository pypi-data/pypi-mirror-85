import { __extends, __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import { Link } from 'react-router';
import styled from '@emotion/styled';
import { PanelItem } from 'app/components/panels';
import { t } from 'app/locale';
import space from 'app/styles/space';
import PluginIcon from 'app/plugins/components/pluginIcon';
import { openModal } from 'app/actionCreators/modal';
import SentryAppPublishRequestModal from 'app/components/modals/sentryAppPublishRequestModal';
import SentryApplicationRowButtons from './sentryApplicationRowButtons';
var SentryApplicationRow = /** @class */ (function (_super) {
    __extends(SentryApplicationRow, _super);
    function SentryApplicationRow() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handlePublish = function () {
            var app = _this.props.app;
            openModal(function (deps) { return <SentryAppPublishRequestModal app={app} {...deps}/>; });
        };
        return _this;
    }
    Object.defineProperty(SentryApplicationRow.prototype, "isInternal", {
        get: function () {
            return this.props.app.status === 'internal';
        },
        enumerable: false,
        configurable: true
    });
    SentryApplicationRow.prototype.hideStatus = function () {
        //no publishing for internal apps so hide the status on the developer settings page
        return this.isInternal;
    };
    SentryApplicationRow.prototype.renderStatus = function () {
        var app = this.props.app;
        if (this.hideStatus()) {
            return null;
        }
        return <PublishStatus status={app.status}/>;
    };
    SentryApplicationRow.prototype.render = function () {
        var _a = this.props, app = _a.app, organization = _a.organization, onRemoveApp = _a.onRemoveApp;
        return (<SentryAppItem data-test-id={app.slug}>
        <StyledFlex>
          <PluginIcon size={36} pluginId={app.slug}/>
          <SentryAppBox>
            <SentryAppName hideStatus={this.hideStatus()}>
              <SentryAppLink to={"/settings/" + organization.slug + "/developer-settings/" + app.slug + "/"}>
                {app.name}
              </SentryAppLink>
            </SentryAppName>
            <SentryAppDetails>{this.renderStatus()}</SentryAppDetails>
          </SentryAppBox>

          <Box>
            <SentryApplicationRowButtons organization={organization} app={app} onClickRemove={onRemoveApp} onClickPublish={this.handlePublish}/>
          </Box>
        </StyledFlex>
      </SentryAppItem>);
    };
    return SentryApplicationRow;
}(React.PureComponent));
export default SentryApplicationRow;
var Flex = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
var Box = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject([""], [""])));
var SentryAppItem = styled(PanelItem)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  flex-direction: column;\n  padding: 5px;\n"], ["\n  flex-direction: column;\n  padding: 5px;\n"])));
var StyledFlex = styled(Flex)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  justify-content: center;\n  padding: 10px;\n"], ["\n  justify-content: center;\n  padding: 10px;\n"])));
var SentryAppBox = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  padding-left: 15px;\n  padding-right: 15px;\n  flex: 1;\n"], ["\n  padding-left: 15px;\n  padding-right: 15px;\n  flex: 1;\n"])));
var SentryAppDetails = styled(Flex)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  align-items: center;\n  margin-top: 6px;\n  font-size: 0.8em;\n"], ["\n  align-items: center;\n  margin-top: 6px;\n  font-size: 0.8em;\n"])));
var SentryAppName = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  font-weight: bold;\n  margin-top: ", ";\n"], ["\n  font-weight: bold;\n  margin-top: ", ";\n"])), function (p) { return (p.hideStatus ? '10px' : '0px'); });
var SentryAppLink = styled(Link)(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (props) { return props.theme.textColor; });
var CenterFlex = styled(Flex)(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  align-items: center;\n"], ["\n  align-items: center;\n"])));
var PublishStatus = styled(function (_a) {
    var status = _a.status, props = __rest(_a, ["status"]);
    return (<CenterFlex>
    <div {...props}>{t("" + status)}</div>
  </CenterFlex>);
})(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  color: ", ";\n  font-weight: light;\n  margin-right: ", ";\n"], ["\n  color: ",
    ";\n  font-weight: light;\n  margin-right: ", ";\n"])), function (props) {
    return props.status === 'published' ? props.theme.success : props.theme.gray300;
}, space(0.75));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10;
//# sourceMappingURL=index.jsx.map