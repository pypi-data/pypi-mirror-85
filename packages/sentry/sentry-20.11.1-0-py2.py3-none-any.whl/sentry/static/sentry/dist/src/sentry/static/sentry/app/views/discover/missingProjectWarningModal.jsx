import { __extends } from "tslib";
import React from 'react';
import Modal, { Header, Body, Footer } from 'react-bootstrap/lib/Modal';
import Button from 'app/components/button';
import { t } from 'app/locale';
var MissingProjectWarningModal = /** @class */ (function (_super) {
    __extends(MissingProjectWarningModal, _super);
    function MissingProjectWarningModal() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    MissingProjectWarningModal.prototype.renderProject = function (id) {
        var project = this.props.organization.projects.find(function (p) { return p.id === id.toString(); });
        return <li key={id}>{project ? project.slug : t("Unknown project " + id)}</li>;
    };
    MissingProjectWarningModal.prototype.render = function () {
        var _this = this;
        var _a = this.props, validProjects = _a.validProjects, invalidProjects = _a.invalidProjects;
        var text = validProjects.length
            ? t("You are not currently a member of all of the projects specified by\n          this query. As a result, data for the following projects will be\n          omitted from the displayed results:")
            : t("You are not currently a member of any of the following projects specified\n           by this query. You may still run this query against other projects you\n           have access to.");
        return (<Modal show onHide={function () { }}>
        <Header>{t('Project access')}</Header>
        <Body>
          <p>{text}</p>
          <ul>{invalidProjects.map(function (id) { return _this.renderProject(id); })}</ul>
        </Body>
        <Footer>
          <Button priority="primary" onClick={this.props.closeModal}>
            {t('View results')}
          </Button>
        </Footer>
      </Modal>);
    };
    return MissingProjectWarningModal;
}(React.Component));
export default MissingProjectWarningModal;
//# sourceMappingURL=missingProjectWarningModal.jsx.map