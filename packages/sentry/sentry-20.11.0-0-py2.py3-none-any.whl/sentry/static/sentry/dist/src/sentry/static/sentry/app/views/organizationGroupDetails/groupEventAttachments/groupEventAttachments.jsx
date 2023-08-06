import { __assign, __extends, __read, __spread } from "tslib";
import React from 'react';
import pick from 'lodash/pick';
import * as ReactRouter from 'react-router';
import { Panel, PanelBody } from 'app/components/panels';
import { t } from 'app/locale';
import EmptyStateWarning from 'app/components/emptyStateWarning';
import LoadingIndicator from 'app/components/loadingIndicator';
import Pagination from 'app/components/pagination';
import AsyncComponent from 'app/components/asyncComponent';
import GroupEventAttachmentsTable from './groupEventAttachmentsTable';
import GroupEventAttachmentsFilter from './groupEventAttachmentsFilter';
var GroupEventAttachments = /** @class */ (function (_super) {
    __extends(GroupEventAttachments, _super);
    function GroupEventAttachments() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleDelete = function (deletedAttachmentId) {
            _this.setState(function (prevState) { return ({
                deletedAttachments: __spread(prevState.deletedAttachments, [deletedAttachmentId]),
            }); });
        };
        return _this;
    }
    GroupEventAttachments.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { deletedAttachments: [] });
    };
    GroupEventAttachments.prototype.getEndpoints = function () {
        var _a = this.props, params = _a.params, location = _a.location;
        return [
            [
                'eventAttachments',
                "/issues/" + params.groupId + "/attachments/",
                {
                    query: __assign(__assign({}, pick(location.query, ['cursor', 'environment', 'types'])), { limit: 50 }),
                },
            ],
        ];
    };
    GroupEventAttachments.prototype.renderNoQueryResults = function () {
        return (<EmptyStateWarning>
        <p>{t('Sorry, no event attachments match your search query.')}</p>
      </EmptyStateWarning>);
    };
    GroupEventAttachments.prototype.renderEmpty = function () {
        return (<EmptyStateWarning>
        <p>{t("There don't seem to be any event attachments yet.")}</p>
      </EmptyStateWarning>);
    };
    GroupEventAttachments.prototype.renderLoading = function () {
        return this.renderBody();
    };
    GroupEventAttachments.prototype.renderInnerBody = function () {
        var _a = this.props, projectSlug = _a.projectSlug, params = _a.params, location = _a.location;
        var _b = this.state, loading = _b.loading, eventAttachments = _b.eventAttachments, deletedAttachments = _b.deletedAttachments;
        if (loading) {
            return <LoadingIndicator />;
        }
        if (eventAttachments.length > 0) {
            return (<GroupEventAttachmentsTable attachments={eventAttachments} orgId={params.orgId} projectId={projectSlug} groupId={params.groupId} onDelete={this.handleDelete} deletedAttachments={deletedAttachments}/>);
        }
        if (location.query.types) {
            return this.renderNoQueryResults();
        }
        return this.renderEmpty();
    };
    GroupEventAttachments.prototype.renderBody = function () {
        return (<React.Fragment>
        <GroupEventAttachmentsFilter />
        <Panel className="event-list">
          <PanelBody>{this.renderInnerBody()}</PanelBody>
        </Panel>
        <Pagination pageLinks={this.state.eventAttachmentsPageLinks}/>
      </React.Fragment>);
    };
    return GroupEventAttachments;
}(AsyncComponent));
export default ReactRouter.withRouter(GroupEventAttachments);
//# sourceMappingURL=groupEventAttachments.jsx.map