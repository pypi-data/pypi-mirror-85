import { __extends, __read } from "tslib";
import React from 'react';
import isEqual from 'lodash/isEqual';
import { DATE_TIME_KEYS } from 'app/constants/globalSelectionHeader';
import { initializeUrlState, updateProjects, updateEnvironments, updateDateTime, } from 'app/actionCreators/globalSelection';
import { getStateFromQuery } from './utils';
var getDateObjectFromQuery = function (query) {
    return Object.fromEntries(Object.entries(query).filter(function (_a) {
        var _b = __read(_a, 1), key = _b[0];
        return DATE_TIME_KEYS.includes(key);
    }));
};
/**
 * Initializes GlobalSelectionHeader
 *
 * Calls an actionCreator to load project/environment from local storage if possible,
 * otherwise populate with defaults.
 *
 * This should only happen when the header is mounted
 * e.g. when changing views or organizations.
 */
var InitializeGlobalSelectionHeader = /** @class */ (function (_super) {
    __extends(InitializeGlobalSelectionHeader, _super);
    function InitializeGlobalSelectionHeader() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    InitializeGlobalSelectionHeader.prototype.componentDidMount = function () {
        var _a = this.props, location = _a.location, router = _a.router, organization = _a.organization, defaultSelection = _a.defaultSelection, forceProject = _a.forceProject, memberProjects = _a.memberProjects, shouldForceProject = _a.shouldForceProject, shouldEnforceSingleProject = _a.shouldEnforceSingleProject, skipLoadLastUsed = _a.skipLoadLastUsed, showAbsolute = _a.showAbsolute;
        initializeUrlState({
            organization: organization,
            queryParams: location.query,
            router: router,
            skipLoadLastUsed: skipLoadLastUsed,
            memberProjects: memberProjects,
            defaultSelection: defaultSelection,
            forceProject: forceProject,
            shouldForceProject: shouldForceProject,
            shouldEnforceSingleProject: shouldEnforceSingleProject,
            showAbsolute: showAbsolute,
        });
    };
    InitializeGlobalSelectionHeader.prototype.componentDidUpdate = function (prevProps) {
        /**
         * This happens e.g. using browser's navigation button, in which case
         * we need to update our store to reflect URL changes
         */
        if (prevProps.location.query !== this.props.location.query) {
            var oldQuery = getStateFromQuery(prevProps.location.query, {
                allowEmptyPeriod: true,
            });
            var newQuery = getStateFromQuery(this.props.location.query, {
                allowEmptyPeriod: true,
            });
            var newEnvironments = newQuery.environment || [];
            var newDateObject = getDateObjectFromQuery(newQuery);
            var oldDateObject = getDateObjectFromQuery(oldQuery);
            /**
             * Do not pass router to these actionCreators, as we do not want to update
             * routes since these state changes are happening due to a change of routes
             */
            if (!isEqual(oldQuery.project, newQuery.project)) {
                updateProjects(newQuery.project || [], null, { environments: newEnvironments });
            }
            else if (!isEqual(oldQuery.environment, newQuery.environment)) {
                /**
                 * When the project stays the same, it's still possible that the environment
                 * changed, so explictly update the enviornment
                 */
                updateEnvironments(newEnvironments);
            }
            if (!isEqual(oldDateObject, newDateObject)) {
                updateDateTime(newDateObject);
            }
        }
    };
    InitializeGlobalSelectionHeader.prototype.render = function () {
        return null;
    };
    return InitializeGlobalSelectionHeader;
}(React.Component));
export default InitializeGlobalSelectionHeader;
//# sourceMappingURL=initializeGlobalSelectionHeader.jsx.map