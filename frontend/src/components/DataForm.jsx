import React, { useEffect, useState } from "react";
import axios from "axios";
import _ from "lodash";
import {
  Accordion,
  Divider,
  Form,
  Icon,
  Loader,
  Message,
} from "semantic-ui-react";
import Airports from "../utils/airports.json";
import Aircrafts from "../utils/aircrafts.json";

const aircraftsIcao = _.map(Aircrafts, (aircraft, index) => ({
  key: index,
  text: aircraft.name,
  value: aircraft.name,
}));

const airportsIcao = _.map(Airports, (airport, index) => ({
  key: index,
  text: airport.icao,
  value: airport.icao,
}));

const DataForm = ({ setFlightPlan, setDateTime }) => {
  const [activeIndex, setActiveIndex] = useState(true);
  const [currentDate, setCurrentDate] = useState("");
  const [defaultTime, setDefaultTime] = useState("");
  const [errorMessages, setErrorMessages] = useState([]);
  const [errorOccurred, setErrorOccurred] = useState(false);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const date = new Date();

    setCurrentDate(
      `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`
    );

    let minutes = date.getUTCMinutes();
    if (minutes < 10) minutes = "0" + minutes;

    if (date.getUTCMinutes())
      setDefaultTime(`${date.getUTCHours()}:${minutes}`);
  }, [currentDate, defaultTime]);

  const handleClick = (e) => {
    setActiveIndex(!activeIndex);
  };

  const submitHandler = async (e) => {
    const Departure = e.target.elements[0].nextSibling.innerText;
    const Arrival = e.target.elements[1].nextSibling.innerText;
    const arrivalDate = e.target.elements[2].value;
    const arrivalTime = e.target.elements[3].value;
    const errors = [];
    setErrorOccurred(false);

    console.log(e.target.elements[2].value);

    setDateTime([arrivalDate, arrivalTime]);

    if (Departure === Arrival) {
      errors[0] = "Arrival it can't be the same as Departure";
      setErrorOccurred(true);
    }
    if (Departure === "Departure" || Arrival === "Arrival") {
      errors[1] = "Arrival Departure can't be empty";
      setErrorOccurred(true);
    }
    // if (Aircraft === "Aircraft") {
    //   errors[2] = "Aircraft can't be empty";
    //   setErrorOccurred(true);
    // }

    setErrorMessages(errors);
    if (errors.length === 0) {
      setLoading(true);
      let response = [];

      response[0] = (
        await axios.get(`http://localhost:5000/api/airport/${Departure}`)
      ).data;
      response[0].icao = Departure;

      response[1] = (
        await axios.get(`http://localhost:5000/api/airport/${Arrival}`)
      ).data;
      response[1].icao = Arrival;

      console.log("odp: ", response);

      setFlightPlan(response);
      setActiveIndex(!activeIndex);
    }
    setLoading(false);
  };

  return (
    <>
      <Accordion>
        <Accordion.Title active={activeIndex} index={0} onClick={handleClick}>
          <Icon name="dropdown" />
          Flight Info
        </Accordion.Title>
        <Accordion.Content active={activeIndex}>
          <Form onSubmit={submitHandler} error={errorOccurred}>
            <Form.Group widths="equal">
              <Form.Select
                search
                fluid
                options={airportsIcao}
                label="Departure"
                placeholder="Departure"
              />
              <Form.Select
                search
                fluid
                options={airportsIcao}
                label="Arrival"
                placeholder="Arrival"
              />
              <Form.Input
                type="date"
                fluid
                label="Date"
                defaultValue={currentDate}
              />
              <Form.Input
                type="time"
                fluid
                label="Time (Zulu)"
                defaultValue={defaultTime}
              />
              <Form.Select
                search
                fluid
                label="Aircraft"
                options={aircraftsIcao}
                placeholder="Aircraft"
              />
            </Form.Group>
            <Message error header="Action Forbidden" list={errorMessages} />
            <div className="form-btn">
              <Form.Button>Submit</Form.Button>
              {loading ? <Loader active inline /> : <Loader disabled inline />}
            </div>
          </Form>
        </Accordion.Content>
      </Accordion>
      <Divider />
    </>
  );
};

export default DataForm;
