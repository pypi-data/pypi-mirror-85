import { __assign, __extends, __read, __spread } from "tslib";
import React from 'react';
import AsyncView from 'app/views/asyncView';
import { Panel, PanelHeader, PanelBody } from 'app/components/panels';
import InternalStatChart from 'app/components/internalStatChart';
import { SelectField } from 'app/components/forms';
var TIME_WINDOWS = ['1h', '1d', '1w'];
var AdminQueue = /** @class */ (function (_super) {
    __extends(AdminQueue, _super);
    function AdminQueue() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    AdminQueue.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { timeWindow: '1w', since: new Date().getTime() / 1000 - 3600 * 24 * 7, resolution: '1h', taskName: null });
    };
    AdminQueue.prototype.getEndpoints = function () {
        return [['taskList', '/internal/queue/tasks/']];
    };
    AdminQueue.prototype.changeWindow = function (timeWindow) {
        var seconds;
        if (timeWindow === '1h') {
            seconds = 3600;
        }
        else if (timeWindow === '1d') {
            seconds = 3600 * 24;
        }
        else if (timeWindow === '1w') {
            seconds = 3600 * 24 * 7;
        }
        else {
            throw new Error('Invalid time window');
        }
        this.setState({
            since: new Date().getTime() / 1000 - seconds,
            timeWindow: timeWindow,
        });
    };
    AdminQueue.prototype.changeTask = function (value) {
        this.setState({ activeTask: value });
    };
    AdminQueue.prototype.renderBody = function () {
        var _a;
        var _this = this;
        var _b = this.state, activeTask = _b.activeTask, taskList = _b.taskList;
        return (<div>
        <div className="btn-group pull-right">
          {TIME_WINDOWS.map(function (r) { return (<a className={"btn btn-sm " + (r === _this.state.timeWindow ? 'btn-primary' : 'btn-default')} onClick={function () { return _this.changeWindow(r); }} key={r}>
              {r}
            </a>); })}
        </div>

        <h3 className="no-border">Queue Overview</h3>

        <Panel>
          <PanelHeader>Global Throughput</PanelHeader>
          <PanelBody withPadding>
            <InternalStatChart since={this.state.since} resolution={this.state.resolution} stat="jobs.all.started" label="jobs started"/>
          </PanelBody>
        </Panel>

        <h3 className="no-border">Task Details</h3>

        <div>
          <div className="m-b-1">
            <label>Show details for task:</label>
            <SelectField deprecatedSelectControl name="task" onChange={function (value) { return _this.changeTask(value); }} value={activeTask} clearable choices={(_a = ['']).concat.apply(_a, __spread(taskList)).map(function (t) { return [t, t]; })}/>
          </div>
          {activeTask ? (<div>
              <Panel key={"jobs.started." + activeTask}>
                <PanelHeader>
                  Jobs Started <small>{activeTask}</small>
                </PanelHeader>
                <PanelBody withPadding>
                  <InternalStatChart since={this.state.since} resolution={this.state.resolution} stat={"jobs.started." + activeTask} label="jobs" height={100}/>
                </PanelBody>
              </Panel>
              <Panel key={"jobs.finished." + activeTask}>
                <PanelHeader>
                  Jobs Finished <small>{activeTask}</small>
                </PanelHeader>
                <PanelBody withPadding>
                  <InternalStatChart since={this.state.since} resolution={this.state.resolution} stat={"jobs.finished." + activeTask} label="jobs" height={100}/>
                </PanelBody>
              </Panel>
            </div>) : null}
        </div>
      </div>);
    };
    return AdminQueue;
}(AsyncView));
export default AdminQueue;
//# sourceMappingURL=adminQueue.jsx.map