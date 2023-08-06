import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import styled from '@emotion/styled';
import { analytics } from 'app/utils/analytics';
import { t } from 'app/locale';
import HookOrDefault from 'app/components/hookOrDefault';
import withOrganization from 'app/utils/withOrganization';
import testableTransition from 'app/utils/testableTransition';
import InviteMembers from './inviteMembers';
import LearnMore from './learnMore';
import ProjectDocs from './projectDocs';
import SetupChoices from './setupChoices';
var recordAnalyticsOptionSelected = function (_a) {
    var organization = _a.organization, choice = _a.choice;
    return analytics('onboarding_v2.setup_choice_selected', {
        org_id: parseInt(organization.id, 10),
        choice: choice,
    });
};
// Member invitation works a bit differently in Sentry's SaaS product, this
// provides a hook for that.
var InviteMembersComponent = HookOrDefault({
    hookName: 'onboarding:invite-members',
    defaultComponent: InviteMembers,
});
var SETUP_CHOICES = [
    {
        id: 'install-guide',
        title: t('Installation Guide'),
        component: ProjectDocs,
    },
    {
        id: 'invite-members',
        title: t('Invite Team Members'),
        component: InviteMembersComponent,
    },
    {
        id: 'learn-more',
        title: t('Take a Tour'),
        component: LearnMore,
    },
];
var DEFAULT_SETUP_OPTION = 'install-guide';
var OnboardingProjectSetup = /** @class */ (function (_super) {
    __extends(OnboardingProjectSetup, _super);
    function OnboardingProjectSetup() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            selectedChoice: DEFAULT_SETUP_OPTION,
        };
        _this.handleSelect = function (id) {
            var organization = _this.props.organization;
            _this.setState({ selectedChoice: id });
            recordAnalyticsOptionSelected({ organization: organization, choice: id });
        };
        return _this;
    }
    OnboardingProjectSetup.prototype.render = function () {
        var selectedChoice = this.state.selectedChoice;
        var SelectedComponent = SETUP_CHOICES.find(function (item) { return item.id === selectedChoice; })
            .component;
        return (<React.Fragment>
        <SetupChoices choices={SETUP_CHOICES} selectedChoice={selectedChoice} onSelect={this.handleSelect}/>
        <ChoiceContainer>
          <AnimatePresence>
            <Choices key={selectedChoice}>
              <SelectedComponent {...this.props}/>
            </Choices>
          </AnimatePresence>
        </ChoiceContainer>
      </React.Fragment>);
    };
    return OnboardingProjectSetup;
}(React.Component));
var ChoiceContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: minmax(0, 1fr);\n"], ["\n  display: grid;\n  grid-template-columns: minmax(0, 1fr);\n"])));
var Choices = styled(motion.div)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  grid-column: 1;\n  grid-row: 1;\n"], ["\n  grid-column: 1;\n  grid-row: 1;\n"])));
Choices.defaultProps = {
    transition: testableTransition(),
    initial: { opacity: 0, x: -20 },
    animate: { opacity: 1, x: 0 },
    exit: { opacity: 0, x: 20 },
};
export default withOrganization(OnboardingProjectSetup);
var templateObject_1, templateObject_2;
//# sourceMappingURL=index.jsx.map