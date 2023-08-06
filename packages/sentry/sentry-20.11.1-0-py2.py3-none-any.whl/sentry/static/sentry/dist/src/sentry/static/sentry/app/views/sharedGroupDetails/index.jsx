import { __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import DocumentTitle from 'react-document-title';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import withApi from 'app/utils/withApi';
import { BorderlessEventEntries } from 'app/components/events/eventEntries';
import Footer from 'app/components/footer';
import LoadingError from 'app/components/loadingError';
import LoadingIndicator from 'app/components/loadingIndicator';
import NotFound from 'app/components/errors/notFound';
import space from 'app/styles/space';
import Link from 'app/components/links/link';
import SentryTypes from 'app/sentryTypes';
import SharedGroupHeader from './sharedGroupHeader';
var SharedGroupDetails = /** @class */ (function (_super) {
    __extends(SharedGroupDetails, _super);
    function SharedGroupDetails() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = _this.getInitialState();
        _this.handleRetry = function () {
            _this.setState(_this.getInitialState());
            _this.fetchData();
        };
        return _this;
    }
    SharedGroupDetails.prototype.getInitialState = function () {
        return {
            group: null,
            loading: true,
            error: false,
        };
    };
    SharedGroupDetails.prototype.getChildContext = function () {
        return {
            group: this.state.group,
        };
    };
    SharedGroupDetails.prototype.componentWillMount = function () {
        document.body.classList.add('shared-group');
    };
    SharedGroupDetails.prototype.componentDidMount = function () {
        this.fetchData();
    };
    SharedGroupDetails.prototype.componentWillUnmount = function () {
        document.body.classList.remove('shared-group');
    };
    SharedGroupDetails.prototype.fetchData = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, params, api, shareId, group, _b;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, params = _a.params, api = _a.api;
                        shareId = params.shareId;
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/shared/issues/" + shareId + "/")];
                    case 2:
                        group = _c.sent();
                        this.setState({ loading: false, group: group });
                        return [3 /*break*/, 4];
                    case 3:
                        _b = _c.sent();
                        this.setState({ loading: false, error: true });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    SharedGroupDetails.prototype.getTitle = function () {
        var group = this.state.group;
        if (group) {
            return group.title;
        }
        return 'Sentry';
    };
    SharedGroupDetails.prototype.render = function () {
        var _a = this.state, group = _a.group, loading = _a.loading, error = _a.error;
        if (loading) {
            return <LoadingIndicator />;
        }
        if (!group) {
            return <NotFound />;
        }
        if (error) {
            return <LoadingError onRetry={this.handleRetry}/>;
        }
        var location = this.props.location;
        var permalink = group.permalink, latestEvent = group.latestEvent, project = group.project;
        var title = this.getTitle();
        return (<DocumentTitle title={title}>
        <div className="app">
          <div className="pattern-bg"/>
          <div className="container">
            <div className="box box-modal">
              <div className="box-header">
                <Link className="logo" to="/">
                  <span className="icon-sentry-logo-full"/>
                </Link>
                {permalink && (<Link className="details" to={permalink}>
                    {t('Details')}
                  </Link>)}
              </div>
              <div className="content">
                <SharedGroupHeader group={group}/>
                <Container className="group-overview event-details-container">
                  <BorderlessEventEntries location={location} organization={project.organization} group={group} event={latestEvent} project={project} isShare/>
                </Container>
                <Footer />
              </div>
            </div>
          </div>
        </div>
      </DocumentTitle>);
    };
    SharedGroupDetails.childContextTypes = {
        group: SentryTypes.Group,
    };
    return SharedGroupDetails;
}(React.Component));
var Container = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: 0 ", ";\n"], ["\n  padding: 0 ", ";\n"])), space(4));
export { SharedGroupDetails };
export default withApi(SharedGroupDetails);
var templateObject_1;
//# sourceMappingURL=index.jsx.map