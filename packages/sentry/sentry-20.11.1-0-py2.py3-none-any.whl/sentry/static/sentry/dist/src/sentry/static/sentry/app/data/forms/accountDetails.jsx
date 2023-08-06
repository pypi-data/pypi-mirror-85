export var route = '/settings/account/details/';
// For fields that are
var getUserIsManaged = function (_a) {
    var user = _a.user;
    return user.isManaged;
};
var formGroups = [
    {
        // Form "section"/"panel"
        title: 'Account Details',
        fields: [
            {
                name: 'name',
                type: 'string',
                required: true,
                // additional data/props that is related to rendering of form field rather than data
                label: 'Name',
                placeholder: 'e.g. John Doe',
                help: 'Your full name',
            },
            {
                name: 'username',
                type: 'string',
                required: true,
                autoComplete: 'username',
                label: 'Username',
                placeholder: 'e.g. name@example.com',
                help: '',
                disabled: getUserIsManaged,
                visible: function (_a) {
                    var user = _a.user;
                    return user.email !== user.username;
                },
            },
        ],
    },
];
export default formGroups;
//# sourceMappingURL=accountDetails.jsx.map