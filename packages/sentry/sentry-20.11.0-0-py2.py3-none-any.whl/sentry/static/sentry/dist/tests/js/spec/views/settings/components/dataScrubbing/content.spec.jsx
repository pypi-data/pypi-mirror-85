import React from 'react';
import { mountWithTheme } from 'sentry-test/enzyme';
import Content from 'app/views/settings/components/dataScrubbing/content';
import convertRelayPiiConfig from 'app/views/settings/components/dataScrubbing/convertRelayPiiConfig';
// @ts-expect-error
var relayPiiConfig = TestStubs.DataScrubbingRelayPiiConfig();
var stringRelayPiiConfig = JSON.stringify(relayPiiConfig);
var convertedRules = convertRelayPiiConfig(stringRelayPiiConfig);
var handleEditRule = jest.fn();
var handleDelete = jest.fn();
describe('Content', function () {
    it('default render - empty', function () {
        var wrapper = mountWithTheme(<Content rules={[]} onEditRule={handleEditRule} onDeleteRule={handleDelete}/>);
        expect(wrapper.text()).toEqual('You have no data scrubbing rules');
    });
    it('render rules', function () {
        var wrapper = mountWithTheme(<Content rules={convertedRules} onEditRule={handleEditRule} onDeleteRule={handleDelete}/>);
        expect(wrapper.find('List')).toHaveLength(1);
    });
});
//# sourceMappingURL=content.spec.jsx.map