import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import EventDataSection from 'app/components/events/eventDataSection';
import AsyncComponent from 'app/components/asyncComponent';
import LazyLoad from 'app/components/lazyLoad';
import space from 'app/styles/space';
import { t } from 'app/locale';
var RRWebIntegration = /** @class */ (function (_super) {
    __extends(RRWebIntegration, _super);
    function RRWebIntegration() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    RRWebIntegration.prototype.getEndpoints = function () {
        var _a = this.props, orgId = _a.orgId, projectId = _a.projectId, event = _a.event;
        return [
            [
                'attachmentList',
                "/projects/" + orgId + "/" + projectId + "/events/" + event.id + "/attachments/",
                { query: { query: 'rrweb.json' } },
            ],
        ];
    };
    RRWebIntegration.prototype.renderLoading = function () {
        // hide loading indicator
        return null;
    };
    RRWebIntegration.prototype.renderBody = function () {
        var attachmentList = this.state.attachmentList;
        if (!(attachmentList === null || attachmentList === void 0 ? void 0 : attachmentList.length)) {
            return null;
        }
        var attachment = attachmentList[0];
        var _a = this.props, orgId = _a.orgId, projectId = _a.projectId, event = _a.event;
        return (<StyledEventDataSection type="context-replay" title={t('Replay')}>
        <LazyLoad component={function () {
            return import(/* webpackChunkName: "rrwebReplayer" */ './rrwebReplayer').then(function (mod) { return mod.default; });
        }} url={"/api/0/projects/" + orgId + "/" + projectId + "/events/" + event.id + "/attachments/" + attachment.id + "/?download"}/>
      </StyledEventDataSection>);
    };
    return RRWebIntegration;
}(AsyncComponent));
var StyledEventDataSection = styled(EventDataSection)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  overflow: hidden;\n  margin-bottom: ", ";\n"], ["\n  overflow: hidden;\n  margin-bottom: ", ";\n"])), space(3));
export default RRWebIntegration;
var templateObject_1;
//# sourceMappingURL=rrwebIntegration.jsx.map