// Export route to make these forms searchable by label/help
import { t } from 'app/locale';
export var route = '/settings/:orgId/projects/:projectId/processing-issues/';
var formGroups = [
    {
        // Form "section"/"panel"
        title: 'Settings',
        fields: [
            {
                name: 'sentry:reprocessing_active',
                type: 'boolean',
                label: t('Reprocessing active'),
                disabled: function (_a) {
                    var access = _a.access;
                    return !access.has('project:write');
                },
                disabledReason: t('Only admins may change reprocessing settings'),
                help: t("If reprocessing is enabled, Events with fixable issues will be\n                held back until you resolve them. Processing issues will then\n                show up in the list above with hints how to fix them.\n                If reprocessing is disabled, Events with unresolved issues will\n                also show up in the stream.\n                "),
                saveOnBlur: false,
                saveMessage: function (_a) {
                    var value = _a.value;
                    return value
                        ? t('Reprocessing applies to future events only.')
                        : t("All events with errors will be flushed into your issues stream.\n                Beware that this process may take some time and cannot be undone.");
                },
                getData: function (form) { return ({ options: form }); },
            },
        ],
    },
];
export default formGroups;
//# sourceMappingURL=processingIssues.jsx.map