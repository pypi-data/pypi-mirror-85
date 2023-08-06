import React from 'react';
import ExternalLink from 'app/components/links/externalLink';
import { IconBitbucket, IconGithub, IconGitlab } from 'app/icons';
function renderIcon(repo) {
    if (!repo.provider) {
        return null;
    }
    var id = repo.provider.id;
    var providerId = id.includes(':') ? id.split(':').pop() : id;
    switch (providerId) {
        case 'github':
            return <IconGithub size="xs"/>;
        case 'gitlab':
            return <IconGitlab size="xs"/>;
        case 'bitbucket':
            return <IconBitbucket size="xs"/>;
        default:
            return null;
    }
}
var PullRequestLink = function (_a) {
    var pullRequest = _a.pullRequest, repository = _a.repository, inline = _a.inline;
    var displayId = repository.name + " #" + pullRequest.id + ": " + pullRequest.title;
    return pullRequest.externalUrl ? (<ExternalLink className={inline ? 'inline-commit' : 'btn btn-default btn-sm'} href={pullRequest.externalUrl}>
      {renderIcon(repository)}
      {inline ? '' : ' '}
      {displayId}
    </ExternalLink>) : (<span>{displayId}</span>);
};
export default PullRequestLink;
//# sourceMappingURL=pullRequestLink.jsx.map