import React from 'react';
import partition from 'lodash/partition';
import flatten from 'lodash/flatten';
import Content from './content';
import CompactContent from './compactContent';
var ReleaseHealth = function (_a) {
    var release = _a.release, orgSlug = _a.orgSlug, location = _a.location, selection = _a.selection, showPlaceholders = _a.showPlaceholders;
    // sort health rows inside release card alphabetically by project name,
    // but put the ones with project selected in global header to top
    var sortedProjects = flatten(partition(release.projects.sort(function (a, b) { return a.slug.localeCompare(b.slug); }), function (p) { return selection.projects.includes(p.id); }));
    var hasAtLeastOneHealthData = sortedProjects.some(function (sortedProject) { return sortedProject.hasHealthData; });
    var contentProps = {
        projects: sortedProjects,
        releaseVersion: release.version,
        orgSlug: orgSlug,
    };
    if (hasAtLeastOneHealthData) {
        return (<Content {...contentProps} location={location} showPlaceholders={showPlaceholders}/>);
    }
    return <CompactContent {...contentProps}/>;
};
export default ReleaseHealth;
//# sourceMappingURL=index.jsx.map