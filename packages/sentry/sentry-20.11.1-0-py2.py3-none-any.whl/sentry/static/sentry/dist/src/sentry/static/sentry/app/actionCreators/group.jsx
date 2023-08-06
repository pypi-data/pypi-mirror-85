import * as Sentry from '@sentry/react';
import { Client } from 'app/api';
import { buildUserId, buildTeamId } from 'app/utils';
import { uniqueId } from 'app/utils/guid';
import GroupActions from 'app/actions/groupActions';
import GroupStore from 'app/stores/groupStore';
export function assignToUser(params) {
    var api = new Client();
    var endpoint = "/issues/" + params.id + "/";
    var id = uniqueId();
    GroupActions.assignTo(id, params.id, {
        email: (params.member && params.member.email) || '',
    });
    var request = api.requestPromise(endpoint, {
        method: 'PUT',
        // Sending an empty value to assignedTo is the same as "clear",
        // so if no member exists, that implies that we want to clear the
        // current assignee.
        data: {
            assignedTo: params.user ? buildUserId(params.user.id) : '',
        },
    });
    request
        .then(function (data) {
        GroupActions.assignToSuccess(id, params.id, data);
    })
        .catch(function (data) {
        GroupActions.assignToError(id, params.id, data);
    });
    return request;
}
export function clearAssignment(groupId) {
    var api = new Client();
    var endpoint = "/issues/" + groupId + "/";
    var id = uniqueId();
    GroupActions.assignTo(id, groupId, {
        email: '',
    });
    var request = api.requestPromise(endpoint, {
        method: 'PUT',
        // Sending an empty value to assignedTo is the same as "clear"
        data: {
            assignedTo: '',
        },
    });
    request
        .then(function (data) {
        GroupActions.assignToSuccess(id, groupId, data);
    })
        .catch(function (data) {
        GroupActions.assignToError(id, groupId, data);
    });
    return request;
}
export function assignToActor(_a) {
    var id = _a.id, actor = _a.actor;
    var api = new Client();
    var endpoint = "/issues/" + id + "/";
    var guid = uniqueId();
    var actorId;
    GroupActions.assignTo(guid, id, { email: '' });
    switch (actor.type) {
        case 'user':
            actorId = buildUserId(actor.id);
            break;
        case 'team':
            actorId = buildTeamId(actor.id);
            break;
        default:
            Sentry.withScope(function (scope) {
                scope.setExtra('actor', actor);
                Sentry.captureException('Unknown assignee type');
            });
    }
    return api
        .requestPromise(endpoint, {
        method: 'PUT',
        data: { assignedTo: actorId },
    })
        .then(function (data) {
        GroupActions.assignToSuccess(guid, id, data);
    })
        .catch(function (data) {
        GroupActions.assignToError(guid, id, data);
    });
}
export function deleteNote(api, group, id, _oldText) {
    var restore = group.activity.find(function (activity) { return activity.id === id; });
    var index = GroupStore.removeActivity(group.id, id);
    if (index === -1) {
        // I dunno, the id wasn't found in the GroupStore
        return Promise.reject(new Error('Group was not found in store'));
    }
    var promise = api.requestPromise("/issues/" + group.id + "/comments/" + id + "/", {
        method: 'DELETE',
    });
    promise.catch(function () { return GroupStore.addActivity(group.id, restore, index); });
    return promise;
}
export function createNote(api, group, note) {
    var promise = api.requestPromise("/issues/" + group.id + "/comments/", {
        method: 'POST',
        data: note,
    });
    promise.then(function (data) { return GroupStore.addActivity(group.id, data); });
    return promise;
}
export function updateNote(api, group, note, id, oldText) {
    GroupStore.updateActivity(group.id, id, { text: note.text });
    var promise = api.requestPromise("/issues/" + group.id + "/comments/" + id + "/", {
        method: 'PUT',
        data: note,
    });
    promise.catch(function () { return GroupStore.updateActivity(group.id, id, { text: oldText }); });
    return promise;
}
//# sourceMappingURL=group.jsx.map