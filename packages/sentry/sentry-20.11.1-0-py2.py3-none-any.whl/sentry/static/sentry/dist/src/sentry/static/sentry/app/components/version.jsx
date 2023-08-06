import { __makeTemplateObject } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import { css } from '@emotion/core';
import styled from '@emotion/styled';
import { withRouter } from 'react-router';
import SentryTypes from 'app/sentryTypes';
import GlobalSelectionLink from 'app/components/globalSelectionLink';
import Link from 'app/components/links/link';
import Tooltip from 'app/components/tooltip';
import { IconCopy } from 'app/icons';
import Clipboard from 'app/components/clipboard';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
import { formatVersion } from 'app/utils/formatters';
import withOrganization from 'app/utils/withOrganization';
import theme from 'app/utils/theme';
var Version = function (_a) {
    var version = _a.version, organization = _a.organization, _b = _a.anchor, anchor = _b === void 0 ? true : _b, preserveGlobalSelection = _a.preserveGlobalSelection, tooltipRawVersion = _a.tooltipRawVersion, withPackage = _a.withPackage, projectId = _a.projectId, truncate = _a.truncate, className = _a.className, location = _a.location;
    var versionToDisplay = formatVersion(version, withPackage);
    var releaseDetailProjectId;
    if (projectId) {
        // we can override preserveGlobalSelection's project id
        releaseDetailProjectId = projectId;
    }
    else if (!(organization === null || organization === void 0 ? void 0 : organization.features.includes('global-views'))) {
        // we need this for users without global-views, otherwise they might get `This release may not be in your selected project`
        releaseDetailProjectId = location === null || location === void 0 ? void 0 : location.query.project;
    }
    var renderVersion = function () {
        if (anchor && (organization === null || organization === void 0 ? void 0 : organization.slug)) {
            var props = {
                to: {
                    pathname: "/organizations/" + (organization === null || organization === void 0 ? void 0 : organization.slug) + "/releases/" + encodeURIComponent(version) + "/",
                    query: releaseDetailProjectId ? { project: releaseDetailProjectId } : undefined,
                },
                className: className,
            };
            if (preserveGlobalSelection) {
                return (<GlobalSelectionLink {...props}>
            <VersionText truncate={truncate}>{versionToDisplay}</VersionText>
          </GlobalSelectionLink>);
            }
            else {
                return (<Link {...props}>
            <VersionText truncate={truncate}>{versionToDisplay}</VersionText>
          </Link>);
            }
        }
        return (<VersionText className={className} truncate={truncate}>
        {versionToDisplay}
      </VersionText>);
    };
    var renderTooltipContent = function () { return (<TooltipContent onClick={function (e) {
        e.stopPropagation();
    }}>
      <TooltipVersionWrapper>{version}</TooltipVersionWrapper>

      <Clipboard value={version}>
        <TooltipClipboardIconWrapper>
          <IconCopy size="xs" color="white"/>
        </TooltipClipboardIconWrapper>
      </Clipboard>
    </TooltipContent>); };
    var getPopperStyles = function () {
        // if the version name is not a hash (sha1 or sha265) and we are not on mobile, allow tooltip to be as wide as 500px
        if (/(^[a-f0-9]{40}$)|(^[a-f0-9]{64}$)/.test(version)) {
            return undefined;
        }
        return css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n      @media (min-width: ", ") {\n        max-width: 500px;\n      }\n    "], ["\n      @media (min-width: ", ") {\n        max-width: 500px;\n      }\n    "])), theme.breakpoints[0]);
    };
    return (<Tooltip title={renderTooltipContent()} disabled={!tooltipRawVersion} isHoverable containerDisplayMode={truncate ? 'block' : 'inline-block'} popperStyle={getPopperStyles()}>
      {renderVersion()}
    </Tooltip>);
};
Version.propTypes = {
    version: PropTypes.string.isRequired,
    organization: SentryTypes.Organization.isRequired,
    anchor: PropTypes.bool,
    preserveGlobalSelection: PropTypes.bool,
    tooltipRawVersion: PropTypes.bool,
    withPackage: PropTypes.bool,
    projectId: PropTypes.string,
    truncate: PropTypes.bool,
    className: PropTypes.string,
};
// TODO(matej): try to wrap version with this when truncate prop is true (in separate PR)
// const VersionWrapper = styled('div')`
//   ${overflowEllipsis};
//   max-width: 100%;
//   width: auto;
//   display: inline-block;
// `;
var VersionText = styled('span')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  ", "\n"], ["\n  ",
    "\n"])), function (p) {
    return p.truncate &&
        "max-width: 100%;\n    display: block;\n  overflow: hidden;\n  text-overflow: ellipsis;\n  white-space: nowrap;";
});
var TooltipContent = styled('span')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var TooltipVersionWrapper = styled('span')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), overflowEllipsis);
var TooltipClipboardIconWrapper = styled('span')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  margin-left: ", ";\n  position: relative;\n  bottom: -", ";\n\n  &:hover {\n    cursor: pointer;\n  }\n"], ["\n  margin-left: ", ";\n  position: relative;\n  bottom: -", ";\n\n  &:hover {\n    cursor: pointer;\n  }\n"])), space(0.5), space(0.25));
export default withOrganization(withRouter(Version));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=version.jsx.map