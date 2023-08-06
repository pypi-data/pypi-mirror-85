import { t } from 'app/locale';
import { addErrorMessage } from 'app/actionCreators/indicator';
export function toggleKeyTransaction(api, isKeyTransaction, orgId, projects, transactionName) {
    var promise = api.requestPromise("/organizations/" + orgId + "/key-transactions/", {
        method: isKeyTransaction ? 'DELETE' : 'POST',
        query: {
            project: projects.map(function (id) { return String(id); }),
        },
        data: { transaction: transactionName },
    });
    promise.catch(function (response) {
        var _a;
        var non_field_errors = (_a = response === null || response === void 0 ? void 0 : response.responseJSON) === null || _a === void 0 ? void 0 : _a.non_field_errors;
        if (Array.isArray(non_field_errors) &&
            non_field_errors.length &&
            non_field_errors[0]) {
            addErrorMessage(response.responseJSON.non_field_errors[0]);
        }
        else {
            addErrorMessage(t('Unable to update key transaction'));
        }
    });
    return promise;
}
//# sourceMappingURL=performance.jsx.map