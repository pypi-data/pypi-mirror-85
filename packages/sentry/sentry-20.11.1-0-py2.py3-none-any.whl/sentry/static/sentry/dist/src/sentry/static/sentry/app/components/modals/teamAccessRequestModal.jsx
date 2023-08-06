import { __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
import { t, tct } from 'app/locale';
import Button from 'app/components/button';
import space from 'app/styles/space';
import withApi from 'app/utils/withApi';
var CreateTeamAccessRequest = /** @class */ (function (_super) {
    __extends(CreateTeamAccessRequest, _super);
    function CreateTeamAccessRequest() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            createBusy: false,
        };
        _this.handleClick = function () { return __awaiter(_this, void 0, void 0, function () {
            var _a, api, memberId, orgId, teamId, closeModal, err_1;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, memberId = _a.memberId, orgId = _a.orgId, teamId = _a.teamId, closeModal = _a.closeModal;
                        this.setState({ createBusy: true });
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/organizations/" + orgId + "/members/" + memberId + "/teams/" + teamId + "/", {
                                method: 'POST',
                            })];
                    case 2:
                        _b.sent();
                        addSuccessMessage(t('Team request sent for approval'));
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _b.sent();
                        addErrorMessage(t('Unable to send team request'));
                        return [3 /*break*/, 4];
                    case 4:
                        this.setState({ createBusy: false });
                        closeModal();
                        return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    CreateTeamAccessRequest.prototype.render = function () {
        var _a = this.props, Body = _a.Body, Footer = _a.Footer, closeModal = _a.closeModal, teamId = _a.teamId;
        return (<React.Fragment>
        <Body>
          {tct('You do not have permission to add members to the #[team] team, but we will send a request to your organization admins for approval.', { team: teamId })}
        </Body>
        <Footer>
          <ButtonGroup>
            <Button onClick={closeModal}>{t('Cancel')}</Button>
            <Button priority="primary" onClick={this.handleClick} busy={this.state.createBusy} autoFocus>
              {t('Continue')}
            </Button>
          </ButtonGroup>
        </Footer>
      </React.Fragment>);
    };
    return CreateTeamAccessRequest;
}(React.Component));
var ButtonGroup = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content max-content;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: max-content max-content;\n  grid-gap: ", ";\n"])), space(1));
export default withApi(CreateTeamAccessRequest);
var templateObject_1;
//# sourceMappingURL=teamAccessRequestModal.jsx.map