import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { IconOpen } from 'app/icons';
import ExternalLink from 'app/components/links/externalLink';
import space from 'app/styles/space';
import effectiveDirectives from './effectiveDirectives';
var linkOverrides = { 'script-src': 'script-src_2' };
var CSPHelp = function (_a) {
    var key = _a.data.effective_directive;
    var getHelp = function () { return ({
        __html: effectiveDirectives[key],
    }); };
    var getLinkHref = function () {
        var baseLink = 'https://developer.mozilla.org/en-US/docs/Web/Security/CSP/CSP_policy_directives#';
        if (key in linkOverrides) {
            return "" + baseLink + linkOverrides[key];
        }
        return "" + baseLink + key;
    };
    var getLink = function () {
        var href = getLinkHref();
        return (<StyledExternalLink href={href}>
        {'developer.mozilla.org'}
        <IconOpen size="xs" className="external-icon"/>
      </StyledExternalLink>);
    };
    return (<div>
      <h4>
        <code>{key}</code>
      </h4>
      <blockquote dangerouslySetInnerHTML={getHelp()}/>
      <StyledP>
        <span>{'\u2014 MDN ('}</span>
        <span>{getLink()}</span>
        <span>{')'}</span>
      </StyledP>
    </div>);
};
export default CSPHelp;
var StyledP = styled('p')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  text-align: right;\n  display: grid;\n  grid-template-columns: repeat(3, max-content);\n  grid-gap: ", ";\n"], ["\n  text-align: right;\n  display: grid;\n  grid-template-columns: repeat(3, max-content);\n  grid-gap: ", ";\n"])), space(0.25));
var StyledExternalLink = styled(ExternalLink)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: inline-flex;\n  align-items: center;\n"], ["\n  display: inline-flex;\n  align-items: center;\n"])));
var templateObject_1, templateObject_2;
//# sourceMappingURL=index.jsx.map