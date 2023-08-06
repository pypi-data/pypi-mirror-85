import { __assign, __makeTemplateObject } from "tslib";
import React from 'react';
import omit from 'lodash/omit';
import xor from 'lodash/xor';
import { withRouter } from 'react-router';
import styled from '@emotion/styled';
import space from 'app/styles/space';
import { t } from 'app/locale';
import ButtonBar from 'app/components/buttonBar';
import Button from 'app/components/button';
var crashReportTypes = ['event.minidump', 'event.applecrashreport'];
var GroupEventAttachmentsFilter = function (props) {
    var _a = props.location, query = _a.query, pathname = _a.pathname;
    var types = query.types;
    var allAttachmentsQuery = omit(query, 'types');
    var onlyCrashReportsQuery = __assign(__assign({}, query), { types: crashReportTypes });
    var activeButton = '';
    if (types === undefined) {
        activeButton = 'all';
    }
    else if (xor(crashReportTypes, types).length === 0) {
        activeButton = 'onlyCrash';
    }
    return (<FilterWrapper>
      <ButtonBar merged active={activeButton}>
        <Button barId="all" size="small" to={{ pathname: pathname, query: allAttachmentsQuery }}>
          {t('All Attachments')}
        </Button>
        <Button barId="onlyCrash" size="small" to={{ pathname: pathname, query: onlyCrashReportsQuery }}>
          {t('Only Crash Reports')}
        </Button>
      </ButtonBar>
    </FilterWrapper>);
};
var FilterWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  justify-content: flex-end;\n  margin-bottom: ", ";\n"])), space(3));
export { crashReportTypes };
export default withRouter(GroupEventAttachmentsFilter);
var templateObject_1;
//# sourceMappingURL=groupEventAttachmentsFilter.jsx.map