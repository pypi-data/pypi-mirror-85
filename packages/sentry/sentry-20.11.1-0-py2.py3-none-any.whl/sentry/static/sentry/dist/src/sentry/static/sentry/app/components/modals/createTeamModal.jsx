import { __extends, __rest } from "tslib";
import React from 'react';
import { createTeam } from 'app/actionCreators/teams';
import { t } from 'app/locale';
import CreateTeamForm from 'app/components/teams/createTeamForm';
import withApi from 'app/utils/withApi';
var CreateTeamModal = /** @class */ (function (_super) {
    __extends(CreateTeamModal, _super);
    function CreateTeamModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleSubmit = function (data, onSuccess, onError) {
            var _a = _this.props, organization = _a.organization, api = _a.api;
            createTeam(api, data, { orgId: organization.slug })
                .then(function (resp) {
                _this.handleSuccess(resp);
                onSuccess(resp);
            })
                .catch(function (err) {
                onError(err);
            });
        };
        return _this;
    }
    CreateTeamModal.prototype.handleSuccess = function (team) {
        if (this.props.onClose) {
            this.props.onClose(team);
        }
        this.props.closeModal();
    };
    CreateTeamModal.prototype.render = function () {
        var _a = this.props, Body = _a.Body, Header = _a.Header, closeModal = _a.closeModal, props = __rest(_a, ["Body", "Header", "closeModal"]);
        return (<React.Fragment>
        <Header closeButton onHide={closeModal}>
          {t('Create Team')}
        </Header>
        <Body>
          <CreateTeamForm {...props} onSubmit={this.handleSubmit}/>
        </Body>
      </React.Fragment>);
    };
    return CreateTeamModal;
}(React.Component));
export default withApi(CreateTeamModal);
//# sourceMappingURL=createTeamModal.jsx.map