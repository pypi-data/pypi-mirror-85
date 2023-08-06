import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import congratsRobotsPlaceholder from 'app/../images/spot/congrats-robots-placeholder.jpg';
import space from 'app/styles/space';
var Placeholder = function () { return (<PlaceholderImage alt={t('Congrats, you have no unresolved issues')} src={congratsRobotsPlaceholder}/>); };
var Message = function () { return (<React.Fragment>
    <EmptyMessage>
      {t("We couldn't find any issues that matched your filters.")}
    </EmptyMessage>
    <p>{t('Get out there and write some broken code!')}</p>
  </React.Fragment>); };
var CongratsRobotsVideo = React.lazy(function () { return import(/* webpackChunkName: "CongratsRobotsVideo" */ './congratsRobots'); });
/**
 * Error boundary for loading the robots video.
 * This can error because of the file size of the video
 *
 * Silently ignore the error, this isn't really important enough to
 * capture in Sentry
 */
var ErrorBoundary = /** @class */ (function (_super) {
    __extends(ErrorBoundary, _super);
    function ErrorBoundary() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            hasError: false,
        };
        return _this;
    }
    ErrorBoundary.getDerivedStateFromError = function () {
        return {
            hasError: true,
        };
    };
    ErrorBoundary.prototype.render = function () {
        if (this.state.hasError) {
            return <Placeholder />;
        }
        return this.props.children;
    };
    return ErrorBoundary;
}(React.Component));
var NoUnresolvedIssues = function () { return (<Wrapper>
    <ErrorBoundary>
      <React.Suspense fallback={<Placeholder />}>
        <CongratsRobotsVideo />
      </React.Suspense>
    </ErrorBoundary>
    <Message />
  </Wrapper>); };
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  padding: ", " ", ";\n  flex-direction: column;\n  align-items: center;\n  text-align: center;\n  color: ", ";\n\n  @media (max-width: ", ") {\n    font-size: ", ";\n  }\n"], ["\n  display: flex;\n  padding: ", " ", ";\n  flex-direction: column;\n  align-items: center;\n  text-align: center;\n  color: ", ";\n\n  @media (max-width: ", ") {\n    font-size: ", ";\n  }\n"])), space(4), space(4), function (p) { return p.theme.subText; }, function (p) { return p.theme.breakpoints[0]; }, function (p) { return p.theme.fontSizeMedium; });
var EmptyMessage = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  font-weight: 600;\n\n  @media (min-width: ", ") {\n    font-size: ", ";\n  }\n"], ["\n  font-weight: 600;\n\n  @media (min-width: ", ") {\n    font-size: ", ";\n  }\n"])), function (p) { return p.theme.breakpoints[0]; }, function (p) { return p.theme.fontSizeExtraLarge; });
var PlaceholderImage = styled('img')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  max-height: 320px; /* This should be same height as video in CongratsRobots */\n"], ["\n  max-height: 320px; /* This should be same height as video in CongratsRobots */\n"])));
export default NoUnresolvedIssues;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=noUnresolvedIssues.jsx.map