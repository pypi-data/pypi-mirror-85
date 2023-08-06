import { __assign, __read, __spread } from "tslib";
import Reflux from 'reflux';
import pick from 'lodash/pick';
import { Client } from 'app/api';
import { addErrorMessage, addLoadingMessage, addSuccessMessage, } from 'app/actionCreators/indicator';
import GroupingActions from 'app/actions/groupingActions';
// Between 0-100
var MIN_SCORE = 0.6;
// @param score: {[key: string]: number}
var checkBelowThreshold = function (scores) {
    if (scores === void 0) { scores = {}; }
    var scoreKeys = Object.keys(scores);
    return !scoreKeys.map(function (key) { return scores[key]; }).find(function (score) { return score >= MIN_SCORE; });
};
var storeConfig = {
    listenables: [GroupingActions],
    api: new Client(),
    init: function () {
        var _this = this;
        var state = this.getInitialState();
        Object.entries(state).forEach(function (_a) {
            var _b = __read(_a, 2), key = _b[0], value = _b[1];
            _this[key] = value;
        });
    },
    getInitialState: function () {
        return {
            // List of fingerprints that belong to issue
            mergedItems: [],
            // Map of {[fingerprint]: Array<fingerprint, event id>} that is selected to be unmerged
            unmergeList: new Map(),
            // Map of state for each fingerprint (i.e. "collapsed")
            unmergeState: new Map(),
            // Disabled state of "Unmerge" button in "Merged" tab (for Issues)
            unmergeDisabled: true,
            // If "Collapse All" was just used, this will be true
            unmergeLastCollapsed: false,
            // "Compare" button state
            enableFingerprintCompare: false,
            similarItems: [],
            filteredSimilarItems: [],
            similarLinks: '',
            mergeState: new Map(),
            mergeList: [],
            mergedLinks: '',
            mergeDisabled: false,
            loading: true,
            error: false,
        };
    },
    setStateForId: function (map, idOrIds, newState) {
        var ids = Array.isArray(idOrIds) ? idOrIds : [idOrIds];
        return ids.map(function (id) {
            var state = (map.has(id) && map.get(id)) || {};
            var mergedState = __assign(__assign({}, state), newState);
            map.set(id, mergedState);
            return mergedState;
        });
    },
    isAllUnmergedSelected: function () {
        var lockedItems = Array.from(this.unmergeState.values()).filter(function (_a) {
            var busy = _a.busy;
            return busy;
        }) || [];
        return (this.unmergeList.size ===
            this.mergedItems.filter(function (_a) {
                var latestEvent = _a.latestEvent;
                return !!latestEvent;
            }).length -
                lockedItems.length);
    },
    convertScoreStructure: function (scoreMap, version) {
        if (scoreMap.hasOwnProperty('exception:stacktrace:application-chunks')) {
            delete scoreMap['exception:stacktrace:application-chunks'];
        }
        if (!version || version === '1') {
            return scoreMap;
        }
        var newScoreMap = {};
        var scoreMapKeys = Object.keys(scoreMap);
        for (var key in scoreMapKeys) {
            var scoreMapKey = scoreMapKeys[key];
            if (scoreMapKey.includes('message:character-5-shingle')) {
                newScoreMap['message:message:character-shingles'] = scoreMap[scoreMapKey];
                continue;
            }
            if (scoreMapKey.includes('value:character-5-shingle')) {
                newScoreMap['exception:message:character-shingles'] = scoreMap[scoreMapKey];
                continue;
            }
            if (scoreMapKey.includes('stacktrace:frames-pairs')) {
                newScoreMap['exception:stacktrace:pairs'] = scoreMap[scoreMapKey];
                continue;
            }
        }
        return newScoreMap;
    },
    // Fetches data
    onFetch: function (toFetchArray) {
        var _this = this;
        var _a;
        var requests = toFetchArray || this.toFetchArray;
        var version = (_a = toFetchArray === null || toFetchArray === void 0 ? void 0 : toFetchArray[0]) === null || _a === void 0 ? void 0 : _a.version;
        // Reset state and trigger update
        this.init();
        this.triggerFetchState();
        var promises = requests.map(function (_a) {
            var endpoint = _a.endpoint, queryParams = _a.queryParams, dataKey = _a.dataKey;
            return new Promise(function (resolve, reject) {
                _this.api.request(endpoint, {
                    method: 'GET',
                    data: queryParams,
                    success: function (data, _, jqXHR) {
                        resolve({
                            dataKey: dataKey,
                            data: data,
                            links: jqXHR ? jqXHR.getResponseHeader('Link') : null,
                        });
                    },
                    error: function (err) {
                        var _a;
                        var error = ((_a = err.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) || true;
                        reject(error);
                    },
                });
            });
        });
        var responseProcessors = {
            merged: function (item) {
                // Check for locked items
                _this.setStateForId(_this.unmergeState, item.id, {
                    busy: item.state === 'locked',
                });
                return item;
            },
            similar: function (_a) {
                var _b = __read(_a, 2), issue = _b[0], scoreMap = _b[1];
                var convertedScore = _this.convertScoreStructure(scoreMap, version);
                // Hide items with a low scores
                var isBelowThreshold = checkBelowThreshold(convertedScore);
                // List of scores indexed by interface (i.e., exception and message)
                var scoresByInterface = Object.keys(convertedScore)
                    .map(function (scoreKey) { return [scoreKey, convertedScore[scoreKey]]; })
                    .reduce(function (acc, _a) {
                    var _b = __read(_a, 2), scoreKey = _b[0], score = _b[1];
                    // tokenize scorekey, first token is the interface name
                    var _c = __read(String(scoreKey).split(':'), 1), interfaceName = _c[0];
                    if (!acc[interfaceName]) {
                        acc[interfaceName] = [];
                    }
                    acc[interfaceName].push([scoreKey, score]);
                    return acc;
                }, {});
                // Aggregate score by interface
                var aggregate = Object.keys(scoresByInterface)
                    .map(function (interfaceName) { return [interfaceName, scoresByInterface[interfaceName]]; })
                    .reduce(function (acc, _a) {
                    var _b = __read(_a, 2), interfaceName = _b[0], allScores = _b[1];
                    // `null` scores means feature was not present in both issues, do not
                    // include in aggregate
                    var scores = allScores.filter(function (_a) {
                        var _b = __read(_a, 2), score = _b[1];
                        return score !== null;
                    });
                    var avg = scores.reduce(function (sum, _a) {
                        var _b = __read(_a, 2), score = _b[1];
                        return sum + score;
                    }, 0) / scores.length;
                    acc[interfaceName] = avg;
                    return acc;
                }, {});
                return {
                    issue: issue,
                    score: convertedScore,
                    scoresByInterface: scoresByInterface,
                    aggregate: aggregate,
                    isBelowThreshold: isBelowThreshold,
                };
            },
        };
        if (toFetchArray) {
            this.toFetchArray = toFetchArray;
        }
        return Promise.all(promises).then(function (resultsArray) {
            resultsArray.forEach(function (_a) {
                var dataKey = _a.dataKey, data = _a.data, links = _a.links;
                var items = dataKey === 'similar'
                    ? data.map(responseProcessors[dataKey])
                    : data.map(responseProcessors[dataKey]);
                _this[dataKey + "Items"] = items;
                _this[dataKey + "Links"] = links;
            });
            _this.loading = false;
            _this.error = false;
            _this.triggerFetchState();
        }, function () {
            _this.loading = false;
            _this.error = true;
            _this.triggerFetchState();
        });
    },
    // Toggle merge checkbox
    onToggleMerge: function (id) {
        var checked = false;
        // Don't do anything if item is busy
        var state = this.mergeState.has(id) ? this.mergeState.get(id) : undefined;
        if ((state === null || state === void 0 ? void 0 : state.busy) === true) {
            return;
        }
        if (this.mergeList.includes(id)) {
            this.mergeList = this.mergeList.filter(function (item) { return item !== id; });
        }
        else {
            this.mergeList = __spread(this.mergeList, [id]);
            checked = true;
        }
        this.setStateForId(this.mergeState, id, {
            checked: checked,
        });
        this.triggerMergeState();
    },
    // Toggle unmerge check box
    onToggleUnmerge: function (_a) {
        var _b = __read(_a, 2), fingerprint = _b[0], eventId = _b[1];
        var checked = false;
        // Uncheck an item to unmerge
        var state = this.unmergeState.get(fingerprint);
        if ((state === null || state === void 0 ? void 0 : state.busy) === true) {
            return;
        }
        if (this.unmergeList.has(fingerprint)) {
            this.unmergeList.delete(fingerprint);
        }
        else {
            this.unmergeList.set(fingerprint, eventId);
            checked = true;
        }
        // Update "checked" state for row
        this.setStateForId(this.unmergeState, fingerprint, {
            checked: checked,
        });
        // Unmerge should be disabled if 0 or all items are selected
        this.unmergeDisabled = this.unmergeList.size === 0 || this.isAllUnmergedSelected();
        this.enableFingerprintCompare = this.unmergeList.size === 2;
        this.triggerUnmergeState();
    },
    onUnmerge: function (_a) {
        var _this = this;
        var groupId = _a.groupId, loadingMessage = _a.loadingMessage, successMessage = _a.successMessage, errorMessage = _a.errorMessage;
        var ids = Array.from(this.unmergeList.keys());
        return new Promise(function (resolve, reject) {
            if (_this.isAllUnmergedSelected()) {
                reject(new Error('Not allowed to unmerge ALL events'));
                return;
            }
            // Disable unmerge button
            _this.unmergeDisabled = true;
            // Disable rows
            _this.setStateForId(_this.unmergeState, ids, {
                checked: false,
                busy: true,
            });
            _this.triggerUnmergeState();
            addLoadingMessage(loadingMessage);
            _this.api.request("/issues/" + groupId + "/hashes/", {
                method: 'DELETE',
                query: {
                    id: ids,
                },
                success: function () {
                    addSuccessMessage(successMessage);
                    // Busy rows after successful merge
                    _this.setStateForId(_this.unmergeState, ids, {
                        checked: false,
                        busy: true,
                    });
                    _this.unmergeList.clear();
                },
                error: function () {
                    addErrorMessage(errorMessage);
                    _this.setStateForId(_this.unmergeState, ids, {
                        checked: true,
                        busy: false,
                    });
                },
                complete: function () {
                    _this.unmergeDisabled = false;
                    resolve(_this.triggerUnmergeState());
                },
            });
        });
    },
    // For cross-project views, we need to pass projectId instead of
    // depending on router params (since we will only have orgId in that case)
    onMerge: function (_a) {
        var _this = this;
        var params = _a.params, query = _a.query, projectId = _a.projectId;
        if (!params) {
            return undefined;
        }
        var ids = this.mergeList;
        this.mergeDisabled = true;
        this.setStateForId(this.mergeState, ids, {
            busy: true,
        });
        this.triggerMergeState();
        var promise = new Promise(function (resolve) {
            // Disable merge button
            var orgId = params.orgId, groupId = params.groupId;
            _this.api.merge({
                orgId: orgId,
                projectId: projectId || params.projectId,
                itemIds: __spread(ids, [groupId]),
                query: query,
            }, {
                success: function (data) {
                    var _a;
                    if ((_a = data === null || data === void 0 ? void 0 : data.merge) === null || _a === void 0 ? void 0 : _a.parent) {
                        _this.trigger({
                            mergedParent: data.merge.parent,
                        });
                    }
                    // Hide rows after successful merge
                    _this.setStateForId(_this.mergeState, ids, {
                        checked: false,
                        busy: true,
                    });
                    _this.mergeList = [];
                },
                error: function () {
                    _this.setStateForId(_this.mergeState, ids, {
                        checked: true,
                        busy: false,
                    });
                },
                complete: function () {
                    _this.mergeDisabled = false;
                    resolve(_this.triggerMergeState());
                },
            });
        });
        return promise;
    },
    // Toggle collapsed state of all fingerprints
    onToggleCollapseFingerprints: function () {
        this.setStateForId(this.unmergeState, this.mergedItems.map(function (_a) {
            var id = _a.id;
            return id;
        }), {
            collapsed: !this.unmergeLastCollapsed,
        });
        this.unmergeLastCollapsed = !this.unmergeLastCollapsed;
        this.trigger({
            unmergeLastCollapsed: this.unmergeLastCollapsed,
            unmergeState: this.unmergeState,
        });
    },
    onToggleCollapseFingerprint: function (fingerprint) {
        var collapsed = this.unmergeState.has(fingerprint) && this.unmergeState.get(fingerprint).collapsed;
        this.setStateForId(this.unmergeState, fingerprint, { collapsed: !collapsed });
        this.trigger({
            unmergeState: this.unmergeState,
        });
    },
    triggerFetchState: function () {
        var state = __assign({ similarItems: this.similarItems.filter(function (_a) {
                var isBelowThreshold = _a.isBelowThreshold;
                return !isBelowThreshold;
            }), filteredSimilarItems: this.similarItems.filter(function (_a) {
                var isBelowThreshold = _a.isBelowThreshold;
                return isBelowThreshold;
            }) }, pick(this, [
            'mergedItems',
            'mergedLinks',
            'similarLinks',
            'mergeState',
            'unmergeState',
            'loading',
            'error',
        ]));
        this.trigger(state);
        return state;
    },
    triggerUnmergeState: function () {
        var state = pick(this, [
            'unmergeDisabled',
            'unmergeState',
            'unmergeList',
            'enableFingerprintCompare',
            'unmergeLastCollapsed',
        ]);
        this.trigger(state);
        return state;
    },
    triggerMergeState: function () {
        var state = pick(this, ['mergeDisabled', 'mergeState', 'mergeList']);
        this.trigger(state);
        return state;
    },
};
export default Reflux.createStore(storeConfig);
//# sourceMappingURL=groupingStore.jsx.map