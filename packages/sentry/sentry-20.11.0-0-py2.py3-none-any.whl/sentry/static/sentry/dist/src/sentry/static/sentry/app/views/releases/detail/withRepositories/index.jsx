import { __awaiter, __extends, __generator } from "tslib";
import React from 'react';
import * as Sentry from '@sentry/react';
import { t } from 'app/locale';
import getDisplayName from 'app/utils/getDisplayName';
import LoadingIndicator from 'app/components/loadingIndicator';
import { addErrorMessage } from 'app/actionCreators/indicator';
import { ReleaseContext } from '..';
import NoRepoConnected from './noRepoConnected';
var withRepositories = function (WrappedComponent) { var _a; return _a = /** @class */ (function (_super) {
        __extends(class_1, _super);
        function class_1() {
            var _this = _super !== null && _super.apply(this, arguments) || this;
            _this.state = {
                repositories: [],
                isLoading: true,
            };
            return _this;
        }
        class_1.prototype.componentDidMount = function () {
            this.fetchRepositories();
        };
        class_1.prototype.UNSAFE_componentWillReceiveProps = function (nextProps) {
            this.setActiveRepo(nextProps);
        };
        class_1.prototype.componentDidUpdate = function (_prevProps, prevState) {
            if (prevState.repositories.length !== this.state.repositories.length) {
                this.setActiveRepo(this.props);
            }
        };
        class_1.prototype.setActiveRepo = function (props) {
            var _a, _b;
            var _c = this.state, repositories = _c.repositories, activeRepository = _c.activeRepository;
            if (!repositories.length) {
                return;
            }
            var activeRepo = (_a = props.location.query) === null || _a === void 0 ? void 0 : _a.activeRepo;
            if (!activeRepo) {
                this.setState({
                    activeRepository: (_b = repositories[0]) !== null && _b !== void 0 ? _b : null,
                });
                return;
            }
            if (activeRepo === (activeRepository === null || activeRepository === void 0 ? void 0 : activeRepository.name)) {
                return;
            }
            var matchedRepository = repositories.find(function (repo) { return repo.name === activeRepo; });
            if (matchedRepository) {
                this.setState({
                    activeRepository: matchedRepository,
                });
                return;
            }
            addErrorMessage(t('The repository you were looking for was not found.'));
        };
        class_1.prototype.getEndpoint = function () {
            var params = this.props.params;
            var release = params.release, orgId = params.orgId;
            var project = this.context.project;
            return "/projects/" + orgId + "/" + project.slug + "/releases/" + encodeURIComponent(release) + "/repositories/";
        };
        class_1.prototype.fetchRepositories = function () {
            return __awaiter(this, void 0, void 0, function () {
                var params, release, repositories, error_1;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            params = this.props.params;
                            release = params.release;
                            this.setState({ isLoading: true });
                            _a.label = 1;
                        case 1:
                            _a.trys.push([1, 3, , 4]);
                            return [4 /*yield*/, this.props.api.requestPromise(this.getEndpoint())];
                        case 2:
                            repositories = _a.sent();
                            this.setState({ repositories: repositories, isLoading: false });
                            return [3 /*break*/, 4];
                        case 3:
                            error_1 = _a.sent();
                            Sentry.captureException(error_1);
                            addErrorMessage(t('An error occured while trying to fetch the repositories of the release: %s', release));
                            return [3 /*break*/, 4];
                        case 4: return [2 /*return*/];
                    }
                });
            });
        };
        class_1.prototype.render = function () {
            var _a = this.state, isLoading = _a.isLoading, activeRepository = _a.activeRepository, repositories = _a.repositories;
            if (isLoading) {
                return <LoadingIndicator />;
            }
            if (!repositories.length) {
                return <NoRepoConnected orgId={this.props.params.orgId}/>;
            }
            if (activeRepository === undefined) {
                return <LoadingIndicator />;
            }
            return (<WrappedComponent {...this.props} projectSlug={this.context.project.slug} repositories={repositories} activeRepository={activeRepository}/>);
        };
        return class_1;
    }(React.Component)),
    _a.displayName = "withRepositories(" + getDisplayName(WrappedComponent) + ")",
    _a.contextType = ReleaseContext,
    _a; };
export default withRepositories;
//# sourceMappingURL=index.jsx.map