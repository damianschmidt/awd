import React from "react";
import image from "./img/logo.png";
import imageMap from "./img/map.png";
import { BrowserRouter, Route, Switch, Redirect } from "react-router-dom";
import {
  Container,
  Divider,
  Form,
  Grid,
  Header,
  Image,
  Menu,
  Segment,
} from "semantic-ui-react";

const options = [
  { key: "b", text: "Airbus a320", value: "Airbus" },
  { key: "a", text: "Boeing 737", value: "Boeing" },
];

const App = () => {
  return (
    <>
      <Menu>
        <Container>
          <Menu.Item as="a" header>
            <Image size="mini" src={image} style={{ marginRight: "1.5em" }} />
            Application Logo
          </Menu.Item>
          <Header as="h2"></Header>
        </Container>
      </Menu>
      <Container>
        <div className="body">
          <Form>
            <Form.Group widths="equal">
              <Form.Input fluid label="Departure" placeholder="Departure" />
              <Form.Input fluid label="Arrive" placeholder="Arrive" />
              <Form.Input fluid label="Date" placeholder="Date" />
              <Form.Input fluid label="Time(Zulu)" placeholder="Time" />
              <Form.Select
                fluid
                label="Aircaft"
                options={options}
                placeholder="Aircraft"
              />
            </Form.Group>

            <Form.Button>Submit</Form.Button>
          </Form>
          <Divider />
          <Grid columns={2}>
            <Grid.Column>
              <Segment>
                <Grid columns={2}>
                  <Divider vertical>
                    <Image src={image} size="mini" />
                  </Divider>
                  <Grid.Column textAlign="center">
                    <Header as="h4">Rio Galeao</Header>
                    <p>SBGL</p>
                    <p>Gate 533</p>
                  </Grid.Column>
                  <Grid.Column textAlign="center">
                    <Header as="h4">Presidente Juscelino</Header>
                    <p>SBBR</p>
                  </Grid.Column>
                </Grid>
              </Segment>
              <Segment>
                <Header as="h4">Deparrture Info</Header>
                <p>
                  Weather: SBGL 092000Z 29002KT 9999 FEW020 BKN100 25/22 Q1010
                </p>
                <p>Runway: 10 CON 13.123 x 148 ft ( 4.000 x 45 m )</p>
                <p>.</p>
                <p>.</p>
                <p>.</p>
              </Segment>
              <Segment>
                <Header as="h4">Arrival Info</Header>
                <p>
                  Weather: SBGL 092000Z 29002KT 9999 FEW020 BKN100 25/22 Q1010
                </p>
                <p>Runway: 11L ASP 10.499 x 148 ft ( 3.200 x 45 m ) lighted</p>
                <p>.</p>
                <p>.</p>
                <p>.</p>
              </Segment>
            </Grid.Column>
            <Grid.Column>
              <Image fluid src={imageMap} />
            </Grid.Column>
          </Grid>
        </div>
      </Container>
    </>
  );
};

export default App;
