import { __awaiter, __extends, __generator, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { addSuccessMessage } from 'app/actionCreators/indicator';
import { analytics } from 'app/utils/analytics';
import { getCurrentMember } from 'app/actionCreators/members';
import { t, tct } from 'app/locale';
import Alert from 'app/components/alert';
import EmailField from 'app/views/settings/components/forms/emailField';
import Form from 'app/views/settings/components/forms/form';
import Panel from 'app/components/panels/panel';
import { IconGroup } from 'app/icons';
import SelectField from 'app/views/settings/components/forms/selectField';
import TextBlock from 'app/views/settings/components/text/textBlock';
import space from 'app/styles/space';
import withApi from 'app/utils/withApi';
import withConfig from 'app/utils/withConfig';
import withOrganization from 'app/utils/withOrganization';
var recordAnalyticsUserInvited = function (_a) {
    var organization = _a.organization, project = _a.project;
    return analytics('onboarding_v2.user_invited', {
        org_id: organization.id,
        project: project === null || project === void 0 ? void 0 : project.slug,
    });
};
var InviteMembers = /** @class */ (function (_super) {
    __extends(InviteMembers, _super);
    function InviteMembers() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            invitedEmails: [],
            roleList: [],
        };
        _this.handleSubmitSuccess = function (data, model) {
            model.fields.set('email', '');
            _this.setState(function (state) { return ({ invitedEmails: __spread(state.invitedEmails, [data.email]) }); });
            addSuccessMessage(t('Invited %s to your organization', data.email));
            var _a = _this.props, organization = _a.organization, project = _a.project;
            recordAnalyticsUserInvited({ organization: organization, project: project });
        };
        return _this;
    }
    InviteMembers.prototype.componentDidMount = function () {
        this.fetchRoleDetails();
    };
    InviteMembers.prototype.fetchRoleDetails = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, api, organization, member;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, organization = _a.organization;
                        return [4 /*yield*/, getCurrentMember(api, organization.slug)];
                    case 1:
                        member = _b.sent();
                        this.setState({ roleList: member.roles });
                        return [2 /*return*/];
                }
            });
        });
    };
    Object.defineProperty(InviteMembers.prototype, "emailSuffix", {
        get: function () {
            return this.props.config.user.email.split('@')[1];
        },
        enumerable: false,
        configurable: true
    });
    InviteMembers.prototype.render = function () {
        var _a, _b;
        var _c = this.state, invitedEmails = _c.invitedEmails, roleList = _c.roleList;
        var _d = this.props, project = _d.project, formProps = _d.formProps, organization = _d.organization;
        return (<React.Fragment>
        {invitedEmails.length > 0 && (<Alert type="success" icon={<IconGroup />}>
            {tct('[emailList] has been invited to your organization.', {
            emailList: <strong>{invitedEmails.join(', ')}</strong>,
        })}
          </Alert>)}
        <Panel>
          <Form apiEndpoint={"/organizations/" + organization.slug + "/members/"} apiMethod="POST" submitLabel={t('Invite Member')} onSubmitSuccess={this.handleSubmitSuccess} initialData={{ teams: [(_b = (_a = project === null || project === void 0 ? void 0 : project.teams) === null || _a === void 0 ? void 0 : _a[0]) === null || _b === void 0 ? void 0 : _b.slug] }} {...formProps}>
            <HelpText>
              {t("Enter the emails of team members you'd like in your\n                 organization. We'll send out their invitation and guide your\n                 teammates through this same setup.")}
            </HelpText>
            <EmailField name="email" required placeholder={"e.g. team.member@" + this.emailSuffix} label={t('Member Email')} help={t('Enter the email of a team member to invite to your Sentry Organization. You may invite more than one.')}/>
            <SelectField deprecatedSelectControl name="role" label={t('Member Role')} required help={t('User roles determine the permission scopes a user will have within your Sentry organization.')} placeholder={t('Select a role')} choices={roleList.map(function (role) { return [
            role.id,
            <React.Fragment key={role.id}>
                  {role.name}
                  <RoleDescriptiom>{role.desc}</RoleDescriptiom>
                </React.Fragment>,
        ]; })}/>
          </Form>
        </Panel>
      </React.Fragment>);
    };
    return InviteMembers;
}(React.Component));
var HelpText = styled(TextBlock)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: ", ";\n  margin: 0;\n  border-bottom: 1px solid ", ";\n"], ["\n  padding: ", ";\n  margin: 0;\n  border-bottom: 1px solid ", ";\n"])), space(2), function (p) { return p.theme.border; });
var RoleDescriptiom = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-top: ", ";\n  line-height: 1.4em;\n  font-size: 0.8em;\n"], ["\n  margin-top: ", ";\n  line-height: 1.4em;\n  font-size: 0.8em;\n"])), space(0.5));
export default withOrganization(withApi(withConfig(InviteMembers)));
var templateObject_1, templateObject_2;
//# sourceMappingURL=inviteMembers.jsx.map