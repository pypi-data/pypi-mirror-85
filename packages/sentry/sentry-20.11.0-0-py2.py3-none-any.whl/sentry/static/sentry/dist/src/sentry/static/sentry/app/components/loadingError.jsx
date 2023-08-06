import { __extends, __makeTemplateObject } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import { IconInfo } from 'app/icons';
import { t } from 'app/locale';
import Alert from 'app/components/alert';
import Button from 'app/components/button';
import { Panel } from 'app/components/panels';
import space from 'app/styles/space';
/**
 * Renders an Alert box of type "error". Renders a "Retry" button only if a `onRetry` callback is defined.
 */
var LoadingError = /** @class */ (function (_super) {
    __extends(LoadingError, _super);
    function LoadingError() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    LoadingError.prototype.shouldComponentUpdate = function () {
        return false;
    };
    LoadingError.prototype.render = function () {
        var _a = this.props, message = _a.message, onRetry = _a.onRetry;
        return (<StyledAlert type="error">
        <Content>
          <IconInfo size="lg"/>
          <div data-test-id="loading-error-message">{message}</div>
          {onRetry && (<Button onClick={onRetry} type="button" priority="default" size="small">
              {t('Retry')}
            </Button>)}
        </Content>
      </StyledAlert>);
    };
    LoadingError.propTypes = {
        onRetry: PropTypes.func,
        message: PropTypes.string,
    };
    LoadingError.defaultProps = {
        message: t('There was an error loading data.'),
    };
    return LoadingError;
}(React.Component));
export default LoadingError;
var StyledAlert = styled(Alert)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  ", " & {\n    border-radius: 0;\n    border-width: 1px 0;\n  }\n"], ["\n  " /* sc-selector */, " & {\n    border-radius: 0;\n    border-width: 1px 0;\n  }\n"])), /* sc-selector */ Panel);
var Content = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: min-content auto max-content;\n  align-items: center;\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: min-content auto max-content;\n  align-items: center;\n"])), space(1));
var templateObject_1, templateObject_2;
//# sourceMappingURL=loadingError.jsx.map