import { __assign, __rest } from "tslib";
import React from 'react';
import Reflux from 'reflux';
import createReactClass from 'create-react-class';
import assign from 'lodash/assign';
import getDisplayName from 'app/utils/getDisplayName';
import MemberListStore from 'app/stores/memberListStore';
import TagStore from 'app/stores/tagStore';
var uuidPattern = /[0-9a-f]{32}$/;
var getUsername = function (_a) {
    var isManaged = _a.isManaged, username = _a.username, email = _a.email;
    // Users created via SAML receive unique UUID usernames. Use
    // their email in these cases, instead.
    if (username && uuidPattern.test(username)) {
        return email;
    }
    else {
        return !isManaged && username ? username : email;
    }
};
/**
 * HOC for getting tags and many useful issue attributes as 'tags' for use
 * in autocomplete selectors or condition builders.
 */
var withIssueTags = function (WrappedComponent) {
    return createReactClass({
        displayName: "withIssueTags(" + getDisplayName(WrappedComponent) + ")",
        mixins: [
            Reflux.listenTo(MemberListStore, 'onMemberListStoreChange'),
            Reflux.listenTo(TagStore, 'onTagsUpdate'),
        ],
        getInitialState: function () {
            var tags = assign({}, TagStore.getAllTags(), TagStore.getIssueAttributes(), TagStore.getBuiltInTags());
            var users = MemberListStore.getAll();
            return { tags: tags, users: users };
        },
        onMemberListStoreChange: function (users) {
            this.setState({ users: users });
            this.setAssigned();
        },
        onTagsUpdate: function (storeTags) {
            var tags = assign({}, storeTags, TagStore.getIssueAttributes(), TagStore.getBuiltInTags());
            this.setState({ tags: tags });
            this.setAssigned();
        },
        setAssigned: function () {
            if (this.state.users && this.state.tags.assigned) {
                var _a = this.state, tags = _a.tags, users = _a.users;
                var usernames = users.map(getUsername);
                usernames.unshift('me');
                this.setState({
                    tags: __assign(__assign({}, tags), { assigned: __assign(__assign({}, tags.assigned), { values: usernames }), bookmarks: __assign(__assign({}, tags.bookmarks), { values: usernames }) }),
                });
            }
        },
        render: function () {
            var _a = this.props, tags = _a.tags, props = __rest(_a, ["tags"]);
            return <WrappedComponent {...__assign({ tags: tags !== null && tags !== void 0 ? tags : this.state.tags }, props)}/>;
        },
    });
};
export default withIssueTags;
//# sourceMappingURL=withIssueTags.jsx.map