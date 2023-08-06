import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import PageHeading from 'app/components/pageHeading';
import ResourceCard from 'app/components/resourceCard';
import space from 'app/styles/space';
import { t } from 'app/locale';
import releasesImg from '../../../images/spot/releases.svg';
import breadcrumbsImg from '../../../images/spot/breadcrumbs-generic.svg';
import docsImg from '../../../images/spot/code-arguments-tags-mirrored.svg';
var Resources = /** @class */ (function (_super) {
    __extends(Resources, _super);
    function Resources() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Resources.prototype.componentDidMount = function () {
        var organization = this.props.organization;
        trackAnalyticsEvent({
            eventKey: 'orgdash.resources_shown',
            eventName: 'Projects Dashboard: Resources Shown',
            organization: organization.id,
        });
    };
    Resources.prototype.render = function () {
        return (<ResourcesWrapper data-test-id="resources">
        <PageHeading withMargins>{t('Resources')}</PageHeading>
        <ResourceCards>
          <ResourceCard link="https://blog.sentry.io/2018/03/06/the-sentry-workflow" imgUrl={releasesImg} title={t('The Sentry Workflow')}/>
          <ResourceCard link="https://sentry.io/vs/logging/" imgUrl={breadcrumbsImg} title={t('Sentry vs Logging')}/>
          <ResourceCard link="https://docs.sentry.io/" imgUrl={docsImg} title={t('Docs')}/>
        </ResourceCards>
      </ResourcesWrapper>);
    };
    return Resources;
}(React.Component));
export default Resources;
var ResourcesWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  border-top: 1px solid ", ";\n  padding: 25px 30px 10px 30px;\n"], ["\n  border-top: 1px solid ", ";\n  padding: 25px 30px 10px 30px;\n"])), function (p) { return p.theme.border; });
var ResourceCards = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: minmax(100px, 1fr);\n  grid-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));\n  }\n"], ["\n  display: grid;\n  grid-template-columns: minmax(100px, 1fr);\n  grid-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));\n  }\n"])), space(3), function (p) { return p.theme.breakpoints[1]; });
var templateObject_1, templateObject_2;
//# sourceMappingURL=resources.jsx.map