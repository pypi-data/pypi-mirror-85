import React from 'react';
import OrganizationSettingsNavigation from 'app/views/settings/organization/organizationSettingsNavigation';
import SettingsLayout from 'app/views/settings/components/settingsLayout';
function OrganizationSettingsLayout(props) {
    return (<SettingsLayout {...props} renderNavigation={function () { return <OrganizationSettingsNavigation />; }}/>);
}
export default OrganizationSettingsLayout;
//# sourceMappingURL=organizationSettingsLayout.jsx.map