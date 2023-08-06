import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import { removeFilterMaskedEntries } from 'app/components/events/interfaces/utils';
import UserAvatar from 'app/components/avatar/userAvatar';
import { getMeta } from 'app/components/events/meta/metaProxy';
import AnnotatedText from 'app/components/events/meta/annotatedText';
import space from 'app/styles/space';
import TextOverflow from 'app/components/textOverflow';
import ContextSummaryNoSummary from './contextSummaryNoSummary';
import Item from './item';
var ContextSummaryUser = function (_a) {
    var data = _a.data;
    var user = removeFilterMaskedEntries(data);
    if (Object.keys(user).length === 0) {
        return <ContextSummaryNoSummary title={t('Unknown User')}/>;
    }
    var renderUserDetails = function (key) {
        var userDetails = {
            subject: t('Username:'),
            value: user.username,
            meta: getMeta(data, 'username'),
        };
        if (key === 'id') {
            userDetails.subject = t('ID:');
            userDetails.value = user.id;
            userDetails.meta = getMeta(data, 'id');
        }
        return (<TextOverflow isParagraph>
        <Subject>{userDetails.subject}</Subject>
        <AnnotatedText value={userDetails.value} meta={userDetails.meta}/>
      </TextOverflow>);
    };
    var getUserTitle = function () {
        if (user.email) {
            return {
                value: user.email,
                meta: getMeta(data, 'email'),
            };
        }
        if (user.ip_address) {
            return {
                value: user.ip_address,
                meta: getMeta(data, 'ip_address'),
            };
        }
        if (user.id) {
            return {
                value: user.id,
                meta: getMeta(data, 'id'),
            };
        }
        if (user.username) {
            return {
                value: user.username,
                meta: getMeta(data, 'username'),
            };
        }
        return undefined;
    };
    var userTitle = getUserTitle();
    if (!userTitle) {
        return <ContextSummaryNoSummary title={t('Unknown User')}/>;
    }
    var icon = userTitle ? (<UserAvatar user={user} size={48} className="context-item-icon" gravatar={false}/>) : (<span className="context-item-icon"/>);
    return (<Item className="user" icon={icon}>
      {userTitle && (<h3 data-test-id="user-title">
          <AnnotatedText value={userTitle.value} meta={userTitle.meta}/>
        </h3>)}
      {user.id && user.id !== (userTitle === null || userTitle === void 0 ? void 0 : userTitle.value)
        ? renderUserDetails('id')
        : user.username &&
            user.username !== (userTitle === null || userTitle === void 0 ? void 0 : userTitle.value) &&
            renderUserDetails('username')}
    </Item>);
};
export default ContextSummaryUser;
var Subject = styled('strong')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(0.5));
var templateObject_1;
//# sourceMappingURL=contextSummaryUser.jsx.map