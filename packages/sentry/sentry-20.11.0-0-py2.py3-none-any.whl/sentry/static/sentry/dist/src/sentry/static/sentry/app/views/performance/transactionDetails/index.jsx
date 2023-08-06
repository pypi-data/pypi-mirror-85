import { __extends, __makeTemplateObject } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import { PageContent } from 'app/styles/organization';
import { t } from 'app/locale';
import LightWeightNoProjectMessage from 'app/components/lightWeightNoProjectMessage';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import SentryTypes from 'app/sentryTypes';
import withOrganization from 'app/utils/withOrganization';
import EventDetailsContent from './content';
var EventDetails = /** @class */ (function (_super) {
    __extends(EventDetails, _super);
    function EventDetails() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.getEventSlug = function () {
            var eventSlug = _this.props.params.eventSlug;
            return typeof eventSlug === 'string' ? eventSlug.trim() : '';
        };
        return _this;
    }
    EventDetails.prototype.render = function () {
        var _a = this.props, organization = _a.organization, location = _a.location, params = _a.params;
        var documentTitle = t('Performance Details');
        return (<SentryDocumentTitle title={documentTitle} objSlug={organization.slug}>
        <StyledPageContent>
          <LightWeightNoProjectMessage organization={organization}>
            <EventDetailsContent organization={organization} location={location} params={params} eventSlug={this.getEventSlug()}/>
          </LightWeightNoProjectMessage>
        </StyledPageContent>
      </SentryDocumentTitle>);
    };
    EventDetails.propTypes = {
        organization: SentryTypes.Organization.isRequired,
        location: PropTypes.object.isRequired,
    };
    return EventDetails;
}(React.Component));
export default withOrganization(EventDetails);
var StyledPageContent = styled(PageContent)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: 0;\n"], ["\n  padding: 0;\n"])));
var templateObject_1;
//# sourceMappingURL=index.jsx.map