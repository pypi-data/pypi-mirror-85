import React from "react";
import { shallow, mount } from "enzyme";
import { AppList, AppTable } from "../js/src/components/list";
import { Loading } from "../js/src/components/loading";
import $ from "jquery";

describe('AppList', () => {
  it('should has app-list as className', () => {
    const wrapper = shallow(
      <AppList url="http://localhost:80/apps/list.json" />
    );
    expect(wrapper.find(".app-list").length).toBe(1);
  });

  it('should contain Loading if its loading', () => {
    const wrapper = shallow(
      <AppList url="http://localhost:80/apps/list.json" />
    );
    wrapper.setState({ loading: true })
    expect(wrapper.find(Loading).length).toBe(1);
  });

  it('should load apps on render', () => {
    $.ajax = jest.fn();
    const wrapper = mount(
      <AppList url="http://localhost:80/apps/list.json" />
    )

    $.ajax.mock.calls[0][0].success({
      apps: [
        { name: "appname", teamowner: "team-A", pool: "dev", plan: { name: "small" } },
        { name: "other", teamowner: "team-B", pool: "dev", plan: { name: "small" } }
      ]
    });

    const expected = {
      apps: [
        { name: "appname", teamowner: "team-A", pool: "dev", plan: { name: "small" } },
        { name: "other", teamowner: "team-B", pool: "dev", plan: { name: "small" } }
      ],
      cached: [
        { name: "appname", teamowner: "team-A", pool: "dev", plan: { name: "small" } },
        { name: "other", teamowner: "team-B", pool: "dev", plan: { name: "small" } }
      ],
      loading: false,
      term: ''
    }

    wrapper.update();
    expect(expected).toEqual(wrapper.state());
    expect(wrapper.find(AppTable).length).toBe(1);
    expect(wrapper.find("td").length).toBe(8);
  });

  it('should filter list by app name', () => {
    $.ajax = jest.fn((obj) => {
      obj.success({
        apps: [
          { name: "appname", teamowner: "team-A", pool: "dev", plan: { name: "small" } },
          { name: "other", teamowner: "team-B", pool: "dev", plan: { name: "small" } }
        ]
      });
    });
    const wrapper = mount(
      <AppList url="http://localhost:80/apps/list.json" />
    )

    const expected = {
      apps: [
        { name: "other", teamowner: "team-B", pool: "dev", plan: { name: "small" } }
      ],
      cached: [
        { name: "appname", teamowner: "team-A", pool: "dev", plan: { name: "small" } },
        { name: "other", teamowner: "team-B", pool: "dev", plan: { name: "small" } }
      ],
      loading: false,
      term: ''
    }

    wrapper.find("input").simulate('change', { target: { value: "oth" } });
    expect(expected).toEqual(wrapper.state());
    expect(wrapper.find("td").length).toBe(4);
  });

  it('should list all on empty search', () => {
    $.ajax = jest.fn((obj) => {
      obj.success({
        apps: [
          { name: "appname", teamowner: "team-A", pool: "dev", plan: { name: "small" } },
          { name: "other", teamowner: "team-B", pool: "dev", plan: { name: "small" } }
        ]
      });

      const wrapper = mount(
        <AppList url="http://localhost:80/apps/list.json" />
      )

      const expected = {
        apps: [
          { name: "other", teamowner: "team-B", pool: "dev", plan: { name: "small" } }
        ],
        cached: [
          { name: "appname", teamowner: "team-A", pool: "dev", plan: { name: "small" } },
          { name: "other", teamowner: "team-B", pool: "dev", plan: { name: "small" } }
        ],
        loading: false,
        term: ''
      };

      wrapper.find("input").simulate('change', { target: { value: "" } });
      expect(expected).toEqual(wrapper.state());
      expect(wrapper.find("td").length).toBe(8);
    });
  });
});
