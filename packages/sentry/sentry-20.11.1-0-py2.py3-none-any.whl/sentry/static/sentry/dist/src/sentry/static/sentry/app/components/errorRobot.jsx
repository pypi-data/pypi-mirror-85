import { __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import { Link } from 'react-router';
import React from 'react';
import styled from '@emotion/styled';
import { t, tct } from 'app/locale';
import Button from 'app/components/button';
import CreateSampleEventButton from 'app/views/onboarding/createSampleEventButton';
import withApi from 'app/utils/withApi';
import { defined } from 'app/utils';
import space from 'app/styles/space';
import robotBackground from 'app/../images/spot/sentry-robot.png';
var ErrorRobot = /** @class */ (function (_super) {
    __extends(ErrorRobot, _super);
    function ErrorRobot() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            error: false,
            loading: false,
            sampleIssueId: _this.props.sampleIssueId,
        };
        return _this;
    }
    ErrorRobot.prototype.componentDidMount = function () {
        this.fetchData();
    };
    ErrorRobot.prototype.fetchData = function () {
        var _a, _b;
        return __awaiter(this, void 0, void 0, function () {
            var _c, org, project, sampleIssueId, url, data, err_1, error;
            return __generator(this, function (_d) {
                switch (_d.label) {
                    case 0:
                        _c = this.props, org = _c.org, project = _c.project;
                        sampleIssueId = this.state.sampleIssueId;
                        if (!project) {
                            return [2 /*return*/];
                        }
                        if (defined(sampleIssueId)) {
                            return [2 /*return*/];
                        }
                        url = "/projects/" + org.slug + "/" + project.slug + "/issues/";
                        this.setState({ loading: true });
                        _d.label = 1;
                    case 1:
                        _d.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.props.api.requestPromise(url, {
                                method: 'GET',
                                data: { limit: 1 },
                            })];
                    case 2:
                        data = _d.sent();
                        this.setState({ sampleIssueId: (data.length > 0 && data[0].id) || '' });
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _d.sent();
                        error = (_b = (_a = err_1 === null || err_1 === void 0 ? void 0 : err_1.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) !== null && _b !== void 0 ? _b : true;
                        this.setState({ error: error });
                        return [3 /*break*/, 4];
                    case 4:
                        this.setState({ loading: false });
                        return [2 /*return*/];
                }
            });
        });
    };
    ErrorRobot.prototype.render = function () {
        var _a = this.state, loading = _a.loading, error = _a.error, sampleIssueId = _a.sampleIssueId;
        var _b = this.props, org = _b.org, project = _b.project, gradient = _b.gradient;
        var sampleLink = project && (loading || error ? null : sampleIssueId) ? (<p>
          <Link to={"/" + org.slug + "/" + project.slug + "/issues/" + sampleIssueId + "/?sample"}>
            {t('Or see your sample event')}
          </Link>
        </p>) : (<p>
          <CreateSampleEventButton priority="link" borderless project={project} source="issues_list" disabled={!project} title={!project ? t('Select a project to create a sample event') : undefined}>
            {t('Create a sample event')}
          </CreateSampleEventButton>
        </p>);
        return (<ErrorRobotWrapper data-test-id="awaiting-events" className="awaiting-events" gradient={gradient}>
        <Robot aria-hidden>
          <Eye />
        </Robot>
        <MessageContainer>
          <h3>{t('Waiting for events…')}</h3>
          <p>
            {tct('Our error robot is waiting to [strike:devour] receive your first event.', {
            strike: <Strikethrough />,
        })}
          </p>
          <p>
            {project && (<Button data-test-id="install-instructions" priority="primary" to={"/" + org.slug + "/" + project.slug + "/getting-started/" + (project.platform || '')}>
                {t('Installation Instructions')}
              </Button>)}
          </p>
          {sampleLink}
        </MessageContainer>
      </ErrorRobotWrapper>);
    };
    return ErrorRobot;
}(React.Component));
export { ErrorRobot };
export default withApi(ErrorRobot);
var ErrorRobotWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  justify-content: center;\n  font-size: ", ";\n  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.08);\n  border-radius: 0 0 3px 3px;\n  padding: 40px ", " ", ";\n  min-height: 260px;\n  ", ";\n\n  @media (max-width: ", ") {\n    flex-direction: column;\n    align-items: center;\n    padding: ", ";\n    text-align: center;\n  }\n"], ["\n  display: flex;\n  justify-content: center;\n  font-size: ", ";\n  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.08);\n  border-radius: 0 0 3px 3px;\n  padding: 40px ", " ", ";\n  min-height: 260px;\n  ",
    ";\n\n  @media (max-width: ", ") {\n    flex-direction: column;\n    align-items: center;\n    padding: ", ";\n    text-align: center;\n  }\n"])), function (p) { return p.theme.fontSizeExtraLarge; }, space(3), space(3), function (p) {
    return p.gradient
        ? "\n          background-image: linear-gradient(to bottom, " + p.theme.backgroundSecondary + ", " + p.theme.background + ");\n         "
        : '';
}, function (p) { return p.theme.breakpoints[0]; }, space(3));
var Robot = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: block;\n  position: relative;\n  width: 220px;\n  height: 260px;\n  background: url(", ");\n  background-size: cover;\n\n  @media (max-width: ", ") {\n    width: 110px;\n    height: 130px;\n  }\n"], ["\n  display: block;\n  position: relative;\n  width: 220px;\n  height: 260px;\n  background: url(", ");\n  background-size: cover;\n\n  @media (max-width: ", ") {\n    width: 110px;\n    height: 130px;\n  }\n"])), robotBackground, function (p) { return p.theme.breakpoints[0]; });
var Eye = styled('span')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  width: 12px;\n  height: 12px;\n  border-radius: 50%;\n  position: absolute;\n  top: 70px;\n  left: 81px;\n  transform: translateZ(0);\n  animation: blink-eye 0.6s infinite;\n\n  @media (max-width: ", ") {\n    width: 6px;\n    height: 6px;\n    top: 35px;\n    left: 41px;\n  }\n\n  @keyframes blink-eye {\n    0% {\n      background: #e03e2f;\n      box-shadow: 0 0 10px #e03e2f;\n    }\n\n    50% {\n      background: #4a4d67;\n      box-shadow: none;\n    }\n\n    100% {\n      background: #e03e2f;\n      box-shadow: 0 0 10px #e03e2f;\n    }\n  }\n"], ["\n  width: 12px;\n  height: 12px;\n  border-radius: 50%;\n  position: absolute;\n  top: 70px;\n  left: 81px;\n  transform: translateZ(0);\n  animation: blink-eye 0.6s infinite;\n\n  @media (max-width: ", ") {\n    width: 6px;\n    height: 6px;\n    top: 35px;\n    left: 41px;\n  }\n\n  @keyframes blink-eye {\n    0% {\n      background: #e03e2f;\n      box-shadow: 0 0 10px #e03e2f;\n    }\n\n    50% {\n      background: #4a4d67;\n      box-shadow: none;\n    }\n\n    100% {\n      background: #e03e2f;\n      box-shadow: 0 0 10px #e03e2f;\n    }\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
var MessageContainer = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  align-self: center;\n  max-width: 480px;\n  margin-left: 40px;\n\n  @media (max-width: ", ") {\n    margin: 0;\n  }\n"], ["\n  align-self: center;\n  max-width: 480px;\n  margin-left: 40px;\n\n  @media (max-width: ", ") {\n    margin: 0;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
var Strikethrough = styled('span')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  text-decoration: line-through;\n"], ["\n  text-decoration: line-through;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=errorRobot.jsx.map