import { __extends } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import classNames from 'classnames';
import * as Sentry from '@sentry/react';
import { t } from 'app/locale';
import { IconFlag } from 'app/icons';
import Button from 'app/components/button';
function openFeedback(e) {
    e.preventDefault();
    Sentry.showReportDialog();
}
var DetailedError = /** @class */ (function (_super) {
    __extends(DetailedError, _super);
    function DetailedError() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    DetailedError.prototype.componentDidMount = function () {
        var _this = this;
        // XXX(epurkhiser): Why is this here?
        setTimeout(function () { return _this.forceUpdate(); }, 100);
    };
    DetailedError.prototype.render = function () {
        var _a = this.props, className = _a.className, heading = _a.heading, message = _a.message, onRetry = _a.onRetry, hideSupportLinks = _a.hideSupportLinks;
        var cx = classNames('detailed-error', className);
        var showFooter = !!onRetry || !hideSupportLinks;
        return (<div className={cx}>
        <div className="detailed-error-icon">
          <IconFlag size="lg"/>
        </div>
        <div className="detailed-error-content">
          <h4>{heading}</h4>

          <div className="detailed-error-content-body">{message}</div>

          {showFooter && (<div className="detailed-error-content-footer">
              <div>
                {onRetry && (<a onClick={onRetry} className="btn btn-default">
                    {t('Retry')}
                  </a>)}
              </div>

              {!hideSupportLinks && (<div className="detailed-error-support-links">
                  {Sentry.lastEventId() && (<Button priority="link" onClick={openFeedback}>
                      {t('Fill out a report')}
                    </Button>)}
                  <a href="https://status.sentry.io/">{t('Service status')}</a>

                  <a href="https://sentry.io/support/">{t('Contact support')}</a>
                </div>)}
            </div>)}
        </div>
      </div>);
    };
    DetailedError.propTypes = {
        className: PropTypes.string,
        onRetry: PropTypes.func,
        heading: PropTypes.string.isRequired,
        message: PropTypes.node,
        hideSupportLinks: PropTypes.bool,
    };
    DetailedError.defaultProps = {
        hideSupportLinks: false,
    };
    return DetailedError;
}(React.Component));
export default DetailedError;
//# sourceMappingURL=detailedError.jsx.map