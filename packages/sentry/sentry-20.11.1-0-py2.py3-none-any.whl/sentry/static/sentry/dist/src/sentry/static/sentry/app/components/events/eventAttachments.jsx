import { __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import { Panel, PanelBody, PanelItem } from 'app/components/panels';
import EventAttachmentActions from 'app/components/events/eventAttachmentActions';
import EventDataSection from 'app/components/events/eventDataSection';
import FileSize from 'app/components/fileSize';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
import AttachmentUrl from 'app/utils/attachmentUrl';
import withApi from 'app/utils/withApi';
import EventAttachmentsCrashReportsNotice from './eventAttachmentsCrashReportsNotice';
var EventAttachments = /** @class */ (function (_super) {
    __extends(EventAttachments, _super);
    function EventAttachments() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            attachmentList: [],
            expanded: false,
        };
        _this.handleDelete = function (deletedAttachmentId) { return __awaiter(_this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                this.setState(function (prevState) { return ({
                    attachmentList: prevState.attachmentList.filter(function (attachment) { return attachment.id !== deletedAttachmentId; }),
                }); });
                return [2 /*return*/];
            });
        }); };
        return _this;
    }
    EventAttachments.prototype.componentDidMount = function () {
        this.fetchData();
    };
    EventAttachments.prototype.componentDidUpdate = function (prevProps) {
        var doFetch = false;
        if (!prevProps.event && this.props.event) {
            // going from having no event to having an event
            doFetch = true;
        }
        else if (this.props.event && this.props.event.id !== prevProps.event.id) {
            doFetch = true;
        }
        if (doFetch) {
            this.fetchData();
        }
    };
    // TODO(dcramer): this API request happens twice, and we need a store for it
    EventAttachments.prototype.fetchData = function () {
        return __awaiter(this, void 0, void 0, function () {
            var event, data, _err_1;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        event = this.props.event;
                        if (!event) {
                            return [2 /*return*/];
                        }
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.props.api.requestPromise("/projects/" + this.props.orgId + "/" + this.props.projectId + "/events/" + event.id + "/attachments/")];
                    case 2:
                        data = _a.sent();
                        this.setState({
                            attachmentList: data,
                        });
                        return [3 /*break*/, 4];
                    case 3:
                        _err_1 = _a.sent();
                        // TODO: Error-handling
                        this.setState({
                            attachmentList: [],
                        });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    EventAttachments.prototype.render = function () {
        var _this = this;
        var _a = this.props, event = _a.event, projectId = _a.projectId, orgId = _a.orgId, location = _a.location;
        var attachmentList = this.state.attachmentList;
        var crashFileStripped = event.metadata.stripped_crash;
        if (!attachmentList.length && !crashFileStripped) {
            return null;
        }
        var title = t('Attachments (%s)', attachmentList.length);
        return (<EventDataSection type="attachments" title={title}>
        {crashFileStripped && (<EventAttachmentsCrashReportsNotice orgSlug={orgId} projectSlug={projectId} groupId={event.groupID} location={location}/>)}

        {attachmentList.length > 0 && (<Panel>
            <PanelBody>
              {attachmentList.map(function (attachment) { return (<PanelItem key={attachment.id} alignItems="center">
                  <AttachmentName>{attachment.name}</AttachmentName>
                  <FileSizeWithGap bytes={attachment.size}/>
                  <AttachmentUrl projectId={projectId} eventId={event.id} attachment={attachment}>
                    {function (url) { return (<EventAttachmentActions url={url} onDelete={_this.handleDelete} attachmentId={attachment.id}/>); }}
                  </AttachmentUrl>
                </PanelItem>); })}
            </PanelBody>
          </Panel>)}
      </EventDataSection>);
    };
    EventAttachments.propTypes = {
        api: PropTypes.object.isRequired,
        event: PropTypes.object.isRequired,
        orgId: PropTypes.string.isRequired,
        projectId: PropTypes.string.isRequired,
    };
    return EventAttachments;
}(React.Component));
export default withApi(EventAttachments);
var AttachmentName = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  flex: 1;\n  margin-right: ", ";\n  font-weight: bold;\n  ", ";\n"], ["\n  flex: 1;\n  margin-right: ", ";\n  font-weight: bold;\n  ", ";\n"])), space(2), overflowEllipsis);
var FileSizeWithGap = styled(FileSize)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(2));
var templateObject_1, templateObject_2;
//# sourceMappingURL=eventAttachments.jsx.map