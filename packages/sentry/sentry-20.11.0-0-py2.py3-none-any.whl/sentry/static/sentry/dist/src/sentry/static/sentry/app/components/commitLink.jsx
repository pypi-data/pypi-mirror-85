import React from 'react';
import { t } from 'app/locale';
import { getShortCommitHash } from 'app/utils';
import Button from 'app/components/button';
import { IconBitbucket, IconGithub, IconGitlab, IconVsts } from 'app/icons';
import ExternalLink from 'app/components/links/externalLink';
// TODO(epurkhiser, jess): This should be moved into plugins.
var SUPPORTED_PROVIDERS = [
    {
        icon: <IconGithub size="xs"/>,
        providerIds: ['github', 'integrations:github', 'integrations:github_enterprise'],
        commitUrl: function (_a) {
            var baseUrl = _a.baseUrl, commitId = _a.commitId;
            return baseUrl + "/commit/" + commitId;
        },
    },
    {
        icon: <IconBitbucket size="xs"/>,
        providerIds: ['bitbucket', 'integrations:bitbucket'],
        commitUrl: function (_a) {
            var baseUrl = _a.baseUrl, commitId = _a.commitId;
            return baseUrl + "/commits/" + commitId;
        },
    },
    {
        icon: <IconVsts size="xs"/>,
        providerIds: ['visualstudio', 'integrations:vsts'],
        commitUrl: function (_a) {
            var baseUrl = _a.baseUrl, commitId = _a.commitId;
            return baseUrl + "/commit/" + commitId;
        },
    },
    {
        icon: <IconGitlab size="xs"/>,
        providerIds: ['gitlab', 'integrations:gitlab'],
        commitUrl: function (_a) {
            var baseUrl = _a.baseUrl, commitId = _a.commitId;
            return baseUrl + "/commit/" + commitId;
        },
    },
];
function CommitLink(_a) {
    var inline = _a.inline, commitId = _a.commitId, repository = _a.repository;
    if (!commitId || !repository) {
        return <span>{t('Unknown Commit')}</span>;
    }
    var shortId = getShortCommitHash(commitId);
    var providerData = SUPPORTED_PROVIDERS.find(function (provider) {
        if (!repository.provider) {
            return false;
        }
        return provider.providerIds.includes(repository.provider.id);
    });
    if (providerData === undefined) {
        return <span>{shortId}</span>;
    }
    var commitUrl = repository.url &&
        providerData.commitUrl({
            commitId: commitId,
            baseUrl: repository.url,
        });
    return !inline ? (<Button external href={commitUrl} size="small" icon={providerData.icon}>
      {shortId}
    </Button>) : (<ExternalLink className="inline-commit" href={commitUrl}>
      {providerData.icon}
      {' ' + shortId}
    </ExternalLink>);
}
export default CommitLink;
//# sourceMappingURL=commitLink.jsx.map