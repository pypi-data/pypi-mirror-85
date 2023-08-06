import { t } from 'app/locale';
import slugify from 'app/utils/slugify';
// Export route to make these forms searchable by label/help
export var route = '/settings/:orgId/';
var formGroups = [
    {
        // Form "section"/"panel"
        title: t('General'),
        fields: [
            {
                name: 'slug',
                type: 'string',
                required: true,
                label: t('Organization Slug'),
                help: t('A unique ID used to identify this organization'),
                transformInput: slugify,
                saveOnBlur: false,
                saveMessageAlertType: 'info',
                saveMessage: t('You will be redirected to the new organization slug after saving'),
            },
            {
                name: 'name',
                type: 'string',
                required: true,
                label: t('Display Name'),
                help: t('A human-friendly name for the organization'),
            },
            {
                name: 'isEarlyAdopter',
                type: 'boolean',
                label: t('Early Adopter'),
                help: t("Opt-in to new features before they're released to the public"),
            },
        ],
    },
    {
        title: 'Membership',
        fields: [
            {
                name: 'defaultRole',
                type: 'array',
                required: true,
                label: t('Default Role'),
                // seems weird to have choices in initial form data
                choices: function (_a) {
                    var _b, _c;
                    var initialData = (_a === void 0 ? {} : _a).initialData;
                    return (_c = (_b = initialData === null || initialData === void 0 ? void 0 : initialData.availableRoles) === null || _b === void 0 ? void 0 : _b.map(function (r) { return [r.id, r.name]; })) !== null && _c !== void 0 ? _c : [];
                },
                help: t('The default role new members will receive'),
                disabled: function (_a) {
                    var access = _a.access;
                    return !access.has('org:admin');
                },
            },
            {
                name: 'openMembership',
                type: 'boolean',
                required: true,
                label: t('Open Membership'),
                help: t('Allow organization members to freely join or leave any team'),
            },
            {
                name: 'eventsMemberAdmin',
                type: 'boolean',
                label: t('Grant Members Events Admin'),
                help: t('Allow members to delete events (including the delete & discard action) by granting them the `event:admin` scope.'),
            },
            {
                name: 'attachmentsRole',
                type: 'array',
                choices: function (_a) {
                    var _b, _c;
                    var _d = _a.initialData, initialData = _d === void 0 ? {} : _d;
                    return (_c = (_b = initialData === null || initialData === void 0 ? void 0 : initialData.availableRoles) === null || _b === void 0 ? void 0 : _b.map(function (r) { return [r.id, r.name]; })) !== null && _c !== void 0 ? _c : [];
                },
                label: t('Attachments Access'),
                help: t('Role required to download event attachments, such as native crash reports or log files.'),
                visible: function (_a) {
                    var features = _a.features;
                    return features.has('event-attachments');
                },
            },
            {
                name: 'debugFilesRole',
                type: 'array',
                choices: function (_a) {
                    var _b, _c;
                    var _d = _a.initialData, initialData = _d === void 0 ? {} : _d;
                    return (_c = (_b = initialData === null || initialData === void 0 ? void 0 : initialData.availableRoles) === null || _b === void 0 ? void 0 : _b.map(function (r) { return [r.id, r.name]; })) !== null && _c !== void 0 ? _c : [];
                },
                label: t('Debug Files Access'),
                help: t('Role required to download debug information files, proguard mappings and source maps.'),
            },
        ],
    },
];
export default formGroups;
//# sourceMappingURL=organizationGeneralSettings.jsx.map