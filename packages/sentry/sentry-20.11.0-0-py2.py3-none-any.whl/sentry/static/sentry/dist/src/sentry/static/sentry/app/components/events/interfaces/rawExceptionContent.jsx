import { __assign, __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import rawStacktraceContent from 'app/components/events/interfaces/rawStacktraceContent';
import LoadingIndicator from 'app/components/loadingIndicator';
import LoadingError from 'app/components/loadingError';
import ClippedBox from 'app/components/clippedBox';
import withApi from 'app/utils/withApi';
import withOrganization from 'app/utils/withOrganization';
import Button from 'app/components/button';
import { t } from 'app/locale';
var RawExceptionContent = /** @class */ (function (_super) {
    __extends(RawExceptionContent, _super);
    function RawExceptionContent() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: false,
            error: false,
            crashReport: '',
        };
        return _this;
    }
    RawExceptionContent.prototype.componentDidMount = function () {
        if (this.isNative()) {
            this.fetchAppleCrashReport();
        }
    };
    RawExceptionContent.prototype.componentDidUpdate = function (prevProps) {
        if (this.isNative() && this.props.type !== prevProps.type) {
            this.fetchAppleCrashReport();
        }
    };
    RawExceptionContent.prototype.isNative = function () {
        var platform = this.props.platform;
        return platform === 'cocoa' || platform === 'native';
    };
    RawExceptionContent.prototype.getAppleCrashReportEndpoint = function (organization) {
        var _a = this.props, type = _a.type, projectId = _a.projectId, eventId = _a.eventId;
        var minified = type === 'minified';
        return "/projects/" + organization.slug + "/" + projectId + "/events/" + eventId + "/apple-crash-report?minified=" + minified;
    };
    RawExceptionContent.prototype.getContent = function (isNative, exc) {
        var type = this.props.type;
        var output = {
            downloadButton: null,
            content: exc.stacktrace
                ? rawStacktraceContent(type === 'original' ? exc.stacktrace : exc.rawStacktrace, this.props.platform, exc)
                : null,
        };
        if (!isNative) {
            return output;
        }
        var _a = this.state, loading = _a.loading, error = _a.error, crashReport = _a.crashReport;
        if (loading) {
            return __assign(__assign({}, output), { content: <LoadingIndicator /> });
        }
        if (error) {
            return __assign(__assign({}, output), { content: <LoadingError /> });
        }
        if (!loading && !!crashReport) {
            var _b = this.props, api = _b.api, organization = _b.organization;
            var downloadButton = null;
            if (organization) {
                var appleCrashReportEndpoint = this.getAppleCrashReportEndpoint(organization);
                downloadButton = (<DownloadBtnWrapper>
            <Button size="xsmall" href={"" + api.baseUrl + appleCrashReportEndpoint + "&download=1"}>
              {t('Download')}
            </Button>
          </DownloadBtnWrapper>);
            }
            return {
                downloadButton: downloadButton,
                content: <ClippedBox clipHeight={250}>{crashReport}</ClippedBox>,
            };
        }
        return output;
    };
    RawExceptionContent.prototype.fetchAppleCrashReport = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, api, organization, data, _b;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, api = _a.api, organization = _a.organization;
                        // Shared issues do not have access to organization
                        if (!organization) {
                            return [2 /*return*/];
                        }
                        this.setState({
                            loading: true,
                            error: false,
                            crashReport: '',
                        });
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise(this.getAppleCrashReportEndpoint(organization))];
                    case 2:
                        data = _c.sent();
                        this.setState({
                            error: false,
                            loading: false,
                            crashReport: data,
                        });
                        return [3 /*break*/, 4];
                    case 3:
                        _b = _c.sent();
                        this.setState({ error: true, loading: false });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    RawExceptionContent.prototype.render = function () {
        var _this = this;
        var values = this.props.values;
        var isNative = this.isNative();
        if (!values) {
            return null;
        }
        return (<React.Fragment>
        {values.map(function (exc, excIdx) {
            var _a = _this.getContent(isNative, exc), downloadButton = _a.downloadButton, content = _a.content;
            if (!downloadButton && !content) {
                return null;
            }
            return (<div key={excIdx}>
              {downloadButton}
              <pre className="traceback plain">{content}</pre>
            </div>);
        })}
      </React.Fragment>);
    };
    return RawExceptionContent;
}(React.Component));
export default withApi(withOrganization(RawExceptionContent));
var DownloadBtnWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: flex-end;\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: flex-end;\n"])));
var templateObject_1;
//# sourceMappingURL=rawExceptionContent.jsx.map