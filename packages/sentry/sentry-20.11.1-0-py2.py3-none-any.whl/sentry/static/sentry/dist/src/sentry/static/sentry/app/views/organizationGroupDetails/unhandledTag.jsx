import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import space from 'app/styles/space';
import Tag from 'app/components/tagDeprecated';
import Feature from 'app/components/acl/feature';
import Tooltip from 'app/components/tooltip';
import { IconSubtract } from 'app/icons';
var TagWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(1));
var TagAndMessageWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
// TODO(matej): remove "unhandled-issue-flag" feature flag once testing is over (otherwise this won't ever be rendered in a shared event)
var UnhandledTag = styled(function (props) { return (<Feature features={['unhandled-issue-flag']}>
    <TagWrapper>
      <Tooltip title={t('An unhandled error was detected in this Issue.')}>
        <Tag priority="error" icon={<IconSubtract size="xs" color="red200" isCircled/>} {...props}>
          {t('Unhandled')}
        </Tag>
      </Tooltip>
    </TagWrapper>
  </Feature>); })(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  /* TODO(matej): There is going to be a major Tag component refactor which should make Tags look something like this - then we can remove these one-off styles */\n  background-color: #ffecf0;\n  color: ", ";\n  text-transform: none;\n  padding: 0 ", ";\n  height: 17px;\n\n  & > span {\n    margin-right: 0 ", ";\n  }\n\n  & > span,\n  & svg {\n    height: 11px;\n    width: 10px;\n  }\n"], ["\n  /* TODO(matej): There is going to be a major Tag component refactor which should make Tags look something like this - then we can remove these one-off styles */\n  background-color: #ffecf0;\n  color: ", ";\n  text-transform: none;\n  padding: 0 ", ";\n  height: 17px;\n\n  & > span {\n    margin-right: 0 ", ";\n  }\n\n  & > span,\n  & svg {\n    height: 11px;\n    width: 10px;\n  }\n"])), function (p) { return p.theme.gray500; }, space(0.75), space(0.5));
export default UnhandledTag;
export { TagAndMessageWrapper };
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=unhandledTag.jsx.map