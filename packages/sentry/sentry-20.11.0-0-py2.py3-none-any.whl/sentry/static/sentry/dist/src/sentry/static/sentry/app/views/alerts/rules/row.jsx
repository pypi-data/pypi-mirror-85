import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import moment from 'moment';
import styled from '@emotion/styled';
import memoize from 'lodash/memoize';
import { t, tct } from 'app/locale';
import { IconDelete, IconSettings } from 'app/icons';
import { PanelItem } from 'app/components/panels';
import Access from 'app/components/acl/access';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import Confirm from 'app/components/confirm';
import ErrorBoundary from 'app/components/errorBoundary';
import IdBadge from 'app/components/idBadge';
import Link from 'app/components/links/link';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
import { isIssueAlert } from '../utils';
import { TableLayout } from './styles';
var RuleListRow = /** @class */ (function (_super) {
    __extends(RuleListRow, _super);
    function RuleListRow() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        /**
         * Memoized function to find a project from a list of projects
         */
        _this.getProject = memoize(function (slug, projects) {
            return projects.find(function (project) { return project.slug === slug; });
        });
        return _this;
    }
    RuleListRow.prototype.render = function () {
        var _a, _b;
        var _c = this.props, rule = _c.rule, projectsLoaded = _c.projectsLoaded, projects = _c.projects, orgId = _c.orgId, onDelete = _c.onDelete;
        var dateCreated = moment(rule.dateCreated).format('ll');
        var slug = rule.projects[0];
        var link = "/organizations/" + orgId + "/alerts/" + (isIssueAlert(rule) ? 'rules' : 'metric-rules') + "/" + slug + "/" + rule.id + "/";
        return (<ErrorBoundary>
        <AlertRulesPanelItem>
          <TableLayout>
            <RuleType>{isIssueAlert(rule) ? t('Issue') : t('Metric')}</RuleType>
            <Title>
              <Link to={link}>{rule.name}</Link>
            </Title>
            <ProjectBadge avatarSize={18} project={!projectsLoaded ? { slug: slug } : this.getProject(slug, projects)}/>
            <CreatedBy>{(_b = (_a = rule === null || rule === void 0 ? void 0 : rule.createdBy) === null || _a === void 0 ? void 0 : _a.name) !== null && _b !== void 0 ? _b : '-'}</CreatedBy>
            <div>{dateCreated}</div>
            <Access access={['project:write']}>
              {function (_a) {
            var hasAccess = _a.hasAccess;
            return (<ButtonBar gap={1}>
                  <Confirm disabled={!hasAccess} message={tct("Are you sure you want to delete [name]? You won't be able to view the history of this alert once it's deleted.", {
                name: rule.name,
            })} header={t('Delete Alert Rule?')} priority="danger" confirmText={t('Delete Rule')} onConfirm={function () { return onDelete(slug, rule); }}>
                    <Button type="button" icon={<IconDelete />} size="small" title={t('Delete')}/>
                  </Confirm>
                  <Button size="small" icon={<IconSettings />} title={t('Edit')} to={link}/>
                </ButtonBar>);
        }}
            </Access>
          </TableLayout>
        </AlertRulesPanelItem>
      </ErrorBoundary>);
    };
    return RuleListRow;
}(React.Component));
var RuleType = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-size: 12px;\n  font-weight: 400;\n  color: ", ";\n  text-transform: uppercase;\n"], ["\n  font-size: 12px;\n  font-weight: 400;\n  color: ", ";\n  text-transform: uppercase;\n"])), function (p) { return p.theme.gray300; });
var Title = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), overflowEllipsis);
var CreatedBy = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), overflowEllipsis);
var AlertRulesPanelItem = styled(PanelItem)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  font-size: ", ";\n  padding: ", " ", ";\n"], ["\n  font-size: ", ";\n  padding: ", " ", ";\n"])), function (p) { return p.theme.fontSizeMedium; }, space(1.5), space(2));
var ProjectBadge = styled(IdBadge)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  flex-shrink: 0;\n"], ["\n  flex-shrink: 0;\n"])));
export default RuleListRow;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=row.jsx.map