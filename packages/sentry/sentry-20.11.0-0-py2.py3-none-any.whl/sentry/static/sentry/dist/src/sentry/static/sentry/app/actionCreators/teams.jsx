import { __read, __spread } from "tslib";
import TeamActions from 'app/actions/teamActions';
import { tct } from 'app/locale';
import { addSuccessMessage, addErrorMessage } from 'app/actionCreators/indicator';
import { uniqueId } from 'app/utils/guid';
import { callIfFunction } from 'app/utils/callIfFunction';
var doCallback = function (params, name) {
    if (params === void 0) { params = {}; }
    var args = [];
    for (var _i = 2; _i < arguments.length; _i++) {
        args[_i - 2] = arguments[_i];
    }
    callIfFunction.apply(void 0, __spread([params[name]], args));
};
// Fetch teams for org
export function fetchTeams(api, params, options) {
    TeamActions.fetchAll(params.orgId);
    return api.request("/teams/" + params.orgId + "/", {
        success: function (data) {
            TeamActions.fetchAllSuccess(params.orgId, data);
            doCallback(options, 'success', data);
        },
        error: function (error) {
            TeamActions.fetchAllError(params.orgId, error);
            doCallback(options, 'error', error);
        },
    });
}
export function fetchTeamDetails(api, params, options) {
    TeamActions.fetchDetails(params.teamId);
    return api.request("/teams/" + params.orgId + "/" + params.teamId + "/", {
        success: function (data) {
            TeamActions.fetchDetailsSuccess(params.teamId, data);
            doCallback(options, 'success', data);
        },
        error: function (error) {
            TeamActions.fetchDetailsError(params.teamId, error);
            doCallback(options, 'error', error);
        },
    });
}
export function updateTeamSuccess(teamId, data) {
    TeamActions.updateSuccess(teamId, data);
}
export function updateTeam(api, params, options) {
    var endpoint = "/teams/" + params.orgId + "/" + params.teamId + "/";
    TeamActions.update(params.teamId, params.data);
    return api.request(endpoint, {
        method: 'PUT',
        data: params.data,
        success: function (data) {
            updateTeamSuccess(params.teamId, data);
            doCallback(options, 'success', data);
        },
        error: function (error) {
            TeamActions.updateError(params.teamId, error);
            doCallback(options, 'error', error);
        },
    });
}
export function joinTeam(api, params, options) {
    var _a;
    var endpoint = "/organizations/" + params.orgId + "/members/" + ((_a = params.memberId) !== null && _a !== void 0 ? _a : 'me') + "/teams/" + params.teamId + "/";
    var id = uniqueId();
    TeamActions.update(id, params.teamId);
    return api.request(endpoint, {
        method: 'POST',
        success: function (data) {
            TeamActions.updateSuccess(params.teamId, data);
            doCallback(options, 'success', data);
        },
        error: function (error) {
            TeamActions.updateError(id, params.teamId, error);
            doCallback(options, 'error', error);
        },
    });
}
export function leaveTeam(api, params, options) {
    var endpoint = "/organizations/" + params.orgId + "/members/" + (params.memberId || 'me') + "/teams/" + params.teamId + "/";
    var id = uniqueId();
    TeamActions.update(id, params.teamId);
    return api.request(endpoint, {
        method: 'DELETE',
        success: function (data) {
            TeamActions.updateSuccess(params.teamId, data);
            doCallback(options, 'success', data);
        },
        error: function (error) {
            TeamActions.updateError(id, params.teamId, error);
            doCallback(options, 'error', error);
        },
    });
}
export function createTeam(api, team, params) {
    TeamActions.createTeam(team);
    return api
        .requestPromise("/organizations/" + params.orgId + "/teams/", {
        method: 'POST',
        data: team,
    })
        .then(function (data) {
        TeamActions.createTeamSuccess(data);
        addSuccessMessage(tct('[team] has been added to the [organization] organization', {
            team: "#" + data.slug,
            organization: params.orgId,
        }));
        return data;
    }, function (err) {
        TeamActions.createTeamError(team.slug, err);
        addErrorMessage(tct('Unable to create [team] in the [organization] organization', {
            team: "#" + team.slug,
            organization: params.orgId,
        }));
        throw err;
    });
}
export function removeTeam(api, params) {
    TeamActions.removeTeam(params.teamId);
    return api
        .requestPromise("/teams/" + params.orgId + "/" + params.teamId + "/", {
        method: 'DELETE',
    })
        .then(function (data) {
        TeamActions.removeTeamSuccess(params.teamId, data);
        addSuccessMessage(tct('[team] has been removed from the [organization] organization', {
            team: "#" + params.teamId,
            organization: params.orgId,
        }));
        return data;
    }, function (err) {
        TeamActions.removeTeamError(params.teamId, err);
        addErrorMessage(tct('Unable to remove [team] from the [organization] organization', {
            team: "#" + params.teamId,
            organization: params.orgId,
        }));
        throw err;
    });
}
//# sourceMappingURL=teams.jsx.map