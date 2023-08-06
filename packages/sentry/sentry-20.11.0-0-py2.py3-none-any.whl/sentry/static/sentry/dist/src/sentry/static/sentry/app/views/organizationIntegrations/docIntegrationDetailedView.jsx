import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import ExternalLink from 'app/components/links/externalLink';
import { IconOpen } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import withOrganization from 'app/utils/withOrganization';
import AbstractIntegrationDetailedView from './abstractIntegrationDetailedView';
import { documentIntegrations } from './constants';
var SentryAppDetailedView = /** @class */ (function (_super) {
    __extends(SentryAppDetailedView, _super);
    function SentryAppDetailedView() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.tabs = ['overview'];
        _this.trackClick = function () {
            _this.trackIntegrationEvent({
                eventKey: 'integrations.installation_start',
                eventName: 'Integrations: Installation Start',
            });
        };
        return _this;
    }
    Object.defineProperty(SentryAppDetailedView.prototype, "integrationType", {
        get: function () {
            return 'document';
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(SentryAppDetailedView.prototype, "integration", {
        get: function () {
            var integrationSlug = this.props.params.integrationSlug;
            var documentIntegration = documentIntegrations[integrationSlug];
            if (!documentIntegration) {
                throw new Error("No document integration of slug " + integrationSlug + " exists");
            }
            return documentIntegration;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(SentryAppDetailedView.prototype, "description", {
        get: function () {
            return this.integration.description;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(SentryAppDetailedView.prototype, "author", {
        get: function () {
            return this.integration.author;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(SentryAppDetailedView.prototype, "resourceLinks", {
        get: function () {
            return this.integration.resourceLinks;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(SentryAppDetailedView.prototype, "installationStatus", {
        get: function () {
            return null;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(SentryAppDetailedView.prototype, "integrationName", {
        get: function () {
            return this.integration.name;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(SentryAppDetailedView.prototype, "featureData", {
        get: function () {
            return this.integration.features;
        },
        enumerable: false,
        configurable: true
    });
    SentryAppDetailedView.prototype.componentDidMount = function () {
        _super.prototype.componentDidMount.call(this);
        this.trackIntegrationEvent({
            eventKey: 'integrations.integration_viewed',
            eventName: 'Integrations: Integration Viewed',
            integration_tab: 'overview',
        });
    };
    SentryAppDetailedView.prototype.renderTopButton = function () {
        return (<ExternalLink href={this.integration.docUrl} onClick={this.trackClick}>
        <LearnMoreButton size="small" priority="primary" style={{ marginLeft: space(1) }} data-test-id="learn-more" icon={<StyledIconOpen size="xs"/>}>
          {t('Learn More')}
        </LearnMoreButton>
      </ExternalLink>);
    };
    // No configurations.
    SentryAppDetailedView.prototype.renderConfigurations = function () {
        return null;
    };
    return SentryAppDetailedView;
}(AbstractIntegrationDetailedView));
var LearnMoreButton = styled(Button)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space(1));
var StyledIconOpen = styled(IconOpen)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  transition: 0.1s linear color;\n  margin: 0 ", ";\n  position: relative;\n  top: 1px;\n"], ["\n  transition: 0.1s linear color;\n  margin: 0 ", ";\n  position: relative;\n  top: 1px;\n"])), space(0.5));
export default withOrganization(SentryAppDetailedView);
var templateObject_1, templateObject_2;
//# sourceMappingURL=docIntegrationDetailedView.jsx.map