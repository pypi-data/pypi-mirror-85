import { __assign, __awaiter, __extends, __generator, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { Panel, PanelBody, PanelHeader, PanelItem } from 'app/components/panels';
import { t, tct } from 'app/locale';
import Access from 'app/components/acl/access';
import AsyncView from 'app/views/asyncView';
import Button from 'app/components/button';
import { IconDelete } from 'app/icons';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import ExternalLink from 'app/components/links/externalLink';
import LinkWithConfirmation from 'app/components/links/linkWithConfirmation';
import PermissionAlert from 'app/views/settings/project/permissionAlert';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import TextBlock from 'app/views/settings/components/text/textBlock';
import Tooltip from 'app/components/tooltip';
import routeTitleGen from 'app/utils/routeTitle';
import space from 'app/styles/space';
var ProjectTags = /** @class */ (function (_super) {
    __extends(ProjectTags, _super);
    function ProjectTags() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleDelete = function (key, idx) { return function () { return __awaiter(_this, void 0, void 0, function () {
            var params, projectId, orgId, tags, error_1;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        params = this.props.params;
                        projectId = params.projectId, orgId = params.orgId;
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise("/projects/" + orgId + "/" + projectId + "/tags/" + key + "/", {
                                method: 'DELETE',
                            })];
                    case 2:
                        _a.sent();
                        tags = __spread(this.state.tags);
                        tags.splice(idx, 1);
                        this.setState({ tags: tags });
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _a.sent();
                        this.setState({ error: true, loading: false });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); }; };
        return _this;
    }
    ProjectTags.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { tags: [] });
    };
    ProjectTags.prototype.getEndpoints = function () {
        var _a = this.props.params, projectId = _a.projectId, orgId = _a.orgId;
        return [['tags', "/projects/" + orgId + "/" + projectId + "/tags/"]];
    };
    ProjectTags.prototype.getTitle = function () {
        var projectId = this.props.params.projectId;
        return routeTitleGen(t('Tags'), projectId, false);
    };
    ProjectTags.prototype.renderBody = function () {
        var _this = this;
        var tags = this.state.tags;
        var isEmpty = !tags || !tags.length;
        return (<React.Fragment>
        <SettingsPageHeader title={t('Tags')}/>
        <PermissionAlert />

        <TextBlock>
          {tct("Each event in Sentry may be annotated with various tags (key and value pairs).\n                 Learn how to [link:add custom tags].", {
            link: (<ExternalLink href="https://docs.sentry.io/enriching-error-data/additional-data/"/>),
        })}
        </TextBlock>

        <Panel>
          <PanelHeader>{t('Tags')}</PanelHeader>
          <PanelBody>
            {isEmpty ? (<EmptyMessage>
                {tct('There are no tags, [link:learn how to add tags]', {
            link: (<ExternalLink href="https://docs.sentry.io/enriching-error-data/additional-data/"/>),
        })}
              </EmptyMessage>) : (<Access access={['project:write']}>
                {function (_a) {
            var hasAccess = _a.hasAccess;
            return tags.map(function (_a, idx) {
                var key = _a.key, canDelete = _a.canDelete;
                var enabled = canDelete && hasAccess;
                return (<TagPanelItem key={key} data-test-id="tag-row">
                        <TagName>{key}</TagName>
                        <Actions>
                          <Tooltip disabled={enabled} title={hasAccess
                    ? t('This tag cannot be deleted.')
                    : t('You do not have permission to remove tags.')}>
                            <LinkWithConfirmation title={t('Remove tag?')} message={t('Are you sure you want to remove this tag?')} onConfirm={_this.handleDelete(key, idx)} disabled={!enabled}>
                              <Button size="xsmall" icon={<IconDelete size="xs"/>} data-test-id="delete" disabled={!enabled}/>
                            </LinkWithConfirmation>
                          </Tooltip>
                        </Actions>
                      </TagPanelItem>);
            });
        }}
              </Access>)}
          </PanelBody>
        </Panel>
      </React.Fragment>);
    };
    return ProjectTags;
}(AsyncView));
export default ProjectTags;
var TagPanelItem = styled(PanelItem)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: 0;\n  align-items: center;\n"], ["\n  padding: 0;\n  align-items: center;\n"])));
var TagName = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  flex: 1;\n  padding: ", ";\n"], ["\n  flex: 1;\n  padding: ", ";\n"])), space(2));
var Actions = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  padding: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  padding: ", ";\n"])), space(2));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=projectTags.jsx.map