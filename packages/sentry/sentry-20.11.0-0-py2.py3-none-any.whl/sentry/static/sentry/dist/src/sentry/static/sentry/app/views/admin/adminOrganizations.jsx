import React from 'react';
import { Link } from 'react-router';
import ResultGrid from 'app/components/resultGrid';
import { t } from 'app/locale';
var getRow = function (row) { return [
    <td key={row.id}>
    <strong>
      <Link to={"/" + row.slug + "/"}>{row.name}</Link>
    </strong>
    <br />
    <small>{row.slug}</small>
  </td>,
]; };
var AdminOrganizations = function (props) { return (<div>
    <h3>{t('Organizations')}</h3>
    <ResultGrid path="/manage/organizations/" endpoint="/organizations/?show=all" method="GET" columns={[<th key="column-org">Organization</th>]} columnsForRow={getRow} hasSearch sortOptions={[
    ['date', 'Date Joined'],
    ['members', 'Members'],
    ['events', 'Events'],
    ['projects', 'Projects'],
    ['employees', 'Employees'],
]} defaultSort="date" {...props}/>
  </div>); };
export default AdminOrganizations;
//# sourceMappingURL=adminOrganizations.jsx.map