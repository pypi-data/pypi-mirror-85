import { __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import { ClassNames } from '@emotion/core';
import React from 'react';
import { addErrorMessage } from 'app/actionCreators/indicator';
import { createProject } from 'app/actionCreators/projects';
import { t, tct } from 'app/locale';
import Button from 'app/components/button';
import PlatformPicker from 'app/components/platformPicker';
import ProjectActions from 'app/actions/projectActions';
import space from 'app/styles/space';
import withApi from 'app/utils/withApi';
import withTeams from 'app/utils/withTeams';
var OnboardingPlatform = /** @class */ (function (_super) {
    __extends(OnboardingPlatform, _super);
    function OnboardingPlatform() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            firstProjectCreated: false,
            progressing: false,
        };
        _this.handleSetPlatform = function (platform) {
            var _a = _this.props, onUpdate = _a.onUpdate, onReturnToStep = _a.onReturnToStep;
            if (platform) {
                onUpdate({ platform: platform });
            }
            else {
                // Platform de-selected
                onReturnToStep({ platform: platform });
            }
        };
        _this.handleContinue = function () { return __awaiter(_this, void 0, void 0, function () {
            var platform;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        this.setState({ progressing: true });
                        platform = this.props.platform;
                        if (platform === null) {
                            return [2 /*return*/];
                        }
                        // Create their first project if they don't already have one. This is a
                        // no-op if they already have a project.
                        return [4 /*yield*/, this.createFirstProject(platform)];
                    case 1:
                        // Create their first project if they don't already have one. This is a
                        // no-op if they already have a project.
                        _a.sent();
                        this.props.onComplete({});
                        return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    OnboardingPlatform.prototype.componentDidUpdate = function (prevProps) {
        if (prevProps.active && !this.props.active) {
            // eslint-disable-next-line react/no-did-update-set-state
            this.setState({ progressing: false });
        }
    };
    Object.defineProperty(OnboardingPlatform.prototype, "hasFirstProject", {
        get: function () {
            return this.props.project || this.state.firstProjectCreated;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(OnboardingPlatform.prototype, "contineButtonLabel", {
        get: function () {
            if (this.state.progressing) {
                return t('Creating Project...');
            }
            if (!this.hasFirstProject) {
                return t('Create Project');
            }
            if (!this.props.active) {
                return t('Project Created');
            }
            return t('Setup Your Project');
        },
        enumerable: false,
        configurable: true
    });
    OnboardingPlatform.prototype.createFirstProject = function (platform) {
        return __awaiter(this, void 0, void 0, function () {
            var _a, api, orgId, teams, data, error_1;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, orgId = _a.orgId, teams = _a.teams;
                        if (this.hasFirstProject) {
                            return [2 /*return*/];
                        }
                        if (teams.length < 1) {
                            return [2 /*return*/];
                        }
                        this.setState({ firstProjectCreated: true });
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, createProject(api, orgId, teams[0].slug, orgId, platform, {
                                defaultRules: false,
                            })];
                    case 2:
                        data = _b.sent();
                        ProjectActions.createSuccess(data);
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _b.sent();
                        addErrorMessage(t('Failed to create project'));
                        throw error_1;
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    OnboardingPlatform.prototype.render = function () {
        var _this = this;
        var _a = this.props, active = _a.active, project = _a.project, platform = _a.platform, scrollTargetId = _a.scrollTargetId;
        var selectedPlatform = platform || (project && project.platform);
        var continueDisabled = !selectedPlatform || this.state.progressing || (this.hasFirstProject && !active);
        return (<React.Fragment>
        <p>
          {tct("Sentry integrates with many different languages and platforms\n             through the official [strong:Sentry SDKs]. Select your platform\n             from the list below to see a tailored installation process for\n             Sentry.", { strong: <strong /> })}
        </p>
        <p>
          {tct("Not seeing your platform in the list below? Select the\n             [strong:other platform], and use a community client!", { strong: <strong /> })}
        </p>
        <ClassNames>
          {function (_a) {
            var css = _a.css;
            return (<PlatformPicker noAutoFilter listClassName={css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n                max-height: 420px;\n                overflow-y: scroll;\n                /* Needed to fix overflow cropping of the de-select button */\n                margin-top: -", ";\n                padding-top: ", ";\n              "], ["\n                max-height: 420px;\n                overflow-y: scroll;\n                /* Needed to fix overflow cropping of the de-select button */\n                margin-top: -", ";\n                padding-top: ", ";\n              "])), space(2), space(2))} listProps={{ id: scrollTargetId }} platform={selectedPlatform} setPlatform={_this.handleSetPlatform}/>);
        }}
        </ClassNames>
        <Button data-test-id="platform-select-next" priority="primary" disabled={continueDisabled} onClick={this.handleContinue}>
          {this.contineButtonLabel}
        </Button>
      </React.Fragment>);
    };
    return OnboardingPlatform;
}(React.Component));
export default withApi(withTeams(OnboardingPlatform));
var templateObject_1;
//# sourceMappingURL=platform.jsx.map