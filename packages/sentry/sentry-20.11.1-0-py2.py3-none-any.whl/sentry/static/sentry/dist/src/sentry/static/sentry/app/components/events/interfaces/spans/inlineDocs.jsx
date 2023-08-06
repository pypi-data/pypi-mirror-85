import { __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import * as Sentry from '@sentry/react';
import withApi from 'app/utils/withApi';
import { loadDocs } from 'app/actionCreators/projects';
import { t, tct } from 'app/locale';
import LoadingIndicator from 'app/components/loadingIndicator';
var InlineDocs = /** @class */ (function (_super) {
    __extends(InlineDocs, _super);
    function InlineDocs() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: true,
            html: undefined,
            link: undefined,
        };
        _this.fetchData = function () { return __awaiter(_this, void 0, void 0, function () {
            var _a, platform, api, orgSlug, projectSlug, tracingPlatform, _b, html, link, error_1;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, platform = _a.platform, api = _a.api, orgSlug = _a.orgSlug, projectSlug = _a.projectSlug;
                        if (!platform) {
                            return [2 /*return*/];
                        }
                        this.setState({ loading: true });
                        switch (platform) {
                            case 'sentry.python': {
                                tracingPlatform = 'python-tracing';
                                break;
                            }
                            case 'sentry.javascript.node': {
                                tracingPlatform = 'node-tracing';
                                break;
                            }
                            default: {
                                this.setState({ loading: false });
                                return [2 /*return*/];
                            }
                        }
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, loadDocs(api, orgSlug, projectSlug, tracingPlatform)];
                    case 2:
                        _b = _c.sent(), html = _b.html, link = _b.link;
                        this.setState({ html: html, link: link });
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _c.sent();
                        Sentry.captureException(error_1);
                        this.setState({ html: undefined, link: undefined });
                        return [3 /*break*/, 4];
                    case 4:
                        this.setState({ loading: false });
                        return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    InlineDocs.prototype.componentDidMount = function () {
        this.fetchData();
    };
    InlineDocs.prototype.render = function () {
        var platform = this.props.platform;
        if (!platform) {
            return null;
        }
        if (this.state.loading) {
            return (<div>
          <LoadingIndicator />
        </div>);
        }
        if (this.state.html) {
            return (<div>
          <h4>{t('Requires Manual Instrumentation')}</h4>
          <DocumentationWrapper dangerouslySetInnerHTML={{ __html: this.state.html }}/>
          <p>
            {tct("For in-depth instructions on setting up tracing, view [docLink:our documentation].", {
                docLink: <a href={this.state.link}/>,
            })}
          </p>
        </div>);
        }
        return (<div>
        <h4>{t('Requires Manual Instrumentation')}</h4>
        <p>
          {tct("To manually instrument certain regions of your code, view [docLink:our documentation].", {
            docLink: <a href="https://docs.sentry.io/performance-monitoring/setup/"/>,
        })}
        </p>
      </div>);
    };
    return InlineDocs;
}(React.Component));
var DocumentationWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  p {\n    line-height: 1.5;\n  }\n  pre {\n    word-break: break-all;\n    white-space: pre-wrap;\n  }\n"], ["\n  p {\n    line-height: 1.5;\n  }\n  pre {\n    word-break: break-all;\n    white-space: pre-wrap;\n  }\n"])));
export default withApi(InlineDocs);
var templateObject_1;
//# sourceMappingURL=inlineDocs.jsx.map