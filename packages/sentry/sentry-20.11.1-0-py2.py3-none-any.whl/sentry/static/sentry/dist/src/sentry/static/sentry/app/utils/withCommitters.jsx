import { __assign } from "tslib";
import React from 'react';
import Reflux from 'reflux';
import createReactClass from 'create-react-class';
import { getCommitters } from 'app/actionCreators/committers';
import CommitterStore from 'app/stores/committerStore';
import getDisplayName from 'app/utils/getDisplayName';
var initialState = {
    committers: [],
};
var withCommitters = function (WrappedComponent) {
    return createReactClass({
        displayName: "withCommitters(" + getDisplayName(WrappedComponent) + ")",
        mixins: [Reflux.listenTo(CommitterStore, 'onStoreUpdate')],
        getInitialState: function () {
            var _a = this.props, organization = _a.organization, project = _a.project, event = _a.event;
            var repoData = CommitterStore.get(organization.slug, project.slug, event.id);
            return __assign(__assign({}, initialState), repoData);
        },
        componentDidMount: function () {
            var group = this.props.group;
            // No committers if group doesn't have any releases
            if (!!(group === null || group === void 0 ? void 0 : group.firstRelease)) {
                this.fetchCommitters();
            }
        },
        fetchCommitters: function () {
            var _a = this.props, api = _a.api, organization = _a.organization, project = _a.project, event = _a.event;
            var repoData = CommitterStore.get(organization.slug, project.slug, event.id);
            if ((!repoData.committers && !repoData.committersLoading) ||
                repoData.committersError) {
                getCommitters(api, {
                    orgSlug: organization.slug,
                    projectSlug: project.slug,
                    eventId: event.id,
                });
            }
        },
        onStoreUpdate: function () {
            var _a = this.props, organization = _a.organization, project = _a.project, event = _a.event;
            var repoData = CommitterStore.get(organization.slug, project.slug, event.id);
            this.setState({ committers: repoData.committers });
        },
        render: function () {
            var _a = this.state.committers, committers = _a === void 0 ? [] : _a;
            // XXX: We do not pass loading/error states because the components using
            // this HOC (suggestedOwners, eventCause) do not have loading/error states
            return (<WrappedComponent {...this.props} committers={committers}/>);
        },
    });
};
export default withCommitters;
//# sourceMappingURL=withCommitters.jsx.map