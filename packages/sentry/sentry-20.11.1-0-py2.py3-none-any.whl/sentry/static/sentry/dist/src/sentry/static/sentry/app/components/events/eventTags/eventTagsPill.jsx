import { __makeTemplateObject } from "tslib";
import React from 'react';
import { Link } from 'react-router';
import { css } from '@emotion/core';
import * as queryString from 'query-string';
import AnnotatedText from 'app/components/events/meta/annotatedText';
import { isUrl } from 'app/utils';
import Pill from 'app/components/pill';
import VersionHoverCard from 'app/components/versionHoverCard';
import TraceHoverCard from 'app/utils/discover/traceHoverCard';
import { IconOpen, IconInfo } from 'app/icons';
import ExternalLink from 'app/components/links/externalLink';
import { getMeta } from 'app/components/events/meta/metaProxy';
import EventTagsPillValue from './eventTagsPillValue';
var iconStyle = css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: relative;\n  top: 1px;\n"], ["\n  position: relative;\n  top: 1px;\n"])));
var EventTagsPill = function (_a) {
    var tag = _a.tag, query = _a.query, orgId = _a.orgId, projectId = _a.projectId, streamPath = _a.streamPath, releasesPath = _a.releasesPath, location = _a.location, hasQueryFeature = _a.hasQueryFeature;
    var locationSearch = "?" + queryString.stringify(query);
    var key = tag.key, value = tag.value;
    var isRelease = key === 'release';
    var isTrace = key === 'trace';
    var name = !key ? <AnnotatedText value={key} meta={getMeta(tag, 'key')}/> : key;
    var type = !key ? 'error' : undefined;
    return (<Pill name={name} value={value} type={type}>
      <EventTagsPillValue tag={tag} meta={getMeta(tag, 'value')} streamPath={streamPath} locationSearch={locationSearch} isRelease={isRelease}/>
      {isUrl(value) && (<ExternalLink href={value} className="external-icon">
          <IconOpen size="xs" css={iconStyle}/>
        </ExternalLink>)}
      {isRelease && (<div className="pill-icon">
          <VersionHoverCard orgSlug={orgId} projectSlug={projectId} releaseVersion={value}>
            <Link to={{ pathname: "" + releasesPath + value + "/", search: locationSearch }}>
              <IconInfo size="xs" css={iconStyle}/>
            </Link>
          </VersionHoverCard>
        </div>)}
      {isTrace && hasQueryFeature && (<TraceHoverCard containerClassName="pill-icon" traceId={value} orgId={orgId} location={location}>
          {function (_a) {
        var to = _a.to;
        return (<Link to={to}>
                <IconOpen size="xs" css={iconStyle}/>
              </Link>);
    }}
        </TraceHoverCard>)}
    </Pill>);
};
export default EventTagsPill;
var templateObject_1;
//# sourceMappingURL=eventTagsPill.jsx.map