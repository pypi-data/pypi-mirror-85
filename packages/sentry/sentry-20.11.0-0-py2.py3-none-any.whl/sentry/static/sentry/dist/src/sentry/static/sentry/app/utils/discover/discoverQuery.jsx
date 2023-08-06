import React from 'react';
import withApi from 'app/utils/withApi';
import GenericDiscoverQuery from './genericDiscoverQuery';
function DiscoverQuery(props) {
    return <GenericDiscoverQuery route="eventsv2" {...props}/>;
}
export default withApi(DiscoverQuery);
//# sourceMappingURL=discoverQuery.jsx.map