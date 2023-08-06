import React from 'react';
import { DEPLOY_PREVIEW_CONFIG, EXPERIMENTAL_SPA } from 'app/constants';
import { t, tct } from 'app/locale';
import AlertActions from 'app/actions/alertActions';
import ExternalLink from 'app/components/links/externalLink';
export function displayDeployPreviewAlert() {
    if (!DEPLOY_PREVIEW_CONFIG) {
        return;
    }
    var branch = DEPLOY_PREVIEW_CONFIG.branch, commitSha = DEPLOY_PREVIEW_CONFIG.commitSha, githubOrg = DEPLOY_PREVIEW_CONFIG.githubOrg, githubRepo = DEPLOY_PREVIEW_CONFIG.githubRepo;
    var repoUrl = "https://github.com/" + githubOrg + "/" + githubRepo;
    var commitLink = (<ExternalLink href={repoUrl + "/commit/" + commitSha}>
      {t('%s@%s', githubOrg + "/" + githubRepo, commitSha.slice(0, 6))}
    </ExternalLink>);
    var branchLink = (<ExternalLink href={repoUrl + "/tree/" + branch}>{branch}</ExternalLink>);
    AlertActions.addAlert({
        id: 'deploy-preview',
        message: tct('You are viewing a frontend deploy preview of [commitLink] ([branchLink])', { commitLink: commitLink, branchLink: branchLink }),
        type: 'warning',
        neverExpire: true,
        noDuplicates: true,
    });
}
export function displayExperimentalSpaAlert() {
    if (!EXPERIMENTAL_SPA) {
        return;
    }
    AlertActions.addAlert({
        id: 'develop-proxy',
        message: t('You are developing against production Sentry API, please BE CAREFUL, as your changes will affect production data.'),
        type: 'warning',
        neverExpire: true,
        noDuplicates: true,
    });
}
//# sourceMappingURL=deployPreview.jsx.map