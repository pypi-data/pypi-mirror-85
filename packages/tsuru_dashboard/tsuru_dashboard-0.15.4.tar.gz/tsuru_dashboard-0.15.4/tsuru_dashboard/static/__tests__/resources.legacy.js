import React from "react";
import { shallow } from "enzyme";
import { Resources } from "../js/src/components/resources.legacy";

describe('Resources', () => {
  it('has resources as className', () => {
    const resources = shallow(<Resources />);
    expect(resources.find(".resources").length).toBe(1);
  });
});
