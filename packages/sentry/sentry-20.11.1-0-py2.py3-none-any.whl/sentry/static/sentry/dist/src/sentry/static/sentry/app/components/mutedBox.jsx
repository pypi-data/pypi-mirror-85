import { __extends } from "tslib";
import React from 'react';
import { BannerContainer, BannerSummary } from 'app/components/events/styles';
import DateTime from 'app/components/dateTime';
import Duration from 'app/components/duration';
import { IconMute } from 'app/icons';
import { t } from 'app/locale';
var MutedBox = /** @class */ (function (_super) {
    __extends(MutedBox, _super);
    function MutedBox() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.renderReason = function () {
            var _a = _this.props.statusDetails, ignoreUntil = _a.ignoreUntil, ignoreCount = _a.ignoreCount, ignoreWindow = _a.ignoreWindow, ignoreUserCount = _a.ignoreUserCount, ignoreUserWindow = _a.ignoreUserWindow;
            if (ignoreUntil) {
                return t('This issue has been ignored until %s', <strong>
          <DateTime date={ignoreUntil}/>
        </strong>);
            }
            else if (ignoreCount && ignoreWindow) {
                return t('This issue has been ignored until it occurs %s time(s) in %s', <strong>{ignoreCount.toLocaleString()}</strong>, <strong>
          <Duration seconds={ignoreWindow * 60}/>
        </strong>);
            }
            else if (ignoreCount) {
                return t('This issue has been ignored until it occurs %s more time(s)', <strong>{ignoreCount.toLocaleString()}</strong>);
            }
            else if (ignoreUserCount && ignoreUserWindow) {
                return t('This issue has been ignored until it affects %s user(s) in %s', <strong>{ignoreUserCount.toLocaleString()}</strong>, <strong>
          <Duration seconds={ignoreUserWindow * 60}/>
        </strong>);
            }
            else if (ignoreUserCount) {
                return t('This issue has been ignored until it affects %s more user(s)', <strong>{ignoreUserCount.toLocaleString()}</strong>);
            }
            return t('This issue has been ignored');
        };
        _this.render = function () { return (<BannerContainer priority="default">
      <BannerSummary>
        <IconMute color="red300" size="sm"/>
        <span>
          {_this.renderReason()}&nbsp;&mdash;&nbsp;
          {t('You will not be notified of any changes and it will not show up by default in feeds.')}
        </span>
      </BannerSummary>
    </BannerContainer>); };
        return _this;
    }
    return MutedBox;
}(React.PureComponent));
export default MutedBox;
//# sourceMappingURL=mutedBox.jsx.map