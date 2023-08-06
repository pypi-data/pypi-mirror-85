import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import PropTypes from 'prop-types';
import * as Sentry from '@sentry/react';
import { t } from 'app/locale';
import { trackAnalyticsEvent, trackAdhocEvent } from 'app/utils/analytics';
import Button from 'app/components/button';
import EmptyStateWarning from 'app/components/emptyStateWarning';
import SentryTypes from 'app/sentryTypes';
import space from 'app/styles/space';
import withOrganization from 'app/utils/withOrganization';
import withProjects from 'app/utils/withProjects';
import UserFeedbackIllustration from './userFeedbackIllustration';
var UserFeedbackEmpty = /** @class */ (function (_super) {
    __extends(UserFeedbackEmpty, _super);
    function UserFeedbackEmpty() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    UserFeedbackEmpty.prototype.componentDidMount = function () {
        var _a = this.props, organization = _a.organization, projectIds = _a.projectIds;
        window.sentryEmbedCallback = function (embed) {
            // Mock the embed's submit xhr to always be successful
            // NOTE: this will not have errors if the form is empty
            embed.submit = function (_body) {
                var _this = this;
                this._submitInProgress = true;
                setTimeout(function () {
                    _this._submitInProgress = false;
                    _this.onSuccess();
                }, 500);
            };
        };
        if (this.hasAnyFeedback === false) {
            // send to reload only due to higher event volume
            trackAdhocEvent({
                eventKey: 'user_feedback.viewed',
                org_id: parseInt(organization.id, 10),
                projects: projectIds,
            });
        }
    };
    UserFeedbackEmpty.prototype.componentWillUnmount = function () {
        window.sentryEmbedCallback = null;
    };
    Object.defineProperty(UserFeedbackEmpty.prototype, "hasAnyFeedback", {
        get: function () {
            var _a = this.props, projects = _a.projects, projectIds = _a.projectIds;
            var selectedProjects = projectIds && projectIds.length
                ? projects.filter(function (_a) {
                    var id = _a.id;
                    return projectIds.includes(id);
                })
                : projects;
            return selectedProjects.some(function (_a) {
                var hasUserReports = _a.hasUserReports;
                return hasUserReports;
            });
        },
        enumerable: false,
        configurable: true
    });
    UserFeedbackEmpty.prototype.trackAnalytics = function (_a) {
        var eventKey = _a.eventKey, eventName = _a.eventName;
        var _b = this.props, organization = _b.organization, projectIds = _b.projectIds;
        trackAnalyticsEvent({
            eventKey: eventKey,
            eventName: eventName,
            organization_id: organization.id,
            projects: projectIds,
        });
    };
    UserFeedbackEmpty.prototype.render = function () {
        var _this = this;
        // Show no user reports if waiting for projects to load or if there is no feedback
        if (this.props.loadingProjects || this.hasAnyFeedback !== false) {
            return (<EmptyStateWarning>
          <p>{t('Sorry, no user reports match your filters.')}</p>
        </EmptyStateWarning>);
        }
        // Show landing page after projects have loaded and it is confirmed no projects have feedback
        return (<UserFeedbackLanding>
        <IllustrationContainer>
          <CardComponentContainer>
            <StyledUserFeedbackIllustration />
          </CardComponentContainer>
        </IllustrationContainer>

        <StyledBox>
          <h3>{t('No User Feedback Collected')}</h3>
          <p>
            {t("Don't rely on stack traces and graphs alone to understand\n              the cause and impact of errors. Enable User Feedback to collect\n              your users' comments when they encounter a crash or bug.")}
          </p>
          <ButtonList>
            <Button external onClick={function () {
            return _this.trackAnalytics({
                eventKey: 'user_feedback.docs_clicked',
                eventName: 'User Feedback Docs Clicked',
            });
        }} href="https://docs.sentry.io/enriching-error-data/user-feedback/">
              {t('Read the docs')}
            </Button>
            <Button priority="primary" onClick={function () {
            Sentry.showReportDialog({
                // should never make it to the Sentry API, but just in case, use throwaway id
                eventId: '00000000000000000000000000000000',
            });
            _this.trackAnalytics({
                eventKey: 'user_feedback.dialog_opened',
                eventName: 'User Feedback Dialog Opened',
            });
        }}>
              {t('Open the report dialog')}
            </Button>
          </ButtonList>
        </StyledBox>
      </UserFeedbackLanding>);
    };
    UserFeedbackEmpty.propTypes = {
        organization: SentryTypes.Organization.isRequired,
        projectIds: PropTypes.arrayOf(PropTypes.string.isRequired),
    };
    return UserFeedbackEmpty;
}(React.Component));
var UserFeedbackLanding = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  flex-wrap: wrap;\n  min-height: 450px;\n  padding: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  flex-wrap: wrap;\n  min-height: 450px;\n  padding: ", ";\n"])), space(1));
var StyledBox = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  flex: 1;\n  padding: ", ";\n"], ["\n  flex: 1;\n  padding: ", ";\n"])), space(3));
var IllustrationContainer = styled(StyledBox)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n"])));
var CardComponentContainer = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  width: 550px;\n  height: 340px;\n\n  @media (max-width: 1150px) {\n    font-size: ", ";\n    width: 450px;\n  }\n\n  @media (max-width: 1000px) {\n    font-size: ", ";\n    width: 320px;\n    max-height: 180px;\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  width: 550px;\n  height: 340px;\n\n  @media (max-width: 1150px) {\n    font-size: ", ";\n    width: 450px;\n  }\n\n  @media (max-width: 1000px) {\n    font-size: ", ";\n    width: 320px;\n    max-height: 180px;\n  }\n"])), function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.fontSizeSmall; });
var StyledUserFeedbackIllustration = styled(UserFeedbackIllustration)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  width: 100%;\n  height: 100%;\n"], ["\n  width: 100%;\n  height: 100%;\n"])));
var ButtonList = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: repeat(auto-fit, minmax(130px, max-content));\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: repeat(auto-fit, minmax(130px, max-content));\n  grid-gap: ", ";\n"])), space(1));
export { UserFeedbackEmpty };
export default withOrganization(withProjects(UserFeedbackEmpty));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=userFeedbackEmpty.jsx.map