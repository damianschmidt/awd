import React from "react";
import { Divider, Form } from "semantic-ui-react";

const options = [
  { key: "b", text: "Airbus a320", value: "Airbus" },
  { key: "a", text: "Boeing 737", value: "Boeing" },
];

const DataForm = () => {
  return (
    <>
      <Form>
        <Form.Group widths="equal">
          <Form.Input fluid label="Departure" placeholder="Departure" />
          <Form.Input fluid label="Arrive" placeholder="Arrive" />
          <Form.Input fluid label="Date" placeholder="Date" />
          <Form.Input fluid label="Time(Zulu)" placeholder="Time" />
          <Form.Select
            fluid
            label="Aircraft"
            options={options}
            placeholder="Aircraft"
          />
        </Form.Group>

        <Form.Button>Submit</Form.Button>
      </Form>
      <Divider />
    </>
  );
};

export default DataForm;
