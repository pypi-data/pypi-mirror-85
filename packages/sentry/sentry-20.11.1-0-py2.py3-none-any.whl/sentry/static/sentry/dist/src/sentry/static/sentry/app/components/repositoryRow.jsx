import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { PanelItem } from 'app/components/panels';
import { RepositoryStatus } from 'app/types';
import { deleteRepository, cancelDeleteRepository } from 'app/actionCreators/integrations';
import { t } from 'app/locale';
import Access from 'app/components/acl/access';
import Button from 'app/components/button';
import Confirm from 'app/components/confirm';
import { IconDelete } from 'app/icons';
import space from 'app/styles/space';
import Tooltip from 'app/components/tooltip';
var RepositoryRow = /** @class */ (function (_super) {
    __extends(RepositoryRow, _super);
    function RepositoryRow() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.cancelDelete = function () {
            var _a = _this.props, api = _a.api, orgId = _a.orgId, repository = _a.repository, onRepositoryChange = _a.onRepositoryChange;
            cancelDeleteRepository(api, orgId, repository.id).then(function (data) {
                if (onRepositoryChange) {
                    onRepositoryChange(data);
                }
            }, function () { });
        };
        _this.deleteRepo = function () {
            var _a = _this.props, api = _a.api, orgId = _a.orgId, repository = _a.repository, onRepositoryChange = _a.onRepositoryChange;
            deleteRepository(api, orgId, repository.id).then(function (data) {
                if (onRepositoryChange) {
                    onRepositoryChange(data);
                }
            }, function () { });
        };
        return _this;
    }
    RepositoryRow.prototype.getStatusLabel = function (repo) {
        switch (repo.status) {
            case RepositoryStatus.PENDING_DELETION:
                return 'Deletion Queued';
            case RepositoryStatus.DELETION_IN_PROGRESS:
                return 'Deletion in Progress';
            case RepositoryStatus.DISABLED:
                return 'Disabled';
            case RepositoryStatus.HIDDEN:
                return 'Disabled';
            default:
                return null;
        }
    };
    Object.defineProperty(RepositoryRow.prototype, "isActive", {
        get: function () {
            return this.props.repository.status === RepositoryStatus.ACTIVE;
        },
        enumerable: false,
        configurable: true
    });
    RepositoryRow.prototype.render = function () {
        var _this = this;
        var _a = this.props, repository = _a.repository, showProvider = _a.showProvider;
        var isActive = this.isActive;
        return (<Access access={['org:integrations']}>
        {function (_a) {
            var hasAccess = _a.hasAccess;
            return (<StyledPanelItem status={repository.status}>
            <RepositoryTitleAndUrl>
              <RepositoryTitle>
                <strong>{repository.name}</strong>
                {!isActive && <small> &mdash; {_this.getStatusLabel(repository)}</small>}
                {repository.status === RepositoryStatus.PENDING_DELETION && (<StyledButton size="xsmall" onClick={_this.cancelDelete} disabled={!hasAccess} data-test-id="repo-cancel">
                    {t('Cancel')}
                  </StyledButton>)}
              </RepositoryTitle>
              <div>
                {showProvider && <small>{repository.provider.name}</small>}
                {showProvider && repository.url && <span>&nbsp;&mdash;&nbsp;</span>}
                {repository.url && (<small>
                    <a href={repository.url}>{repository.url.replace('https://', '')}</a>
                  </small>)}
              </div>
            </RepositoryTitleAndUrl>

            <Tooltip title={t('You must be an organization owner, manager or admin to remove a repository.')} disabled={hasAccess}>
              <Confirm disabled={!hasAccess ||
                (!isActive && repository.status !== RepositoryStatus.DISABLED)} onConfirm={_this.deleteRepo} message={t('Are you sure you want to remove this repository? All associated commit data will be removed in addition to the repository.')}>
                <Button size="xsmall" icon={<IconDelete size="xs"/>} label={t('delete')} disabled={!hasAccess}/>
              </Confirm>
            </Tooltip>
          </StyledPanelItem>);
        }}
      </Access>);
    };
    RepositoryRow.defaultProps = {
        showProvider: false,
    };
    return RepositoryRow;
}(React.Component));
var StyledPanelItem = styled(PanelItem)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  /* shorter top padding because of title lineheight */\n  padding: ", " ", " ", ";\n  justify-content: space-between;\n  align-items: center;\n  flex: 1;\n\n  ", ";\n\n  &:last-child {\n    border-bottom: none;\n  }\n"], ["\n  /* shorter top padding because of title lineheight */\n  padding: ", " ", " ", ";\n  justify-content: space-between;\n  align-items: center;\n  flex: 1;\n\n  ",
    ";\n\n  &:last-child {\n    border-bottom: none;\n  }\n"])), space(1), space(2), space(2), function (p) {
    return p.status === RepositoryStatus.DISABLED &&
        "\n    filter: grayscale(1);\n    opacity: 0.4;\n  ";
});
var StyledButton = styled(Button)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space(1));
var RepositoryTitleAndUrl = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n"], ["\n  display: flex;\n  flex-direction: column;\n"])));
var RepositoryTitle = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin-bottom: ", ";\n  /* accommodate cancel button height */\n  line-height: 26px;\n"], ["\n  margin-bottom: ", ";\n  /* accommodate cancel button height */\n  line-height: 26px;\n"])), space(1));
export default RepositoryRow;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=repositoryRow.jsx.map