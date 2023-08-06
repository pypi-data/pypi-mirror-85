import { __read, __spread, __values } from "tslib";
import jaro from 'wink-jaro-distance';
import { parseTrace, generateRootSpan, isOrphanSpan, toPercent, } from 'app/components/events/interfaces/spans/utils';
// Minimum threshold score for descriptions that are similar.
var COMMON_SIMILARITY_DESCRIPTION_THRESHOLD = 0.8;
export function isTransactionEvent(event) {
    if (!event) {
        return false;
    }
    return (event === null || event === void 0 ? void 0 : event.type) === 'transaction';
}
export function diffTransactions(_a) {
    var e_1, _b, e_2, _c;
    var _d, _e;
    var baselineEvent = _a.baselineEvent, regressionEvent = _a.regressionEvent;
    var baselineTrace = parseTrace(baselineEvent);
    var regressionTrace = parseTrace(regressionEvent);
    var rootSpans = [];
    var childSpans = {};
    try {
        // merge childSpans of baselineTrace and regressionTrace together
        for (var _f = __values(Object.entries(baselineTrace.childSpans)), _g = _f.next(); !_g.done; _g = _f.next()) {
            var _h = __read(_g.value, 2), parentSpanId = _h[0], children = _h[1];
            childSpans[parentSpanId] = children.map(function (baselineSpan) {
                return {
                    comparisonResult: 'baseline',
                    baselineSpan: baselineSpan,
                };
            });
        }
    }
    catch (e_1_1) { e_1 = { error: e_1_1 }; }
    finally {
        try {
            if (_g && !_g.done && (_b = _f.return)) _b.call(_f);
        }
        finally { if (e_1) throw e_1.error; }
    }
    try {
        for (var _j = __values(Object.entries(regressionTrace.childSpans)), _k = _j.next(); !_k.done; _k = _j.next()) {
            var _l = __read(_k.value, 2), parentSpanId = _l[0], children = _l[1];
            childSpans[parentSpanId] = children.map(function (regressionSpan) {
                return {
                    comparisonResult: 'regression',
                    regressionSpan: regressionSpan,
                };
            });
        }
    }
    catch (e_2_1) { e_2 = { error: e_2_1 }; }
    finally {
        try {
            if (_k && !_k.done && (_c = _j.return)) _c.call(_j);
        }
        finally { if (e_2) throw e_2.error; }
    }
    // merge the two transaction's span trees
    // we maintain a stack of spans to be compared
    var spansToBeCompared = [
        {
            type: 'root',
            baselineSpan: generateRootSpan(baselineTrace),
            regressionSpan: generateRootSpan(regressionTrace),
        },
    ];
    while (spansToBeCompared.length > 0) {
        var currentSpans = spansToBeCompared.pop();
        if (!currentSpans) {
            // typescript assumes currentSpans is undefined due to the nature of Array.prototype.pop()
            // returning undefined if spansToBeCompared is empty. the loop invariant guarantees that spansToBeCompared
            // is a non-empty array. we handle this case for sake of completeness
            break;
        }
        // invariant: the parents of currentSpans are matched spans; with the exception of the root spans of the baseline
        //            transaction and the regression transaction.
        // invariant: any unvisited siblings of currentSpans are in spansToBeCompared.
        // invariant: currentSpans and their siblings are already in childSpans
        var baselineSpan = currentSpans.baselineSpan, regressionSpan = currentSpans.regressionSpan;
        // The span from the base transaction is considered 'identical' to the span from the regression transaction
        // only if they share the same op name, depth level, and description.
        //
        // baselineSpan and regressionSpan have equivalent depth levels due to the nature of the tree traversal algorithm.
        if (matchableSpans({ baselineSpan: baselineSpan, regressionSpan: regressionSpan }) === 0) {
            if (currentSpans.type === 'root') {
                var spanComparisonResults = [
                    {
                        comparisonResult: 'baseline',
                        baselineSpan: baselineSpan,
                    },
                    {
                        comparisonResult: 'regression',
                        regressionSpan: regressionSpan,
                    },
                ];
                rootSpans.push.apply(rootSpans, __spread(spanComparisonResults));
            }
            // since baselineSpan and regressionSpan are considered not identical, we do not
            // need to compare their sub-trees
            continue;
        }
        var spanComparisonResult = {
            comparisonResult: 'matched',
            span_id: generateMergedSpanId({ baselineSpan: baselineSpan, regressionSpan: regressionSpan }),
            op: baselineSpan.op,
            description: baselineSpan.description,
            baselineSpan: baselineSpan,
            regressionSpan: regressionSpan,
        };
        if (currentSpans.type === 'root') {
            rootSpans.push(spanComparisonResult);
        }
        var _m = createChildPairs({
            parent_span_id: spanComparisonResult.span_id,
            baseChildren: (_d = baselineTrace.childSpans[baselineSpan.span_id]) !== null && _d !== void 0 ? _d : [],
            regressionChildren: (_e = regressionTrace.childSpans[regressionSpan.span_id]) !== null && _e !== void 0 ? _e : [],
        }), comparablePairs = _m.comparablePairs, children = _m.children;
        spansToBeCompared.push.apply(spansToBeCompared, __spread(comparablePairs));
        if (children.length > 0) {
            childSpans[spanComparisonResult.span_id] = children;
        }
    }
    rootSpans.sort(sortByMostTimeAdded);
    var report = {
        rootSpans: rootSpans,
        childSpans: childSpans,
    };
    return report;
}
function createChildPairs(_a) {
    // invariant: the parents of baseChildren and regressionChildren are matched spans
    var e_3, _b, e_4, _c;
    var parent_span_id = _a.parent_span_id, baseChildren = _a.baseChildren, regressionChildren = _a.regressionChildren;
    // for each child in baseChildren, pair them with the closest matching child in regressionChildren
    var comparablePairs = [];
    var children = [];
    var remainingRegressionChildren = __spread(regressionChildren);
    var _loop_1 = function (baselineSpan) {
        // reduce remainingRegressionChildren down to spans that are applicable candidate
        // of spans that can be paired with baselineSpan
        var candidates = remainingRegressionChildren.reduce(function (acc, regressionSpan, index) {
            var matchScore = matchableSpans({ baselineSpan: baselineSpan, regressionSpan: regressionSpan });
            if (matchScore !== 0) {
                acc.push({
                    regressionSpan: regressionSpan,
                    index: index,
                    matchScore: matchScore,
                });
            }
            return acc;
        }, []);
        if (candidates.length === 0) {
            children.push({
                comparisonResult: 'baseline',
                baselineSpan: baselineSpan,
            });
            return "continue";
        }
        // the best candidate span is one that has the closest start timestamp to baselineSpan;
        // and one that has a duration that's close to baselineSpan
        var baselineSpanDuration = Math.abs(baselineSpan.timestamp - baselineSpan.start_timestamp);
        var _a = candidates.reduce(function (bestCandidate, nextCandidate) {
            var thisSpan = bestCandidate.regressionSpan, thisSpanMatchScore = bestCandidate.matchScore;
            var otherSpan = nextCandidate.regressionSpan, otherSpanMatchScore = nextCandidate.matchScore;
            // calculate the deltas of the start timestamps relative to baselineSpan's
            // start timestamp
            var deltaStartTimestampThisSpan = Math.abs(thisSpan.start_timestamp - baselineSpan.start_timestamp);
            var deltaStartTimestampOtherSpan = Math.abs(otherSpan.start_timestamp - baselineSpan.start_timestamp);
            // calculate the deltas of the durations relative to the baselineSpan's
            // duration
            var thisSpanDuration = Math.abs(thisSpan.timestamp - thisSpan.start_timestamp);
            var otherSpanDuration = Math.abs(otherSpan.timestamp - otherSpan.start_timestamp);
            var deltaDurationThisSpan = Math.abs(thisSpanDuration - baselineSpanDuration);
            var deltaDurationOtherSpan = Math.abs(otherSpanDuration - baselineSpanDuration);
            var thisSpanScore = deltaDurationThisSpan + deltaStartTimestampThisSpan + (1 - thisSpanMatchScore);
            var otherSpanScore = deltaDurationOtherSpan + deltaStartTimestampOtherSpan + (1 - otherSpanMatchScore);
            if (thisSpanScore < otherSpanScore) {
                return bestCandidate;
            }
            if (thisSpanScore > otherSpanScore) {
                return nextCandidate;
            }
            return bestCandidate;
        }), regressionSpan = _a.regressionSpan, index = _a.index;
        // remove regressionSpan from list of remainingRegressionChildren
        remainingRegressionChildren.splice(index, 1);
        comparablePairs.push({
            type: 'descendent',
            parent_span_id: parent_span_id,
            baselineSpan: baselineSpan,
            regressionSpan: regressionSpan,
        });
        children.push({
            comparisonResult: 'matched',
            span_id: generateMergedSpanId({ baselineSpan: baselineSpan, regressionSpan: regressionSpan }),
            op: baselineSpan.op,
            description: baselineSpan.description,
            baselineSpan: baselineSpan,
            regressionSpan: regressionSpan,
        });
    };
    try {
        for (var baseChildren_1 = __values(baseChildren), baseChildren_1_1 = baseChildren_1.next(); !baseChildren_1_1.done; baseChildren_1_1 = baseChildren_1.next()) {
            var baselineSpan = baseChildren_1_1.value;
            _loop_1(baselineSpan);
        }
    }
    catch (e_3_1) { e_3 = { error: e_3_1 }; }
    finally {
        try {
            if (baseChildren_1_1 && !baseChildren_1_1.done && (_b = baseChildren_1.return)) _b.call(baseChildren_1);
        }
        finally { if (e_3) throw e_3.error; }
    }
    try {
        // push any remaining un-matched regressionSpans
        for (var remainingRegressionChildren_1 = __values(remainingRegressionChildren), remainingRegressionChildren_1_1 = remainingRegressionChildren_1.next(); !remainingRegressionChildren_1_1.done; remainingRegressionChildren_1_1 = remainingRegressionChildren_1.next()) {
            var regressionSpan = remainingRegressionChildren_1_1.value;
            children.push({
                comparisonResult: 'regression',
                regressionSpan: regressionSpan,
            });
        }
    }
    catch (e_4_1) { e_4 = { error: e_4_1 }; }
    finally {
        try {
            if (remainingRegressionChildren_1_1 && !remainingRegressionChildren_1_1.done && (_c = remainingRegressionChildren_1.return)) _c.call(remainingRegressionChildren_1);
        }
        finally { if (e_4) throw e_4.error; }
    }
    // sort children by most time added
    children.sort(sortByMostTimeAdded);
    return {
        comparablePairs: comparablePairs,
        children: children,
    };
}
function jaroSimilarity(thisString, otherString) {
    // based on https://winkjs.org/wink-distance/string-jaro-winkler.js.html
    // and https://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance
    if (thisString === otherString) {
        return 1;
    }
    var jaroDistance = jaro(thisString, otherString).distance;
    // Constant scaling factor for how much the score is adjusted upwards for having common prefixes.
    // This is only used for the Jaro–Winkler Similarity procedure.
    var scalingFactor = 0.1;
    // boostThreshold is the upper bound threshold of which if the Jaro score was less-than or equal
    // to boostThreshold, then the Jaro–Winkler Similarity procedure is applied. Otherwise,
    // 1 - jaroDistance is returned.
    var boostThreshold = 0.3;
    if (jaroDistance > boostThreshold) {
        return 1 - jaroDistance;
    }
    var pLimit = Math.min(thisString.length, otherString.length, 4);
    var l = 0;
    for (var i = 0; i < pLimit; i += 1) {
        if (thisString[i] === otherString[i]) {
            l += 1;
        }
        else {
            break;
        }
    }
    jaroDistance -= l * scalingFactor * jaroDistance;
    return 1 - jaroDistance;
}
function matchableSpans(_a) {
    var baselineSpan = _a.baselineSpan, regressionSpan = _a.regressionSpan;
    var opNamesEqual = baselineSpan.op === regressionSpan.op;
    if (!opNamesEqual) {
        return 0;
    }
    // remove whitespace and convert string to lower case as the individual characters
    // adds noise to the edit distance function
    var baselineDescription = (baselineSpan.description || '')
        .replace(/\s+/g, '')
        .toLowerCase();
    var regressionDescription = (regressionSpan.description || '')
        .replace(/\s+/g, '')
        .toLowerCase();
    var score = jaroSimilarity(baselineDescription, regressionDescription);
    return score >= COMMON_SIMILARITY_DESCRIPTION_THRESHOLD ? score : 0;
}
function generateMergedSpanId(_a) {
    var baselineSpan = _a.baselineSpan, regressionSpan = _a.regressionSpan;
    return "" + baselineSpan.span_id + regressionSpan.span_id;
}
function getDiffSpanDuration(diffSpan) {
    switch (diffSpan.comparisonResult) {
        case 'matched': {
            return Math.max(getSpanDuration(diffSpan.baselineSpan), getSpanDuration(diffSpan.regressionSpan));
        }
        case 'baseline': {
            return getSpanDuration(diffSpan.baselineSpan);
        }
        case 'regression': {
            return getSpanDuration(diffSpan.regressionSpan);
        }
        default: {
            throw Error('Unknown comparisonResult');
        }
    }
}
export function getSpanDuration(span) {
    return Math.abs(span.timestamp - span.start_timestamp);
}
function getMatchedSpanDurationDeltas(_a) {
    var baselineSpan = _a.baselineSpan, regressionSpan = _a.regressionSpan;
    return getSpanDuration(regressionSpan) - getSpanDuration(baselineSpan);
}
function sortDiffSpansByDuration(firstSpan, secondSpan) {
    var firstSpanDuration = getDiffSpanDuration(firstSpan);
    var secondSpanDuration = getDiffSpanDuration(secondSpan);
    if (firstSpanDuration > secondSpanDuration) {
        // sort firstSpan before secondSpan
        return -1;
    }
    if (firstSpanDuration < secondSpanDuration) {
        // sort secondSpan before firstSpan
        return 1;
    }
    return 0;
}
function sortSpans(firstSpan, secondSpan) {
    var firstSpanDuration = getSpanDuration(firstSpan);
    var secondSpanDuration = getSpanDuration(secondSpan);
    if (firstSpanDuration > secondSpanDuration) {
        // sort firstSpan before secondSpan
        return -1;
    }
    if (firstSpanDuration < secondSpanDuration) {
        // sort secondSpan before firstSpan
        return 1;
    }
    // try to break ties by sorting by start timestamp in ascending order
    if (firstSpan.start_timestamp < secondSpan.start_timestamp) {
        // sort firstSpan before secondSpan
        return -1;
    }
    if (firstSpan.start_timestamp > secondSpan.start_timestamp) {
        // sort secondSpan before firstSpan
        return 1;
    }
    return 0;
}
function sortByMostTimeAdded(firstSpan, secondSpan) {
    // Sort the spans by most time added. This means that when comparing the spans of the regression transaction
    // against the spans of the baseline transaction, we sort the spans by those that have regressed the most
    // relative to their baseline counter parts first.
    //
    // In terms of sort, we display them in the following way:
    // - Regression only spans; sorted first by duration (descending), and then start timestamps (ascending)
    // - Matched spans:
    //     - slower -- i.e. regression.duration - baseline.duration > 0 (sorted by duration deltas, and by duration)
    //     - no change -- i.e. regression.duration - baseline.duration == 0 (sorted by duration)
    //     - faster -- i.e. regression.duration - baseline.duration < 0 (sorted by duration deltas, and by duration)
    // - Baseline only spans; sorted by duration
    switch (firstSpan.comparisonResult) {
        case 'regression': {
            switch (secondSpan.comparisonResult) {
                case 'regression': {
                    return sortSpans(firstSpan.regressionSpan, secondSpan.regressionSpan);
                }
                case 'baseline':
                case 'matched': {
                    // sort firstSpan (regression) before secondSpan (baseline)
                    return -1;
                }
                default: {
                    throw Error('Unknown comparisonResult');
                }
            }
        }
        case 'baseline': {
            switch (secondSpan.comparisonResult) {
                case 'baseline': {
                    return sortSpans(firstSpan.baselineSpan, secondSpan.baselineSpan);
                }
                case 'regression':
                case 'matched': {
                    // sort secondSpan (regression or matched) before firstSpan (baseline)
                    return 1;
                }
                default: {
                    throw Error('Unknown comparisonResult');
                }
            }
        }
        case 'matched': {
            switch (secondSpan.comparisonResult) {
                case 'regression': {
                    // sort secondSpan (regression) before firstSpan (matched)
                    return 1;
                }
                case 'baseline': {
                    // sort firstSpan (matched) before secondSpan (baseline)
                    return -1;
                }
                case 'matched': {
                    var firstSpanDurationDelta = getMatchedSpanDurationDeltas({
                        regressionSpan: firstSpan.regressionSpan,
                        baselineSpan: firstSpan.baselineSpan,
                    });
                    var secondSpanDurationDelta = getMatchedSpanDurationDeltas({
                        regressionSpan: secondSpan.regressionSpan,
                        baselineSpan: secondSpan.baselineSpan,
                    });
                    if (firstSpanDurationDelta > 0) {
                        // firstSpan has slower regression span relative to the baseline span
                        if (secondSpanDurationDelta > 0) {
                            // secondSpan has slower regression span relative to the baseline span
                            if (firstSpanDurationDelta > secondSpanDurationDelta) {
                                // sort firstSpan before secondSpan
                                return -1;
                            }
                            if (firstSpanDurationDelta < secondSpanDurationDelta) {
                                // sort secondSpan before firstSpan
                                return 1;
                            }
                            return sortDiffSpansByDuration(firstSpan, secondSpan);
                        }
                        // case: secondSpan is either "no change" or "faster"
                        // sort firstSpan before secondSpan
                        return -1;
                    }
                    if (firstSpanDurationDelta === 0) {
                        // firstSpan has a regression span relative that didn't change relative to the baseline span
                        if (secondSpanDurationDelta > 0) {
                            // secondSpan has slower regression span relative to the baseline span
                            // sort secondSpan before firstSpan
                            return 1;
                        }
                        if (secondSpanDurationDelta < 0) {
                            // faster
                            // sort firstSpan before secondSpan
                            return -1;
                        }
                        // secondSpan has a regression span relative that didn't change relative to the baseline span
                        return sortDiffSpansByDuration(firstSpan, secondSpan);
                    }
                    // case: firstSpanDurationDelta < 0
                    if (secondSpanDurationDelta >= 0) {
                        // either secondSpan has slower regression span relative to the baseline span,
                        // or the secondSpan has a regression span relative that didn't change relative to the baseline span
                        // sort secondSpan before firstSpan
                        return 1;
                    }
                    // case: secondSpanDurationDelta < 0
                    if (firstSpanDurationDelta < secondSpanDurationDelta) {
                        // sort firstSpan before secondSpan
                        return -1;
                    }
                    if (firstSpanDurationDelta > secondSpanDurationDelta) {
                        // sort secondSpan before firstSpan
                        return 1;
                    }
                    return sortDiffSpansByDuration(firstSpan, secondSpan);
                }
                default: {
                    throw Error('Unknown comparisonResult');
                }
            }
        }
        default: {
            throw Error('Unknown comparisonResult');
        }
    }
}
export function getSpanID(diffSpan) {
    switch (diffSpan.comparisonResult) {
        case 'matched': {
            return diffSpan.span_id;
        }
        case 'baseline': {
            return diffSpan.baselineSpan.span_id;
        }
        case 'regression': {
            return diffSpan.regressionSpan.span_id;
        }
        default: {
            throw Error('Unknown comparisonResult');
        }
    }
}
export function getSpanOperation(diffSpan) {
    switch (diffSpan.comparisonResult) {
        case 'matched': {
            return diffSpan.op;
        }
        case 'baseline': {
            return diffSpan.baselineSpan.op;
        }
        case 'regression': {
            return diffSpan.regressionSpan.op;
        }
        default: {
            throw Error('Unknown comparisonResult');
        }
    }
}
export function getSpanDescription(diffSpan) {
    switch (diffSpan.comparisonResult) {
        case 'matched': {
            return diffSpan.description;
        }
        case 'baseline': {
            return diffSpan.baselineSpan.description;
        }
        case 'regression': {
            return diffSpan.regressionSpan.description;
        }
        default: {
            throw Error('Unknown comparisonResult');
        }
    }
}
export function isOrphanDiffSpan(diffSpan) {
    switch (diffSpan.comparisonResult) {
        case 'matched': {
            return isOrphanSpan(diffSpan.baselineSpan) || isOrphanSpan(diffSpan.regressionSpan);
        }
        case 'baseline': {
            return isOrphanSpan(diffSpan.baselineSpan);
        }
        case 'regression': {
            return isOrphanSpan(diffSpan.regressionSpan);
        }
        default: {
            throw Error('Unknown comparisonResult');
        }
    }
}
function generateWidth(_a) {
    var duration = _a.duration, largestDuration = _a.largestDuration;
    if (duration <= 0) {
        return {
            type: 'WIDTH_PIXEL',
            width: 1,
        };
    }
    return {
        type: 'WIDTH_PERCENTAGE',
        width: duration / largestDuration,
    };
}
export function boundsGenerator(rootSpans) {
    // get largest duration among the root spans.
    // invariant: this is the largest duration among all of the spans on the transaction
    //            comparison page.
    var largestDuration = Math.max.apply(Math, __spread(rootSpans.map(function (rootSpan) {
        return getDiffSpanDuration(rootSpan);
    })));
    return function (span) {
        switch (span.comparisonResult) {
            case 'matched': {
                var baselineDuration = getSpanDuration(span.baselineSpan);
                var regressionDuration = getSpanDuration(span.regressionSpan);
                var baselineWidth = generateWidth({
                    duration: baselineDuration,
                    largestDuration: largestDuration,
                });
                var regressionWidth = generateWidth({
                    duration: regressionDuration,
                    largestDuration: largestDuration,
                });
                if (baselineDuration >= regressionDuration) {
                    return {
                        background: baselineWidth,
                        foreground: regressionWidth,
                        baseline: baselineWidth,
                        regression: regressionWidth,
                    };
                }
                // case: baselineDuration < regressionDuration
                return {
                    background: regressionWidth,
                    foreground: baselineWidth,
                    baseline: baselineWidth,
                    regression: regressionWidth,
                };
            }
            case 'regression': {
                var regressionDuration = getSpanDuration(span.regressionSpan);
                var regressionWidth = generateWidth({
                    duration: regressionDuration,
                    largestDuration: largestDuration,
                });
                return {
                    background: regressionWidth,
                    foreground: undefined,
                    baseline: undefined,
                    regression: regressionWidth,
                };
            }
            case 'baseline': {
                var baselineDuration = getSpanDuration(span.baselineSpan);
                var baselineWidth = generateWidth({
                    duration: baselineDuration,
                    largestDuration: largestDuration,
                });
                return {
                    background: baselineWidth,
                    foreground: undefined,
                    baseline: baselineWidth,
                    regression: undefined,
                };
            }
            default: {
                var _exhaustiveCheck = span;
                return _exhaustiveCheck;
            }
        }
    };
}
export function generateCSSWidth(width) {
    if (!width) {
        return undefined;
    }
    switch (width.type) {
        case 'WIDTH_PIXEL': {
            return width.width + "px";
        }
        case 'WIDTH_PERCENTAGE': {
            return toPercent(width.width);
        }
        default: {
            var _exhaustiveCheck = width;
            return _exhaustiveCheck;
        }
    }
}
//# sourceMappingURL=utils.jsx.map