import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { tct, t } from 'app/locale';
import ExternalLink from 'app/components/links/externalLink';
import Button from 'app/components/button';
import { Panel } from 'app/components/panels';
import space from 'app/styles/space';
var Intro = /** @class */ (function (_super) {
    __extends(Intro, _super);
    function Intro() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Intro.prototype.getExampleQueries = function () {
        return [
            {
                title: t('Events by stack filename'),
                description: 'What is my most problematic code?',
                query: {
                    fields: ['stack.filename'],
                    aggregations: [['count()', null, 'count']],
                    conditions: [],
                    orderby: '-count',
                },
            },
            {
                title: t('Unique issues by user'),
                description: t("Who's having the worst time?"),
                query: {
                    fields: ['user.id', 'user.username', 'user.email', 'user.ip'],
                    aggregations: [['uniq', 'issue.id', 'uniq_issue_id']],
                    conditions: [],
                    orderby: '-uniq_issue_id',
                },
            },
            {
                title: t('Events by geography'),
                description: 'Are my services less reliable in some regions?',
                query: {
                    fields: ['geo.country_code', 'geo.region', 'geo.city'],
                    aggregations: [['count()', null, 'count']],
                    conditions: [],
                    orderby: '-count',
                },
            },
        ];
    };
    Intro.prototype.render = function () {
        var _this = this;
        return (<IntroContainer>
        <Content>
          <Heading>{t('Discover lets you query raw event data in Sentry')}</Heading>
          <TextBlock>
            {tct("Getting started? Try running one of the example queries below.\n            To learn more about how to use the query builder, [docs:see the docs].", {
            docs: <ExternalLink href="https://docs.sentry.io/product/discover/"/>,
        })}
          </TextBlock>
          <TextBlock>
            {this.getExampleQueries().map(function (_a, idx) {
            var title = _a.title, description = _a.description, query = _a.query;
            return (<ExampleQuery key={idx}>
                <div>
                  <div>{title}</div>
                  <ExampleQueryDescription>{description}</ExampleQueryDescription>
                </div>
                <div>
                  <Button size="small" onClick={function () {
                _this.props.updateQuery(query);
            }}>
                    {t('Run')}
                  </Button>
                </div>
              </ExampleQuery>);
        })}
          </TextBlock>
        </Content>
      </IntroContainer>);
    };
    return Intro;
}(React.Component));
export default Intro;
var IntroContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  font-size: ", ";\n  color: ", ";\n  width: 100%;\n  height: 100%;\n  min-height: 420px;\n  min-width: 500px;\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  font-size: ", ";\n  color: ", ";\n  width: 100%;\n  height: 100%;\n  min-height: 420px;\n  min-width: 500px;\n"])), function (p) { return p.theme.fontSizeLarge; }, function (p) { return p.theme.textColor; });
var Content = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  max-width: 560px;\n"], ["\n  max-width: 560px;\n"])));
var Heading = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-size: ", ";\n  font-weight: 700;\n  margin: 0 0 20px;\n"], ["\n  font-size: ", ";\n  font-weight: 700;\n  margin: 0 0 20px;\n"])), function (p) { return p.theme.fontSizeExtraLarge; });
var TextBlock = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin: 0 0 20px;\n"], ["\n  margin: 0 0 20px;\n"])));
var ExampleQuery = styled(Panel)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n  padding: ", ";\n"], ["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n  padding: ", ";\n"])), space(2));
var ExampleQueryDescription = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  font-size: ", ";\n  color: ", ";\n"], ["\n  font-size: ", ";\n  color: ", ";\n"])), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.gray200; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=intro.jsx.map