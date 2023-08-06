import { __awaiter, __extends, __generator, __read, __spread } from "tslib";
import React from 'react';
import pick from 'lodash/pick';
import { t } from 'app/locale';
import EmptyStateWarning from 'app/components/emptyStateWarning';
import { createFuzzySearch } from 'app/utils/createFuzzySearch';
import DragManager from './dragManager';
import SpanTree from './spanTree';
import { generateRootSpan, getSpanID, getTraceContext } from './utils';
import TraceViewHeader from './header';
import * as CursorGuideHandler from './cursorGuideHandler';
var TraceView = /** @class */ (function (_super) {
    __extends(TraceView, _super);
    function TraceView(props) {
        var _this = _super.call(this, props) || this;
        _this.minimapInteractiveRef = React.createRef();
        _this.renderHeader = function (dragProps, parsedTrace) { return (<TraceViewHeader minimapInteractiveRef={_this.minimapInteractiveRef} dragProps={dragProps} trace={parsedTrace}/>); };
        _this.state = {
            filterSpans: undefined,
        };
        _this.filterOnSpans(props.searchQuery);
        return _this;
    }
    TraceView.prototype.componentDidUpdate = function (prevProps) {
        if (prevProps.searchQuery !== this.props.searchQuery) {
            this.filterOnSpans(this.props.searchQuery);
        }
    };
    TraceView.prototype.filterOnSpans = function (searchQuery) {
        return __awaiter(this, void 0, void 0, function () {
            var parsedTrace, spans, transformed, fuse, results, spanIDs;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        if (!searchQuery) {
                            // reset
                            if (this.state.filterSpans !== undefined) {
                                this.setState({
                                    filterSpans: undefined,
                                });
                            }
                            return [2 /*return*/];
                        }
                        parsedTrace = this.props.parsedTrace;
                        spans = parsedTrace.spans;
                        transformed = __spread([generateRootSpan(parsedTrace)], spans).map(function (span) {
                            var _a;
                            var indexed = [];
                            // basic properties
                            var pickedSpan = pick(span, [
                                // TODO: do we want this?
                                // 'trace_id',
                                'span_id',
                                'start_timestamp',
                                'timestamp',
                                'op',
                                'description',
                            ]);
                            var basicValues = Object.values(pickedSpan)
                                .filter(function (value) { return !!value; })
                                .map(function (value) { return String(value); });
                            indexed.push.apply(indexed, __spread(basicValues));
                            // tags
                            var tagKeys = [];
                            var tagValues = [];
                            var tags = span === null || span === void 0 ? void 0 : span.tags;
                            if (tags) {
                                tagKeys = Object.keys(tags);
                                tagValues = Object.values(tags);
                            }
                            var data = (_a = span === null || span === void 0 ? void 0 : span.data) !== null && _a !== void 0 ? _a : {};
                            var dataKeys = [];
                            var dataValues = [];
                            if (data) {
                                dataKeys = Object.keys(data);
                                dataValues = Object.values(data).map(function (value) { return JSON.stringify(value, null, 4) || ''; });
                            }
                            return {
                                span: span,
                                indexed: indexed,
                                tagKeys: tagKeys,
                                tagValues: tagValues,
                                dataKeys: dataKeys,
                                dataValues: dataValues,
                            };
                        });
                        return [4 /*yield*/, createFuzzySearch(transformed, {
                                keys: ['indexed', 'tagKeys', 'tagValues', 'dataKeys', 'dataValues'],
                                includeMatches: false,
                                threshold: 0.6,
                                location: 0,
                                distance: 100,
                                maxPatternLength: 32,
                            })];
                    case 1:
                        fuse = _a.sent();
                        results = fuse.search(searchQuery);
                        spanIDs = results.reduce(function (setOfSpanIDs, result) {
                            var spanID = getSpanID(result.item.span);
                            if (spanID) {
                                setOfSpanIDs.add(spanID);
                            }
                            return setOfSpanIDs;
                        }, new Set());
                        this.setState({
                            filterSpans: {
                                results: results,
                                spanIDs: spanIDs,
                            },
                        });
                        return [2 /*return*/];
                }
            });
        });
    };
    TraceView.prototype.render = function () {
        var _this = this;
        var _a = this.props, event = _a.event, parsedTrace = _a.parsedTrace;
        if (!getTraceContext(event)) {
            return (<EmptyStateWarning>
          <p>{t('There is no trace for this transaction')}</p>
        </EmptyStateWarning>);
        }
        var _b = this.props, orgId = _b.orgId, organization = _b.organization, spansWithErrors = _b.spansWithErrors, operationNameFilters = _b.operationNameFilters;
        return (<DragManager interactiveLayerRef={this.minimapInteractiveRef}>
        {function (dragProps) { return (<CursorGuideHandler.Provider interactiveLayerRef={_this.minimapInteractiveRef} dragProps={dragProps} trace={parsedTrace}>
            {_this.renderHeader(dragProps, parsedTrace)}
            <SpanTree event={event} trace={parsedTrace} dragProps={dragProps} filterSpans={_this.state.filterSpans} orgId={orgId} organization={organization} spansWithErrors={spansWithErrors} operationNameFilters={operationNameFilters}/>
          </CursorGuideHandler.Provider>); }}
      </DragManager>);
    };
    return TraceView;
}(React.PureComponent));
export default TraceView;
//# sourceMappingURL=traceView.jsx.map