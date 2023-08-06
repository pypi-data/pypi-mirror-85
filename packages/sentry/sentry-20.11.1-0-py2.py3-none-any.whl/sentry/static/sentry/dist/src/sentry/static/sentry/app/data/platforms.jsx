var _a;
import { __assign, __read, __spread } from "tslib";
import { platforms } from 'integration-docs-platforms';
import { t } from 'app/locale';
import { tracing } from './platformCategories';
var otherPlatform = {
    integrations: [
        {
            link: 'https://docs.sentry.io/platforms/',
            type: 'language',
            id: 'other',
            name: t('Other'),
        },
    ],
    id: 'other',
    name: t('Other'),
};
export default (_a = []).concat.apply(_a, __spread([[]], __spread(platforms, [otherPlatform]).map(function (platform) {
    return platform.integrations
        .map(function (i) { return (__assign(__assign({}, i), { language: platform.id })); })
        // filter out any tracing platforms; as they're not meant to be used as a platform for
        // the project creation flow
        .filter(function (integration) { return !tracing.includes(integration.id); });
})));
//# sourceMappingURL=platforms.jsx.map