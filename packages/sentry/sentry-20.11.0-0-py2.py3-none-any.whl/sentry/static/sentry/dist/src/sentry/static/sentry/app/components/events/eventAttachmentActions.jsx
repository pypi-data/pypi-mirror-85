import { __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import Button from 'app/components/button';
import space from 'app/styles/space';
import Confirm from 'app/components/confirm';
import { IconDelete, IconDownload } from 'app/icons';
import withApi from 'app/utils/withApi';
var EventAttachmentActions = /** @class */ (function (_super) {
    __extends(EventAttachmentActions, _super);
    function EventAttachmentActions() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleDelete = function () { return __awaiter(_this, void 0, void 0, function () {
            var _a, api, url, onDelete, attachmentId, _err_1;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, url = _a.url, onDelete = _a.onDelete, attachmentId = _a.attachmentId;
                        if (!url) return [3 /*break*/, 4];
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise(url, {
                                method: 'DELETE',
                            })];
                    case 2:
                        _b.sent();
                        onDelete(attachmentId);
                        return [3 /*break*/, 4];
                    case 3:
                        _err_1 = _b.sent();
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    EventAttachmentActions.prototype.render = function () {
        var url = this.props.url;
        return (<React.Fragment>
        <DownloadButton size="xsmall" icon={<IconDownload size="xs"/>} href={url ? url + "?download=1" : ''} disabled={!url} title={!url ? t('Insufficient permissions to download attachments') : undefined}>
          {t('Download')}
        </DownloadButton>

        <Confirm confirmText={t('Delete')} message={t('Are you sure you wish to delete this file?')} priority="danger" onConfirm={this.handleDelete} disabled={!url}>
          <Button size="xsmall" icon={<IconDelete size="xs"/>} disabled={!url} priority="danger" title={!url ? t('Insufficient permissions to delete attachments') : undefined}/>
        </Confirm>
      </React.Fragment>);
    };
    return EventAttachmentActions;
}(React.Component));
var DownloadButton = styled(Button)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(0.5));
export default withApi(EventAttachmentActions);
var templateObject_1;
//# sourceMappingURL=eventAttachmentActions.jsx.map