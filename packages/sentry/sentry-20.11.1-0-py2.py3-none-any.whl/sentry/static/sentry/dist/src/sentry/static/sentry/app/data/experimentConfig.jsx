import { __assign } from "tslib";
import { ExperimentType } from 'app/types/experiments';
/**
 * This is the value an experiment will have when the unit of assignment
 * (organization, user, etc) is not part of any experiment group.
 *
 * This likely indicates they should see nothing, or the original version of
 * what's being tested.
 */
export var unassignedValue = -1;
/**
 * Frontend experiment configuration object
 */
export var experimentList = [
    {
        key: 'IntegrationDirectoryCategoryExperiment',
        type: ExperimentType.Organization,
        parameter: 'variant',
        assignments: ['0', '1'],
    },
    {
        key: 'TrialEndingNotice',
        type: ExperimentType.Organization,
        parameter: 'exposed',
        assignments: [0, 1],
    },
];
export var experimentConfig = experimentList.reduce(function (acc, exp) {
    var _a;
    return (__assign(__assign({}, acc), (_a = {}, _a[exp.key] = exp, _a)));
}, {});
//# sourceMappingURL=experimentConfig.jsx.map