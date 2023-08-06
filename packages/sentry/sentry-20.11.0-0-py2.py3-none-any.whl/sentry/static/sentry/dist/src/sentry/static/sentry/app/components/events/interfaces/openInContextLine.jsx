import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { SentryAppIcon } from 'app/components/sentryAppIcon';
import { addQueryParamsToExistingUrl } from 'app/utils/queryString';
import space from 'app/styles/space';
import { t } from 'app/locale';
import { recordInteraction } from 'app/utils/recordSentryAppInteraction';
import ExternalLink from 'app/components/links/externalLink';
var OpenInContextLine = function (_a) {
    var lineNo = _a.lineNo, filename = _a.filename, components = _a.components;
    var handleRecordInteraction = function (slug) { return function () {
        recordInteraction(slug, 'sentry_app_component_interacted', {
            componentType: 'stacktrace-link',
        });
    }; };
    var getUrl = function (url) {
        return addQueryParamsToExistingUrl(url, { lineNo: lineNo, filename: filename });
    };
    return (<OpenInContainer columnQuantity={components.length + 1}>
      <div>{t('Open this line in')}</div>
      {components.map(function (component) {
        var url = getUrl(component.schema.url);
        var slug = component.sentryApp.slug;
        var onClickRecordInteraction = handleRecordInteraction(slug);
        return (<OpenInLink key={component.uuid} data-test-id={"stacktrace-link-" + slug} href={url} onClick={onClickRecordInteraction} onContextMenu={onClickRecordInteraction} openInNewTab>
            <SentryAppIcon slug={slug}/>
            <OpenInName>{t("" + component.sentryApp.name)}</OpenInName>
          </OpenInLink>);
    })}
    </OpenInContainer>);
};
export { OpenInContextLine };
export var OpenInContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: relative;\n  z-index: 1;\n  display: grid;\n  grid-template-columns: repeat(", ", max-content);\n  grid-gap: ", ";\n  color: ", ";\n  background-color: ", ";\n  font-family: ", ";\n  border-bottom: 1px solid ", ";\n  padding: ", " ", ";\n  box-shadow: ", ";\n  text-indent: initial;\n  overflow: auto;\n  white-space: nowrap;\n"], ["\n  position: relative;\n  z-index: 1;\n  display: grid;\n  grid-template-columns: repeat(", ", max-content);\n  grid-gap: ", ";\n  color: ", ";\n  background-color: ", ";\n  font-family: ", ";\n  border-bottom: 1px solid ", ";\n  padding: ", " ", ";\n  box-shadow: ", ";\n  text-indent: initial;\n  overflow: auto;\n  white-space: nowrap;\n"])), function (p) { return p.columnQuantity; }, space(1), function (p) { return p.theme.subText; }, function (p) { return p.theme.background; }, function (p) { return p.theme.text.family; }, function (p) { return p.theme.border; }, space(0.25), space(3), function (p) { return p.theme.dropShadowLightest; });
export var OpenInLink = styled(ExternalLink)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: inline-grid;\n  align-items: center;\n  grid-template-columns: max-content auto;\n  grid-gap: ", ";\n  color: ", ";\n"], ["\n  display: inline-grid;\n  align-items: center;\n  grid-template-columns: max-content auto;\n  grid-gap: ", ";\n  color: ", ";\n"])), space(0.75), function (p) { return p.theme.gray300; });
export var OpenInName = styled('strong')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  color: ", ";\n  font-weight: 700;\n"], ["\n  color: ", ";\n  font-weight: 700;\n"])), function (p) { return p.theme.subText; });
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=openInContextLine.jsx.map