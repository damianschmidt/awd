import React from "react";
import imageLogo from "../img/logo.png";
import { Divider, Grid, Header, Image, Segment } from "semantic-ui-react";
import Map from "./Map";

const InfoPanel = ({ flightPlan }) => {
  return (
    <Grid columns={2} stackable>
      <Grid.Column>
        <Segment>
          <Grid stackable columns={2}>
            <Divider vertical>
              <Image src={imageLogo} size="mini" />
            </Divider>
            <Grid.Column textAlign="center">
              <Header as="h4">
                {flightPlan.fromName ? flightPlan.fromName : "..."}
              </Header>
              <p>{flightPlan.fromICAO ? flightPlan.fromICAO : "..."}</p>
            </Grid.Column>
            <Grid.Column textAlign="center">
              <Header as="h4">
                {flightPlan.toName ? flightPlan.toName : "..."}
              </Header>
              <p>{flightPlan.toICAO ? flightPlan.toICAO : "..."}</p>
            </Grid.Column>
          </Grid>
        </Segment>
        <Segment>
          <Header as="h4">Departure Info</Header>
          <p>Weather: SBGL 092000Z 29002KT 9999 FEW020 BKN100 25/22 Q1010</p>
          <p>Runway: 10 CON 13.123 x 148 ft ( 4.000 x 45 m )</p>
          <p>.</p>
          <p>.</p>
          <p>.</p>
        </Segment>
        <Segment>
          <Header as="h4">Arrival Info</Header>
          <p>Weather: SBGL 092000Z 29002KT 9999 FEW020 BKN100 25/22 Q1010</p>
          <p>Runway: 11L ASP 10.499 x 148 ft ( 3.200 x 45 m ) lighted</p>
          <p>.</p>
          <p>.</p>
          <p>.</p>
        </Segment>
      </Grid.Column>
      <Grid.Column>
        <Segment>
          <Map />
        </Segment>
      </Grid.Column>
    </Grid>
  );
};

export default InfoPanel;
