import Cookies from 'js-cookie';
import * as queryString from 'query-string';
export default function getPendingInvite() {
    var data = Cookies.get('pending-invite');
    if (!data) {
        return null;
    }
    return queryString.parse(data);
}
//# sourceMappingURL=getPendingInvite.jsx.map