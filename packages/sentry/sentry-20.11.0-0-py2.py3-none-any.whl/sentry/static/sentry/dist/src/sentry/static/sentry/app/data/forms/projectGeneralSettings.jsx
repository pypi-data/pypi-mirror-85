import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import PlatformIcon from 'platformicons';
import { extractMultilineFields, convertMultilineFieldValue } from 'app/utils';
import { t, tct, tn } from 'app/locale';
import HintPanelItem from 'app/components/panels/hintPanelItem';
import getDynamicText from 'app/utils/getDynamicText';
import marked from 'app/utils/marked';
import platforms from 'app/data/platforms';
import slugify from 'app/utils/slugify';
import ExternalLink from 'app/components/links/externalLink';
import space from 'app/styles/space';
import { GroupingConfigItem } from 'app/components/events/groupingInfo';
// Export route to make these forms searchable by label/help
export var route = '/settings/:orgId/projects/:projectId/';
var getResolveAgeAllowedValues = function () {
    var i = 0;
    var values = [];
    while (i <= 720) {
        values.push(i);
        if (i < 12) {
            i += 1;
        }
        else if (i < 24) {
            i += 3;
        }
        else if (i < 36) {
            i += 6;
        }
        else if (i < 48) {
            i += 12;
        }
        else {
            i += 24;
        }
    }
    return values;
};
var RESOLVE_AGE_ALLOWED_VALUES = getResolveAgeAllowedValues();
var ORG_DISABLED_REASON = t("This option is enforced by your organization's settings and cannot be customized per-project.");
export var fields = {
    slug: {
        name: 'slug',
        type: 'string',
        required: true,
        label: t('Name'),
        placeholder: t('my-service-name'),
        help: t('A unique ID used to identify this project'),
        transformInput: slugify,
        saveOnBlur: false,
        saveMessageAlertType: 'info',
        saveMessage: t('You will be redirected to the new project slug after saving'),
    },
    platform: {
        name: 'platform',
        type: 'array',
        label: t('Platform'),
        choices: function () {
            return platforms.map(function (_a) {
                var id = _a.id, name = _a.name;
                return [
                    id,
                    <PlatformWrapper key={id}>
          <StyledPlatformIcon platform={id}/>
          {name}
        </PlatformWrapper>,
                ];
            });
        },
        help: t('The primary platform for this project, used only for aesthetics'),
    },
    subjectPrefix: {
        name: 'subjectPrefix',
        type: 'string',
        label: t('Subject Prefix'),
        placeholder: t('e.g. [my-org]'),
        help: t('Choose a custom prefix for emails from this project'),
    },
    resolveAge: {
        name: 'resolveAge',
        type: 'range',
        allowedValues: RESOLVE_AGE_ALLOWED_VALUES,
        label: t('Auto Resolve'),
        help: t("Automatically resolve an issue if it hasn't been seen for this amount of time"),
        formatLabel: function (val) {
            val = Number(val);
            if (val === 0) {
                return t('Disabled');
            }
            if (val > 23 && val % 24 === 0) {
                // Based on allowed values, val % 24 should always be true
                val = val / 24;
                return tn('%s day', '%s days', val);
            }
            return tn('%s hour', '%s hours', val);
        },
        saveOnBlur: false,
        saveMessage: tct('[Caution]: Enabling auto resolve will immediately resolve anything that has ' +
            'not been seen within this period of time. There is no undo!', {
            Caution: <strong>Caution</strong>,
        }),
        saveMessageAlertType: 'warning',
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
            var changelog = (selection && selection.changelog) || '';
            if (!changelog) {
                return null;
            }
            return (<HintPanelItem>
          <div>
            <h2>{selection.id}:</h2>
            <div dangerouslySetInnerHTML={{ __html: marked(changelog) }}/>
          </div>
        </HintPanelItem>);
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
        label: t('Grouping Enhancements Base'),
        saveOnBlur: false,
        saveMessageAlertType: 'info',
        saveMessage: t('Changing grouping enhancements will apply to future events only.'),
        selectionInfoFunction: function (args) {
            var groupingEnhancementBases = args.groupingEnhancementBases, value = args.value;
            var selection = groupingEnhancementBases.find(function (_a) {
                var id = _a.id;
                return id === value;
            });
            var changelog = (selection && selection.changelog) || '';
            if (!changelog) {
                return null;
            }
            return (<HintPanelItem>
          <div>
            <h2>{selection.id}:</h2>
            <div dangerouslySetInnerHTML={{ __html: marked(changelog) }}/>
          </div>
        </HintPanelItem>);
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
        help: t('The built-in base version of grouping enhancements.'),
        visible: function (_a) {
            var features = _a.features;
            return features.has('set-grouping-config');
        },
    },
    groupingEnhancements: {
        name: 'groupingEnhancements',
        type: 'string',
        label: t('Custom Grouping Enhancements'),
        placeholder: t('function:raise_an_exception ^-group\nfunction:namespace::* +app'),
        multiline: true,
        monospace: true,
        autosize: true,
        inline: false,
        maxRows: 20,
        saveOnBlur: false,
        saveMessageAlertType: 'info',
        saveMessage: t('Changing grouping enhancements will apply to future events only.'),
        formatMessageValue: false,
        help: (<React.Fragment>
        <div style={{ marginBottom: 3 }}>
          {tct("This can be used to enhance the grouping algorithm with custom rules.\n        Rules follow the pattern [pattern]. [docs:Read the docs] for more information.", {
            pattern: <code>matcher:glob [^v]?[+-]flag</code>,
            docs: (<ExternalLink href="https://docs.sentry.io/platform-redirect/?next=%2Fdata-management%2Fevent-grouping%2Fgrouping-enhancements%2F"/>),
        })}
        </div>
        <pre>
          {'# remove all frames above a certain function from grouping\n' +
            'stack.function:panic_handler      ^-group\n' +
            '# mark all functions following a prefix in-app\n' +
            'stack.function:mylibrary_*        +app\n'}
        </pre>
      </React.Fragment>),
        validate: function () { return []; },
        visible: true,
    },
    fingerprintingRules: {
        name: 'fingerprintingRules',
        type: 'string',
        label: t('Server Side Fingerprinting'),
        placeholder: t('error.type:MyException -> fingerprint-value\nstack.function:some_panic_function -> fingerprint-value'),
        multiline: true,
        monospace: true,
        autosize: true,
        inline: false,
        maxRows: 20,
        saveOnBlur: false,
        saveMessageAlertType: 'info',
        saveMessage: t('Changing fingerprinting rules will apply to future events only.'),
        formatMessageValue: false,
        help: (<React.Fragment>
        <div style={{ marginBottom: 3 }}>
          {tct("This can be used to modify the fingerprinting rules on the server with custom rules.\n        Rules follow the pattern [pattern]. [docs:Read the docs] for more information.", {
            pattern: <code>matcher:glob -&gt; fingerprint, values</code>,
            docs: (<ExternalLink href="https://docs.sentry.io/platform-redirect/?next=%2Fdata-management%2Fevent-grouping%2Fserver-side-fingerprinting%2F"/>),
        })}
        </div>
        <pre>
          {'# force all errors of the same type to have the same fingerprint\n' +
            'error.type:DatabaseUnavailable -> system-down\n' +
            '# force all memory allocation errors to be grouped together\n' +
            'stack.function:malloc -> memory-allocation-error\n'}
        </pre>
      </React.Fragment>),
        visible: true,
    },
    allowedDomains: {
        name: 'allowedDomains',
        type: 'string',
        multiline: true,
        autosize: true,
        maxRows: 10,
        placeholder: t('https://example.com or example.com'),
        label: t('Allowed Domains'),
        help: t('Separate multiple entries with a newline'),
        getValue: function (val) { return extractMultilineFields(val); },
        setValue: function (val) { return convertMultilineFieldValue(val); },
    },
    scrapeJavaScript: {
        name: 'scrapeJavaScript',
        type: 'boolean',
        // if this is off for the organization, it cannot be enabled for the project
        disabled: function (_a) {
            var organization = _a.organization, name = _a.name;
            return !organization[name];
        },
        disabledReason: ORG_DISABLED_REASON,
        // `props` are the props given to FormField
        setValue: function (val, props) { return props.organization && props.organization[props.name] && val; },
        label: t('Enable JavaScript source fetching'),
        help: t('Allow Sentry to scrape missing JavaScript source context when possible'),
    },
    securityToken: {
        name: 'securityToken',
        type: 'string',
        label: t('Security Token'),
        help: t('Outbound requests matching Allowed Domains will have the header "{token_header}: {token}" appended'),
        setValue: function (value) { return getDynamicText({ value: value, fixed: '__SECURITY_TOKEN__' }); },
    },
    securityTokenHeader: {
        name: 'securityTokenHeader',
        type: 'string',
        placeholder: t('X-Sentry-Token'),
        label: t('Security Token Header'),
        help: t('Outbound requests matching Allowed Domains will have the header "{token_header}: {token}" appended'),
    },
    verifySSL: {
        name: 'verifySSL',
        type: 'boolean',
        label: t('Verify TLS/SSL'),
        help: t('Outbound requests will verify TLS (sometimes known as SSL) connections'),
    },
};
var PlatformWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var StyledPlatformIcon = styled(PlatformIcon)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(1));
var templateObject_1, templateObject_2;
//# sourceMappingURL=projectGeneralSettings.jsx.map