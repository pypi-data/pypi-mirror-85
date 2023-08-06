import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import Access from 'app/components/acl/access';
import Button from 'app/components/button';
import Confirm from 'app/components/confirm';
import { IconDelete, IconEdit } from 'app/icons';
import space from 'app/styles/space';
import Tooltip from 'app/components/tooltip';
import IdBadge from 'app/components/idBadge';
var RepositoryProjectPathConfigRow = /** @class */ (function (_super) {
    __extends(RepositoryProjectPathConfigRow, _super);
    function RepositoryProjectPathConfigRow() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    RepositoryProjectPathConfigRow.prototype.render = function () {
        var _a = this.props, pathConfig = _a.pathConfig, project = _a.project, onEdit = _a.onEdit, onDelete = _a.onDelete;
        return (<Access access={['org:integrations']}>
        {function (_a) {
            var hasAccess = _a.hasAccess;
            return (<React.Fragment>
            <NameRepoColumn>
              <ProjectRepoHolder>
                <RepoName>{pathConfig.repoName}</RepoName>
                <ProjectAndBranch>
                  <IdBadge project={project} avatarSize={14} displayName={project.slug} avatarProps={{ consistentWidth: true }}/>
                  <BranchWrapper>&nbsp;|&nbsp;{pathConfig.defaultBranch}</BranchWrapper>
                </ProjectAndBranch>
              </ProjectRepoHolder>
            </NameRepoColumn>
            <OutputPathColumn>{pathConfig.sourceRoot}</OutputPathColumn>
            <InputPathColumn>{pathConfig.stackRoot}</InputPathColumn>
            <ButtonColumn>
              <Tooltip title={t('You must be an organization owner, manager or admin to edit or remove a code mapping.')} disabled={hasAccess}>
                <StyledButton size="small" icon={<IconEdit size="sm"/>} label={t('edit')} disabled={!hasAccess} onClick={function () { return onEdit(pathConfig); }}/>
                <Confirm disabled={!hasAccess} onConfirm={function () { return onDelete(pathConfig); }} message={t('Are you sure you want to remove this code mapping?')}>
                  <StyledButton size="small" icon={<IconDelete size="sm"/>} label={t('delete')} disabled={!hasAccess}/>
                </Confirm>
              </Tooltip>
            </ButtonColumn>
          </React.Fragment>);
        }}
      </Access>);
    };
    return RepositoryProjectPathConfigRow;
}(React.Component));
export default RepositoryProjectPathConfigRow;
var ProjectRepoHolder = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n"], ["\n  display: flex;\n  flex-direction: column;\n"])));
var RepoName = styled("span")(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  padding-bottom: ", ";\n"], ["\n  padding-bottom: ", ";\n"])), space(1));
var StyledButton = styled(Button)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin: ", ";\n"], ["\n  margin: ", ";\n"])), space(0.5));
var ProjectAndBranch = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: row;\n  color: ", ";\n"], ["\n  display: flex;\n  flex-direction: row;\n  color: ", ";\n"])), function (p) { return p.theme.gray300; });
//match the line eight of the badge
var BranchWrapper = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  line-height: 1.2;\n"], ["\n  line-height: 1.2;\n"])));
//Columns below
var Column = styled('span')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  overflow: hidden;\n  overflow-wrap: break-word;\n"], ["\n  overflow: hidden;\n  overflow-wrap: break-word;\n"])));
export var NameRepoColumn = styled(Column)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  grid-area: name-repo;\n"], ["\n  grid-area: name-repo;\n"])));
export var OutputPathColumn = styled(Column)(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  grid-area: output-path;\n"], ["\n  grid-area: output-path;\n"])));
export var InputPathColumn = styled(Column)(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  grid-area: input-path;\n"], ["\n  grid-area: input-path;\n"])));
export var ButtonColumn = styled(Column)(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  grid-area: button;\n  text-align: right;\n"], ["\n  grid-area: button;\n  text-align: right;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10;
//# sourceMappingURL=repositoryProjectPathConfigRow.jsx.map