import React from 'react';
import { mountWithTheme } from 'sentry-test/enzyme';
import Rules from 'app/views/settings/components/dataScrubbing/rules';
import convertRelayPiiConfig from 'app/views/settings/components/dataScrubbing/convertRelayPiiConfig';
// @ts-expect-error
var relayPiiConfig = TestStubs.DataScrubbingRelayPiiConfig();
var stringRelayPiiConfig = JSON.stringify(relayPiiConfig);
var convertedRules = convertRelayPiiConfig(stringRelayPiiConfig);
var rules = convertedRules;
var handleShowEditRule = jest.fn();
var handleDelete = jest.fn();
describe('Rules', function () {
    it('default render', function () {
        var wrapper = mountWithTheme(<Rules rules={rules}/>);
        expect(wrapper.find('ListItem')).toHaveLength(3);
    });
    it('render correct description', function () {
        var wrapper = mountWithTheme(<Rules rules={rules}/>);
        var listItems = wrapper.find('ListItem');
        expect(listItems.at(1).text()).toEqual('[Mask] [Credit card numbers] from [$message]');
        expect(listItems.at(0).text()).toEqual('[Replace] [Password fields]  with [Scrubbed] from [password]');
    });
    it('render disabled list', function () {
        var wrapper = mountWithTheme(<Rules rules={rules} disabled/>);
        expect(wrapper.find('List').prop('isDisabled')).toEqual(true);
    });
    it('render edit and delete buttons', function () {
        var wrapper = mountWithTheme(<Rules rules={rules} onEditRule={handleShowEditRule} onDeleteRule={handleDelete}/>);
        expect(wrapper.find('[aria-label="Edit Rule"]').hostNodes()).toHaveLength(3);
        expect(wrapper.find('[aria-label="Delete Rule"]').hostNodes()).toHaveLength(3);
    });
    it('render disabled edit and delete buttons', function () {
        var wrapper = mountWithTheme(<Rules rules={rules} onEditRule={handleShowEditRule} onDeleteRule={handleDelete} disabled/>);
        expect(wrapper.find('[aria-label="Edit Rule"]').hostNodes().at(0).prop('aria-disabled')).toEqual(true);
        expect(wrapper.find('[aria-label="Delete Rule"]').hostNodes().at(0).prop('aria-disabled')).toEqual(true);
    });
    it('render edit button only', function () {
        var wrapper = mountWithTheme(<Rules rules={rules} onEditRule={handleShowEditRule}/>);
        expect(wrapper.find('[aria-label="Edit Rule"]').hostNodes()).toHaveLength(3);
        expect(wrapper.find('[aria-label="Delete Rule"]')).toHaveLength(0);
    });
    it('render delete button only', function () {
        var wrapper = mountWithTheme(<Rules rules={rules} onDeleteRule={handleDelete}/>);
        expect(wrapper.find('[aria-label="Edit Rule"]')).toHaveLength(0);
        expect(wrapper.find('[aria-label="Delete Rule"]').hostNodes()).toHaveLength(3);
    });
});
//# sourceMappingURL=rules.spec.jsx.map