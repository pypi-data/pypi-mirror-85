import { __assign, __extends, __makeTemplateObject } from "tslib";
import * as ReactRouter from 'react-router';
import React from 'react';
import styled from '@emotion/styled';
import { t, tct } from 'app/locale';
import Button from 'app/components/button';
import Text from 'app/components/text';
import recreateRoute from 'app/utils/recreateRoute';
var RedirectToProjectModal = /** @class */ (function (_super) {
    __extends(RedirectToProjectModal, _super);
    function RedirectToProjectModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            timer: 5,
        };
        return _this;
    }
    RedirectToProjectModal.prototype.componentDidMount = function () {
        var _this = this;
        setInterval(function () {
            if (_this.state.timer <= 1) {
                window.location.assign(_this.newPath);
                return;
            }
            _this.setState(function (state) { return ({
                timer: state.timer - 1,
            }); });
        }, 1000);
    };
    Object.defineProperty(RedirectToProjectModal.prototype, "newPath", {
        get: function () {
            var _a = this.props, params = _a.params, slug = _a.slug;
            return recreateRoute('', __assign(__assign({}, this.props), { params: __assign(__assign({}, params), { projectId: slug }) }));
        },
        enumerable: false,
        configurable: true
    });
    RedirectToProjectModal.prototype.render = function () {
        var _a = this.props, slug = _a.slug, Header = _a.Header, Body = _a.Body;
        return (<React.Fragment>
        <Header>{t('Redirecting to New Project...')}</Header>

        <Body>
          <div>
            <Text>
              <p>{t('The project slug has been changed.')}</p>

              <p>
                {tct('You will be redirected to the new project [project] in [timer] seconds...', {
            project: <strong>{slug}</strong>,
            timer: "" + this.state.timer,
        })}
              </p>
              <ButtonWrapper>
                <Button priority="primary" href={this.newPath}>
                  {t('Continue to %s', slug)}
                </Button>
              </ButtonWrapper>
            </Text>
          </div>
        </Body>
      </React.Fragment>);
    };
    return RedirectToProjectModal;
}(React.Component));
export default ReactRouter.withRouter(RedirectToProjectModal);
export { RedirectToProjectModal };
var ButtonWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n"], ["\n  display: flex;\n  justify-content: flex-end;\n"])));
var templateObject_1;
//# sourceMappingURL=redirectToProject.jsx.map