import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import Banner from 'app/components/banner';
import Button from 'app/components/button';
import localStorage from 'app/utils/localStorage';
import space from 'app/styles/space';
import backgroundLighthouse from '../../../../images/spot/background-lighthouse.svg';
var BANNER_DISMISSED_KEY = 'releases-banner-dismissed';
var IntroBanner = /** @class */ (function (_super) {
    __extends(IntroBanner, _super);
    function IntroBanner() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isBannerHidden: localStorage.getItem(BANNER_DISMISSED_KEY) === 'true',
        };
        _this.handleBannerCloseClick = function () {
            localStorage.setItem(BANNER_DISMISSED_KEY, 'true');
            _this.setState({ isBannerHidden: true });
        };
        return _this;
    }
    IntroBanner.prototype.render = function () {
        if (this.state.isBannerHidden) {
            return null;
        }
        return (<StyledBanner title={t('Spot Release Changes')} subtitle={t('See differences between releases, from crash analytics to adoption rates.')} backgroundImg={backgroundLighthouse} onCloseClick={this.handleBannerCloseClick}>
        <BannerButton href="https://docs.sentry.io/workflow/releases/health/" external>
          {t('View Features')}
        </BannerButton>
        <BannerButton href="https://docs.sentry.io/workflow/releases/health/#getting-started" external priority="primary">
          {t('Update SDK')}
        </BannerButton>
      </StyledBanner>);
    };
    return IntroBanner;
}(React.Component));
var StyledBanner = styled(Banner)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  color: ", ";\n  min-height: 200px;\n\n  @media (min-width: ", ") {\n    min-height: 220px;\n  }\n\n  @media (min-width: ", ") {\n    min-height: 260px;\n  }\n"], ["\n  color: ", ";\n  min-height: 200px;\n\n  @media (min-width: ", ") {\n    min-height: 220px;\n  }\n\n  @media (min-width: ", ") {\n    min-height: 260px;\n  }\n"])), function (p) { return p.theme.textColor; }, function (p) { return p.theme.breakpoints[1]; }, function (p) { return p.theme.breakpoints[3]; });
var BannerButton = styled(Button)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin: ", ";\n"], ["\n  margin: ", ";\n"])), space(1));
export default IntroBanner;
var templateObject_1, templateObject_2;
//# sourceMappingURL=introBanner.jsx.map