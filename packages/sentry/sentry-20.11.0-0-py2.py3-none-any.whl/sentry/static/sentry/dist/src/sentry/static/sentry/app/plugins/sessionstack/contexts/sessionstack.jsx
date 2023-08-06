import { __extends } from "tslib";
import $ from 'jquery';
import React from 'react';
import ReactDOM from 'react-dom';
import PropTypes from 'prop-types';
var ASPECT_RATIO = 16 / 9;
var SessionStackContextType = /** @class */ (function (_super) {
    __extends(SessionStackContextType, _super);
    function SessionStackContextType() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.propTypes = {
            data: PropTypes.object.isRequired,
        };
        _this.state = {
            showIframe: false,
        };
        _this.getTitle = function () { return 'SessionStack'; };
        return _this;
    }
    SessionStackContextType.prototype.componentDidMount = function () {
        var _this = this;
        // eslint-disable-next-line react/no-find-dom-node
        var domNode = ReactDOM.findDOMNode(this);
        this.parentNode = domNode.parentNode;
        window.addEventListener('resize', function () { return _this.setIframeSize(); }, false);
        this.setIframeSize();
    };
    SessionStackContextType.prototype.componentWillUnmount = function () {
        var _this = this;
        window.removeEventListener('resize', function () { return _this.setIframeSize(); }, false);
    };
    SessionStackContextType.prototype.setIframeSize = function () {
        if (!this.state.showIframe && this.parentNode) {
            var parentWidth = $(this.parentNode).width();
            this.setState({
                width: parentWidth,
                height: parentWidth / ASPECT_RATIO,
            });
        }
    };
    SessionStackContextType.prototype.playSession = function () {
        this.setState({
            showIframe: true,
        });
        this.setIframeSize();
    };
    SessionStackContextType.prototype.render = function () {
        var _this = this;
        var session_url = this.props.data.session_url;
        if (!session_url) {
            return <h4>Session not found.</h4>;
        }
        return (<div className="panel-group">
        {this.state.showIframe ? (<iframe src={session_url} sandbox="allow-scripts allow-same-origin" width={this.state.width} height={this.state.height}/>) : (<button className="btn btn-default" type="button" onClick={function () { return _this.playSession(); }}>
            Play session
          </button>)}
      </div>);
    };
    return SessionStackContextType;
}(React.Component));
export default SessionStackContextType;
//# sourceMappingURL=sessionstack.jsx.map