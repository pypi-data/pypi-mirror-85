import { __read, __spread } from "tslib";
import React from 'react';
import UserAvatar from 'app/components/avatar/userAvatar';
import { removeFilterMaskedEntries } from 'app/components/events/interfaces/utils';
import ContextBlock from 'app/components/events/contexts/contextBlock';
import ErrorBoundary from 'app/components/errorBoundary';
import KeyValueList from 'app/components/events/interfaces/keyValueList/keyValueList';
import { defined } from 'app/utils';
import getUserKnownData from './getUserKnownData';
import { UserKnownDataType, UserIgnoredDataType } from './types';
import getUnknownData from '../getUnknownData';
var userKnownDataValues = [
    UserKnownDataType.ID,
    UserKnownDataType.EMAIL,
    UserKnownDataType.USERNAME,
    UserKnownDataType.IP_ADDRESS,
    UserKnownDataType.NAME,
];
var userIgnoredDataValues = [UserIgnoredDataType.DATA];
var User = function (_a) {
    var data = _a.data;
    var getKeyValueData = function (val) { return Object.keys(val).map(function (key) { return [key, val[key]]; }); };
    return (<div className="user-widget">
      <div className="pull-left">
        <UserAvatar user={removeFilterMaskedEntries(data)} size={48} gravatar={false}/>
      </div>
      <ContextBlock data={getUserKnownData(data, userKnownDataValues)}/>
      <ContextBlock data={getUnknownData(data, __spread(userKnownDataValues, userIgnoredDataValues))}/>
      {defined(data === null || data === void 0 ? void 0 : data.data) && (<ErrorBoundary mini>
          <KeyValueList data={getKeyValueData(data.data)} isContextData/>
        </ErrorBoundary>)}
    </div>);
};
export default User;
//# sourceMappingURL=user.jsx.map