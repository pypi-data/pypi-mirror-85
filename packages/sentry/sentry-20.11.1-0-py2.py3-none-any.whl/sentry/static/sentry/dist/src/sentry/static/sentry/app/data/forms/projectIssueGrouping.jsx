import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import space from 'app/styles/space';
import { t, tct } from 'app/locale';
import marked from 'app/utils/marked';
import ExternalLink from 'app/components/links/externalLink';
import { GroupingConfigItem } from 'app/components/events/groupingInfo';
// Export route to make these forms searchable by label/help
export var route = '/settings/:orgId/projects/:projectId/issue-grouping/';
export var fields = {
    fingerprintingRules: {
        name: 'fingerprintingRules',
        type: 'string',
        label: t('Fingerprint Rules'),
        hideLabel: true,
        placeholder: t('error.type:MyException -> fingerprint-value\nstack.function:some_panic_function -> fingerprint-value'),
        multiline: true,
        monospace: true,
        autosize: true,
        inline: false,
        maxRows: 20,
        saveOnBlur: false,
        saveMessageAlertType: 'info',
        saveMessage: t('Changing fingerprint rules will apply to future events only.'),
        formatMessageValue: false,
        help: function () { return (<React.Fragment>
        <RuleDescription>
          {tct("This can be used to modify the fingerprint rules on the server with custom rules.\n        Rules follow the pattern [pattern]. To learn more about fingerprint rules, [docs:read the docs].", {
            pattern: <code>matcher:glob -&gt; fingerprint, values</code>,
            docs: (<ExternalLink href="https://docs.sentry.io/platform-redirect/?next=%2Fdata-management%2Fevent-grouping%2Fserver-side-fingerprinting%2F"/>),
        })}
        </RuleDescription>
        <RuleExample>
          {"# force all errors of the same type to have the same fingerprint\nerror.type:DatabaseUnavailable -> system-down\n# force all memory allocation errors to be grouped together\nstack.function:malloc -> memory-allocation-error"}
        </RuleExample>
      </React.Fragment>); },
        visible: true,
    },
    groupingEnhancements: {
        name: 'groupingEnhancements',
        type: 'string',
        label: t('Stack Trace Rules'),
        hideLabel: true,
        placeholder: t('stack.function:raise_an_exception ^-group\nstack.function:namespace::* +app'),
        multiline: true,
        monospace: true,
        autosize: true,
        inline: false,
        maxRows: 20,
        saveOnBlur: false,
        saveMessageAlertType: 'info',
        saveMessage: t('Changing stack trace rules will apply to future events only.'),
        formatMessageValue: false,
        help: function () { return (<React.Fragment>
        <RuleDescription>
          {tct("This can be used to enhance the grouping algorithm with custom rules.\n        Rules follow the pattern [pattern]. To learn more about stack trace rules, [docs:read the docs].", {
            pattern: <code>matcher:glob [^v]?[+-]flag</code>,
            docs: (<ExternalLink href="https://docs.sentry.io/platform-redirect/?next=%2Fdata-management%2Fevent-grouping%2Fgrouping-enhancements%2F"/>),
        })}
        </RuleDescription>
        <RuleExample>
          {"# remove all frames above a certain function from grouping\nstack.function:panic_handler ^-group\n# mark all functions following a prefix in-app\nstack.function:mylibrary_* +app"}
        </RuleExample>
      </React.Fragment>); },
        validate: function () { return []; },
        visible: true,
    },
    groupingConfig: {
        name: 'groupingConfig',
        type: 'array',
        label: t('Grouping Config'),
        saveOnBlur: false,
        saveMessageAlertType: 'info',
        saveMessage: t('Changing grouping config will apply to future events only.'),
        selectionInfoFunction: function (args) {
            var groupingConfigs = args.groupingConfigs, value = args.value;
            var selection = groupingConfigs.find(function (_a) {
                var id = _a.id;
                return id === value;
            });
            var changelog = (selection === null || selection === void 0 ? void 0 : selection.changelog) || '';
            if (!changelog) {
                return null;
            }
            return (<Changelog>
          <ChangelogTitle>
            {tct('New in version [version]', { version: selection.id })}:
          </ChangelogTitle>
          <div dangerouslySetInnerHTML={{ __html: marked(changelog) }}/>
        </Changelog>);
        },
        choices: function (_a) {
            var groupingConfigs = _a.groupingConfigs;
            return groupingConfigs.map(function (_a) {
                var id = _a.id, hidden = _a.hidden;
                return [
                    id.toString(),
                    <GroupingConfigItem key={id} isHidden={hidden}>
          {id}
        </GroupingConfigItem>,
                ];
            });
        },
        help: t('Sets the grouping algorithm to be used for new events.'),
        visible: function (_a) {
            var features = _a.features;
            return features.has('set-grouping-config');
        },
    },
    groupingEnhancementsBase: {
        name: 'groupingEnhancementsBase',
        type: 'array',
        label: t('Stack Trace Rules Base'),
        saveOnBlur: false,
        saveMessageAlertType: 'info',
        saveMessage: t('Changing base will apply to future events only.'),
        selectionInfoFunction: function (args) {
            var groupingEnhancementBases = args.groupingEnhancementBases, value = args.value;
            var selection = groupingEnhancementBases.find(function (_a) {
                var id = _a.id;
                return id === value;
            });
            var changelog = (selection === null || selection === void 0 ? void 0 : selection.changelog) || '';
            if (!changelog) {
                return null;
            }
            return (<Changelog>
          <ChangelogTitle>
            {tct('New in version [version]', { version: selection.id })}:
          </ChangelogTitle>
          <div dangerouslySetInnerHTML={{ __html: marked(changelog) }}/>
        </Changelog>);
        },
        choices: function (_a) {
            var groupingEnhancementBases = _a.groupingEnhancementBases;
            return groupingEnhancementBases.map(function (_a) {
                var id = _a.id;
                return [
                    id.toString(),
                    <GroupingConfigItem key={id}>{id}</GroupingConfigItem>,
                ];
            });
        },
        help: t('The built-in base version of stack trace rules.'),
        visible: function (_a) {
            var features = _a.features;
            return features.has('set-grouping-config');
        },
    },
};
var RuleDescription = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: ", ";\n  margin-top: -", ";\n  margin-right: 36px;\n"], ["\n  margin-bottom: ", ";\n  margin-top: -", ";\n  margin-right: 36px;\n"])), space(1), space(1));
var RuleExample = styled('pre')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-bottom: ", ";\n  margin-right: 36px;\n"], ["\n  margin-bottom: ", ";\n  margin-right: 36px;\n"])), space(1));
var Changelog = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  position: relative;\n  top: -1px;\n  margin-bottom: -1px;\n  padding: ", ";\n  border-bottom: 1px solid ", ";\n  background: ", ";\n  font-size: ", ";\n\n  &:last-child {\n    border: 0;\n    border-bottom-left-radius: ", ";\n    border-bottom-right-radius: ", ";\n  }\n"], ["\n  position: relative;\n  top: -1px;\n  margin-bottom: -1px;\n  padding: ", ";\n  border-bottom: 1px solid ", ";\n  background: ", ";\n  font-size: ", ";\n\n  &:last-child {\n    border: 0;\n    border-bottom-left-radius: ", ";\n    border-bottom-right-radius: ", ";\n  }\n"])), space(2), function (p) { return p.theme.innerBorder; }, function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.borderRadius; });
var ChangelogTitle = styled('h3')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  font-size: ", ";\n  margin-bottom: ", " !important;\n"], ["\n  font-size: ", ";\n  margin-bottom: ", " !important;\n"])), function (p) { return p.theme.fontSizeMedium; }, space(0.75));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=projectIssueGrouping.jsx.map