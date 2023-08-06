import { __assign, __read, __spread } from "tslib";
import pick from 'lodash/pick';
import { t } from 'app/locale';
import EventView from 'app/utils/discover/eventView';
import { getUtcDateString } from 'app/utils/dates';
import { URL_PARAM } from 'app/constants/globalSelectionHeader';
import { stringifyQueryObject, QueryResults } from 'app/utils/tokenizeSearch';
/**
 * Convert list of individual file changes into a per-file summary grouped by repository
 */
export function getFilesByRepository(fileList) {
    return fileList.reduce(function (filesByRepository, file) {
        var filename = file.filename, repoName = file.repoName, author = file.author, type = file.type;
        if (!filesByRepository.hasOwnProperty(repoName)) {
            filesByRepository[repoName] = {};
        }
        if (!filesByRepository[repoName].hasOwnProperty(filename)) {
            filesByRepository[repoName][filename] = {
                authors: {},
                types: new Set(),
            };
        }
        if (author.email) {
            filesByRepository[repoName][filename].authors[author.email] = author;
        }
        filesByRepository[repoName][filename].types.add(type);
        return filesByRepository;
    }, {});
}
/**
 * Convert list of individual commits into a summary grouped by repository
 */
export function getCommitsByRepository(commitList) {
    return commitList.reduce(function (commitsByRepository, commit) {
        var _a, _b;
        var repositoryName = (_b = (_a = commit.repository) === null || _a === void 0 ? void 0 : _a.name) !== null && _b !== void 0 ? _b : t('unknown');
        if (!commitsByRepository.hasOwnProperty(repositoryName)) {
            commitsByRepository[repositoryName] = [];
        }
        commitsByRepository[repositoryName].push(commit);
        return commitsByRepository;
    }, {});
}
export function getQuery(_a) {
    var location = _a.location, _b = _a.perPage, perPage = _b === void 0 ? 40 : _b, activeRepository = _a.activeRepository;
    var query = __assign(__assign({}, pick(location.query, __spread(Object.values(URL_PARAM), ['cursor']))), { per_page: perPage });
    if (!activeRepository) {
        return query;
    }
    return __assign(__assign({}, query), { repo_name: activeRepository.name });
}
/**
 * Get repositories to render according to the activeRepository
 */
export function getReposToRender(repos, activeRepository) {
    if (!activeRepository) {
        return repos;
    }
    return [activeRepository.name];
}
/**
 * Get high level transaction information for this release
 */
export function getReleaseEventView(selection, version, organization) {
    var projects = selection.projects, environments = selection.environments, datetime = selection.datetime;
    var start = datetime.start, end = datetime.end, period = datetime.period;
    var discoverQuery = {
        id: undefined,
        version: 2,
        name: "" + t('Release Apdex'),
        fields: ["apdex(" + organization.apdexThreshold + ")"],
        query: stringifyQueryObject(new QueryResults(["release:" + version, 'event.type:transaction', 'count():>0'])),
        range: period,
        environment: environments,
        projects: projects,
        start: start ? getUtcDateString(start) : undefined,
        end: end ? getUtcDateString(end) : undefined,
    };
    return EventView.fromSavedQuery(discoverQuery);
}
//# sourceMappingURL=utils.jsx.map