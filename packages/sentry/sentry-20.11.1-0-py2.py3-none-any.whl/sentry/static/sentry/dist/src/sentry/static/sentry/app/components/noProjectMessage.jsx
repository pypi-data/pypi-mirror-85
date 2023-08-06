import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import PropTypes from 'prop-types';
import { t } from 'app/locale';
import Button from 'app/components/button';
import PageHeading from 'app/components/pageHeading';
import SentryTypes from 'app/sentryTypes';
import space from 'app/styles/space';
import ConfigStore from 'app/stores/configStore';
import ButtonBar from 'app/components/buttonBar';
/* TODO: replace with I/O when finished */
import img from '../../images/spot/hair-on-fire.svg';
var NoProjectMessage = /** @class */ (function (_super) {
    __extends(NoProjectMessage, _super);
    function NoProjectMessage() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    NoProjectMessage.prototype.render = function () {
        var _a = this.props, children = _a.children, organization = _a.organization, projects = _a.projects, loadingProjects = _a.loadingProjects;
        var orgId = organization.slug;
        var canCreateProject = organization.access.includes('project:write');
        var canJoinTeam = organization.access.includes('team:read');
        var orgHasProjects;
        var hasProjectAccess;
        if ('projects' in organization) {
            var isSuperuser = ConfigStore.get('user').isSuperuser;
            orgHasProjects = organization.projects.length > 0;
            hasProjectAccess = isSuperuser
                ? organization.projects.some(function (p) { return p.hasAccess; })
                : organization.projects.some(function (p) { return p.isMember && p.hasAccess; });
        }
        else {
            hasProjectAccess = projects ? projects.length > 0 : false;
            orgHasProjects = hasProjectAccess;
        }
        if (hasProjectAccess || loadingProjects) {
            return children;
        }
        // If the organization has some projects, but the user doesn't have access to
        // those projects, the primary action is to Join a Team. Otherwise the primary
        // action is to create a project.
        var joinTeamAction = (<Button title={canJoinTeam ? undefined : t('You do not have permission to join a team.')} disabled={!canJoinTeam} priority={orgHasProjects ? 'primary' : 'default'} to={"/settings/" + orgId + "/teams/"}>
        {t('Join a Team')}
      </Button>);
        var createProjectAction = (<Button title={canCreateProject
            ? undefined
            : t('You do not have permission to create a project.')} disabled={!canCreateProject} priority={orgHasProjects ? 'default' : 'primary'} to={"/organizations/" + orgId + "/projects/new/"}>
        {t('Create project')}
      </Button>);
        return (<Wrapper>
        <HeightWrapper>
          <img src={img} height={350} alt="Nothing to see"/>
          <Content>
            <StyledPageHeading>{t('Remain Calm')}</StyledPageHeading>
            <HelpMessage>
              {t('You need at least one project to use this view')}
            </HelpMessage>
            <Actions gap={1}>
              {!orgHasProjects ? (createProjectAction) : (<React.Fragment>
                  {joinTeamAction}
                  {createProjectAction}
                </React.Fragment>)}
            </Actions>
          </Content>
        </HeightWrapper>
      </Wrapper>);
    };
    NoProjectMessage.propTypes = {
        /* if the user has access to any projects, we show whatever
        children are included. Otherwise we show the message */
        children: PropTypes.node,
        organization: SentryTypes.Organization,
        projects: PropTypes.arrayOf(SentryTypes.Project),
        loadingProjects: PropTypes.bool,
    };
    return NoProjectMessage;
}(React.Component));
export default NoProjectMessage;
var StyledPageHeading = styled(PageHeading)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-size: 28px;\n  margin-bottom: ", ";\n"], ["\n  font-size: 28px;\n  margin-bottom: ", ";\n"])), space(1.5));
var HelpMessage = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(2));
var Flex = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
var Wrapper = styled(Flex)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  flex: 1;\n  align-items: center;\n  justify-content: center;\n"], ["\n  flex: 1;\n  align-items: center;\n  justify-content: center;\n"])));
var HeightWrapper = styled(Flex)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  height: 350px;\n"], ["\n  height: 350px;\n"])));
var Content = styled(Flex)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  flex-direction: column;\n  justify-content: center;\n  margin-left: 40px;\n"], ["\n  flex-direction: column;\n  justify-content: center;\n  margin-left: 40px;\n"])));
var Actions = styled(ButtonBar)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  width: fit-content;\n"], ["\n  width: fit-content;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=noProjectMessage.jsx.map