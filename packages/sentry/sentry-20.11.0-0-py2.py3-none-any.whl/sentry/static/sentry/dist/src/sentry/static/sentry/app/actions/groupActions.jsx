import Reflux from 'reflux';
// TODO(dcramer): we should probably just make every parameter update
// work on bulk groups
var GroupActions = Reflux.createActions([
    'assignTo',
    'assignToError',
    'assignToSuccess',
    'delete',
    'deleteError',
    'deleteSuccess',
    'discard',
    'discardError',
    'discardSuccess',
    'update',
    'updateError',
    'updateSuccess',
    'merge',
    'mergeError',
    'mergeSuccess',
]);
export default GroupActions;
//# sourceMappingURL=groupActions.jsx.map