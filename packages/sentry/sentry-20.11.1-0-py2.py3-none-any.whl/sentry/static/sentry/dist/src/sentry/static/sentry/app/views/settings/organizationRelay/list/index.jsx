import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import orderBy from 'lodash/orderBy';
import space from 'app/styles/space';
import { getRelaysByPublicKey } from './utils';
import CardHeader from './cardHeader';
import ActivityList from './activityList';
import WaitingActivity from './waitingActivity';
var List = function (_a) {
    var relays = _a.relays, relayActivities = _a.relayActivities, onRefresh = _a.onRefresh, onDelete = _a.onDelete, onEdit = _a.onEdit;
    var orderedRelays = orderBy(relays, function (relay) { return relay.created; }, ['desc']);
    var relaysByPublicKey = getRelaysByPublicKey(orderedRelays, relayActivities);
    var renderCardContent = function (activities) {
        if (!activities.length) {
            return <WaitingActivity onRefresh={onRefresh}/>;
        }
        return <ActivityList activities={activities}/>;
    };
    return (<Wrapper>
      {Object.keys(relaysByPublicKey).map(function (relayByPublicKey) {
        var _a = relaysByPublicKey[relayByPublicKey], name = _a.name, description = _a.description, created = _a.created, activities = _a.activities;
        return (<Card key={relayByPublicKey}>
            <CardHeader publicKey={relayByPublicKey} name={name} description={description} created={created} onEdit={onEdit} onDelete={onDelete}/>
            {renderCardContent(activities)}
          </Card>);
    })}
    </Wrapper>);
};
export default List;
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n"])), space(3));
var Card = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n"])), space(1));
var templateObject_1, templateObject_2;
//# sourceMappingURL=index.jsx.map