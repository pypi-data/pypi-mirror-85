import { __makeTemplateObject } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import AvatarList from 'app/components/avatar/avatarList';
import { t, tn } from 'app/locale';
import space from 'app/styles/space';
var ReleaseStats = function (_a) {
    var release = _a.release, _b = _a.withHeading, withHeading = _b === void 0 ? true : _b;
    var commitCount = release.commitCount || 0;
    var authorCount = (release.authors && release.authors.length) || 0;
    if (commitCount === 0) {
        return null;
    }
    var releaseSummary = [
        tn('%s commit', '%s commits', commitCount),
        t('by'),
        tn('%s author', '%s authors', authorCount),
    ].join(' ');
    return (<div className="release-stats">
      {withHeading && <ReleaseSummaryHeading>{releaseSummary}</ReleaseSummaryHeading>}
      <span style={{ display: 'inline-block' }}>
        <AvatarList users={release.authors} avatarSize={25} typeMembers="authors"/>
      </span>
    </div>);
};
ReleaseStats.propTypes = {
    release: PropTypes.object,
};
var ReleaseSummaryHeading = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n  line-height: 1.2;\n  font-weight: 600;\n  text-transform: uppercase;\n  margin-bottom: ", ";\n"], ["\n  color: ", ";\n  font-size: ", ";\n  line-height: 1.2;\n  font-weight: 600;\n  text-transform: uppercase;\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.gray300; }, function (p) { return p.theme.fontSizeSmall; }, space(0.5));
export default ReleaseStats;
var templateObject_1;
//# sourceMappingURL=releaseStats.jsx.map