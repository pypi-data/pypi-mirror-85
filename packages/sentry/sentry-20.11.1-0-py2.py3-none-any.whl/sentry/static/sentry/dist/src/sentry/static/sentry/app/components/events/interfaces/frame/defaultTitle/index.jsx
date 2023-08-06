import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { defined, isUrl } from 'app/utils';
import Tooltip from 'app/components/tooltip';
import Truncate from 'app/components/truncate';
import { IconQuestion, IconOpen } from 'app/icons';
import ExternalLink from 'app/components/links/externalLink';
import AnnotatedText from 'app/components/events/meta/annotatedText';
import { t } from 'app/locale';
import { getMeta } from 'app/components/events/meta/metaProxy';
import space from 'app/styles/space';
import FunctionName from '../functionName';
import { getPlatform, trimPackage } from '../utils';
import OriginalSourceInfo from './originalSourceInfo';
var DefaultTitle = function (_a) {
    var frame = _a.frame, platform = _a.platform;
    var title = [];
    var framePlatform = getPlatform(frame.platform, platform);
    var handleExternalLink = function (event) {
        event.stopPropagation();
    };
    var getPathName = function (shouldPrioritizeModuleName) {
        if (shouldPrioritizeModuleName) {
            if (frame.module) {
                return {
                    key: 'module',
                    value: frame.module,
                    meta: getMeta(frame, 'module'),
                };
            }
            if (frame.filename) {
                return {
                    key: 'filename',
                    value: frame.filename,
                    meta: getMeta(frame, 'filename'),
                };
            }
            return undefined;
        }
        if (frame.filename) {
            return {
                key: 'filename',
                value: frame.filename,
                meta: getMeta(frame, 'filename'),
            };
        }
        if (frame.module) {
            return {
                key: 'module',
                value: frame.module,
                meta: getMeta(frame, 'module'),
            };
        }
        return undefined;
    };
    // TODO(dcramer): this needs to use a formatted string so it can be
    // localized correctly
    if (defined(frame.filename || frame.module)) {
        // prioritize module name for Java as filename is often only basename
        var shouldPrioritizeModuleName = framePlatform === 'java' || framePlatform === 'csharp';
        var pathName = getPathName(shouldPrioritizeModuleName);
        var enablePathTooltip = defined(frame.absPath) && frame.absPath !== (pathName === null || pathName === void 0 ? void 0 : pathName.value);
        if (pathName) {
            title.push(<Tooltip key={pathName.key} title={frame.absPath} disabled={!enablePathTooltip}>
          <code key="filename" className="filename">
            <AnnotatedText value={<Truncate value={pathName.value} maxLength={100} leftTrim/>} meta={pathName.meta}/>
          </code>
        </Tooltip>);
        }
        // in case we prioritized the module name but we also have a filename info
        // we want to show a litle (?) icon that on hover shows the actual filename
        if (shouldPrioritizeModuleName && frame.filename && framePlatform !== 'csharp') {
            title.push(<Tooltip key={frame.filename} title={frame.filename}>
          <a className="in-at real-filename">
            <IconQuestion size="xs"/>
          </a>
        </Tooltip>);
        }
        if (frame.absPath && isUrl(frame.absPath)) {
            title.push(<StyledExternalLink href={frame.absPath} key="share" onClick={handleExternalLink}>
          <IconOpen size="xs"/>
        </StyledExternalLink>);
        }
        if (defined(frame.function) || defined(frame.rawFunction)) {
            title.push(<span className="in-at" key="in">
          {" " + t('in') + " "}
        </span>);
        }
    }
    if (defined(frame.function) || defined(frame.rawFunction)) {
        title.push(<FunctionName frame={frame} key="function" className="function"/>);
    }
    // we don't want to render out zero line numbers which are used to
    // indicate lack of source information for native setups.  We could
    // TODO(mitsuhiko): only do this for events from native platforms?
    if (defined(frame.lineNo) && frame.lineNo !== 0) {
        title.push(<span className="in-at in-at-line" key="no">
        {" " + t('at line') + " "}
      </span>);
        title.push(<code key="line" className="lineno">
        {defined(frame.colNo) ? frame.lineNo + ":" + frame.colNo : frame.lineNo}
      </code>);
    }
    if (defined(frame.package) && framePlatform !== 'csharp') {
        title.push(<span className="within" key="within">
        {" " + t('within') + " "}
      </span>);
        title.push(<code title={frame.package} className="package" key="package">
        {trimPackage(frame.package)}
      </code>);
    }
    if (defined(frame.origAbsPath)) {
        title.push(<Tooltip key="info-tooltip" title={<OriginalSourceInfo mapUrl={frame.mapUrl} map={frame.map}/>}>
        <a className="in-at original-src">
          <IconQuestion size="xs"/>
        </a>
      </Tooltip>);
    }
    return <React.Fragment>{title}</React.Fragment>;
};
var StyledExternalLink = styled(ExternalLink)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: relative;\n  top: 2px;\n  margin-left: ", ";\n"], ["\n  position: relative;\n  top: 2px;\n  margin-left: ", ";\n"])), space(0.5));
export default DefaultTitle;
var templateObject_1;
//# sourceMappingURL=index.jsx.map