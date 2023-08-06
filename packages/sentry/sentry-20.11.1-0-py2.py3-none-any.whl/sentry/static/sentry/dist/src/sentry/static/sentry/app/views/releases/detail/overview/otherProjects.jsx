import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t, tn } from 'app/locale';
import space from 'app/styles/space';
import Link from 'app/components/links/link';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import Button from 'app/components/button';
import ProjectBadge from 'app/components/idBadge/projectBadge';
import { SectionHeading, Wrapper } from './styles';
var OtherProjects = /** @class */ (function (_super) {
    __extends(OtherProjects, _super);
    function OtherProjects() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            collapsed: true,
        };
        _this.onCollapseToggle = function () {
            _this.setState(function (prevState) { return ({
                collapsed: !prevState.collapsed,
            }); });
        };
        return _this;
    }
    OtherProjects.prototype.render = function () {
        var _a = this.props, projects = _a.projects, location = _a.location;
        var collapsed = this.state.collapsed;
        var canExpand = projects.length > OtherProjects.MAX_WHEN_COLLAPSED;
        var projectsToRender = projects;
        if (collapsed && canExpand) {
            projectsToRender = projects.slice(0, OtherProjects.MAX_WHEN_COLLAPSED);
        }
        var numberOfCollapsedProjects = projects.length - projectsToRender.length;
        return (<Wrapper>
        <SectionHeading>
          {tn('Other Project for This Release', 'Other Projects for This Release', projects.length)}
        </SectionHeading>
        {projectsToRender.map(function (project) { return (<Row key={project.id}>
            <StyledLink to={{
            pathname: location.pathname,
            query: __assign(__assign({}, location.query), { project: project.id, yAxis: undefined }),
        }}>
              <ProjectBadge project={project} avatarSize={16}/>
            </StyledLink>
          </Row>); })}
        {numberOfCollapsedProjects > 0 && (<CollapseToggle priority="link" onClick={this.onCollapseToggle}>
            {tn('Show %s collapsed project', 'Show %s collapsed projects', numberOfCollapsedProjects)}
          </CollapseToggle>)}
        {numberOfCollapsedProjects === 0 && canExpand && (<CollapseToggle priority="link" onClick={this.onCollapseToggle}>
            {t('Collapse')}
          </CollapseToggle>)}
      </Wrapper>);
    };
    OtherProjects.MAX_WHEN_COLLAPSED = 5;
    return OtherProjects;
}(React.Component));
var Row = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: ", ";\n  font-size: ", ";\n  color: ", ";\n  ", "\n"], ["\n  margin-bottom: ", ";\n  font-size: ", ";\n  color: ", ";\n  ", "\n"])), space(0.25), function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.blue300; }, overflowEllipsis);
var StyledLink = styled(Link)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: inline-block;\n"], ["\n  display: inline-block;\n"])));
var CollapseToggle = styled(Button)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  width: 100%;\n"], ["\n  width: 100%;\n"])));
export default OtherProjects;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=otherProjects.jsx.map